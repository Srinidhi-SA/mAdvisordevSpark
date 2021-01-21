from rest_framework import serializers
from .models import Task, ReviewRequest, OCRRules
from ocr.models import OCRImage
from ocr.serializers import OCRImageReviewSerializer
import simplejson as json
from api.user_helper import UserSerializer

class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """
    def to_representation(self, instance):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(instance, ReviewRequest):
            serializer = ReviewRequestSerializer(instance)
            return serializer.data
        elif isinstance(instance, Task):
            serializer = TaskSerializer(instance)
            return serializer.data

        raise Exception('Unexpected type of tagged object')

class TaskSerializer(serializers.ModelSerializer):
    """
    """
    def to_representation(self, instance):
        serialized_data = super(TaskSerializer, self).to_representation(instance)
        serialized_data['assigned_user'] = UserSerializer(instance.assigned_user).data['username']

        return serialized_data

    class Meta:
        """
        Meta class definition for TaskSerializer
        """
        model = Task
        fields = ("id", "assigned_user", "is_closed", 'reviewed_on')

class ReviewRequestListSerializer(serializers.ModelSerializer):
    """
    """

    def to_representation(self, instance):
        serialized_data = super(ReviewRequestListSerializer, self).to_representation(instance)
        return serialized_data
    class Meta:
        """
        Meta class definition for ReviewRequestListSerializer
        """
        model = ReviewRequest
        fields = ('id', 'slug', 'status')

class ReviewRequestSerializer(serializers.ModelSerializer):
    """
    """
    status_mapping = {"created": "Created",
                      "submitted_for_review(L1)": "Review Pending(L1)",
                      "submitted_for_review(L2)": "Review Pending(L2)",
                      "reviewerL1_reviewed": "Review Completed(L1)",
                      "reviewerL2_rejected": "Rejected L2",
                      "reviewerL2_reviewed": "Review Completed(L2)",
                      "reviewerL1_rejected": "Rejected L1"}

    tasks=ContentObjectRelatedField(many=True, queryset=Task.objects.all())
    def to_representation(self, instance):
        serialized_data = super(ReviewRequestSerializer, self).to_representation(instance)
        Image_instance = OCRImage.objects.get(id=instance.ocr_image.id)
        serialized_data['status'] = self.status_mapping[serialized_data['status']]
        serialized_data['ocrImageData'] = OCRImageReviewSerializer(Image_instance).data
        serialized_data['project'] = Image_instance.project.name
        serialized_data['modified_by'] = (UserSerializer(instance.modified_by).data['username']).capitalize()
        return serialized_data

    class Meta:
        """
        Meta class definition for ReviewRequestSerializer
        """
        model = ReviewRequest
        exclude = ('id', 'slug', 'ocr_image', 'created_by', 'rule')

class OCRRulesSerializer(serializers.ModelSerializer):
    """
    Provides Serialized json data of OCR rules.
    """

    def to_representation(self, instance):
        serialized_data = super(OCRRulesSerializer, self).to_representation(instance)
        serialized_data['rulesL1'] = json.loads(serialized_data['rulesL1'])
        serialized_data['rulesL2'] = json.loads(serialized_data['rulesL2'])
        return serialized_data
    class Meta:
        """
        Meta class definition for OCRRulesSerializer
        """
        model = OCRRules
        exclude = ('id',)
