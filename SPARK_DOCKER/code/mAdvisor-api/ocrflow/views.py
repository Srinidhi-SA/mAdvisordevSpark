import datetime

import simplejson as json
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ocr.models import OCRImage, Template
from ocr.pagination import CustomOCRPagination
from ocr.permission import IsOCRClientUser
from ocr.query_filtering import get_listed_data, get_specific_assigned_requests
from ocrflow.forms import feedbackForm
from ocrflow.models import Task, ReviewRequest, OCRRules
from .serializers import TaskSerializer, \
    ReviewRequestListSerializer, \
    ReviewRequestSerializer, \
    OCRRulesSerializer
from api.datasets.helper import convert_to_string
from api.exceptions import *


# Create your views here.
class OCRRulesView(viewsets.ModelViewSet):
    """
    Model: OCRRules
    Description : Defines OCR rules for reviewer task assignments
    """
    serializer_class = OCRRulesSerializer
    model = OCRRules
    permission_classes = (IsAuthenticated, IsOCRClientUser)

    defaults = {
        "auto_assignmentL1":True,
        "auto_assignmentL2":True,
        "rulesL1": {
            "custom":{
                "max_docs_per_reviewer": 10,
                "selected_reviewers": [],
                "remainaingDocsDistributionRule": 2,
                "active": "False"
                },
            "auto":{
                "max_docs_per_reviewer": 10,
                "remainaingDocsDistributionRule": 2,
                "active": "True"
                }
            },
        "rulesL2":{
            "custom":{
                "max_docs_per_reviewer": 10,
                "selected_reviewers": [],
                "remainaingDocsDistributionRule": 2,
                "active": "False"
                },
            "auto":{
                "max_docs_per_reviewer": 10,
                "remainaingDocsDistributionRule": 2,
                "active": "True"
                }
            }
    }

    @list_route(methods=['post'])
    def autoAssignment(self, request):
        data = request.data

        if data['autoAssignment'] == "True":
            if data['stage'] == "initial":
                ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
                ruleObj.auto_assignmentL1 = True
                ruleObj.save()
                return JsonResponse({"message": "Initial Auto-Assignment Active.", "status": True})
            elif data['stage'] == "secondary":
                ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
                ruleObj.auto_assignmentL2 = True
                ruleObj.save()
                return JsonResponse({"message": "Secondary Auto-Assignment Active.", "status": True})
        else:
            if data['stage'] == "initial":
                ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
                ruleObj.auto_assignmentL1 = False
                ruleObj.save()
                return JsonResponse({"message": "Initial Auto-Assignment De-active.", "status": True})
            elif data['stage'] == "secondary":
                ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
                ruleObj.auto_assignmentL2 = False
                ruleObj.save()
                return JsonResponse({"message": "Secondary Auto-Assignment De-active.", "status": True})

    @list_route(methods=['post'])
    def modifyRulesL1(self, request, *args, **kwargs):
        modifiedrule = request.data
        ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
        ruleObj.rulesL1 = json.dumps(modifiedrule)
        ruleObj.modified_at = datetime.datetime.now()
        ruleObj.save()
        return JsonResponse({"message": "Rules L1 Updated.", "status": True})

    @list_route(methods=['post'])
    def modifyRulesL2(self, request, *args, **kwargs):
        modifiedrule = request.data
        ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
        ruleObj.rulesL2 = json.dumps(modifiedrule)
        ruleObj.modified_at = datetime.datetime.now()
        ruleObj.save()
        return JsonResponse({"message": "Rules L2 Updated.", "status": True})

    @list_route(methods=['get'])
    def get_rules(self, request):
        ruleObj, created = OCRRules.objects.get_or_create(created_by=request.user, defaults=self.defaults)
        if created:
            ruleObj.rulesL1 = json.dumps(self.defaults['rulesL1'])
            ruleObj.rulesL2 = json.dumps(self.defaults['rulesL2'])
            ruleObj.save()
        serializer = OCRRulesSerializer(instance=ruleObj, context={"request": self.request})
        return Response(serializer.data)


class TaskView(viewsets.ModelViewSet):
    """
    Model: Task
    Description :
    """
    serializer_class = TaskSerializer
    model = Task
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomOCRPagination,
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

    def list(self, request):

        return get_listed_data(
            viewset=self,
            request=request,
            list_serializer=TaskSerializer
        )
    # def get_object(self,id):
    #     return Task.objects.get(id=id)

    # @property
    # def task(self,id):
    #     return self.get_object(id)
    def update_pdfReview(self,user,slug):
        imageObject = OCRImage.objects.get(slug=slug)
        reviewObject = ReviewRequest.objects.get(ocr_image_id=imageObject.id)

        if imageObject.is_L2assigned == True:
            ocrImageStatus = 'ready_to_export'
            reviewObject.status = "reviewerL2_reviewed"
        else:
            ocrImageStatus = 'l1_verified'
            reviewObject.status = "reviewerL1_reviewed"

        imageObject.modified_at = datetime.datetime.now()
        imageObject.modified_by = user
        imageObject.update_status(status=ocrImageStatus)

        reviewObject.modified_at = datetime.datetime.now()
        reviewObject.modified_by = user
        reviewObject.save()


    @list_route(methods=['post'])
    def submit_task(self, request, *args, **kwargs):
        try:
            data = request.data

            for id in data['task_id']:
                task_object = Task.objects.get(id=id)
                if request.user == task_object.assigned_user:
                    form = task_object.get_approval_form(request.POST)
                    form.data['status'] = data['status']
                    form.data['remarks'] = data['remarks']
                    if form.is_valid():
                        task_object.submit(
                            form,
                            request.user
                        )
                    else:
                        return JsonResponse({
                            "submitted": False,
                            "is_closed": True,
                            "message": form.errors
                        })
                else:
                    raise PermissionDenied("Not allowed to perform this action.")

            if data['slug']!="":
                self.update_pdfReview(request.user,slug=data['slug'])

            return JsonResponse({
                        "submitted": True,
                        "is_closed": True,
                        "message": "Task Updated Successfully."
                    })
        except Exception as err:
            return JsonResponse({
                        "submitted": False,
                        "Error": str(err)
                    })

    @list_route(methods=['post'])
    def feedback(self, request, *args, **kwargs):
        try:
            data = request.data
            for id in data['task_id']:
                instance = Task.objects.get(id=id)
                if request.user == instance.assigned_user:
                    form = feedbackForm(request.POST)
                    form.data['bad_scan'] = data['bad_scan']
                    if form.is_valid():
                        instance.bad_scan = form.cleaned_data['bad_scan']
                        instance.is_closed = True
                        instance.save()
                        reviewrequest = ReviewRequest.objects.get(id=instance.object_id)
                        reviewrequest.status = "reviewerL1_reviewed"
                        reviewrequest.modified_at = datetime.datetime.now()
                        reviewrequest.modified_by = request.user
                        reviewrequest.save()
                        image_queryset = OCRImage.objects.get(id=reviewrequest.ocr_image.id)
                        image_queryset.status = "bad_scan"
                        image_queryset.modified_by = self.request.user
                        image_queryset.save()
                    else:
                        return JsonResponse({
                            "submitted": False,
                            "message": form.errors
                        })
                else:
                    raise PermissionDenied("Not allowed to perform this POST action.")
            if data['slug']!="":
                imageObject = OCRImage.objects.get(slug=data['slug'])
                reviewObject = ReviewRequest.objects.get(ocr_image_id=imageObject.id)

                reviewObject.status = "reviewerL1_reviewed"
                reviewObject.modified_at = datetime.datetime.now()
                reviewObject.modified_by = request.user
                reviewObject.save()

                imageObject.status = "bad_scan"
                imageObject.modified_by = self.request.user
                imageObject.save()

            return JsonResponse({
                            "submitted": True,
                            "message": "Feedback submitted Successfully."
                        })
        except Exception as error:
            return JsonResponse({
                        "submitted": False,
                        "message": str(error)
                    })



class ReviewRequestView(viewsets.ModelViewSet):
    """
    Model: ReviewRequest
    Description :
    """
    serializer_class = ReviewRequestListSerializer
    model = ReviewRequest
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomOCRPagination

    def get_queryset(self):
        queryset = ReviewRequest.objects.all().order_by('-created_on')
        return queryset

    def get_specific_assigned_queryset(self, username):
        queryset = ReviewRequest.objects.filter(
            #tasks__assigned_user__username=username,
            ocr_image__assignee__username=username,
            ocr_image__deleted=False
        ).exclude(doc_type='pdf_page').order_by('-created_on')
        return queryset

    def get_object_from_all(self):

        return ReviewRequest.objects.get(
            slug=self.kwargs.get('pk')
        )

    def get_task_from_all(self):

        return Task.objects.get(
            id=self.kwargs.get('pk')
        )

    def list(self, request):

        return get_listed_data(
            viewset=self,
            request=request,
            list_serializer=ReviewRequestListSerializer
        )

    @list_route(methods=['get'])
    def assigned_requests(self, request, *args, **kwargs):
        username = self.request.query_params.get('username')
        response = get_specific_assigned_requests(
            viewset=self,
            request=request,
            list_serializer=ReviewRequestSerializer,
            username=username
        )
        temp_obj = Template.objects.first()
        values = list(json.loads(temp_obj.template_classification).keys())
        value = [i.upper() for i in values]
        response.data.update({'values': value})
        return response

    def retrieve(self, request, *args, **kwargs):
        """Returns specific object details"""
        instance = self.get_object_from_all()

        if instance is None:
            return retrieve_failed_exception("ReviewRequest object Doesn't exist.")

        serializer = ReviewRequestSerializer(instance=instance, context={'request': request})

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        data = convert_to_string(data)

        try:
            if 'deleted' in data:
                userGroup = request.user.groups.all()[0].name

                if userGroup == "ReviewerL1":
                    instance = self.get_task_from_all()
                    instance.delete()
                    ocr_image= OCRImage.objects.get(slug=data['image_slug'])
                    if ocr_image.l1_assignee == request.user:
                        ocr_image.l1_assignee = None
                        ocr_image.save()

                    return JsonResponse({'message': 'Deleted'})
                elif userGroup == "ReviewerL2":
                    instance = self.get_task_from_all()
                    instance.delete()
                    ocr_image= OCRImage.objects.get(slug=data['image_slug'])
                    if ocr_image.assignee == request.user:
                        ocr_image.assignee = None
                        ocr_image.save()
                    return JsonResponse({'message': 'Deleted'})
                elif userGroup == "Superuser":
                    instance = self.get_task_from_all()
                    instance.delete()
                    ocr_image= OCRImage.objects.get(slug=data['image_slug'])
                    ocr_image.l1_assignee = None
                    ocr_image.assignee = None
                    ocr_image.save()
                    return JsonResponse({'message': 'Deleted'})
                else:
                    return update_failed_exception("You are not allowed for this operation.")
        except FileNotFoundError:
            return creation_failed_exception("File Doesn't exist.")
