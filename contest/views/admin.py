import dateutil.parser
from utils.api import APIView, validate_serializer
from django.utils import timezone
from account.models import AdminType
from ..serializers import CreateConetestSeriaizer, ContestSerializer
from ..models import Contest


class ContestAPI(APIView):
    @validate_serializer(CreateConetestSeriaizer)
    def post(self, request):
        data = request.data
        data["start_time"] = dateutil.parser.parse(data["start_time"])
        data["end_time"] = dateutil.parser.parse(data["end_time"])
        data["created_by"] = request.user
        if data["end_time"] <= data["start_time"]:
            return self.error("Start time must occur earlier than end time")
        if not data["password"]:
            data["password"] = None
        Contest.objects.create(**data)
        return self.success()

    def get(self, request):
        contest_id = request.GET.get("id")
        if contest_id:
            try:
                contest = Contest.objects.get(id=contest_id)
                if request.user.is_admin_role():
                    contest = contest.get(created_by=request.user)
                return self.success(ContestSerializer(contest).data)
            except Contest.DoesNotExist:
                return self.error("Contest does not exist")
        contests = Contest.objects.all().order_by("-create_time")
        if request.user.is_admin_role():
            contests = contests.filter(created_by=request.user)
        return self.success(self.paginate_data(request, contests, ContestSerializer))