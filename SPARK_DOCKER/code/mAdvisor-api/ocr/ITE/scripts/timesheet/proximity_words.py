#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import os

import re
import time
import copy
import cv2
import json
from collections import Counter

import numpy as np
import pandas as pd


def proxim(bounding_box, threshold, wc):  # WORKING AWSM

    th = threshold
    p1, p2, p3, p4 = bounding_box[:2], bounding_box[2:4], bounding_box[4:6], bounding_box[6:]
    p1x, p1y = [p1[0] - th, p1[1]], [p1[0], p1[1] - th]
    p2x, p2y = [p2[0] + th, p2[1]], [p2[0], p2[1] - th]
    p3x, p3y = [p3[0] + th, p3[1]], [p3[0], p3[1] + th]
    p4x, p4y = [p4[0] - th, p4[1]], [p4[0], p4[1] + th]

    top_bb = [p1y, p2y, p2, p1]
    bottom_bb = [p4, p3, p3y, p4y]

    left_bb = [p1x, p1, p4, p4x]
    right_bb = [p2, p2x, p3x, p3]

    #    p = Point(cord)
    top_proximity, bottom_proximity = Polygon(top_bb), Polygon(bottom_bb)
    left_proximity, right_proximity = Polygon(left_bb), Polygon(right_bb)

    top_bucket, bottom_bucket, left_bucket, right_bucket = [], [], [], []
    for line in wc:

        present_line = wc[line]
        for bb, word in present_line:
            # p1     p2    p3    p4
            centroid = ((bb[0] + bb[4]) * 0.5, (bb[1] + bb[5]) * 0.5)  ### [x1,y1,x2,y2,x3,y3,x4,y4]
            p = Point(centroid)

            if top_proximity.contains(p):
                top_bucket.append(word)
            elif bottom_proximity.contains(p):
                bottom_bucket.append(word)
            elif left_proximity.contains(p):
                left_bucket.append(word)
            elif right_proximity.contains(p):
                right_bucket.apppend(word)
            else:
                pass

    return top_bucket, bottom_bucket, left_bucket, right_bucket


# proxim([885, 246, 948, 250, 948, 273, 885, 271],100,wc)

def date_extractor(analysis):
    date_match = re.compile(
        r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+|[\d]{1,2}/[\d]{1,2}')
    date_match2 = re.compile(r'^[1-9]$|[1-2][0-9]$|3[01]$')

    dates = []
    wc = {}
    for i, line in enumerate(analysis["recognitionResults"][0]["lines"]):
        wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

    for line in wc:

        present_line = wc[line]
        for bb, word in present_line:

            if date_match.search(word.lower()):
                dates.append((bb, word))

    return dates


def centroid(bb):
    return (int((bb[0] + bb[4]) * 0.5), int((bb[1] + bb[5]) * 0.5))


def check_orientation(l):  # DATES

    if len(l) >= 2:
        centroids = [centroid(bb) for bb, txt in l]

        xs = [cen[0] for cen in centroids]
        ys = [cen[1] for cen in centroids]

        #        print(xs)
        #        print(ys)
        x_dict = dict(enumerate(grouper(xs), 1))
        y_dict = dict(enumerate(grouper(ys), 1))

        x_lens = [len(val) for val in list(x_dict.values())]
        y_lens = [len(val) for val in list(y_dict.values())]

        x_oriented = sum([1 for val in list(x_dict.values()) if len(val) > 3]) > 0
        y_oriented = sum([1 for val in list(y_dict.values()) if len(val) > 3]) > 0

        if x_oriented:
            return "ver"
        elif y_oriented:
            return "hor"
        else:
            return "No Orientation"
    else:
        return "Too few Dates"


def grouper(iterable):
    prev = None
    group = []
    for item in iterable:
        if not prev or item - prev <= 15:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group


def group_matches_on_axis(dates, typ='hor'):
    word_p1_p3 = {i: (tup[0][:2], tup[0][4:6]) for i, tup in enumerate(dates)}
    word_text = {i: tup[1] for i, tup in enumerate(dates)}
    #    if typ == 'hor':

    axis_points = {}
    clubbed_groups = {}
    clubbed_groups_locations = {}

    for word_number in word_p1_p3:
        p1, p3 = word_p1_p3[word_number]

        if typ == 'hor':
            axis_points[word_number] = (p1[1] + p3[1]) * 0.5
        else:
            axis_points[word_number] = (p1[0] + p3[0]) * 0.5

        if word_number == 0:
            group_number = 1
            clubbed_groups[group_number] = [word_number]
            clubbed_groups_locations[group_number] = [(p1, p3)]
        else:
            group_number = compare_axis_points(word_number, clubbed_groups, axis_points)
            #                print('WORD NUMBER:',word_number,'SELECTED GROUP:',group_number,'\n********************' )
            if group_number in clubbed_groups:

                new_val = clubbed_groups[group_number] + [word_number]
                new_val2 = clubbed_groups_locations[group_number] + [(p1, p3)]
                #                    print('COMIN HERE',new_val )
                clubbed_groups[group_number] = new_val
                clubbed_groups_locations[group_number] = new_val2
            else:
                clubbed_groups[group_number] = [word_number]
                clubbed_groups_locations[group_number] = [(p1, p3)]

    #        print('clubbed_groups_locations :',clubbed_groups_locations)
    group_dates_output = {}
    for group in clubbed_groups:
        group_dates_output[group] = [word_text[word_number] for word_number in clubbed_groups[group]]

    #    print("group_dates_output:",group_dates_output)
    return group_dates_output, clubbed_groups_locations


def compare_axis_points(word_number, clubbed_groups_dict, axis_points_dict):
    present_axis_point = axis_points_dict[word_number]

    for group in clubbed_groups_dict:
        compare_with = int(np.mean([axis_points_dict[word_number] for word_number in clubbed_groups_dict[group]]))

        if int(present_axis_point) in range(compare_with - 15, compare_with + 16):
            return group

    return np.max(list(clubbed_groups_dict.keys())) + 1


def direct_mapping(header, data_list,
                   typ='hor'):  ## header = weekdays or dates /////data_list = [weekday,hours] [hours]

    header_groups, header_group_loc = group_matches_on_axis(header, typ=typ)

    for group in header_groups:
        if len(header_groups[group]) > 3:
            headers = header_groups[group]
            header_loc = header_group_loc[group]
        #            print('Header :', headers)
        #            print('HEADER LOC: ',header_loc)
        else:
            pass
    #    print("datagroups")
    #    data_groups,data_group_loc = group_matches_on_axis(data_list[0],typ =typ)
    #    for group in data_groups:
    #        print(data_groups[group],data_group_loc[group])

    if ('headers' in globals()) or ('headers' in locals()):
        df = pd.DataFrame(columns=headers)
        pass
    else:
        print("No valid Header")
        return None

    rows = {}
    row_location = {}

    prefered_row_axis = []  ## CAPTURES THE LOCATION OF TOTAL KEYWORD

    for data in data_list:
        data_groups, data_group_loc = group_matches_on_axis(data, typ=typ)

        print('DATA GRPS:', data_groups)
        #        print('Data Locations',data_group_loc)

        for group in data_groups:
            #            print('\ndata_groups[group] ',data_groups[group])
            #            print('Headers:',headers)

            if (len(data_groups[group]) == 1) and (data_groups[group][0] in ['Total', 'total',
                                                                             'TOTAL']):  ## GETTING THE ROW IN ALIGNMENT WITH 'TOTAL' Keyword

                if typ == 'hor':
                    prefered_row_axis.append(centroid_p1p3(data_group_loc[group][0])[1])
                else:
                    prefered_row_axis.append((centroid_p1p3(data_group_loc[group][0])[0]))

            #                print('\nprefered_row_axis:',prefered_row_axis,'\n')

            #            elif (len(data_groups[group]) == len(headers)): ## LEN OF HEADERS MATCH THE LENGHT OF DATA ROW
            #
            #                curr_row = data_groups[group]
            #                rows[group] = curr_row
            #
            #                if typ == 'hor': row_location[group] = centroid_p1p3(data_group_loc[group][0])[1]
            #                else : row_location[group] = centroid_p1p3(data_group_loc[group][0])[0]

            elif len(data_groups[group]) > 3 and (list(filter(lambda x: x != 'NA', headers)) != data_groups[group]):

                if typ == 'hor':
                    row_location[group] = centroid_p1p3(data_group_loc[group][0])[1]
                else:
                    row_location[group] = centroid_p1p3(data_group_loc[group][0])[0]

                curr_row = ['NA' for header in headers]
                curr_index = -1
                for i, header in enumerate(headers):

                    p1, p3 = header_loc[i]  ##PRESENT HEADER LOC
                    found = False

                    if typ == 'hor':

                        x1, x2 = p1[0], p3[0]  # HEADER LOC
                        for j, p1_p3 in enumerate(data_group_loc[group]):
                            cord = p1_p3[0][0], p1_p3[1][0]  ## x1,x2 of data
                            if found == False:
                                if (cord[0] in range(x1 - 15, x1 + 16)) or (cord[1] in range(x2 - 15, x2 + 16)) \
                                        or (abs(sum(cord) - sum((x1, x2))) <= 25) or (
                                        int(sum(cord) * 0.5) in range(x1, x2)):

                                    if j > curr_index:
                                        if curr_row[i] != 'NA':
                                            curr_row[i] = curr_row[i] + ' ' + data_groups[group][j]
                                        else:
                                            curr_row[i] = data_groups[group][j]
                            else:
                                pass
                    else:
                        y1, y2 = p1[1], p3[1]  # HEADER LOC
                        for j, p1_p3 in enumerate(data_group_loc[group]):
                            cord = p1_p3[0][1], p1_p3[1][1]
                            if found == False:
                                #                                print("y1_y2",y1,y2)
                                if (cord[0] in range(y1 - 15, y1 + 16)) or (cord[1] in range(y2 - 15, y2 + 16)) \
                                        or (abs(sum(cord) - sum((y1, y2))) <= 25) or (
                                        int(sum(cord) * 0.5) in range(y1, y2)):

                                    if j > curr_index:
                                        curr_row[i] = data_groups[group][j]

                                    curr_index = j
                                    found = True
                            else:
                                pass
                rows[group] = curr_row
            else:
                pass

        ################################## SELECTING THE CORRECT HRS ROW

        if len(row_location) == 0:
            break
        first_row_group = min(row_location, key=row_location.get)
        first_row = rows[first_row_group]
        first_row_location = row_location[first_row_group]

        last_row_group = max(row_location, key=row_location.get)
        last_row = rows[last_row_group]
        last_row_location = row_location[last_row_group]
        #        print('\nSELECTED ROW:',selected_row)
        #        print('Selected row location:',selected_row_location)

        del row_location[last_row_group]
        if len(row_location) > 0:
            backup_row_group = max(row_location, key=row_location.get)
            backup_row = rows[backup_row_group]
            backup_row_location = row_location[backup_row_group]
        #            print('\nBACKUPROW',backup_row)

        else:
            pass

        final_selected_row = []
        ### CHECK WITH TOTAL KEYWORD AXIS
        if len(prefered_row_axis) > 0:
            for loc in prefered_row_axis:
                if loc in range(first_row_location - 5, first_row_location + 5):
                    final_selected_row = last_row
                    break

                if loc in range(last_row_location - 5, last_row_location + 5):
                    final_selected_row = last_row
                    break

                if 'backup_row_location' in locals() or 'backup_row_location' in globals():

                    if loc in range(backup_row_location - 5, backup_row_location + 5):
                        final_selected_row = backup_row
                        break
        else:
            pass

        if len(final_selected_row) > 0:
            print('\nTotal Hrs Found****\n')
            df = pd.DataFrame([final_selected_row], columns=headers)
        #            print("/nY row Picke UP",'*'*10)
        elif 'backup_row_location' in locals() or 'backup_row_location' in globals():
            #            final_selected_row = finalise_row(selected_row,backup_row)
            if assess_row(last_row):  ### CHECK IF LAST ROW IS VALID
                df = pd.DataFrame([last_row], columns=headers)
                print("/nZ row Picke UP", '*' * 10)
            elif assess_row(backup_row):
                print("/nY row Picke UP", '*' * 10)
                df = pd.DataFrame([backup_row], columns=headers)
            else:
                df = pd.DataFrame([first_row], columns=headers)
                print("/nA row Picke UP", '*' * 10)
        else:
            df = pd.DataFrame([last_row], columns=headers)
            print("/nZ* row Picke UP", '*' * 10)
    #        df = pd.DataFrame(list(rows.values()),columns = headers)
    #        print('ROWLOCATION:',row_location)
    #        print('ROWS:',rows)
    return df


def assess_row(last_row):
    hour_match = re.compile('^(1?[1-9]|2[0-3]):[0-5][0-9]$')  ### 08:00
    hour_match2 = re.compile(r'[-+]?\d*\.\d+')  # 8.00
    hour_match3 = re.compile(r'^[1-9]$')

    matches = []
    for word in last_row:

        if hour_match.search(word.lower()) or hour_match2.search(word.lower()) or hour_match3.search(word.lower()):
            matches.append(True)
        else:
            matches.append(False)

    #    print('\nMATCHES :',matches)
    if sum(matches) == 0:
        return False
    else:
        return True


def centroid_p1p3(p1p3):
    p1, p3 = p1p3[0], p1p3[1]
    return (int((p1[0] + p3[0]) * 0.5), int((p1[1] + p3[1]) * 0.5))


def same_axis_check(dates, weekdays, typ='hor'):
    dates_groups, dates_group_loc = group_matches_on_axis(dates, typ=typ)

    for group in dates_groups:
        if len(dates_groups[group]) > 3:
            selected_dates = dates_groups[group]
            selected_dates_loc = dates_group_loc[group]
            selected_dates_axis = centroid_p1p3(selected_dates_loc[0])

            break
        else:
            pass

    weekdays_groups, weekdays_group_loc = group_matches_on_axis(weekdays, typ=typ)

    for group in weekdays_groups:
        if len(weekdays_groups[group]) > 3:
            selected_weekdays = weekdays_groups[group]
            selected_weekdays_loc = weekdays_group_loc[group]
            selected_weekdays_axis = centroid_p1p3(selected_weekdays_loc[0])

            break
        else:
            pass

    if (('selected_dates_axis' in locals()) or ('selected_dates_axis' in globals())) and (
            ('selected_weekdays_axis' in locals()) or ('selected_weekdays_axis' in globals())):
        if typ == 'hor' and abs(selected_dates_axis[1] - selected_weekdays_axis[1]) < 5:
            return True
        elif typ == 'ver' and abs(selected_dates_axis[0] - selected_weekdays_axis[0]) < 5:
            return True
        else:
            return False
    else:
        return False


def stitch(dates, weekdays, typ='hor'):
    bucket = []
    for i, el in enumerate(dates):

        bb_d, date = el
        p1, p2, p3, p4 = bb_d[:2], bb_d[2:4], bb_d[4:6], bb_d[6:]

        th = abs(bb_d[2] - bb_d[0])  ## taking the width of date itself as threshold

        p1x = [p1[0] - th, p1[1]]
        p2x = [p2[0] + th, p2[1]]
        p3x = [p3[0] + th, p3[1]]
        p4x = [p4[0] - th, p4[1]]

        left_bb = [p1x, p1, p4, p4x]
        right_bb = [p2, p2x, p3x, p3]

        #        print('DATE : ',date, 'RIGHTBB :' ,right_bb)
        left_prox = Polygon(left_bb)
        right_prox = Polygon(right_bb)

        for bb_w, day in weekdays:

            weekday_centroid = Point(centroid(bb_w))
            #            print("WEEKDAY : ",day, 'CENTROID : ',centroid(bb_w))
            if left_prox.contains(weekday_centroid):
                stiched_bb = [bb_w[:2], p2, p3, bb_w[6:]]
                stiched_bb = [cord for sublist in stiched_bb for cord in sublist]
                bucket.append((stiched_bb, date))
                #                print('BBUPDATED -left')
                break
            elif right_prox.contains(weekday_centroid):
                stiched_bb = [p1, bb_w[2:4], bb_w[4:6], p4]
                stiched_bb = [cord for sublist in stiched_bb for cord in sublist]
                bucket.append((stiched_bb, date))
                #                print('BBUPDATED -right')
                break
            else:
                #                print('NO UPDATE')
                pass

    return bucket


def fetch_proxim(bb, threshold, wc, *regex, side="right"):
    """
    bb :bounding box  of the header


    """
    th = threshold
    p1, p2, p3, p4 = bb[:2], bb[2:4], bb[4:6], bb[6:]
    p1x, p1y = [p1[0] - th, p1[1]], [p1[0], p1[1] - th]
    p2x, p2y = [p2[0] + th, p2[1]], [p2[0], p2[1] - th]
    p3x, p3y = [p3[0] + th, p3[1]], [p3[0], p3[1] + th]
    p4x, p4y = [p4[0] - th, p4[1]], [p4[0], p4[1] + th]

    top_bb = [p1y, p2y, p2, p1]
    bottom_bb = [p4, p3, p3y, p4y]

    left_bb = [p1x, p1, p4, p4x]
    right_bb = [p2, p2x, p3x, p3]

    #    p = Point(cord)
    if side == 'right':
        prox = Polygon(right_bb)
    elif side == 'left':
        prox = Polygon(left_bb)
    elif side == 'top':
        prox = Polygon(top_bb)
    else:
        prox = Polygon(bottom_bb)

    bucket = []
    for line in wc:

        present_line = wc[line]
        for bb, word in present_line:
            # p1     p2    p3    p4
            centroid = ((bb[0] + bb[4]) * 0.5, (bb[1] + bb[5]) * 0.5)  ### [x1,y1,x2,y2,x3,y3,x4,y4]
            p = Point(centroid)

            if prox.contains(p):

                if side == 'left':
                    stiched_bb = [bb[:2], p2, p3, bb[6:]]
                    stiched_bb = [cord for sublist in stiched_bb for cord in sublist]
                    bucket.append((stiched_bb, word))
                elif side == 'right':
                    stiched_bb = [p1, bb[2:4], bb[4:6], p4]
                    stiched_bb = [cord for sublist in stiched_bb for cord in sublist]
                    bucket.append((stiched_bb, word))
                else:
                    x1, y1 = min(p1[0], bb[0]), min(p1[1], bb[1])
                    x3, y3 = max(p3[0], bb[4]), max(p3[1], bb[5])
                    stiched_bb = bb
                    stiched_bb[0], stiched_bb[1], stiched_bb[4], stiched_bb[5] = x1, y1, x3, y3
                    bucket.append((stiched_bb, word))
            else:
                pass
    # print('*'*20,bucket)
    #    print(regex)

    words = [(bb, word) for bb, word in bucket for reg in regex if reg.search(word.lower())]

    if len(words) > 0:
        return words[0]
    else:
        return None


def group_filter(header, typ='hor'):
    header_groups, header_group_loc = group_matches_on_axis(header, typ=typ)

    for group in header_groups:
        if len(header_groups[group]) > 3:
            headers = header_groups[group]
            break
        else:
            pass
    if 'headers' in locals() or 'headers' in globals():
        filtered_header = [(bb, word) for bb, word in header if word in headers]
    else:
        filtered_header = header

    return filtered_header


def threshold_mapping(header, analysis, shape, typ='hor', combine=False):
    header = group_filter(header, typ=typ)

    if typ == 'hor':
        window = int(shape[1] / 20)
    else:
        window = int(shape[0] / 20)

    wc = {}
    for i, line in enumerate(analysis["lines"]):
        wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

    regex = re.compile(r'^0?[1-9]$|[1-2][0-9]$|3[01]$')
    regex2 = re.compile(
        r'(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?[a-z\s,.]*(?:\d{1,2}[-/th|st|nd|rd)\s,]*)+(?:\d{2,4})+|[\d]{1,2}/[\d]{1,2}')

    i = 1
    while i <= 3:  ## DEPTH OF 3 TIMES

        th = i * window
        for bounding_box, data in header:  # LOOP OVER ALL THE HEADERS

            #            th = i*abs(bounding_box[0]-bounding_box[2])
            date_location = None
            res = check_proxim(bounding_box, th, wc, regex, regex2)
            #            print(res)
            if res != "Date not found in Proxim":
                date_location = res
                threshold = th
                break
            else:
                pass

        if date_location:
            break
        else:
            i = i + 1

    print("\nDATELOACATION:", date_location)
    if date_location:
        curr_row = ['NA' for bb, data in header]

        for i, el in enumerate(header):

            bb, data = el
            word = fetch_proxim(bb, threshold, wc, regex, regex2, side=date_location)
            # fetch_proxim([751, 413, 799, 415, 799, 434, 751, 431],50,wc,regex,regex2,side = "top")
            if not combine:
                if word:
                    curr_row[i] = word
                else:
                    curr_row[i] = (bb, 'NA')
            else:
                if word:
                    curr_row[i] = (word[0], word[1] + ' ' + data)
                else:
                    curr_row[i] = (bb, '_ ' + data)
        #        return list(filter(lambda x: x!= 'NA',curr_row))
        # dates = list(filter(lambda x: x!= 'NA',curr_row))
        dates = curr_row
        els = [val for bb, val in curr_row if val != 'NA']
        nas = sum([1 if val == 'NA' else 0 for bb, val in curr_row])

        if len(dates) > 0 and nas <= int(len(curr_row) / 2) + 1 and len(set(els)) >= len(els) - 2:

            return dates
        else:

            return None
    else:

        return None


def check_proxim(bb, th, wc, *regex):
    p1, p2, p3, p4 = bb[:2], bb[2:4], bb[4:6], bb[6:]
    p1x, p1y = [p1[0] - th, p1[1]], [p1[0], p1[1] - th]
    p2x, p2y = [p2[0] + th, p2[1]], [p2[0], p2[1] - th]
    p3x, p3y = [p3[0] + th, p3[1]], [p3[0], p3[1] + th]
    p4x, p4y = [p4[0] - th, p4[1]], [p4[0], p4[1] + th]

    top_bb = [p1y, p2y, p2, p1]
    bottom_bb = [p4, p3, p3y, p4y]

    left_bb = [p1x, p1, p4, p4x]
    right_bb = [p2, p2x, p3x, p3]

    #    p = Point(cord)
    top_proximity, bottom_proximity = Polygon(top_bb), Polygon(bottom_bb)
    left_proximity, right_proximity = Polygon(left_bb), Polygon(right_bb)

    for line in wc:

        present_line = wc[line]
        for bb, word in present_line:
            # p1     p2    p3    p4
            centroid = ((bb[0] + bb[4]) * 0.5, (bb[1] + bb[5]) * 0.5)  ### [x1,y1,x2,y2,x3,y3,x4,y4]
            p = Point(centroid)

            if right_proximity.contains(p):
                if True in [True if reg.search(word.lower()) else False for reg in regex]:
                    return "right"
            elif left_proximity.contains(p):
                if True in [True if reg.search(word.lower()) else False for reg in regex]:
                    return "left"
            elif bottom_proximity.contains(p):
                if True in [True if reg.search(word.lower()) else False for reg in regex]:
                    return "bottom"
            elif top_proximity.contains(p):
                if True in [True if reg.search(word.lower()) else False for reg in regex]:
                    return "top"
            else:
                pass

    return "Date not found in Proxim"
