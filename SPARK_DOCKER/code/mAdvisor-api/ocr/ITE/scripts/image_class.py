# -*- coding: utf-8 -*-
import cv2
import os
import json


class image_cls:
    def __init__(self, image_path, image_with_extension):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.image_shape = self.image.shape[:2]
        self.all_JSON = {}
        self.page_metadata = {"order": [], "table": {}, "paragraph": {}}
        self.image_name, _ = os.path.splitext(image_with_extension)

    def set_microsoft_analysis(self, analysis):
        self.microsoft_analysis = analysis

    def set_google_response(self, response):
        self.google_response = response

    def set_domain_flag(self, flag):
        self.domain_flag = flag

    def set_bwimage(self, bw):
        self.bwimage = bw

    def set_deskewed_denoised_blurred_image(
            self, desk_image, denois_image, blurred_img):
        self.deskewed_image = desk_image
        self.denoised_image = denois_image
        self.blurred_img = blurred_img
        self.gray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
        self.bwimage = cv2.adaptiveThreshold(
            ~self.gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 15, -2)

    def set_final_json_mask_metadata(self, final_json, mask, metadata):
        self.mask = mask
        self.final_json = final_json
        self.metadata = metadata

    def get_bwimage(self):
        return self.bwimage

    def get_original_image(self):
        return self.image

    def get_microsoft_analysis(self):
        return self.microsoft_analysis

    def save_result_to_data_base(self):
        image_directory = (os.getcwd() + "/database/" + self.image_name)
        if not os.path.exists(image_directory):
            os.mkdir(image_directory)
        white_background_mask = cv2.bitwise_not(self.mask)
        cv2.imwrite(image_directory + "/mask.png", white_background_mask)
        with open(image_directory + '/final_json.json', 'w') as outfile:
            json.dump(self.final_json, outfile)
        with open(image_directory + '/metadata.json', 'w') as outfile:
            json.dump(self.metadata, outfile)
        cv2.imwrite(image_directory + "/" + self.image_name + ".png", self.image)
