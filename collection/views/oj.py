from django.http import HttpResponse
from django.utils.timezone import now
from django.core.cache import cache
from django.db.models import prefetch_related_objects, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from utils.api import APIView
from account.decorators import login_required, check_contest_permission, check_contest_password
from problem.views.oj import ProblemAPI

from ..models import Course, Practice
from ..serializers import CourseSerializer, PracticeSerializer


class CollectionListAPI(APIView):
    def get(self, request):
        collection_type = request.GET.get("type")
        if collection_type == 'course':
            course_id = request.GET.get("id")
            if course_id:
                try:
                    course = Course.objects.get(id=course_id)
                    return self.success(CourseSerializer(course).data)
                except Course.DoesNotExist:
                    return self.error("Course does not exist")

            courses = Course.objects.all().order_by("-create_time")
            keyword = request.GET.get("keyword")
            if keyword:
                courses = courses.filter(title__contains=keyword)
            return self.success(self.paginate_data(request, courses, CourseSerializer))
        else:
            practice_id = request.GET.get("id")
            if practice_id:
                try:
                    practice = Practice.objects.get(id=practice_id)
                    return self.success(PracticeSerializer(practice).data)
                except Practice.DoesNotExist:
                    return self.error("Practice does not exist")

            practices = Practice.objects.all().order_by("-create_time")
            keyword = request.GET.get("keyword")
            if keyword:
                practices = practices.filter(title__contains=keyword)
            return self.success(self.paginate_data(request, practices, PracticeSerializer))


class UserCollectionListAPI(APIView):
    @staticmethod
    def _add_problem_status(request, data):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            problems_status = profile.acm_problems_status.get("problems", {})
            collections = data.get("results")
            if collections is None:
                return
            for col in collections:
                for problem in col["problems"]:
                    problem["my_status"] = problems_status.get(str(problem["id"]), {}).get("status")

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, **kwargs):
        """
        判断是否登录， 若登录返回用户信息
        """
        user = request.user
        if not user.is_authenticated:
            return self.success()

        collection_type = request.GET.get("type")

        if collection_type == 'course':
            collections = user.course_set.all()
            data = self.paginate_data(request, collections, PracticeSerializer)
            self._add_problem_status(request, data)
            return self.success(data)
        else:
            collections = user.practice_set.all()
            data = self.paginate_data(request, collections, PracticeSerializer)
            self._add_problem_status(request, data)
            return self.success(data)