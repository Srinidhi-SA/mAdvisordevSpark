"""
Miscellaneous celery tasks module for OCRflow.
"""

from django.conf import settings
from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from config.settings.config_file_name_to_run import CONFIG_FILE_NAME
from ocr.models import OCRImage
from ocrflow.models import *
import datetime
import math
import random

def get_L2_task_assignment_count(querysetCount, percentage):
    percentage = int(math.floor((percentage/100)*querysetCount))
    return percentage

@periodic_task(run_every=(crontab(minute='*/1')), name="start_auto_assignment_L1", ignore_result=False,
               queue=CONFIG_FILE_NAME)
def start_auto_assignment_L1():
    OCRRules_queryset = OCRRules.objects.all()
    for OCRRule in OCRRules_queryset:
        if OCRRule.auto_assignmentL1:
            print("~" * 90)
            #TODO
            #1.Filter all Images with Recognised True, assigned = False
            ocrImageQueryset = OCRImage.objects.filter(
                is_recognized=True,
                is_L1assigned=False,
                created_by = OCRRule.created_by
            ).order_by('created_at')
            if len(ocrImageQueryset)>0:
                for image in ocrImageQueryset:
                    #TODO Checkif reviewrequest already exists.
                    if len(ReviewRequest.objects.filter(ocr_image=image))==0:
                        object = ReviewRequest.objects.create(
                            ocr_image = image,
                            created_by = image.created_by,
                            rule = OCRRule
                        )
                    else:
                        #TODO Try to assign the backlog task
                        object = ReviewRequest.objects.get(ocr_image = image)
                        object.start_simpleflow()

                    if object.status =='submitted_for_review(L1)':
                        task=Task.objects.get(object_id = object.id)
                        print("Task assigned:  {0}  -  User:  {1}".format(image.name, task.assigned_user))
                        continue
                    else:
                        print("~" * 90)
                        break

                print("~" * 90)
            else:
                print("All images got assigned for review for Superuser-{0}".format(OCRRule.created_by))
                print("~" * 90)
        else:
            print("~" * 90)
            print("Auto-Assignment is not Active for Superuser-{0}".format(OCRRule.created_by))
            print("~" * 90)

@periodic_task(run_every=(crontab(minute='*/1')), name="start_auto_assignment_L2", ignore_result=False,
               queue=CONFIG_FILE_NAME)
def start_auto_assignment_L2():
    OCRRules_queryset = OCRRules.objects.all()
    for OCRRule in OCRRules_queryset:
        if OCRRule.auto_assignmentL2:
            print("~" * 90)
            reviewRequestIDs = ReviewRequest.objects.filter(
                tasks__is_closed = True,
                ocr_image__is_L2assigned = False,
                ocr_image__status__in = ["l1_verified"],
                ocr_image__created_by = OCRRule.created_by,
                ocr_image__modified_at__gt = datetime.datetime.now()-datetime.timedelta(days=7),
                ocr_image__modified_at__lte = datetime.datetime.now()
            ).values_list('id', flat=True)

            #Calculate taskLimit as per the percentage of Assignment and Total reviewRequestIDs

            percentage = settings.OCR_SECONDARY_TASK_PERCENTAGE
            querysetCount = len(reviewRequestIDs)
            taskLimit = get_L2_task_assignment_count(querysetCount, percentage)

            #Randomly select Review Objects as per the taskLimit
            random_reviewRequestIDs_list = random.sample(list(reviewRequestIDs), min(len(reviewRequestIDs), taskLimit))
            reviewRequestQueryset = ReviewRequest.objects.filter(id__in=random_reviewRequestIDs_list)
            print("~~~~~~~~~~~~~~~~~~~~~~~ Superuser - {0} ~~~~~~~~~~~~~~~~~~~~~".format(OCRRule.created_by))
            print("Total Pending Tasks for L2 Review: {0}".format(querysetCount))
            print("Percentage Assignment :  {0}".format(percentage))
            print("Total Task in Queue for L2 assignment :  {0}".format(taskLimit))
            if taskLimit > 0:
                for reviewObj in reviewRequestQueryset:
                    reviewObj.start_simpleflow(initial_state='RL2_approval')

                    if reviewObj.status =='submitted_for_review(L2)':
                        task=Task.objects.get(object_id = reviewObj.id, is_closed=False)
                        print("Task assigned:  {0}  -  User:  {1}".format(reviewObj.ocr_image.name, task.assigned_user))
            else:
                print("All images got assigned for L2 review for Superuser-{0}".format(OCRRule.created_by))

            print("~" * 90)
        else:
            print("~" * 90)
            print("Auto-Assignment is not Active for Superuser-{0}".format(OCRRule.created_by))
            print("~" * 90)



#    print("~" * 100)
