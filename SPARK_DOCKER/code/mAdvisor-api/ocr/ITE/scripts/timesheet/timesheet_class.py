# -*- coding: utf-8 -*-
import cv2


class timesheet_cls:
    def __init__(self, image_size):
        # self.image_path = image_path
        # self.image = cv2.imread(image_path)
        self.image_shape = image_size
        # self.image_name = image_with_extension.split(".")[0]

    def set_microsoft_analysis(self, analysis):
        self.microsoft_analysis = analysis

    def set_words(self, only_words, words_with_coordinates):
        self.only_words = only_words
        self.words_with_coordinates = words_with_coordinates

    def set_weekdays_found(self, weekdays_found):
        self.weekdays_found = weekdays_found

    def set_alignment(self, time_sheet_alignment):
        self.alignment = time_sheet_alignment

    def set_dates_found(self, dates_found):
        self.dates_found = dates_found

    def set_hours_found(self, hours_found):
        self.hours_found = hours_found
