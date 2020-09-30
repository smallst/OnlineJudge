from utils.api import UsernameSerializer, serializers

from .models import Course, Practice
from account.models import User
from problem.serializers import ProblemSerializer


class CourseSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    problems = ProblemSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description']


class EditCourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description']


class PracticeSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
    problems = ProblemSerializer(many=True)

    class Meta:
        model = Practice
        fields = "__all__"


class CreatePracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = ['title', 'description']


class EditPracticeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Practice
        fields = ['id', 'title', 'description']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"