# Generated by Django 2.1.7 on 2020-09-29 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0003_auto_20200901_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practice',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='practice',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_practices', to=settings.AUTH_USER_MODEL),
        ),
    ]