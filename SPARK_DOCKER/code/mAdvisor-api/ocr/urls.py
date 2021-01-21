"""
URLs file for OCR app.
"""
from django.conf.urls import url
from rest_framework import routers

# from ocr import views
from ocr.views import ocr_datasource_config_list, ProjectView, \
    get_dashboard_metrics, get_recent_activity
from ocr.views import OCRImageView, OCRImagesetView, OCRUserView, \
    OCRUserProfileView, GroupListView

# -------------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# -------------------------------------------------------------------------------

router = routers.DefaultRouter()
router.register(
    'ocrimage',
    OCRImageView,
    base_name='ocrimages'
)

router.register(
    'ocrimageset',
    OCRImagesetView,
    base_name='ocrimagesets'
)

router.register(
    'user',
    OCRUserView,
    base_name='user'
)

router.register(
    'userprofile',
    OCRUserProfileView,
    base_name='userprofile'
)
router.register(
    'project',
    ProjectView,
    base_name='projects'
)

urlpatterns = [
    url(r'^datasource/ocr_datasource_config_list$', ocr_datasource_config_list, name="ocr_datasource_config_list"),
    url(r'^groups/',GroupListView.as_view(), name="groups"),
    url(r'^get_dashboard_metrics', get_dashboard_metrics, name="get_dashboard_metrics"),
    url(r'^get_recent_activity', get_recent_activity, name="get_recent_activity"),

]
urlpatterns += router.urls
