from utils.api import UsernameSerializer, serializers

from .models import Course, Practice


class CourseSerializer(serializers.ModelSerializer):
    created_by = UsernameSerializer()
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

