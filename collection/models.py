from utils.constants import ContestRuleType  # noqa
from django.db import models
from django.utils.timezone import now
from utils.models import JSONField

from utils.constants import ContestStatus, ContestType
from account.models import User
from problem.models import Problem
from utils.models import RichTextField


class Practice(models.Model):
    title = models.TextField()
    description = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    problems = models.ManyToManyField(Problem)
    # 是否可见 false的话相当于删除
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "practice"
        ordering = ("-create_time",)


class Course(models.Model):
    title = models.TextField()
    description = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    problems = models.ManyToManyField(Problem)
    practices = models.ManyToManyField(Practice)
    # 是否可见 false的话相当于删除
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "course"
        ordering = ("-create_time",)
