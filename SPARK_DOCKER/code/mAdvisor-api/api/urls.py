# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework import routers

from api import views
from api.utils import ChangePasswordSerializer
from .datasets.views import DatasetView
# from views import RegressionView
from .dummyModel.models import DummyView
from .views import AppView
from .views import AudiosetView
from .views import ChangePasswordView
from .views import DatasetScoreDeployementView
from .views import ModelDeployementView
from .views import RoboView
from .views import ScoreView, StockDatasetView, get_concepts_to_show_in_ui
from .views import SignalView, get_datasource_config_list, get_algorithm_config_list
from .views import TrainAlgorithmMappingView
from .views import TrainerView
from .views import UserView

# Start adding urlconf from here

router = routers.DefaultRouter()
router.register(
    'datasets',
    DatasetView,
    base_name='datasets'
)

router.register(
    'signals',
    SignalView,
    base_name='signals'
)

router.register(
    'trainer',
    TrainerView,
    base_name='trainer'
)

router.register(
    'score',
    ScoreView,
    base_name='score'
)

router.register(
    'robo',
    RoboView,
    base_name='robo'
)

router.register(
    'audioset',
    AudiosetView,
    base_name='audioset'
)

router.register(
    'stockdataset',
    StockDatasetView,
    base_name='stockdataset'
)

router.register(
    'apps',
    AppView,
    base_name='apps'
)

router.register(
    'dummy',
    DummyView,
    base_name='dummy'
)

router.register(
    'trainalgomapping',
    TrainAlgorithmMappingView,
    base_name='trainalgomapping'
)

router.register(
    'deploymodel',
    ModelDeployementView,
    base_name='deploymodel'
)

router.register(
    'datasetscoredeploy',
    DatasetScoreDeployementView,
    base_name='datasetscoredeploy'
)

router.register(
    'users',
    UserView,
    base_name='users'
)
# router.register(
#     'regression',
#     RegressionView,
#     base_name='regression'
# )

from api.user_helper import upload_photo, get_profile_image

urlpatterns = [
    url(r'^view_model_summary_autoML', views.view_model_summary_autoML, name="view_model_summary_autoML"),
    url(r'^view_model_summary_detail', views.view_model_summary_detail, name="view_model_summary_detail"),
    url(r'^datasource/get_config_list$', get_datasource_config_list, name="datasource_get_config_list"),
    url(r'^job/(?P<slug>[^/.]+)/get_config$', views.get_config, name="get_config"),
    url(r'^job/(?P<slug>[^/.]+)/set_result', views.set_result, name="set_result"),
    url(r'^job/(?P<slug>[^/.]+)/rest_in_peace', views.end_of_this_world, name="end_of_this_world"),
    url(r'^job/(?P<slug>[^/.]+)/use_set_result', views.use_set_result, name="use_set_result"),
    url(r'^job/(?P<slug>[^/.]+)/dump_complete_messages', views.dump_complete_messages, name="dump_complete_messages"),
    url(r'^download_data/(?P<slug>[^/.]+)', views.get_chart_or_small_data, name="get_chart_or_small_data"),
    url(r'^get_info', views.get_info, name="get_info"),
    url(r'^messages/(?P<slug>[^/.]+)/', views.set_messages, name="set_messages"),
    url(r'^xml/(?P<slug>[^/.]+)/', views.set_pmml, name="set_pmml"),
    url(r'^get_job_kill/(?P<slug>[^/.]+)/', views.get_job_kill, name="get_job_kill"),
    url(r'^get_job_refreshed/(?P<slug>[^/.]+)/', views.get_job_refreshed, name="get_job_refreshed"),
    url(r'^get_job_restarted/(?P<slug>[^/.]+)/', views.get_job_restarted, name="get_job_restarted"),
    url(r'^get_xml/(?P<slug>[^/.]+)/(?P<algoname>[^/.]+)/', views.get_pmml, name="get_pmml"),
    url(r'^set_job_report/(?P<slug>[^/.]+)/(?P<report_name>[^/.]+)/', views.set_job_reporting,
        name="set_job_reporting"),
    url(r'^get_job_report/(?P<slug>[^/.]+)/', views.get_job_report, name="get_job_report"),
    url(r'^upload_photo', upload_photo, name="upload_photo"),
    url(r'^get_profile_image/(?P<slug>[^/.]+)/', get_profile_image, name="get_profile_image"),
    url(r'^stockdatasetfiles/(?P<slug>[^/.]+)/', views.get_stockdatasetfiles, name="get_stockdatasetfiles"),
    url(r'^get_concepts/', get_concepts_to_show_in_ui, name="get_concepts"),
    url(r'^get_metadata_for_mlscripts/(?P<slug>[^/.]+)/', views.get_metadata_for_mlscripts,
        name="get_metadata_for_mlscripts"),
    url(r'^get_score_data_and_return_top_n/', views.get_score_data_and_return_top_n,
        name="get_score_data_and_return_top_n"),
    url(r'^get_recent_activity', views.get_recent_activity, name="get_recent_activity"),
    url(r'^delete_and_keep_only_ten_from_all_models', views.delete_and_keep_only_ten_from_all_models,
        name="delete_and_keep_only_ten_from_all_models"),
    url(r'^get_app_algorithm_config_list/', get_algorithm_config_list, name="get_app_algorithm_config_list"),
    url(r'^get_app_id_map', views.get_appID_appName_map, name="get_app_id_map"),
    url(r'^nifi_update', views.updateFromNifi, name="nifi_update"),
    url(r'^all_apps_for_users', views.all_apps_for_users, name="all_apps_for_users"),
    url(r'^disable_all_periodic_tasks', views.disable_all_periodic_tasks, name="disable_all_periodic_tasks"),
    url(r'^request_from_alexa', views.request_from_alexa, name="request_from_alexa"),
    # url(r'^get_all_models', views.get_all_models, name="get_all_models"),
    # url(r'^get_all_signals', views.get_all_signals, name="get_all_signals"),
    # url(r'^get_all_users', views.get_all_users, name="get_all_users"),
    url(r'^kill_timeout_job_from_ui', views.kill_timeout_job_from_ui, name="kill_timeout_job_from_ui"),
    url(r'^change-user-password/', ChangePasswordView.as_view(serializer_class=ChangePasswordSerializer)),
    # url(r'^get_all_user/', UserView.as_view()),
    # url(r'^some_random_things', views.some_random_things, name="nifi_update"),
]

urlpatterns += router.urls
# print urlpatterns
