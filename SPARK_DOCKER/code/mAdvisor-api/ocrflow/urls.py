from django.conf.urls import url
from rest_framework import routers

from ocrflow.views import(
    TaskView,
    ReviewRequestView,
    OCRRulesView
)

router = routers.DefaultRouter()
router.register(
    'tasks',
    TaskView,
    base_name='tasks'
)
router.register(
    'review',
    ReviewRequestView,
    base_name='review'
)
router.register(
    'rules',
    OCRRulesView,
    base_name='rules'
)

urlpatterns = [
]
urlpatterns += router.urls
