"""
Miscellaneous celery tasks module for OCR.
"""
import os

import cv2
import simplejson as json
from celery.decorators import task
from celery_progress.backend import ProgressRecorder
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File

from config.settings.config_file_name_to_run import CONFIG_FILE_NAME
from ocr.ITE.master_ite import main, main2, main3
from ocr.ITE.scripts.data_ingestion import ingestion_1
from ocr.ITE.scripts.ui_corrections import ui_flag_v2, ui_flag_v3, ui_flag_v4
from ocr.utils import error_message


@task(name='send_welcome_email', queue=CONFIG_FILE_NAME)
def send_welcome_email(username=None):
    if settings.SEND_WELCOME_MAIL:
        from api.helper import get_outlook_auth
        r = get_outlook_auth(settings.OUTLOOK_AUTH_CODE, settings.OUTLOOK_REFRESH_TOKEN,
                             settings.OUTLOOK_DETAILS)
        result = r.json()
        access_token = result['access_token']
        user = User.objects.get(username=username)
        print("~" * 90)
        print("Sending Welcome mail to : {0}".format(username))

        welcome_mail('send', access_token=access_token, return_mail_id=user.email,
                     subject='Marlabs-Welcome', username=username)
        print("~" * 90)
    else:
        print("Please enable SEND_WELCOME_MAIL=True in order to send welcome email to users.")


@task(name='send_info_email', queue=CONFIG_FILE_NAME)
def send_info_email(username, supervisor):
    if settings.SEND_INFO_MAIL:
        from api.helper import get_outlook_auth
        r = get_outlook_auth(settings.OUTLOOK_AUTH_CODE, settings.OUTLOOK_REFRESH_TOKEN,
                             settings.OUTLOOK_DETAILS)
        result = r.json()
        access_token = result['access_token']
        user = User.objects.get(username=supervisor)
        print("~" * 90)
        print("Sending Info mail to : {0}".format(supervisor))

        info_mail('send', access_token=access_token, return_mail_id=user.email,
                  subject='Marlabs-INFO', username=username, supervisor=supervisor)
        print("~" * 90)
    else:
        print("Please enable SEND_INFO_MAIL=True in order to send info email to Admin.")


def info_mail(action_type=None, access_token=None, return_mail_id=None, subject=None, username=None, supervisor=None):
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        try:
            htmlData = """<!DOCTYPE html><html><body>Dear {},</br></br>User <b>{}</b> is successfully added to mAdvisor.
            </br></br>Have a great day ahead.</br></br>Regards,</br>mAdvisor</body></html>""" \
                .format(supervisor, username)

            messages = send_my_messages(access_token, return_mail_id, subject, htmlData)
            if messages[:3] == '202':
                print("Info mail sent to : {0}".format(supervisor))
        except Exception as e:
            print(e)
            print("Some issue with mail sending module...")


def welcome_mail(action_type=None, access_token=None, return_mail_id=None, subject=None, username=None):
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        try:
            htmlData = """<!DOCTYPE html><html><body>Dear {},</br></br><b>Welcome to mAdvisor.
            </b></br></br>Have a great day ahead.</br></br>Regards,</br>mAdvisor</body></html>""" \
                .format(username)

            messages = send_my_messages(access_token, return_mail_id, subject, htmlData)
            if messages[:3] == '202':
                print("Welcome mail sent.")
        except Exception as e:
            print(e)
            print("Some issue with mail sending module...")


def send_my_messages(access_token, return_mail_id, subject, htmlData):
    '''
    Replies to the mail with attachments
    '''
    get_messages_url = 'https://graph.microsoft.com/v1.0/me/' + '/sendmail'

    payload = {

        "Message": {

            "Subject": subject,
            "Body": {

                "ContentType": "HTML",
                "Content": htmlData,

            },
            "ToRecipients": [
                {
                    "EmailAddress": {
                        "Address": return_mail_id
                    }
                }
            ],
        },
        "SaveToSentItems": "true",

    }
    from api.helper import make_api_call
    import requests

    r = make_api_call('POST', get_messages_url, access_token, payload=payload)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


@task(name='write_to_ocrimage', queue=CONFIG_FILE_NAME, bind=True)
def write_to_ocrimage(self, image, slug, template):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(1, 6, 'Starting recognition')
    path, extension, filename = ingestion_1(image, os.getcwd() + "/ocr/ITE/pdf_to_images_folder")
    progress_recorder.set_progress(2, 6, 'Converting documents')
    res = dict()
    progress_recorder.set_progress(3, 6, 'Running analysis')
    if os.path.isdir(path):
        for index, image in enumerate(os.listdir(path)):
            res[index] = main2(os.path.join(path, image), template)
            res[index]['extension'] = extension
    else:
        res[0] = main2(path, template, slug)
    progress_recorder.set_progress(4, 6, 'Finished analysis')

    from django.apps import apps
    from .models import OCRImage, Template
    from ocr.serializers import OCRImageSerializer

    image_queryset = get_db_object(model_name=OCRImage.__name__,
                                   model_slug=slug
                                   )
    data = {}
    results = []
    image_list = []

    for response in res.values():
        if 'status' in response and response['status'] == 'failed':
            try:
                image_queryset.status = 'failed'
                image_queryset.save()
            except Exception as e:
                data['slug'] = response['image_slug']
                data['imagefile'] = File(name='{}_original_image.png'.format(slug),
                                         file=open(
                                             'ocr/ITE/database/{}_original_image.png'.format(slug),
                                             'rb'))
                data['imageset'] = image_queryset.imageset.id
                data['project'] = image_queryset.project.id
                data['created_by'] = image_queryset.created_by.id
                data['name'] = response['image_name']
                data['status'] = 'failed'
                serializer = OCRImageSerializer(data=data, context={"request": self.request})
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            results.append(
                {'slug': response['image_slug'], 'name': image_queryset.name,
                 'error': error_message(response['category']), 'message': 'FAILED'})
        else:
            slug = response['image_slug']
            progress_recorder.set_progress(5, 6, 'Starting db operations')
            serializer = process_image(data, response, slug, image_queryset)
            if serializer.is_valid():
                serializer.save()
                results.append(
                    {'slug': slug, 'status': serializer.data['status'], 'name': serializer.data['name'],
                     'message': 'SUCCESS'})

                my_model = apps.get_model('ocr', Template.__name__)
                temp_obj = my_model.objects.first()
                temp_obj.template_classification = json.dumps(response['template'])
                temp_obj.save()
                if image_queryset.imagefile.path[-4:] == '.pdf':
                    image_queryset.status = 'ready_to_assign'
                    image_queryset.is_recognized = True
                    image_queryset.save()

                progress_recorder.set_progress(6, 6, 'Extract Successful')
            else:
                image_list.append(response['image_slug'])
                results.append(serializer.errors)
                progress_recorder.set_progress(6, 6, 'Extract Failed')
    if image_list:
        for slug in image_list:
            image_queryset = OCRImage.objects.get(slug=slug)
            image_queryset.status = 'failed'
            image_queryset.save()
    return results


@task(name='write_to_ocrimage_lang_support', queue=CONFIG_FILE_NAME, bind=True)
def write_to_ocrimage_lang_support(self, image, slug, language_input, template):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(1, 6, 'Starting recognition')
    path, extension, filename = ingestion_1(image, os.getcwd() + "/ocr/ITE/pdf_to_images_folder")
    progress_recorder.set_progress(2, 6, 'Converting documents')
    res = dict()
    progress_recorder.set_progress(3, 6, 'Running analysis')
    if os.path.isdir(path):
        for index, image in enumerate(os.listdir(path)):
            res[index] = main3(os.path.join(path, image), template, language_input)
            res[index]['extension'] = extension
    else:
        res[0] = main3(path, template, language_input, slug)
    progress_recorder.set_progress(4, 6, 'Finished analysis')

    from django.apps import apps
    from .models import OCRImage, Template
    from ocr.serializers import OCRImageSerializer

    image_queryset = get_db_object(model_name=OCRImage.__name__,
                                   model_slug=slug
                                   )
    data = {}
    results = []
    image_list = []

    for response in res.values():
        if 'status' in response and response['status'] == 'failed':
            try:
                image_queryset.status = 'failed'
                image_queryset.save()
            except Exception as e:
                data['slug'] = response['image_slug']
                data['imagefile'] = File(name='{}_original_image.png'.format(slug),
                                         file=open(
                                             'ocr/ITE/database/{}_original_image.png'.format(slug),
                                             'rb'))
                data['imageset'] = image_queryset.imageset.id
                data['project'] = image_queryset.project.id
                data['created_by'] = image_queryset.created_by.id
                data['name'] = response['image_name']
                data['status'] = 'failed'
                serializer = OCRImageSerializer(data=data, context={"request": self.request})
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            results.append(
                {'slug': response['image_slug'], 'name': image_queryset.name,
                 'error': error_message(response['category']), 'message': 'FAILED'})
        else:
            slug = response['image_slug']
            progress_recorder.set_progress(5, 6, 'Starting db operations')
            serializer = process_image_lang_support(data, response, slug, image_queryset, language_input)
            if serializer.is_valid():
                serializer.save()
                results.append(
                    {'slug': slug, 'status': serializer.data['status'], 'name': serializer.data['name'],
                     'message': 'SUCCESS'})

                my_model = apps.get_model('ocr', Template.__name__)
                temp_obj = my_model.objects.first()
                temp_obj.template_classification = json.dumps(response['template'])
                temp_obj.save()
                if image_queryset.imagefile.path[-4:] == '.pdf':
                    image_queryset.status = 'ready_to_assign'
                    image_queryset.deleted = True
                    image_queryset.save()

                progress_recorder.set_progress(6, 6, 'Extract Successful')
            else:
                image_list.append(response['image_slug'])
                results.append(serializer.errors)
                progress_recorder.set_progress(6, 6, 'Extract Failed')
    if image_list:
        for slug in image_list:
            image_queryset = OCRImage.objects.get(slug=slug)
            image_queryset.status = 'failed'
            image_queryset.save()
    return results


def process_image(data, response, slug, image_queryset):
    from ocr.serializers import OCRImageSerializer

    data['final_result'] = json.dumps(response['final_json'])
    data['analysis'] = json.dumps(response['analysis'])
    data['mask'] = File(name='{}_mask.png'.format(slug),
                        file=open('ocr/ITE/database/{}_mask.png'.format(slug), 'rb'))
    gen_image, doc_accuracy, total_words = ui_flag_v3(cv2.imread("ocr/ITE/database/{}_mask.png".format(slug)),
                                                      response['final_json'],
                                                      'ocr/ITE/database/{}_gen_image.png'.format(slug),
                                                      response['analysis'])
    data['generated_image'] = File(name='{}_gen_image.png'.format(slug),
                                   file=open('ocr/ITE/database/{}_gen_image.png'.format(slug), 'rb'))
    data['metadata'] = json.dumps(response['metadata'])

    data['is_recognized'] = True
    data['status'] = "ready_to_assign"
    data['slug'] = slug
    data['flag'] = response['flag']
    data['classification'] = str(response['final_json']['temp_number'][0]).upper()

    data['fields'] = total_words
    data['confidence'] = round(doc_accuracy * 100, 2)

    if 'extension' in response and response['extension'] == '.pdf':
        data['imagefile'] = File(name='{}_original_image.png'.format(slug),
                                 file=open('ocr/ITE/database/{}_original_image.png'.format(slug), 'rb'))
        data['imageset'] = image_queryset.imageset.id
        data['identifier'] = image_queryset.identifier
        data['project'] = image_queryset.project.id
        data['created_by'] = image_queryset.created_by.id
        data['name'] = response['image_name']
        data['doctype'] = 'pdf_page'
        serializer = OCRImageSerializer(data=data)
    else:
        del data['slug']
        serializer = OCRImageSerializer(instance=image_queryset, data=data, partial=True)
    return serializer


def process_image_lang_support(data, response, slug, image_queryset, language):
    from ocr.serializers import OCRImageSerializer

    data['final_result'] = json.dumps(response['final_json'])
    data['analysis'] = json.dumps(response['analysis'])
    data['mask'] = File(name='{}_mask.png'.format(slug),
                        file=open('ocr/ITE/database/{}_mask.png'.format(slug), 'rb'))
    print('UI FLAG 4')
    gen_image, total_words = ui_flag_v4(cv2.imread("ocr/ITE/database/{}_mask.png".format(slug)),
                                        response['final_json'],
                                        'ocr/ITE/database/{}_gen_image.png'.format(slug),
                                        response['analysis'], language)
    data['generated_image'] = File(name='{}_gen_image.png'.format(slug),
                                   file=open('ocr/ITE/database/{}_gen_image.png'.format(slug), 'rb'))
    data['metadata'] = json.dumps(response['metadata'])

    data['is_recognized'] = True
    data['status'] = "ready_to_assign"
    data['slug'] = slug
    data['flag'] = response['flag']
    data['classification'] = str(response['final_json']['temp_number'][0]).upper()

    data['fields'] = total_words
    data['confidence'] = round(0.85 * 100, 2)

    if 'extension' in response and response['extension'] == '.pdf':
        data['imagefile'] = File(name='{}_original_image.png'.format(slug),
                                 file=open('ocr/ITE/database/{}_original_image.png'.format(slug), 'rb'))
        data['imageset'] = image_queryset.imageset.id
        data['project'] = image_queryset.project.id
        data['created_by'] = image_queryset.created_by.id
        data['name'] = response['image_name']
        serializer = OCRImageSerializer(data=data)
    else:
        del data['slug']
        serializer = OCRImageSerializer(instance=image_queryset, data=data, partial=True)
    return serializer


def get_db_object(model_name, model_slug):
    from django.apps import apps
    my_model = apps.get_model('ocr', model_name)
    obj = my_model.objects.get(slug=model_slug)
    return obj
