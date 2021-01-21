# -*- coding: utf-8 -*-

from PIL import Image, ImageChops
import glob
import cv2
import numpy as np


class Preprocessing:
    def __init__(self, image_path):
        self.image_path = image_path

    def crop_and_save(self, path_to_save):
        img = cv2.imread(self.image_path)  # Read in the image and convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = 255 * (gray < 128).astype(np.uint8)  # To invert the text to white
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
        rect = img[y:y + h, x:x + w]  # Crop the image - note we do this on the original image
        #        cv2.imshow("Cropped", rect) # Show it
        # cv2.waitKey(0)
        #        cv2.destroyAllWindows()
        # print("paaaaaaaaaaaaaaaaaaaaaath")
        # print(path_to_save)
        cv2.imwrite(path_to_save, rect)

    # def crop_and_save(self,path_to_save):
    #     cropped_image=self.crop_image(self.image_path)
    #     cropped_image.save(path_to_save)
