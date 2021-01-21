import datetime
from ocr.models import OCRImage


def update_reviewrequest_after_RL1_approval(form, reviewrequest, user):
    """This function will get trigger after ReviewerL1 approval.
    Use this function for appropriate state in PROCESS config(process.py).
    """
    status = form.cleaned_data['status']

    reviewrequest.status = "reviewerL1_{}".format(status)
    reviewrequest.modified_at = datetime.datetime.now()
    reviewrequest.modified_by = user
    ocrImageObj = OCRImage.objects.get(id=reviewrequest.ocr_image.id)
    ocrImageStatus = 'l1_verified'
    ocrImageObj.modified_at = datetime.datetime.now()
    ocrImageObj.modified_by = user
    ocrImageObj.update_status(status=ocrImageStatus)
    reviewrequest.save()


def update_reviewrequest_after_RL2_approval(form, reviewrequest, user):
    """This function will get trigger after ReviewerL2 approval.
    Use this function for appropriate state in PROCESS config(process.py).
    """
    status = form.cleaned_data['status']

    reviewrequest.status = "reviewerL2_{}".format(status)
    reviewrequest.modified_at = datetime.datetime.now()
    reviewrequest.modified_by = user
    ocrImageObj = OCRImage.objects.get(id=reviewrequest.ocr_image.id)
    ocrImageStatus = 'ready_to_export'
    ocrImageObj.modified_at = datetime.datetime.now()
    ocrImageObj.modified_by = user
    ocrImageObj.update_status(status=ocrImageStatus)
    reviewrequest.save()
