# -*- coding: utf-8 -*-
import numpy as np
import cv2


def linesObjectContours(CONTOUR, height, width):
    wholeline_indices_V = []
    wholeline_indices_H = []
    VERTICAL_THRESHOLD = int(height * 0.07)
    HORIZONTAL_THRESHOLD = int(width * 0.10)
    contourlist = CONTOUR.copy()
    for idx in range(len(contourlist)):
        eachobject = contourlist[idx]
        x, y, w, h = cv2.boundingRect(eachobject)
        if HORIZONTAL_THRESHOLD < w:
            wholeline_indices_H.append(idx)
            continue
        if VERTICAL_THRESHOLD < h:
            wholeline_indices_V.append(idx)
    return wholeline_indices_H + wholeline_indices_V


def contourLinePlot(CONTOUR, height, width, wholeline_indices):
    blank_image = np.zeros((height, width), np.uint8)
    for idx in wholeline_indices:
        eachobject = CONTOUR[idx]
        i = 0
        j = 1
        while i < len(eachobject):
            currentpoint = eachobject[i][0]
            if j == len(eachobject):
                nextpoint = eachobject[0][0]
            else:
                nextpoint = eachobject[j][0]
            horizontallinelen = abs(nextpoint[0] - currentpoint[0])
            verticallinelen = abs(nextpoint[1] - currentpoint[1])
            tan = verticallinelen / horizontallinelen
            if abs(tan) > 0.03492077 and abs(tan) < 28.63625328:
                i = i + 1
                j = j + 1
            elif horizontallinelen < 7 and verticallinelen < 7:
                i = i + 1
                j = j + 1
            else:
                blank_image = cv2.line(blank_image, (currentpoint[0], currentpoint[1]), (nextpoint[0], nextpoint[1]),
                                       (255, 255, 255), 1)
                i = i + 1
                j = j + 1
    return blank_image


def optimal_params(bw, task='table', scalev=40, scaleh=20):
    if task == 'table':

        vals_v = {i: countour_count(bw, scalev=i, scaleh=20, task='table') for i in np.linspace(30, 60, 10)}
        optimal_scalev = max(vals_v, key=vals_v.get)

        #         optimal_scalev = opt.fminbound(lambda x: countour_count(scalev = x,task = 'table'), 40, 60,xtol=5)

        vals_h = {i: countour_count(bw, scalev=optimal_scalev, scaleh=i, task='table') for i in [10, 20]}
        optimal_scaleh = max(vals_h, key=vals_h.get)

        return round(optimal_scalev), optimal_scaleh

    else:

        vals_v = {i: countour_count(bw, scalev=i, scaleh=20, task='cells') for i in np.linspace(scalev, scalev + 20, 5)}
        max_cnt = max(vals_v.values())
        optimal_scalev = min([int(k) for k in vals_v.keys() if vals_v[k] == max_cnt])

        return optimal_scalev, 20


def countour_count(bw, scalev=40, scaleh=20, task='table'):
    mask, _, _ = extract_mask(bw, scalev=scalev, scaleh=20)

    if task == 'table':
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        parent_area = mask.shape[0] * mask.shape[1]
        areaThr = 0.003 * parent_area
        count = 0
        table_count_dict = {}
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, width, height = cv2.boundingRect(cnt)
            # if  area > areaThr  and  min(width, height) > 12  and  is_single_celled(x, y, x+width, y+height, intersection_coordinates):
            if area > areaThr and min(width, height) > 12:
                table_count_dict[count] = [x, y, x + width - 1, y + height - 1]
                count += 1

        return count

    else:

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areaThr = 1200
        count = 0
        table_count_dict = {}
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, width, height = cv2.boundingRect(cnt)
            # if  area > areaThr  and  min(width, height) > 12  and  is_single_celled(x, y, x+width, y+height, intersection_coordinates):
            if area > areaThr and min(width, height) > 12:
                table_count_dict[count] = [x, y, x + width - 1, y + height - 1]
                count += 1

        return count


def extract_mask(bw, scalev=40, scaleh=20):  ## OVERLAP OF HORIZONTAL AND VERTICAL MASKS
    # Scalev and Scaleh are Used to increase/decrease the amount of lines to be detected

    horizontal = bw.copy()
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal.shape[1] // int(scaleh), 1))
    horizontal = cv2.erode(horizontal, horizontalStructure, iterations=1)
    horizontal = cv2.dilate(horizontal, horizontalStructure, iterations=1)
    # horizontal = cv2.dilate(horizontal, np.ones((4, 4)))
    horizontal = horizontal + cv2.morphologyEx(horizontal, cv2.MORPH_GRADIENT, np.ones((4, 4)))

    vertical = bw.copy()
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical.shape[0] // int(scalev)))
    vertical = cv2.erode(vertical, verticalStructure, iterations=1)
    vertical = cv2.dilate(vertical, verticalStructure, iterations=1)
    # vertical = cv2.dilate(vertical, np.ones((4, 4)))
    vertical = vertical + cv2.morphologyEx(vertical, cv2.MORPH_GRADIENT, np.ones(
        (4, 4)))  ## ADDDING OUTPUT TO ADDITIONAL LAYER OF EXO SKELETON OF THE LINES
    mask = horizontal + vertical

    return mask, horizontal, vertical


def extract_mask_horizontal(bw, scalev=40, scaleh=20):  ## OVERLAP OF HORIZONTAL AND VERTICAL MASKS
    # Scalev and Scaleh are Used to increase/decrease the amount of lines to be detected

    horizontal = bw.copy()
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal.shape[1] // int(scaleh), 1))
    horizontal = cv2.erode(horizontal, horizontalStructure, iterations=2)
    horizontal = cv2.dilate(horizontal, horizontalStructure, iterations=1)
    # horizontal = cv2.dilate(horizontal, np.ones((4, 4)))
    horizontal = horizontal + cv2.morphologyEx(horizontal, cv2.MORPH_GRADIENT, np.ones((4, 4)))

    return horizontal, horizontal, None


def extract_mask_clean(mask):
    # Scalev and Scaleh are Used to increase/decrease the amount of lines to
    # be detected

    black_page = 0 * np.ones(mask.shape).astype(mask.dtype)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    parent_area = mask.shape[0] * mask.shape[1]
    areaThr = 0.003 * parent_area
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area <= areaThr:
            x, y, w, h = cv2.boundingRect(cnt)
            if (h < 0.05 * mask.shape[0]) and (w < 0.05 * mask.shape[1]):  ## 20 % border size check
                mask[y:y + h, x:x + w] = black_page[y:y + h, x:x + w]
            else:
                pass
        else:
            pass

    return mask


def extract_mask_clean_vert(mask):
    black_page = 0 * np.ones(mask.shape).astype(mask.dtype)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    parent_area = mask.shape[0] * mask.shape[1]
    areaThr = 0.003 * parent_area
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area <= areaThr:
            x, y, w, h = cv2.boundingRect(cnt)
            if h < 0.1 * mask.shape[0]:
                mask[y:y + h, x:x + w] = black_page[y:y + h, x:x + w]
            else:
                pass
        else:
            pass

    return mask
