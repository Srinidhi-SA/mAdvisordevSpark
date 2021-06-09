from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from django.contrib import admin
from django.conf import settings
from .utils import json_prettify_for_admin
import simplejson as json

# Register your models here.

from api.models import Dataset, Insight, Job, Score, Trainer,\
    CustomApps, CustomAppsUserMapping, StockDataset, \
    Robo, TrainAlgorithmMapping, DatasetScoreDeployment, ModelDeployment, \
    OutlookToken
from api.user_helper import Profile
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule

admin.site.disable_action('delete_selected')

class DatasetAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">cloud_done</i>'
    search_fields = ["name", "slug"]
    list_display = ["name", "slug", "shared", "created_at", "deleted"]  # TODO: @Ankush Add "created_by"
    # list_filter = []
    list_filter = ["status", "shared", "deleted", "created_by","shared_by"]
    readonly_fields = ["created_at", "deleted", "created_by", "job", "slug", "shared_slug"]


class InsightAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">bubble_chart</i>'
    name = "Signals"
    search_fields = ["name", "slug", "target_column"]
    list_display = ["name", "slug", "type", "target_column", "dataset", "status", "analysis_done", "created_at",
                    "created_by"]
    list_filter = ["status", "deleted", "created_by"]
    readonly_fields = ["created_at", "created_by", "job", "dataset", "slug"]


class JobAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">settings_input_component</i>'
    search_fields = ["name", "slug", "job_type", "url"]
    list_display = ["name", "YARN_URL_html", "job_type", "deleted", "status", 'submitted_by',
                    "msg_count", "time_difference", 'created_at'
                    ]
    list_filter = ["job_type", "status", "submitted_by"]
    # readonly_fields = ("created_at", "javascript_like_config" , "python_like_config", "submitted_by")
    readonly_fields = ("created_at", "submitted_by", "slug")
    actions = ['kill_selected_jobs', 'start_selected_jobs', 'refresh_status']

    def config_prettified(self, instance):
        """Function to display pretty version of our config"""
        return json_prettify_for_admin(json.loads(instance.config))
    config_prettified.short_description = 'ConfigPrettified'
    config_prettified.verbose_name = 'Verbose ConfigPrettified'

    def javascript_like_config(self, instance):
        config_str = instance.config
        replace_words = {
            'None': 'null',
            'True': 'true',
            'False': 'false'
        }

        for key in replace_words:
            config_str.replace(key, replace_words[key])

        return config_str

    def python_like_config(self, instance):
        config_str = instance.config
        replace_words = {
            'null': 'None',
            'true': 'True',
            'false': 'False'
        }

        for key in replace_words:
            config_str.replace(key, replace_words[key])

        return config_str

    def time_difference(self, instance):
        time_difference = instance.updated_at - instance.created_at
        time_delta = str(time_difference).split('.')[0]
        return time_delta


    def messages_prettified(self, instance):
        """Function to display pretty version of our config"""
        return json_prettify_for_admin(json.loads(instance.message_log))
    messages_prettified.short_description = 'MessagespPrettified'

    def YARN_URL_html(self, instance):
        return '<a href="http://{}:{}/cluster/app/{}">{}</a>'.format(settings.YARN.get("host"),
                                                                     settings.YARN.get("port"), instance.url, instance.url)
    YARN_URL_html.short_description = "YARN URL"
    YARN_URL_html.allow_tags = True


    def kill_selected_jobs(self, request, queryset):
        for instance in queryset:
            instance.kill()
        return 'good grace'

    def pause_selected_jobs(self, request, queryset):
        for instance in queryset:
            instance.kill()
        return 'good grace'

    def start_selected_jobs(self, request, queryset):
        for instance in queryset:
            try:
                # if instance.status is 'KILLED' or instance.status is 'FAILED':
                instance.start()
            except Exception as exc:
                print(exc)
        return 'good grace'

    def refresh_status(self, request, queryset):
        for instance in queryset:
            instance.update_status()
        return 'good grace'

    def msg_count(self, instance):
        message_log_json = json.loads(instance.message_log)
        message_count = len(message_log_json)

        error_report_json = json.loads(instance.error_report)
        msgKeys = list(error_report_json.keys())
        msgKeys = list(set(msgKeys))
        errorKeys = [x for x in msgKeys if x != "jobRuntime"]
        timeMsg = "No"
        if "jobRuntime" in msgKeys:
            timeMsg= "Yes"
        error_report_count = len(errorKeys)
        return "Msg:{0}/Err:{1}/Time:{2}".format(message_count, error_report_count,timeMsg)

    def script_time_difference(self, instance):
        message_log_json = json.loads(instance.message_log)
        message_box = ""
        if 'jobRuntime' in message_log_json:
            run_time_msg = message_log_json['jobRuntime']
            for time_msg in run_time_msg:
                if 'endTime' in time_msg and 'startTime' in time_msg:
                    message_box = message_box + " | " +  time_msg['endTime'] - time_msg['startTime']
        return message_box

class ScoreAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assessment</i>'
    search_fields = ["name", "slug"]
    list_display = ["name", "slug", "analysis_done", "created_at", "created_by", "status"]
    list_filter = ["status", "deleted", "created_by"]
    readonly_fields = ["created_at", "trainer",  "created_by", "job", "dataset"]


class TrainerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">tune</i>'
    search_fields = ["name", "slug"]
    list_display = ["name", "slug", "mode", "app_id", "analysis_done", "created_at",
                    "created_by", "deleted", "status"]
    list_filter = ["deleted", "created_by", "status", "mode"]
    readonly_fields = ["created_at", "created_by", "job", "dataset"]

class CustomAppsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">widgets</i>'
    search_fields = ["name", "slug"]
    list_display = ["name", "slug", "app_id","created_by","status","created_at"]
    list_filter = ["status"]
    readonly_fields = ["status","app_id"]

class ProfileAdmin(admin.ModelAdmin):
    # pass
    icon = '<i class="material-icons">Profile</i>'
    list_display = ["name", "website", "city", "phone"]
    # search_fields = ["name"]

    def name(self, instance):
        return instance.user


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Insight, InsightAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Trainer, TrainerAdmin)


from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from .models import Role


admin.site.unregister(Group)
admin.site.register(Role, GroupAdmin)

from django.contrib.auth.models import Permission

class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['name']



# from guardian.admin import GuardedModelAdmin
# from guardian.backends import ObjectPermissionBackend
#
# class DatasetGaurdianAdmin(GuardedModelAdmin):
#     icon = '<i class="material-icons">cloud_done</i>'
#     search_fields = ["name", "slug"]
#     list_display = ["name", "slug", "created_at", "deleted"]  # TODO: @Ankush Add "created_by"
#     # list_filter = []
#     readonly_fields = ["created_at", "deleted", "created_by", "job"]
#
# admin.site.register(Dataset, DatasetGaurdianAdmin)

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class MyUserAdmin(UserAdmin):
    readonly_fields = ("last_login", "date_joined")

class CustomAppUserMappingAdmin(admin.ModelAdmin):
    list_display = ["user", "app", "active", "rank"]
    list_filter = ["user", "app", "active", "rank"]

class StockDatasetAdmin(admin.ModelAdmin):
    pass

class RoboAdmin(admin.ModelAdmin):
    pass

class ModelDeploymentAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assessment</i>'
    search_fields = ["name", "slug"]
    list_display = ["name", "slug", "created_at", "created_by", "status", "deleted", "config"]
    list_filter = ["status", "deleted", "created_by"]
    readonly_fields = ["created_at", "created_by", "slug"]

# class PeriodicTaskAdmin(admin.ModelAdmin):
#     pass

class OutlookTokenAdmin(admin.ModelAdmin):
    list_display = ["id","updated_at", "created_at"]
    readonly_fields = ("updated_at", "created_at")

admin.site.register(User, MyUserAdmin)
admin.site.register(ModelDeployment, ModelDeploymentAdmin)

import django_celery_beat.admin
import auditlog.admin
from auditlog.models import LogEntry
'''
HIDE_FROM_CELERY_FROM_ADMIN = True
KEEP_OTHERS_IN_ADMIN = False
HIDE_AUDIT_LOGS = True
'''

if settings.HIDE_FROM_CELERY_FROM_ADMIN:
    admin.site.unregister(IntervalSchedule)
    admin.site.unregister(CrontabSchedule)
    admin.site.unregister(SolarSchedule)
    admin.site.unregister(PeriodicTask)

if settings.HIDE_AUDIT_LOGS:
    admin.site.unregister(LogEntry)

if settings.KEEP_OTHERS_IN_ADMIN:
    admin.site.register(CustomAppsUserMapping, CustomAppUserMappingAdmin)
    admin.site.register(CustomApps, CustomAppsAdmin)
    admin.site.register(StockDataset, StockDatasetAdmin)
    admin.site.register(Robo, RoboAdmin)
    admin.site.register(Profile, ProfileAdmin)
    admin.site.register(Permission, PermissionAdmin)
    admin.site.register(OutlookToken, OutlookTokenAdmin)
