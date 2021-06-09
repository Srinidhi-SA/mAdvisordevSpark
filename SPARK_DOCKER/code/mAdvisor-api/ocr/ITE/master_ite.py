# -*- coding: utf-8 -*-
import base64
import random
import string
import sys
import time
import os

import cv2
from django.template.defaultfilters import slugify

from ocr.ITE.scripts.data_ingestion import ingestion_1
from ocr.ITE.scripts.image_class import image_cls
from ocr.ITE.scripts.apis import Api_Call, fetch_google_response2, Api_Call2
from ocr.ITE.scripts.domain_classification import Domain
from ocr.ITE.scripts.pep_module import Pep
from ocr.ITE.scripts.preprocessing import Preprocess
from ocr.ITE.scripts.base_module import BaseModule
from ocr.ITE.scripts.timesheet.timesheet_preprocessing import Preprocessing
from ocr.ITE.scripts.transcripts import Transcript


def main(input_path, template, slug=None):
    print("Loading File")
    print("Waiting For API Response")

    if slug is None:
        slug = slugify("img-" + ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    try:
        api_response = Api_Call(input_path)
    except Exception as e:
        image = cv2.imread(input_path)
        original_image = "ocr/ITE/database/{}_original_image.png".format(slug)
        cv2.imwrite(original_image, image)

        with open(original_image, mode='rb') as file:
            img = file.read()

        og = base64.encodebytes(img)
        response = {
            'image_slug': slug,
            'original_image': og,
            'image_name': input_path.split('/')[-1].split('.')[0],
            'status': 'failed',
            'error': str(e)
        }
        return response
    # google_response2 = fetch_google_response2(input_path)

    flag = Domain().process_domain(api_response.page_wise_response(1), cv2.imread(input_path))
    if flag == "Time Sheet":
        Preprocessing(input_path).crop_and_save(input_path)
        api_response = Api_Call(input_path)
    image_obj = image_cls(input_path, input_path.split('/')[-1])
    image_obj.set_microsoft_analysis(api_response.page_wise_response(1))

    analysis = image_obj.microsoft_analysis
    image_obj.set_domain_flag(flag)
    print('\n FLAG : ', flag)

    de_skewed_img, de_noised_img, blurred_img = Preprocess().pre_process(
        image_obj.image, image_obj.image_shape)

    image_obj.set_deskewed_denoised_blurred_image(
        de_skewed_img, de_noised_img, blurred_img)

    if flag == 'Transcript':

        trobj = Transcript()

        x, y = trobj.intermediate_1(image_obj.microsoft_analysis, image_obj.image_path, return_sem_info=False)

        print('\n SEM INFO  : \n', x)
    else:

        base_obj = BaseModule(image_obj, input_path.split('/')[-1])
        final_json, mask, metadata, template = base_obj.extract_info(template, base_obj.bwimage, flag,
                                                                     image_obj.image_shape)
        image_obj.set_final_json_mask_metadata(final_json, mask, metadata)
        white_background_mask = cv2.bitwise_not(mask)
        if os.path.exists("ocr/ITE/database/{}_mask.png".format(slug)):
            with open("ocr/ITE/database/{}_mask.png".format(slug), mode='rb') as file:
                img = file.read()
            mask = base64.encodebytes(img)
        else:
            cv2.imwrite("ocr/ITE/database/{}_mask.png".format(slug), white_background_mask)
            with open("ocr/ITE/database/{}_mask.png".format(slug), mode='rb') as file:
                img = file.read()
            mask = base64.encodebytes(img)

        image = cv2.imread(input_path)
        original_image = "ocr/ITE/database/{}_original_image.png".format(slug)
        cv2.imwrite(original_image, image)

        with open(original_image, mode='rb') as file:
            img = file.read()

        og = base64.encodebytes(img)

        response = {
            'final_json': final_json,
            'mask': mask,
            'metadata': metadata,
            'analysis': analysis,
            # 'google_response2': google_response2,
            'flag': flag,
            'image_slug': slug,
            'original_image': og,
            'image_name': input_path.split('/')[-1].split('.')[0],
            'template': template
        }
        return response


def main2(input_path, template, slug=None):
    print("Loading File")
    print("Waiting For API Response")

    if slug is None:
        slug = slugify("img-" + ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    try:
        pep = Pep(input_path)
    except Exception as e:
        image = cv2.imread(input_path)
        original_image = "ocr/ITE/database/{}_original_image.png".format(slug)
        cv2.imwrite(original_image, image)

        response = {
            'image_slug': slug,
            'original_image': original_image,
            'image_name': input_path.split('/')[-1].split('.')[0],
            'status': 'failed',
            'error': str(e),
            'category': e.__class__.__name__
        }
        return response
    # google_response2 = fetch_google_response2(input_path)

    flag = Domain().process_domain(pep.fetch_analysis(), cv2.imread(input_path))
    if flag == "Time Sheet":
        Preprocessing(input_path).crop_and_save(input_path)
        pep = Pep(input_path)
    image_obj = image_cls(input_path, input_path.split('/')[-1])
    image_obj.set_microsoft_analysis(pep.fetch_analysis())

    analysis = image_obj.microsoft_analysis
    image_obj.set_domain_flag(flag)
    print('\n FLAG : ', flag)

    de_skewed_img, de_noised_img, blurred_img = Preprocess().pre_process(
        image_obj.image, image_obj.image_shape)

    image_obj.set_deskewed_denoised_blurred_image(
        de_skewed_img, de_noised_img, blurred_img)

    if flag == 'Transcript':

        trobj = Transcript()

        x, y = trobj.intermediate_1(image_obj.microsoft_analysis, image_obj.image_path, return_sem_info=False)

        print('\n SEM INFO  : \n', x)
    else:

        base_obj = BaseModule(image_obj, input_path.split('/')[-1])
        final_json, mask, metadata, template = base_obj.extract_info(template, base_obj.bwimage, flag,
                                                                     image_obj.image_shape)
        image_obj.set_final_json_mask_metadata(final_json, mask, metadata)

        from ocr.ITE.scripts.ensemble import ensemble_main
        text_resp = fetch_google_response2(input_path)
        fj = ensemble_main(final_json, pep.fetch_analysis(), text_resp)

        white_background_mask = cv2.bitwise_not(mask)
        if not os.path.exists("ocr/ITE/database/{}_mask.png".format(slug)):
            cv2.imwrite("ocr/ITE/database/{}_mask.png".format(slug), white_background_mask)

        image = cv2.imread(input_path)
        original_image = "ocr/ITE/database/{}_original_image.png".format(slug)
        cv2.imwrite(original_image, image)

        response = {
            'final_json': fj,
            'mask': "ocr/ITE/database/{}_mask.png".format(slug),
            'metadata': metadata,
            'analysis': analysis,
            'flag': flag,
            'image_slug': slug,
            'original_image': original_image,
            'image_name': input_path.split('/')[-1].split('.')[0],
            'template': template
        }
        return response


def main3(input_path, template, language_input, slug=None):
    print("Loading File")
    print("Waiting For API Response")

    if slug is None:
        slug = slugify("img-" + ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    try:
        api_response = Api_Call2(input_path, language_input)
    except Exception as e:
        image = cv2.imread(input_path)
        original_image = "ocr/ITE/database/{}_original_image.png".format(slug)
        cv2.imwrite(original_image, image)

        response = {
            'image_slug': slug,
            'original_image': original_image,
            'image_name': input_path.split('/')[-1].split('.')[0],
            'status': 'failed',
            'error': str(e),
            'category': e.__class__.__name__
        }
        return response
    # google_response2 = fetch_google_response2(input_path)

    flag = Domain().process_domain(api_response.page_wise_response(1), cv2.imread(input_path))
    image_obj = image_cls(input_path, input_path.split('/')[-1])
    image_obj.set_microsoft_analysis(api_response.page_wise_response(1))

    analysis = image_obj.microsoft_analysis
    image_obj.set_domain_flag(flag)
    print('\n FLAG : ', flag)

    de_skewed_img, de_noised_img, blurred_img = Preprocess().pre_process(
        image_obj.image, image_obj.image_shape)

    image_obj.set_deskewed_denoised_blurred_image(
        de_skewed_img, de_noised_img, blurred_img)

    if flag == 'Transcript':

        trobj = Transcript()

        x, y = trobj.intermediate_1(image_obj.microsoft_analysis, image_obj.image_path, return_sem_info=False)

        print('\n SEM INFO  : \n', x)
    else:

        base_obj = BaseModule(image_obj, input_path.split('/')[-1])
        final_json, mask, metadata, template = base_obj.extract_info(template, base_obj.bwimage, flag,
                                                                     image_obj.image_shape)
        image_obj.set_final_json_mask_metadata(final_json, mask, metadata)
        white_background_mask = cv2.bitwise_not(mask)
        if not os.path.exists("ocr/ITE/database/{}_mask.png".format(slug)):
            cv2.imwrite("ocr/ITE/database/{}_mask.png".format(slug), white_background_mask)

        image = cv2.imread(input_path)
        original_image = "ocr/ITE/database/{}_original_image.png".format(slug)
        cv2.imwrite(original_image, image)

        response = {
            'final_json': final_json,
            'mask': "ocr/ITE/database/{}_mask.png".format(slug),
            'metadata': metadata,
            'analysis': analysis,
            'flag': flag,
            'image_slug': slug,
            'original_image': original_image,
            'image_name': input_path.split('/')[-1].split('.')[0],
            'template': template
        }
        return response

