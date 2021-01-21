#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 17:42:15 2020

@author: rampfire
"""

from ocr.ITE.scripts.data_ingestion import ingestion_1
from ocr.ITE.scripts.apis import Api_Call
from ocr.ITE.scripts.timesheet.timesheet_helper import timesheet_helper_cls
from ocr.ITE.scripts.timesheet.timesheet_class import timesheet_cls
from ocr.ITE.scripts.timesheet.weekdays_in_timesheet import weekdays_timesheet
from ocr.ITE.scripts.timesheet.dates_in_timesheet import dates_timesheet
from ocr.ITE.scripts.timesheet.proximity_words import check_orientation, direct_mapping, group_matches_on_axis, \
    threshold_mapping, same_axis_check, stitch
from ocr.ITE.scripts.timesheet.timesheet_preprocessing import Preprocessing
import os
import sys
from operator import xor
import json
#
import pandas as pd
import time
# from dateutil.parser import parse
from ocr.ITE.scripts.date_corrections import date_operations, year_finder, month_finder, write_new_dates_to_dataframe, \
    check_if_day_first


def timesheet_main(final_json_out):
    df_final = pd.DataFrame()

    data = final_json_out
    updated_analysis = convert_json(data)
    image_shape = data["image_shape"]

    timesheet_obj = timesheet_cls(image_shape)
    timesheet_obj.set_microsoft_analysis(updated_analysis)

    weekdays_found, weekdays_with_coordinates = weekdays_timesheet().check_days(timesheet_obj.microsoft_analysis)
    timesheet_obj.set_weekdays_found(weekdays_found)

    dates_found, dates_with_coordinates = dates_timesheet().date_extractor(timesheet_obj.microsoft_analysis)
    timesheet_obj.set_dates_found(dates_found)
    dates_filter_for_brackets = []
    for detes in dates_with_coordinates:
        bb_detes = list(detes)[0]
        date_cleaned = list(detes)[1].replace('(', '')
        date_cleaned = date_cleaned.replace(')', '')
        dates_filter_for_brackets.append((bb_detes, date_cleaned))

    print("dates_filter_for_brackets:", dates_filter_for_brackets)
    dates_with_coordinates = dates_filter_for_brackets

    hours_found, hours_with_coordinates = timesheet_helper_cls().check_hours(timesheet_obj.microsoft_analysis)
    timesheet_obj.set_hours_found(hours_found)

    print("\ndates_found:", dates_found)
    print("weekdays_found:", weekdays_found)
    print("hours_found:\n", hours_found)

    dates_found = logic_less_filter(dates_with_coordinates)
    print("Dates_with_coordinates:", dates_with_coordinates)
    print("\nDates_found_after_filter:", dates_found)

    ### SECOND CHECK FOR DATES
    if not dates_found:
        dates_found, special_dates_with_coordinates = dates_timesheet().special_date_extractor(
            timesheet_obj.microsoft_analysis)
        print('*' * 20, 'Months found :', special_dates_with_coordinates)
        dates_found = logic_less_filter(special_dates_with_coordinates)
        print('*' * 20, 'Special dates found :', dates_found)

        orientation = check_orientation(special_dates_with_coordinates)
        dates_detected = threshold_mapping(special_dates_with_coordinates, timesheet_obj.microsoft_analysis,
                                           timesheet_obj.image_shape, typ=orientation, combine=True)
        if dates_detected:
            dates_with_coordinates = dates_detected
            print('*' * 20, 'COMBINED DATES :', dates_with_coordinates)
        else:
            print('Special Dates Not found')
    else:
        pass

    dates_as_list = [date_without_bb[1] for date_without_bb in dates_with_coordinates]
    default_year_timesheet_found, default_year_timesheet = year_finder(dates_as_list)
    if default_year_timesheet == 0:
        default_year_timesheet = 2001
    else:
        pass
    default_month_timesheet_found, default_month_timesheet = month_finder(dates_as_list)
    if default_month_timesheet == 0:
        default_month_timesheet = 1
        print("default timesheet not  found setting to 1!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        pass

    weekdays_found = logic_less_filter(weekdays_with_coordinates)
    print("\nWeekdays_with_coordinates:", weekdays_with_coordinates)
    print("Weekdays_found_after_filter:", weekdays_found)

    print("\n Hours with coordinates:", hours_with_coordinates)

    df_to_write = pd.DataFrame()
    df = []

    if dates_found == True and weekdays_found == True and hours_found == True:
        orientation = check_orientation(dates_with_coordinates)
        print('COMING HERE', '*' * 20)
        if same_axis_check(dates_with_coordinates, weekdays_with_coordinates, typ=orientation):

            print("\n Weekdays found on same axis as dates \n")
            dates_with_coordinates = stitch(dates_with_coordinates, weekdays_with_coordinates, typ=orientation)
        else:
            pass

        print("\nOrientation:", orientation)
        df = direct_mapping(dates_with_coordinates, [weekdays_with_coordinates, hours_with_coordinates],
                            typ=orientation)
        print("df:\n", df)
    elif dates_found == True and weekdays_found == False and hours_found == True:
        orientation = check_orientation(dates_with_coordinates)
        print("\nOrientation:", orientation)
        df = direct_mapping(dates_with_coordinates, [hours_with_coordinates], typ=orientation)
        print("df:\n", df)
    elif dates_found == False and weekdays_found == True and hours_found == True:
        orientation = check_orientation(weekdays_with_coordinates)
        print("\nOrientation:", orientation)
        df_with_weekday = direct_mapping(weekdays_with_coordinates, [hours_with_coordinates], typ=orientation)
        dates_detected = threshold_mapping(weekdays_with_coordinates, timesheet_obj.microsoft_analysis,
                                           timesheet_obj.image_shape, typ=orientation)

        if dates_detected:
            print('\nDates Detected Through Threshold:', dates_detected)
            df = direct_mapping(dates_detected, [weekdays_with_coordinates, hours_with_coordinates], typ=orientation)
            print("df:\n", df)
        else:
            print('\nMapping with weekday as header\n')
            df = df_with_weekday
            print("df:\n", df)
            print('\nIgnoreing DF because no dates\n')
            df = None

    else:
        print("\nnot a timesheet")

    if isinstance(df, pd.DataFrame):
        #            df_list.append(df)
        df_to_write = pd.concat([df_to_write, df], axis=0, ignore_index=True)
    #            print('DATA : \n',df)
    else:
        pass
        print('PROPER STRUCTURE NOT FOUND')

    updated_date_in_dict = date_operations(df_to_write, default_year_timesheet, default_month_timesheet)
    dates_corrected_dataframe = write_new_dates_to_dataframe(df_to_write, updated_date_in_dict)
    print('DF TO WRITE :\n', df_to_write)
    print('dates_corrected_dataframe:\n', dates_corrected_dataframe)
    print("days_first_flag:", check_if_day_first(df_to_write))
    print('PROPER STRUCTURE NOT FOUND')
    #    print('DF TO WRITE :',df_to_write)info_to_process=main(input("enter the file path : "))
    if 'dates_corrected_dataframe' in locals() or 'dates_corrected_dataframe' in globals():
        if isinstance(dates_corrected_dataframe, pd.DataFrame):
            df_final = pd.concat([df_final, dates_corrected_dataframe], axis=1, ignore_index=False)
        else:
            pass
        print('\nDF Extracted :\n', df)
        print('\ndates_corrected_dataframe:\n', dates_corrected_dataframe)
    else:
        print('\nDF Extracted :\n', df)

    print('\nFINAL DATA FRAME : ', df_final)
    return df_final


def logic_less_filter(dates_with_coordinates):
    dates_found = False
    try:
        try:
            del (headers)
        except:
            pass
        header_groups, header_group_loc = group_matches_on_axis(dates_with_coordinates, typ="hor")
        for group in header_groups:
            if len(header_groups[group]) > 3:
                headers = header_groups[group]
                header_loc = header_group_loc[group]
            else:
                pass

        if headers:
            orientation = "hor"
            dates_found_in_horizontal = True
    except:
        orientation = "not hor"
        dates_found_in_horizontal = False

    try:
        try:
            del (headers)
        except:
            pass
        header_groups, header_group_loc = group_matches_on_axis(dates_with_coordinates, typ="ver")
        for group in header_groups:
            if len(header_groups[group]) > 3:
                headers = header_groups[group]
                header_loc = header_group_loc[group]
            else:
                pass
        if headers:
            orientation = "ver"
            dates_found_in_vertical = True
    except:
        orientation = "not ver"
        dates_found_in_vertical = False

    print("xor:", xor(dates_found_in_vertical, dates_found_in_horizontal))
    dates_found = xor(dates_found_in_vertical, dates_found_in_horizontal)

    return dates_found


def convert_json(data):
    data.pop("table_coordinates")
    data.pop("temp_number")
    data.pop("domain_classification")
    analysis = {}
    analysis["lines"] = []

    for table in data["tables"].keys():
        for cell in data["tables"][table]:

            if "words" in data["tables"][table][cell]:
                empty_list = []
                for dict_data in (data["tables"][table][cell]["words"]):
                    p1 = dict_data["boundingBox"]["p1"]
                    p3 = dict_data["boundingBox"]["p3"]
                    dict_data["boundingBox"] = [p1[0], p1[1], p3[0], p1[1], p3[0], p3[1], p1[0], p3[1]]
                    empty_list.append(dict_data)
                ne = {"words": empty_list}
                analysis["lines"].append(ne)

    for para in data["paragraphs"]:

        for para_list in data["paragraphs"][para]:
            empty_list = []
            for dict_data in para_list:
                p1 = dict_data["boundingBox"]["p1"]
                p3 = dict_data["boundingBox"]["p3"]
                dict_data["boundingBox"] = [p1[0], p1[1], p3[0], p1[1], p3[0], p3[1], p1[0], p3[1]]
                empty_list.append(dict_data)
            ne = {"words": empty_list}
            analysis["lines"].append(ne)
    return analysis


# THIS FUNCTION NEEDS TO BE CALLED AFTER L1/L2 updates
# timesheet_main('/home/sainadh/ITE_APP_DEV/Intelligent-Text-Extraction/database/we 03-13-20_page_1/final_json.json')
