import copy
import os
import zipfile
from ipaddress import ip_network

import dateutil.parser
from django.http import FileResponse

from problem.models import Problem
from problem.views.admin import ProblemBase
from problem.serializers import CreateProblemSerializer
from account.decorators import check_course_permission, ensure_created_by
from account.models import User
from submission.models import Submission, JudgeStatus
from utils.api import APIView, validate_serializer
from utils.cache import cache
from utils.constants import CacheKey
from utils.shortcuts import rand_str
from utils.tasks import delete_files
from ..models import Course, Practice
from ..serializers import (CourseSerializer, CreateCourseSerializer, EditCourseSerializer,
                           PracticeSerializer, CreatePracticeSerializer, EditPracticeSerializer,
                           ParticipantSerializer)


class CourseAPI(APIView):
    @validate_serializer(CreateCourseSerializer)
    def post(self, request):
        data = request.data
        data["created_by"] = request.user
        course = Course.objects.create(**data)
        return self.success(CourseSerializer(course).data)

    @validate_serializer(EditCourseSerializer)
    def put(self, request):
        data = request.data
        try:
            course = Course.objects.get(id=data.pop("id"))
            ensure_created_by(course, request.user)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        for k, v in data.items():
            setattr(course, k, v)
        course.save()
        return self.success(CourseSerializer(course).data)

    def get(self, request):
        course_id = request.GET.get("id")
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                ensure_created_by(course, request.user)
                return self.success(CourseSerializer(course).data)
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        courses = Course.objects.all().order_by("-create_time")
        if request.user.is_admin():
            courses = courses.filter(created_by=request.user)

        keyword = request.GET.get("keyword")
        if keyword:
            courses = courses.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, courses, CourseSerializer))


class CoursePracticeAPI(APIView):
    def get(self, request):
        course = Course.objects.get(id=request.GET.get("id"))
        return self.success(self.paginate_data(request, course.practices.all(),
                                               PracticeSerializer))

    def post(self, request):
        data = request.data
        course = Course.objects.get(id=data.pop("cid"))
        practice = Practice.objects.get(id=data.pop("pid"))
        course.practices.add(practice)
        return self.success()


class PracticeAPI(APIView):
    @validate_serializer(CreatePracticeSerializer)
    def post(self, request):
        data = request.data
        data["created_by"] = request.user
        practice = Practice.objects.create(**data)
        return self.success(PracticeSerializer(practice).data)

    @validate_serializer(EditPracticeSerializer)
    def put(self, request):
        data = request.data
        try:
            practice = Practice.objects.get(id=data.pop("id"))
            ensure_created_by(practice, request.user)
        except Practice.DoesNotExist:
            return self.error("Practice does not exist")

        for k, v in data.items():
            setattr(practice, k, v)
        practice.save()
        return self.success(PracticeSerializer(practice).data)

    def get(self, request):
        practice_id = request.GET.get("id")
        if practice_id:
            try:
                practice = Practice.objects.get(id=practice_id)
                ensure_created_by(practice, request.user)
                return self.success(PracticeSerializer(practice).data)
            except Practice.DoesNotExist:
                return self.error("Practice does not exist")

        practices = Practice.objects.all().order_by("-create_time")
        if request.user.is_admin():
            practices = practices.filter(created_by=request.user)

        keyword = request.GET.get("keyword")
        if keyword:
            practices = practices.filter(title__contains=keyword)
        return self.success(self.paginate_data(request, practices, PracticeSerializer))


class AddCollectionProblemAPI(APIView):
    def post(self, request):
        data = request.data
        collectionType = data.pop('type')
        if collectionType == 'course':
            collection = Course.objects.get(id=data.pop('cid'))
        else:
            collection = Practice.objects.get(id=data.pop('cid'))
        problem = Problem.objects.get(id=data.pop('pid'))
        collection.problems.add(problem)
        collection.save()
        return self.success()


class CollectionParticipantAPI(APIView):
    def get(self, request):
        collectionType = request.GET.get("collection_type")
        collectionId = request.GET.get("collection_id")
        if collectionType == 'course':
            collection = Course.objects.get(id=collectionId)
        else:
            collection = Practice.objects.get(id=collectionId)
        return self.success(self.paginate_data(request, collection.participants.all(), ParticipantSerializer))

    def post(self, request):
        data = request.data
        collectionType = data.pop('type')
        if collectionType == 'course':
            collection = Course.objects.get(id=data.pop('cid'))
        else:
            collection = Practice.objects.get(id=data.pop('cid'))
        user = User.objects.get(id=data.pop('uid'))
        collection.participants.add(user)
        collection.save()
        return self.success()

    def delete(self, request):
        collectionType = request.GET.get("type")
        collectionId = request.GET.get("cid")
        userId = request.GET.get("id")
        if not collectionType or not collectionId or not userId:
            return self.error("Invalid parameter, type/cid/id are required")

        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return self.error("User does not exists")

        if collectionType == 'course':
            collection = Course.objects.get(id=collectionId)
        else:
            collection = Practice.objects.get(id=collectionId)
        
        try:
            collection.participants.remove(user)
        except Exception:
            return self.error("no such user in participants list")
        return self.success()

