from django.conf.urls import url

from ..views.admin import CourseAPI, PracticeAPI, AddCollectionProblemAPI, CollectionParticipantAPI

urlpatterns = [
    url(r"^course/?$", CourseAPI.as_view(), name="course_admin_api"),
    url(r"^practice/?$", PracticeAPI.as_view(), name="practice_admin_api"),
    url(r"^collection/add_problem_from_public/?$", AddCollectionProblemAPI.as_view(), name="add_collection_problem_from_public_api"),
    url(r"^collection/participant/?$", CollectionParticipantAPI.as_view(), name="collection_participant_api")
]
