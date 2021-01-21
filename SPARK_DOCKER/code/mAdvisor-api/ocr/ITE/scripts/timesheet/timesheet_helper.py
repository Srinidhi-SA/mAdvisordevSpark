# -*- coding: utf-8 -*-
from statistics import mean
import numpy as np
import re
from itertools import compress


class timesheet_helper_cls():
    def __init__(self):
        self.weekday_keyword_list = ["sun", "mon", "tue", "wed", "thu", "fri", "sat", "sunday", "monday", "tuesday",
                                     "wednesday", "thursday", "friday", "saturday"]

    def extract_words_from_response(self, analysis):
        """
        function to retrieve all the words from the response

        input:pagewise response from microsoft analysis
        with_coordinates:if True retrieve's the coordinates also
        return:list of all the words in dictionary format with and without coordinates
        """

        only_words = [bb['text'] for line in analysis["lines"] for bb in line['words']]
        words_with_coordinates = []
        for line in analysis["lines"]:
            for bb in line['words']:
                words_with_coordinates.append(bb)
        return only_words, words_with_coordinates

    def timesheet_contains_weekdays(self, words):
        """
        function to find if the time sheet contains weekdays

        input:word_list
        return: True if timesheet contains weekdays
                number of weekdays found
        """
        weekdays_found = False
        number_of_weekdays_found = 0

        for i in words:
            if i.lower() in self.weekday_keyword_list:
                number_of_weekdays_found += 1
                weekdays_found = True
        return weekdays_found, number_of_weekdays_found

    def classify_whether_hor_vert_weekdays(self, word_coordinates):
        """
        function to classify whether the time sheet belongs to  a horizontal
        or vertical class.

        input:wordlist with coorinates
        output:"horizontal":if time sheet is horizontally aligned(refer image
                hhhhhhhhhhhhhh for definition for same)
                "vertical":if time sheet is vertically aligned(refer image
                vvvvvvvvvv for definition for same)
        """
        weekdays_in_timesheet_with_cordinates = []

        for i in word_coordinates:
            if (i["text"]).lower() in self.weekday_keyword_list:
                weekdays_in_timesheet_with_cordinates.append(i)

        weekday_centroid_x_only = []
        weekday_centroid_y_only = []
        for weekday in weekdays_in_timesheet_with_cordinates:
            p1 = weekday["boundingBox"][0:2]
            p3 = weekday["boundingBox"][4:6]
            c = centroid_between_p1_p3(p1, p3)
            weekday.update({"centroid": c})
            weekday_centroid_x_only.append(c[0])
            weekday_centroid_y_only.append(c[1])

        mean_centroid_y_only = mean(weekday_centroid_y_only)
        mean_centroid_x_only = mean(weekday_centroid_x_only)

        difference_y = np.array(weekday_centroid_y_only) - mean_centroid_y_only

        difference_x = np.array(weekday_centroid_x_only) - mean_centroid_x_only
        # =============================================================================
        #         print("weekdays_in_timesheet_with_cordinates",weekdays_in_timesheet_with_cordinates)
        #         print("difference_y",difference_y)
        #         print("difference_x",difference_x)
        # =============================================================================
        if all(abs(i) < 2.5 for i in difference_y):
            return "horizontal"
        elif all(abs(i) < 20 for i in difference_x):
            return "vertical"

    def date_extractor(self, analysis):

        date_match = re.compile(
            r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+|[\d]{1,2}/[\d]{1,2}')
        date_match2 = re.compile(r'^[1-9]$|[1-2][0-9]$|3[01]$')

        dates = []
        wc = {}
        for i, line in enumerate(analysis["lines"]):
            wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

        for line in wc:

            present_line = wc[line]
            for bb, word in present_line:

                if date_match.search(word.lower()):
                    dates.append((bb, word))
        return dates

    #    def check_hours(self,analysis):
    #
    #        cords = []
    #        polygons = []
    #        status = True
    #        time_sheet_hours = re.compile('(^(([0-4]{0,1}[0-9]( )?)|(([0]?[1-9]|1[0-2])(:|-|\.)[0-5][0-9]( )?)|(([0]?[0-9]|1[0-9]|2[0-3])(:|-|\.)[0-5][0-9]))$)')
    #
    #
    #
    #        # Extract the recognized text, with bounding boxes.
    #        polygons = [(line["boundingBox"], line["text"]) for line in analysis["lines"]]
    #
    #        cords = [word if time_sheet_hours.search(word[1]) else False for word in polygons]
    #        polygons = list(compress(polygons,cords))
    #
    #        if len(polygons) >= 5:
    #            print(status)
    #            return polygons,status
    #
    #        else:
    #            print(False)
    #            status = False
    #            return polygons,status

    def check_hours(self, analysis):

        time_sheet_hours = re.compile(
            '(^(([0-4]{0,1}[0-9]( )?)|(([0]?[1-9]|1[0-2])(:|-|\.)[0-5][0-9]( )?)|(([0]?[0-9]|1[0-9]|2[0-3])(:|-|\.)[0-5][0-9]))$)')
        hour_match = re.compile('^(([0-1]{0,1}[0-9]( )?(H|h))(:| |-)([0-5][0-9]( )?(M|m))$)')  ### 08:00
        #        hour_match = re.compile('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')   ### 08:00
        hour_match2 = re.compile(r'[-+]?\d*\.\d+')  # 8.00
        hour_match3 = re.compile(r'^[0-9]$')
        hours_match4 = re.compile('[o|b][h|m]|[0-9]{1,2}[h|m]')
        Hours = []
        wc = {}
        for i, line in enumerate(analysis["lines"]):
            wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

        for line in wc:

            present_line = wc[line]
            for bb, word in present_line:

                if hour_match.search(word.lower()) or hour_match2.search(word.lower()) or hour_match3.search(
                        word.lower()) or hours_match4.search(word.lower()) or time_sheet_hours.search(word.lower()):
                    Hours.append((bb, word))
        if Hours:
            return True, Hours
        else:
            return False, Hours


def centroid_between_p1_p3(p1, p3):
    """
    function to calculate the centroid between points p1 and p3

    input:p1:list of x and y coordinate
          p3:list of x and y coordinate
    output:centroid:list of x and y
    """

    centroid_x = (p1[0] + p3[0]) * 0.5
    centroid_y = (p1[1] + p3[1]) * 0.5
    return [centroid_x, centroid_y]
