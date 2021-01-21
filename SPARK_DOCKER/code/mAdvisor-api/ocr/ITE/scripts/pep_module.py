#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests

import cv2
import numpy as np

import PIL
import pillowfight

import concurrent.futures
import backoff


# from scripts.apis import call_counter
# from ITE.scripts.apis import Api_Call
# from debug import debugMode

class Pep:  # preprocess_extract_pipeline

    def __init__(self, image_path, crop=False, c2=True, enhance=True):

        debug = False
        self.image_path = image_path
        self.org_image = cv2.imread(image_path)

        if enhance and min(self.org_image.shape[:2]) >= 1000:
            enhance = False
            enhanced_img = self.adjust_gamma(self.org_image.copy(), gamma=0.4)
            cv2.imwrite(self.image_path, enhanced_img)
            if debug == True: print('prep msg: img quick enhanced')

        if enhance:
            if enhance: self.image_enhancement(self.image_path)
            if debug == True: print('prep msg: img enhanced')

        if crop:
            self.crop_and_save()  ## Edge cropping
            if debug == True: print('prep msg: Crop Success')
        else:
            pass

        if c2:
            _, check = self.crop_img(self.image_path)  ## C2 Cropping
            filename, file_extension = os.path.splitext(self.image_path)

            if type(check) == type(None):  ## C2 FAILED
                self.pep_analysis = self.text_from_Azure_API(self.image_path)
                if debug == True: print('prep msg: C2 Failed , analysis returned')
            else:
                list_of_analysis = []
                paths_to_process = [filename + "_part1.jpg", filename + "_part2.jpg"]

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(self.text_from_Azure_API, path) for path in paths_to_process]
                    loa = {path: futures[i].result() for i, path in enumerate(paths_to_process)}
                for an in sorted(loa):
                    # print("*"*20,an,"*"*20)
                    list_of_analysis.append(loa[an])

                analysis_ite = self.join_analysis(list_of_analysis)
                self.pep_analysis = analysis_ite
                if debug == True: print('prep msg: C2 Success, analysis joined')
        else:
            self.pep_analysis = self.text_from_Azure_API(self.image_path)

        try:
            os.remove(filename + "_part1.jpg")
            os.remove(filename + "_part2.jpg")
            if debug == True: print('prep msg: 2 Parts removed')
        except:
            pass

        cv2.imwrite(self.image_path, self.org_image)  ## write back the original image in prf_to_img folder
        if debug == True: print('prep msg: Original Image written back')

    #    @call_counter
    @backoff.on_exception(backoff.expo, exception=requests.exceptions.HTTPError, max_time=60)
    def text_from_Azure_API(self, path):

        # print("Waiting For API Response")
        subscription_key = "8f6ad67b6c4344779e6148ddc48d96c0"
        vision_base_url = 'https://74psiiujd1.execute-api.us-east-2.amazonaws.com/dev/'
        text_recognition_url = vision_base_url
        data = open(path, "rb").read()

        headers = {'x-api-key': '04jAWz0LXuaLKwtul56lS3PAEpTLNtdn1Gsrgl3k',
                   'Ocp-Apim-Subscription-Key': subscription_key,
                   'Content-Type': 'application/octet-stream'}

        response = requests.post(
            text_recognition_url,
            headers=headers,
            data=data)
        response.raise_for_status()
        analysis = {}
        poll = True
        while (poll):
            response_final = requests.get(
                response.headers["Operation-Location"], headers=headers)
            analysis = response_final.json()
            if ("status" in analysis and analysis['status'] == 'succeeded'):
                poll = False
        return [i for i in analysis["analyzeResult"]["readResults"] if (i["page"] == 1)][0]

    def fetch_analysis(self):
        return self.pep_analysis

    def crop_img(self, image_path):
        filename, file_extension = os.path.splitext(image_path)
        #    print(filename)

        image = cv2.imread(image_path)
        # print("image :",image)
        index = self.crop_2parts(image)

        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            pass
            # print("prep msg: The file does not exist")

        height, width = image.shape[:2]

        if not index:
            # print('prep msg: C2 Failed')
            cv2.imwrite(filename + ".jpg", image)
            return image, None

        elif index >= 50 and index <= height - 50:
            image1, image2 = image[:index, :, :], image[index:, :, :]
            cv2.imwrite(filename + "_part1.jpg", image1)
            cv2.imwrite(filename + "_part2.jpg", image2)
            return image1, image2

        else:
            # print('prep msg: C2 Failed')
            cv2.imwrite(filename + "_part1.jpg", image)
            return image, None

    def crop_2parts(self, image):
        # Binaryconversion : 0 - Black & 1 - White
        #    img_array = np.array(Image.fromarray(image).convert('1')).astype('uint8')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_array = np.where(gray > 127, 1, 0).astype(np.uint8)

        height, width = img_array.shape
        center = height // 2
        index = []
        for i, ar in enumerate(img_array):
            if sum(ar) == len(ar):
                if i > 50 and i <= height - 50:
                    index.append(i)

        if len(index) >= 1:
            crop_index = min(index, key=lambda x: abs(x - center))

            if sum([1 if crop_index + i in index else 0 for i in range(-5, 6)]) >= 10:
                # print('prep msg: optimal point already selected')
                return crop_index
            else:

                optness = {ind: sum([1 if ind + i in index else 0 for i in range(-5, 6)]) for ind in
                           range(crop_index - 10, crop_index + 11) if
                           ind in index}  # Checking in selected pixel +10 pixels for better index
                new_crop_index = max(optness, key=optness.get)
                #            print('OPTNESS : ' ,optness)
                if crop_index == new_crop_index:
                    # print('prep msg: Selected point is close to text')
                    return crop_index
                else:
                    # print('prep msg: selecting optimal point')
                    return new_crop_index


        else:
            sort_array = {i: sum(ar) for i, ar in enumerate(img_array) if (i > 50) and (i < height - 50)}
            highest_value = sort_array[max(sort_array, key=sort_array.get)]
            #            print('HV :',highest_value)
            if highest_value >= int(0.9 * (width)):
                sort_orders = sorted(sort_array.items(), key=lambda x: x[1], reverse=True)
                filtered_indices = [m for m, n in sort_orders if n == highest_value]
                crop_index = min(filtered_indices, key=lambda x: abs(x - center))
                #                print("2")
                # print('prep msg: Selecting best possible index for cut')
                return crop_index

            else:
                return None

    def crop_and_save(self):
        # Read in the image and convert to grayscale
        img = cv2.imread(self.image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # To invert the text to white
        gray = 255 * (gray < 128).astype(np.uint8)
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
        # Find minimum spanning bounding box
        x, y, w, h = cv2.boundingRect(coords)
        # Crop the image - note we do this on the original image
        if ((img.shape[0] > (y + h + 10)) and (img.shape[1] > (x + w + 10))):
            rect = img[y:y + h + 10, x:x + w + 10]
        else:
            rect = img[y:y + h, x:x + w]

        cv2.imwrite(self.image_path, rect)

    def image_enhancement(self, path):
        input_img = PIL.Image.open(path)
        output_img = pillowfight.ace(input_img)
        output_img.save(path)

    def adjust_gamma(self, image, gamma):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) *
                          255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def join_analysis(self, list_of_analysis):

        final_analysis = {}
        current_depth = 0

        for analysis in list_of_analysis:
            current_anlysis = analysis.copy()

            if current_depth != 0:
                for line_number, line in enumerate(analysis['lines']):

                    bb = line['boundingBox'].copy()
                    bb = [bb[i] + current_depth if i % 2 == 1 else bb[i] for i, x in enumerate(bb)]
                    current_anlysis['lines'][line_number]['boundingBox'] = bb

                    for word_number, word in enumerate(analysis['lines'][line_number]['words']):
                        bb = word['boundingBox'].copy()
                        bb = [bb[i] + current_depth if i % 2 == 1 else bb[i] for i, x in enumerate(bb)]
                        current_anlysis['lines'][line_number]['words'][word_number]['boundingBox'] = bb

                    final_analysis['lines'] = final_analysis['lines'] + [current_anlysis['lines'][line_number]]

            else:
                final_analysis = analysis.copy()

            current_depth = current_depth + current_anlysis['height']

        final_analysis['height'] = current_depth
        return final_analysis

# def get_azure_api_calls():
#    azure_api_calls = Pep.text_from_Azure_API.calls
#    Pep.text_from_Azure_API.calls = 0
#    # print("azure_api_calls: ", azure_api_calls)
#    return azure_api_calls
