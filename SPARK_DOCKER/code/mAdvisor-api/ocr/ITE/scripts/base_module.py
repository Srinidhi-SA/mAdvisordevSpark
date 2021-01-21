# -*- coding: utf-8 -*-
from ocr.ITE.scripts.utils import optimal_params, extract_mask_clean, extract_mask_clean_vert
from ocr.ITE.scripts.utils import extract_mask, extract_mask_horizontal, linesObjectContours, contourLinePlot
import numpy as np
import cv2
from sklearn.cluster import DBSCAN
from math import ceil
from collections import OrderedDict
from scipy.spatial import distance
from ocr.ITE.scripts.templates import Templates


class BaseModule:
    def __init__(self, img_obj, image_name):
        self.bwimage = img_obj.get_bwimage()
        self.original_image = img_obj.get_original_image()
        self.microsoft_analysis = img_obj.get_microsoft_analysis()
        self.image_name = image_name

    def extract_info(self, template, bwimage, domain_flag, image_shape):
        height = bwimage.shape[0]
        width = bwimage.shape[1]
        CONTOUR, _ = cv2.findContours(bwimage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        wholeline_indices = linesObjectContours(CONTOUR, height, width)
        genimage = contourLinePlot(CONTOUR, height, width, wholeline_indices)
        scalev, scaleh = optimal_params(bwimage, task='table')
        self.mask, horizontal, vertical = extract_mask(bwimage, scalev=scalev,
                                                       scaleh=scaleh)

        cy, cx = np.where(np.bitwise_and(vertical, horizontal) == 255)
        intersection_coordinates = list(zip(list(cx), list(cy)))
        self.borderless_mask, \
        table_count_dict, \
        table_area_dict, \
        parent_area, areaThr, table_rel_centroid_dist_dict = self.remove_borders_if_present(self.mask)

        self.updated_table_count_dict, table_rel_centroid_dist_dict = self.check_if_table_in_table(
            table_count_dict,
            table_area_dict,
            parent_area,
            self.borderless_mask,
            areaThr,
            table_rel_centroid_dist_dict)
        self.table_cell_dict, \
        self.final_mapped_dict_table, \
        order = self.detect_cells_for_respective_tables(
            self.original_image, self.updated_table_count_dict,
            self.borderless_mask, scalev)
        self.final_mapped_dict_table = self.map_info_to_cells(
            self.microsoft_analysis,
            self.table_cell_dict, self.final_mapped_dict_table)
        paras, rel_para_area = self.detect_paragraphs(
            self.microsoft_analysis, self.table_cell_dict, order, parent_area)
        self.paras = self.final_json_para_corrections(paras)
        self.metadata = self.fetch_metadata(
            table_area_dict, table_count_dict, order, self.microsoft_analysis, rel_para_area, self.paras,
            table_rel_centroid_dist_dict, self.table_cell_dict)

        template_obj = Templates(template, {self.image_name: self.metadata})
        self.final_json = {
            'tables': self.final_mapped_dict_table,
            'paragraphs': self.paras,
            'table_coordinates': table_count_dict,
            'temp_number': template_obj.template_number,
            'domain_classification': domain_flag,
            'image_shape': image_shape}

        tables = self.final_mapped_dict_table
        #        print('TABLES : ' , tables)
        if max(self.mask.shape) <= 500:
            white_canvas = 0 * np.ones(self.mask.shape).astype(self.mask.dtype)
            self.mask2 = white_canvas.copy()
            return self.final_json, self.mask2 + genimage, self.metadata, template_obj.template

        elif (len(tables) > 0) and (sum([len(tables[table]) for table in tables]) > 0):

            clean_mask = extract_mask_clean(horizontal.copy()) + extract_mask_clean_vert(vertical.copy())
            table_mask = self.extract_tables_only_mask(table_count_dict, self.mask)
            self.mask = clean_mask + table_mask

        elif min(self.mask.shape) <= 500:
            self.mask, horizontal, vertical = extract_mask_horizontal(
                bwimage, scalev=scalev, scaleh=scaleh)
        else:
            self.mask = extract_mask_clean(horizontal.copy()) + extract_mask_clean_vert(vertical.copy())
        return self.final_json, self.mask + genimage, self.metadata, template_obj.template

    #        page metadata for paragraphs to be done here
    #        pdf's with large size not working

    def extract_tables_only_mask(self, table_count_dict, mask):

        black_page = 0 * np.ones(mask.shape).astype(mask.dtype)

        for table in table_count_dict:
            temp = table_count_dict[table]
            black_page[temp[1]:temp[3], temp[0]:temp[2]] = mask[temp[1]:temp[3], temp[0]:temp[2]]

        return black_page

    def remove_borders_if_present(self, mask):
        """
        some images may have borders which the program will consider as
        tables to remove such borders
        """
        # ONLY WHEN THE PAGE HAS BOARDERS WHICH ARE NOT ACTUALLY A TABLE
        weird = True
        offset = 0
        mask_original = mask.copy()
        while weird:
            parent_area = mask.shape[0] * mask.shape[1]
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            table_number = 0
            areaThr = 0.003 * parent_area  # threshold will be
            table_area_dict = {}  # Dictionary with the area of the table
            table_count_dict = {}  # Dictionary with table number and the
            #            bounding co-ordinates
            #            table_centroid_dict = {}
            table_rel_centroid_dist_dict = {}
            count = 0
            for cnt in contours:

                area = cv2.contourArea(cnt)  # Area of the contour

                peri = cv2.arcLength(cnt, True)  # Perimeter of the contour
                approx = cv2.approxPolyDP(
                    cnt, 0.02 * peri, True)  # EDGES (explained in the end)

                x, y, width, height = cv2.boundingRect(cnt)

                # CHECKING IF THE TABLE IS SINGLE CELLED!!!!

                #                cells, _ = cv2.findContours(
                #                    mask[y + 10:y + height - 10, x + 10:x + width - 10],
                #                    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                #
                #                cells_peri = [cv2.arcLength(cnt, True) for cnt in cells]
                #                cells_approxs_lens = [len(cv2.approxPolyDP(
                #                    cells[i], 0.02 * cells_peri[i], True))
                #                    for i in range(len(cells))]

                if (area > 0.8 * parent_area):  # BORDERS CONSIDERED AS TABLE

                    print('Border Detected, offseting mask')
                    mask = mask[y + 10:y + height - 10, x + 10:x + width - 10].copy()
                    offset += 10
                    break

                if (
                        area > areaThr) and (
                        len(approx) >= 4) and (
                        len(approx) <= 6) and (
                        (abs(
                            approx[1][0][0] -
                            approx[2][0][0]) < 20) or (
                                abs(
                                    approx[0][0][0] -
                                    approx[1][0][0]) < 20)) and (
                        min(
                            width,
                            height)) > 20:
                    table_count_dict[table_number + 1] = [x + offset,
                                                          y + offset, x + width - 1 + offset,
                                                          y + height - 1 + offset]
                    table_area_dict[table_number +
                                    1] = round((area / parent_area), 3)

                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    table_rel_centroid_dist_dict[table_number + 1] = round(
                        ((cx) ** 2 + (cy) ** 2) ** 0.5 / (mask.shape[0] + mask.shape[1]), 2)

                    # table_centroid_dict[table_number + 1] = [(cx, cy)]
                    table_number = table_number + 1
                    weird = False

                count += 1
            if count == len(contours): weird = False

        return mask_original, table_count_dict, table_area_dict, parent_area, areaThr, table_rel_centroid_dist_dict

    def check_if_table_in_table(
            self,
            table_count_dict,
            table_area_dict,
            parent_area,
            mask,
            areaThr,
            table_rel_centroid_dist_dict):
        #        table_centroid_dict = {}
        #        table_rel_centroid_dist_dict = {}
        inner_table_dict = {}
        for table_number in table_count_dict:

            if table_area_dict[table_number] > 0.5 * (parent_area):

                #             print('imgoing in')
                temp = table_count_dict[table_number]

                #             print(og_cor)

                # startY and endY coordinates, followed by the startX and endX
                outer_table_mask = mask[temp[1] +
                                        10:temp[3] - 10, temp[0] +
                                                         10:temp[2] - 10]

                contours_inner, _ = cv2.findContours(
                    outer_table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                inner_table_number = 0
                #             print(contours_inner)

                for cnt in contours_inner:
                    area = cv2.contourArea(cnt)
                    x, y, width, height = cv2.boundingRect(cnt)

                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                    if ((area > areaThr)
                            and (area < 0.8 * table_area_dict[table_number])
                            and (len(approx) == 4)
                            and ((abs(approx[1][0][0] -
                                      approx[2][0][0]) < 20)
                                 or (abs(approx[0][0][0] -
                                         approx[1][0][0]) < 20))
                            and (min(width, height) > 20)):
                        table_area_dict[int(
                            str(table_number) +
                            str(inner_table_number + 1))] = round(
                            (area / (outer_table_mask.shape[0] * outer_table_mask.shape[1])), 3)

                        M = cv2.moments(cnt)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        table_rel_centroid_dist_dict[int(str(table_number) + str(inner_table_number + 1))] = round(
                            ((cx) ** 2 + (cy) ** 2) ** 0.5 / (mask.shape[0] + mask.shape[1]), 2)

                        inner_table_dict[int(str(table_number) +
                                             str(inner_table_number +
                                                 1))] = [x +
                                                         temp[0] +
                                                         10, y +
                                                         temp[1] +
                                                         10, x +
                                                         width -
                                                         1 +
                                                         temp[0] +
                                                         10, y +
                                                         height -
                                                         1 +
                                                         temp[1] +
                                                         10]
                        inner_table_number = inner_table_number + 1

        if len(inner_table_dict) > 0:
            for inner_table in inner_table_dict:
                table_count_dict[inner_table] = inner_table_dict[inner_table]
        return table_count_dict, table_rel_centroid_dist_dict

    def detect_cells_for_respective_tables(self, img, table_count_dict, mask,
                                           scalev):
        order = {}
        table_cell_dict = {}
        # WHite PAGE with same size as the BW image
        white_page = 255 * np.ones(img.shape).astype(img.dtype)
        # NOW SAVING THE INDIVIDUAL TABLE IMAGES AND EXTRACTING CO-ORDINATES
        # FROM EACH TABLE
        for table_number in table_count_dict:

            temp = table_count_dict[table_number]

            order['t_' + str(table_number)] = temp[1]

            stencil = white_page.copy()
            stencil[temp[1]:temp[3], temp[0]:temp[2]] = img[temp[1]:temp[3],
                                                        temp[0]:temp[2]]
            # EXTRACTING ORIGINAL TABLE ON A WHITE PAGE

            stencil2 = white_page.copy()
            # TAKING THIS INSTEAD OF TAKING TABLE EXTRACTION
            mask_inverted = cv2.cvtColor(
                cv2.bitwise_not(mask),
                cv2.COLOR_GRAY2RGB)  # TO Extract Lines in BLACK

            stencil2[temp[1]:temp[3],
            temp[0]:temp[2]] = mask_inverted[temp[1]:temp[3],
                               temp[0]:temp[2]]
            # BLACK LINES ON WHITE PAGE

            # Check for inner tables and removing from the parent table

            pos_inner_tabs = set([int(str(table_number) + str(i))
                                  for i in range(1, 10)])
            # possible inner tabs
            # all the tables in the page
            keys_sets = set(table_count_dict.keys())

            inner_tabs = list(pos_inner_tabs.intersection(keys_sets))

            if inner_tabs:
                # REMOVING INNER TABLES TO AVOID REPETITION IN DATA EXTRACTION

                for inner_table in inner_tabs:
                    temp = table_count_dict[inner_table]
                    stencil2[temp[1]:temp[3], temp[0]:temp[2]
                    ] = white_page[temp[1]:temp[3], temp[0]:temp[2]]

            table_cell_dict[table_number] = self.get_cell_coordinates(
                stencil2, scalev_optimal=scalev)

        final_mapped_dict_table = {}
        tables = list(table_cell_dict.keys())
        for table in tables:
            final_mapped_dict_cell = {}
            if table_cell_dict[table]:
                for cell in table_cell_dict[table].keys():
                    p1 = table_cell_dict[table][cell][0][0]
                    p3 = table_cell_dict[table][cell][1][1]
                    final_mapped_dict_cell[cell] = {"boundingBox": {"p1": p1,
                                                                    "p3": p3},
                                                    "words": []}
                final_mapped_dict_table[table] = final_mapped_dict_cell
            else:
                del table_cell_dict[table]
                del self.updated_table_count_dict[table]

        return table_cell_dict, final_mapped_dict_table, order

    def get_cell_coordinates(self, img, scalev_optimal=40):

        try:
            img_copy = img.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            bw = cv2.adaptiveThreshold(
                ~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY, 15, -2)

            scalev, scaleh = optimal_params(
                bw, task='cells', scalev=scalev_optimal)

            mask, horizontal, vertical = extract_mask(
                bw, scalev=scalev, scaleh=scaleh)

            cy, cx = np.where(np.bitwise_and(vertical, horizontal) == 255)

            if len(cy):
                clustering = DBSCAN(
                    eps=10,
                    min_samples=2,
                    algorithm='ball_tree',
                    n_jobs=-
                    1).fit(
                    np.array(
                        list(
                            zip(
                                cy,
                                cx))))
                cluster_labels = clustering.labels_

                grouped = [[y[0:2] for y in zip(
                    cy, cx, cluster_labels) if y[2] == cluster_label]
                           for cluster_label in set(cluster_labels)]

                # Grouped has all the pixel coordinates of the intersection of
                # horizonta and vertical lines

                grouped_centroids = [(int(sum([i[0] for i in grouped[j]]) /
                                          len(grouped[j])),
                                      int(sum([i[1] for i in grouped[j]]) /
                                          len(grouped[j])))
                                     for j in range(len(grouped))]

                # Assuming height/width of a table > threshold.
                def cluster_1D(values, threshold=5):

                    values = sorted(values)  # ;    print(values)
                    _ = map(
                        list, np.split(
                            values, np.where(
                                np.diff(values) > threshold)[0] + 1))
                    return ([int(ceil(np.average(i))) for i in list(_)
                             if len(i) > 1])

                    # CHANGE MADE HERE TO CORRECT THE CELL NAMING

                cy_list, \
                cx_list = cluster_1D([i[0] for i in grouped_centroids]), \
                          cluster_1D([i[1] for i in grouped_centroids])

                edge_present = dict()
                for ix in range(len(cx_list) - 1):
                    for iy in range(len(cy_list) - 1):
                        if ix != 0:
                            cx = cx_list[ix]
                            count = np.count_nonzero(
                                mask[cy_list[iy]:cy_list[iy + 1] + 1,
                                cx - 3:cx + 4])
                            _ = round(
                                float(count) / float(cy_list[iy + 1] -
                                                     cy_list[iy] + 1), 2)
                            edge_present[str(ix) + '_' +
                                         str(iy) + 'v'] = _ > 2.67

                        if iy != 0:
                            cy = cy_list[iy]
                            count = np.count_nonzero(
                                mask[cy - 3:cy + 4, cx_list[ix]:cx_list[ix + 1]
                                                                + 1])
                            _ = round(
                                float(count) / float(cx_list[ix + 1] -
                                                     cx_list[ix] + 1), 2)
                            edge_present[str(ix) + '_' +
                                         str(iy) + 'h'] = _ > 2.67

                cell_coordinates = dict()
                # initialization for all unit cells. DETECTING CELLS NAMES
                for j in range(len(cx_list) - 1):
                    for i in range(len(cy_list) - 1):
                        cell_coordinates['r' + str(i) + 'c' + str(j)] = (
                            cx_list[j], cy_list[i], cx_list[j + 1],
                            cy_list[i + 1])

                temp_dict = {i: [i] for i in cell_coordinates}
                temp = []
                for edge in edge_present:
                    if not edge_present[edge]:
                        i, j = map(int, edge[:-1].split('_'))

                        if edge.endswith('h'):
                            val = temp_dict['r'
                                            + str(j - 1) + 'c' + str(i)] + \
                                  temp_dict['r' + str(j) + 'c' + str(i)]

                            for k in temp_dict['r' + str(j - 1) + 'c' + str(
                                    i)] + temp_dict['r' + str(j) + 'c' +
                                                    str(i)]:
                                temp_dict[k] = val
                        else:
                            val = temp_dict['r'
                                            + str(j) + 'c' + str(i - 1)] + \
                                  temp_dict['r' + str(j) + 'c' + str(i)]

                            for k in temp_dict['r' + str(j) + 'c' + str(
                                    i - 1)] + temp_dict['r' + str(j) + 'c'
                                                        + str(i)]:
                                temp_dict[k] = val

                        temp.append('r' + str(j) + 'c' + str(i))

                for i in set(temp):
                    del temp_dict[i]

                temp_dict2 = OrderedDict()
                for merged_cell in temp_dict:
                    # MERGING CELLS WHERE EDGE IS NOT PRESENT
                    x1, y1, x2, y2 = \
                        (min([cell_coordinates[i][0]
                              for i in temp_dict[merged_cell]]),
                         min([cell_coordinates[i][1]
                              for i in temp_dict[merged_cell]]), max(
                            [cell_coordinates[i][2]
                             for i in temp_dict[merged_cell]]),
                         max([cell_coordinates[i][3]
                              for i in temp_dict[merged_cell]]))

                    temp123 = merged_cell[1:].split('c')
                    key = 'c' + temp123[1] + 'r' + temp123[0]
                    temp_dict2[key] = [
                        [[x1, y1], [x2, y1]], [[x1, y2], [x2, y2]]]
                    cv2.putText(img_copy,
                                merged_cell,
                                (int((x1 + x2) / 2) - 10,
                                 int((y1 + y2) / 2) + 2),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0,
                                 0,
                                 255))
                    cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 1)

                return temp_dict2

            else:
                print('0 cell detected.')

        except Exception as e:
            print(e)

    def map_info_to_cells(self, analysis,
                          table_cell_dict, final_mapped_dict_table):
        len_check = 0
        for i in range(len(analysis['lines'])):
            # print(analysis['recognitionResults'][0]['lines'][i])
            for h in range(len(analysis['lines'][i]['words'])):
                da_c_main = analysis['lines'][i]['words'][h]['boundingBox']
                x = (da_c_main[0] + da_c_main[2] +
                     da_c_main[4] + da_c_main[6]) / 4
                y = (da_c_main[3] + da_c_main[5] +
                     da_c_main[1] + da_c_main[7]) / 4

                for j in table_cell_dict:
                    tab_cell = list(table_cell_dict[j].keys())
                    for l in tab_cell:
                        x1 = table_cell_dict[j][l][0][0][0]
                        x2 = table_cell_dict[j][l][0][1][0]
                        y2 = table_cell_dict[j][l][0][1][1]
                        y3 = table_cell_dict[j][l][1][0][1]

                        if round(x) in range(
                                x1,
                                x2) and round(y) in range(
                            y2,
                            y3):
                            len_check += 1
                            # print(word_cord['recognitionResults'][0]['lines'][i]['words'][h]['text'],j,l)
                            info = analysis['lines'][i]['words'][h]
                            final_mapped_dict_table[j][l]["words"].append(
                                {"text": info['text'],
                                 "boundingBox": {
                                     "p1": info['boundingBox'][0:2],
                                     "p3": info['boundingBox'][4:6]}})
        return final_mapped_dict_table

    # GET ALL THE POLYGONS WHICH HAVE SAME START OR STOP PLACES
    """def get_similar(self, line_number, p1_p3, lines, dst,
                    parent_area):  ## GET ALL THE POLYGONS WHICH HAVE SAME START OR STOP PLACES

        x1, x3 = p1_p3[line_number][0][0], p1_p3[line_number][1][0]
        y1, y3 = p1_p3[line_number][0][1], p1_p3[line_number][1][1]

        thrx = round(((x3 - x1) / len(lines[line_number])) * 6)  ## USUAL INTEND IS 5 SPACES

        #     net1,net2  = range(x1-10,x1+10),range(x3-10,x3+10)    ## net for X's
        #     net3,net4 = range(y1-100,y1+100),range(y3-100,y3+100) ## net for Y's

        similar = []

        thr_centroid = (
                    y3 - y1)  # + (y3-y1)*1.45   ##For most text, the optimal line spacing is between 120% and 145% of the point size
        similar = [y for (x, y) in dst.keys() if (x == line_number) and (dst[(x, y)] < thr_centroid)]
        similar = similar + [x for (x, y) in dst.keys() if (y == line_number) and (dst[(x, y)] < thr_centroid)]

        # if len(similar): thry = round(((y3-y1) + (y3-y1))*0.5 *1.25) * 2
        for i, key in enumerate(p1_p3):  ## Key here is line number!!!!

            p1, p3 = p1_p3[key]

            if (key not in similar) and (key != line_number):

                if i == 0 and len(similar) > 0:
                    x1, x3 = p1_p3[similar[0]][0][0], p1_p3[similar[0]][1][0]
                    y1, y3 = p1_p3[similar[0]][0][1], p1_p3[similar[0]][1][1]

                thry = round(((y3 - y1) + (y3 - y1)) * 0.5 * 1.25)

                netx1, netx3 = range(x1 - thrx, x1 + thrx), range(x3 - thrx, x3 + thrx)  ## net for X's
                nety1, nety3 = range(y1 + 1, y1 + thry), range(y3 + 1, y3 + thry)
                text_size_diff = abs((p3[1] - p1[1]) - (y3 - y1))

                if ((p1[0] in netx1) or (p3[0] in netx3)) and (
                        (p1[1] in nety1) or (p3[1] in nety3)):  # or (p3[1] in net2)):

                    similar.append(key)
                    #                 thrx = thrx
                    x1, x3 = p1[0], p3[0]
                    y1, y3 = p1[1], p3[1]
        #     similar_lines = [lines[i] for i in similar]
        # if para_cord == True:
        #     p1 = [p1_p3[line_number][0][0],p1_p3[line_number][0][1]]
        #     p3 = [x3,y3]
        #     p2 = [p1[1],p3[0]]
        #     p4 = [p1[0],p3[1]]
        #
        #     return [p1,p2,p3,p4]

        width = abs(p1_p3[line_number][0][0] - p1_p3[line_number][1][0])
        height = abs(p1_p3[line_number][0][1] - y3)
        para_area = width * height
        rel_area = round((para_area / parent_area), 4) * 100

        return similar, p1_p3[line_number][0][1], rel_area  ## ALL THE LINE NUMBERS AND Y1 AND RELATIVE AREA OF PARA

    def detect_paragraphs(self, analysis, table_cell_dict, order, parent_area):
        polygons = []
        polygons = analysis["lines"]

        table_coordinates = {}
        for table in table_cell_dict:
            i = sum([sum(sum(table_cell_dict[table][i], []), [])
                     for i in table_cell_dict[table]], [])
            #     print(i)
            try:
                table_coordinates[table] = [
                    (min(i[::2]), min(i[1::2])), (max(i[::2]), max(i[1::2]))]
            except BaseException:
                pass
        polygons_ = []
        for i in polygons:  # Filtering all the polygons that are inside tables
            x_min, y_min, x_max, y_max = min(i['boundingBox'][::2]), \
                                         min(i['boundingBox'][1::2]), max(i['boundingBox'][::2]), \
                                         max(i['boundingBox'][1::2])
            flag = True
            for v in table_coordinates.values():
                if ((v[0][0] <= x_min <= v[1][0]) or
                    (v[0][0] <= x_max <= v[1][0])) and (
                        (v[0][1] <= y_min <= v[1][1])
                        or (v[0][1] <= y_max <= v[1][1])):
                    flag = False
                    break
            if flag:
                polygons_.append(i)

        polygons = polygons_

        # {line_number: Content of that line}
        lines = {i: polygons[i - 1] for i in range(1, len(polygons) + 1)}

        # Point 1 Point 3 DICTIONARY FOR ALL THE POLYGONS {line_number:
        # [point1,point3]}
        p1_p3 = {}
        centroids = {}

        for line_number, line in enumerate(polygons):
            line_number = line_number + 1
            p1_p3[line_number] = line["boundingBox"][: 2], \
                                 line["boundingBox"][4:6]
            #     print(p1_p3[line_number][1][0])
            centroids[line_number] = (p1_p3[line_number][0][0] +
                                      p1_p3[line_number][1][0]) * 0.5, \
                                     (p1_p3[line_number][0][1] +
                                      p1_p3[line_number][1][1]) * 0.5
        line_numbers = p1_p3.keys()

        combinations = [(x, y) for x in line_numbers
                        for y in line_numbers if x != y and y > x]
        dst = {combination: distance.euclidean(centroids[combination[0]],
                                               centroids[combination[1]])
               for combination in combinations}
        rel_para_area = {}
        paras = {}  # PARAGRAPHS  { para_1 : [line1,line2]}
        para = 1
        i = 1
        clubbed_lines = []
        for line_number in p1_p3:
            # if (len(lines[line_number])<6) or(' ' not in lines[line_number]):
            # ALL THE SMALL WORDS WHICH WILL BE EXTRACTED SEPERATELY LATER
            #     pass
            if (line_number not in clubbed_lines):
                clubbed_lines.append(line_number)
                clubbed_lines_, depth, relative_para_area = self.get_similar(line_number, p1_p3,
                                                                             lines, dst, parent_area)
                # print(clubbed_lines_)
                clubbed_lines = clubbed_lines + clubbed_lines_
                rel_para_area['p_' + str(para)] = relative_para_area
                paras['p_' + str(para)] = \
                    [lines[line_number]] + [lines[line_number]
                                            for line_number in clubbed_lines_]
                order['p_' + str(para)] = depth
                para = para + 1

        return paras, rel_para_area"""

    def get_similar(self, line_number, p1_p3, lines, dst, parent_area,
                    cl=[]):  ## GET ALL THE POLYGONS WHICH HAVE SAME START OR STOP PLACES

        x1, x3 = p1_p3[line_number][0][0], p1_p3[line_number][1][0]
        y1, y3 = p1_p3[line_number][0][1], p1_p3[line_number][1][1]

        thrx = round(((x3 - x1) / len(lines[line_number]['text'])) * 6)  ## USUAL INTEND IS 5 SPACES

        #     net1,net2  = range(x1-10,x1+10),range(x3-10,x3+10)    ## net for X's
        #     net3,net4 = range(y1-100,y1+100),range(y3-100,y3+100) ## net for Y's

        similar = []

        thr_centroid = int(1.2 * abs(
            y3 - y1))  # + (y3-y1)*1.45   ##For most text, the optimal line spacing is between 120% and 145% of the point size
        similar = [y for (x, y) in dst.keys() if
                   (x == line_number) and (dst[(x, y)] < thr_centroid) and (y not in cl)]
        similar = similar + [x for (x, y) in dst.keys() if
                             (y == line_number) and (dst[(x, y)] < thr_centroid) and (x not in cl)]

        #        print('SIMILAR FOR : ', lines[line_number]['text'])
        #        r = [lines[ln]['text']  for ln in similar]
        #        print(r,'\n')
        # if len(similar): thry = round(((y3-y1) + (y3-y1))*0.5 *1.25) * 2
        #        current_line = ''
        for i, key in enumerate(p1_p3):  ## Key here is line number!!!!

            p1, p3 = p1_p3[key]

            if (key not in similar) and (key != line_number) and (key not in cl):

                if i == 0 and len(similar) > 0:  ## PRESENT LINE IS NOT INITAL LINE
                    x1, x3 = p1_p3[similar[0]][0][0], p1_p3[similar[0]][1][0]
                    y1, y3 = p1_p3[similar[0]][0][1], p1_p3[similar[0]][1][1]

                thrx = round(((x3 - x1) / len(lines[line_number]['text'])) * 6)
                #                thry = round(((y3-y1) + (y3-y1))*0.5 *1.25)
                thry = round((y3 - y1) * 1.25)

                netx1, netx3 = range(x1 - thrx, x1 + thrx), range(x3 - thrx, x3 + thrx)  ## net for X's
                nety1, nety3 = range(y1 + 1, y1 + thry), range(y3 + 1, y3 + thry)
                #                text_size_diff = abs((p3[1]-p1[1]) - (y3-y1))

                if ((p1[0] in netx1) or (p3[0] in netx3)) and (
                        (p1[1] in nety1) or (p3[1] in nety3)):  # or (p3[1] in net2)):

                    similar.append(key)
                    #                 thrx = thrx

                    #
                    #                    if lines[key]['text'] in ['U.S.A.','U.S.A'] :
                    #
                    #                        print('\n CAUGHT', lines[key]['text'] ,' WITH :' , current_line)
                    #                        print('ref coord :', )

                    #                    current_line = lines[key]['text']
                    x1, x3 = p1[0], p3[0]
                    y1, y3 = p1[1], p3[1]
        #     similar_lines = [lines[i] for i in similar]
        # if para_cord == True:
        #     p1 = [p1_p3[line_number][0][0],p1_p3[line_number][0][1]]
        #     p3 = [x3,y3]
        #     p2 = [p1[1],p3[0]]
        #     p4 = [p1[0],p3[1]]
        #
        #     return [p1,p2,p3,p4]

        width = abs(p1_p3[line_number][0][0] - p1_p3[line_number][1][0])
        height = abs(p1_p3[line_number][0][1] - y3)
        para_area = width * height
        rel_area = round((para_area / parent_area), 4) * 100

        return similar, p1_p3[line_number][0][1], rel_area  ## ALL THE LINE NUMBERS AND Y1 AND RELATIVE AREA OF PARA

    def detect_paragraphs(self, analysis, table_cell_dict, order, parent_area):
        polygons = []
        polygons = analysis["lines"]
        #        polygons = [(line["boundingBox"], line["text"]) for line in analysis["lines"]]

        #        print('polygons!!!!!!!!!!!!!!!!!!!! \n\n', polygons,'\n\n')
        table_coordinates = {}
        for table in table_cell_dict:
            i = sum([sum(sum(table_cell_dict[table][i], []), [])
                     for i in table_cell_dict[table]], [])
            #     print(i)
            try:
                table_coordinates[table] = [
                    (min(i[::2]), min(i[1::2])), (max(i[::2]), max(i[1::2]))]
            except BaseException:
                pass
        polygons_ = []
        for i in polygons:  # Filtering all the polygons that are inside tables
            x_min, y_min, x_max, y_max = min(i['boundingBox'][::2]), \
                                         min(i['boundingBox'][1::2]), max(i['boundingBox'][::2]), \
                                         max(i['boundingBox'][1::2])
            flag = True
            for v in table_coordinates.values():
                if ((v[0][0] <= x_min <= v[1][0]) or
                    (v[0][0] <= x_max <= v[1][0])) and (
                        (v[0][1] <= y_min <= v[1][1])
                        or (v[0][1] <= y_max <= v[1][1])):
                    flag = False
                    break
            if flag:
                polygons_.append(i)

        polygons = polygons_

        # {line_number: Content of that line}
        lines = {i: polygons[i - 1] for i in range(1, len(polygons) + 1)}
        #        print('LINES :' ,lines)
        # Point 1 Point 3 DICTIONARY FOR ALL THE POLYGONS {line_number:
        # [point1,point3]}
        p1_p3 = {}
        centroids = {}

        for line_number, line in enumerate(polygons):
            line_number = line_number + 1
            p1_p3[line_number] = line["boundingBox"][: 2], \
                                 line["boundingBox"][4:6]
            #     print(p1_p3[line_number][1][0])
            centroids[line_number] = (p1_p3[line_number][0][0] +
                                      p1_p3[line_number][1][0]) * 0.5, \
                                     (p1_p3[line_number][0][1] +
                                      p1_p3[line_number][1][1]) * 0.5
        line_numbers = p1_p3.keys()

        combinations = [(x, y) for x in line_numbers
                        for y in line_numbers if x != y and y > x]
        dst = {combination: distance.euclidean(centroids[combination[0]],
                                               centroids[combination[1]])
               for combination in combinations}
        rel_para_area = {}
        paras = {}  # PARAGRAPHS  { para_1 : [line1,line2]}
        para = 1
        i = 1
        clubbed_lines = []
        for line_number in p1_p3:
            # if (len(lines[line_number])<6) or(' ' not in lines[line_number]):
            # ALL THE SMALL WORDS WHICH WILL BE EXTRACTED SEPERATELY LATER
            #     pass
            if (line_number not in clubbed_lines):
                clubbed_lines.append(line_number)
                clubbed_lines_, depth, relative_para_area = self.get_similar(line_number, p1_p3,
                                                                             lines, dst, parent_area,
                                                                             cl=clubbed_lines)
                # print(clubbed_lines_)
                clubbed_lines = clubbed_lines + clubbed_lines_
                rel_para_area['p_' + str(para)] = relative_para_area
                paras['p_' + str(para)] = \
                    [lines[line_number]] + [lines[line_number]
                                            for line_number in clubbed_lines_]
                order['p_' + str(para)] = depth
                para = para + 1

        return paras, rel_para_area

    """def fetch_metadata(self, table_area_dict, table_count_dict, order, analysis, rel_para_area, paras,
                       table_rel_centroid_dist_dict):
        page_metadata = {}
        page_metadata = {"order": [], "table": {}, "para_rel_area": {}}
        for table_number in table_count_dict:
            # page_metadata[page_name]["table"][table_number] = table_centroid_dict[table_number]
            page_metadata["table"][table_number] = [table_rel_centroid_dist_dict[table_number]]
            page_metadata["table"][table_number].append(table_area_dict[table_number])

        if len(table_count_dict) == 0:
            # page_metadata["words"] = extract_words(analysis)
            pass
        else:
            page_metadata["words"] = []
        page_metadata["no_of_tables"] = len(page_metadata["table"])
        page_metadata["total_relative_table_area"] = sum(table_area_dict.values())

        page_metadata['para_rel_area'] = rel_para_area
        page_metadata['no_of_paras'] = len(paras)
        page_metadata['order'] = sorted(order, key=order.get)
        return page_metadata"""

    def extract_words(self, analysis):

        words = [bb['text'] for line in analysis["lines"] for bb in line['words']]
        return words

    """def extract_struct_details(self, table_cell_dict):
        table_struc_stats = {}
        for table in table_cell_dict:
            table_struc_stats[table] = {}

            cells_dict = dict(table_cell_dict[table])
            cells = list(cells_dict.keys())

            ncols = max([int(cell.split('r')[0].split('c')[1]) for cell in cells])
            nrows = max([int(cell.split('r')[1]) for cell in cells])
            #        print('ncols:',ncols , '*'*20)
            #        print('nrows:',nrows , '*'*20)

            table_struc_stats[table]['ncols'] = ncols
            table_struc_stats[table]['nrows'] = nrows

        return table_struc_stats"""

    def extract_struct_details(self, table_cell_dict):
        table_struc_stats = {}
        for table in table_cell_dict:

            table_struc_stats[table] = {}

            if len(table_cell_dict[table]) > 0:
                cells_dict = dict(table_cell_dict[table])
                cells = list(cells_dict.keys())

                ncols = max([int(cell.split('r')[0].split('c')[1]) for cell in cells])
                nrows = max([int(cell.split('r')[1]) for cell in cells])
                #        print('ncols:',ncols , '*'*20)
                #        print('nrows:',nrows , '*'*20)

                table_struc_stats[table]['ncols'] = ncols
                table_struc_stats[table]['nrows'] = nrows
            else:
                table_struc_stats[table]['ncols'] = 0
                table_struc_stats[table]['nrows'] = 0

        return table_struc_stats

    def check_if_centroid_inbetween_p1_p3(self, centroid, p1, p3):
        if p1[0] <= centroid[0] <= p3[0] and p1[1] <= centroid[1] <= p3[1]:
            return True
        else:
            return False

    def calculate_centroid(self, p1, p3):
        x_centroid = int((p1[0] + p3[0]) * 0.5)
        y_centroid = int((p1[1] + p3[1]) * 0.5)
        return x_centroid, y_centroid

    def extract_spread(self):

        h, w = self.original_image.shape[:2]
        q1 = {'p1': [0, 0], 'p3': [int(w * 0.5), int(h * 0.5)]}
        q2 = {'p1': [int(w * 0.5), 0], 'p3': [w, int(h * 0.5)]}
        q3 = {'p1': [0, int(h * 0.5)], 'p3': [int(w * 0.5), h]}
        #        q4 = {'p1':[int(w*0.5),int(h*0.5)] ,'p3' : [w, h]}

        paras = self.paras
        spread = {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0}
        for para in paras:
            for line in paras[para]:
                for word in line:
                    bb = word["boundingBox"]
                    p_centroid = self.calculate_centroid(bb['p1'], bb['p3'])
                    if self.check_if_centroid_inbetween_p1_p3(p_centroid, q1['p1'], q1['p3']):
                        spread['q1'] += 1
                    elif self.check_if_centroid_inbetween_p1_p3(p_centroid, q2['p1'], q2['p3']):
                        spread['q2'] += 1
                    elif self.check_if_centroid_inbetween_p1_p3(p_centroid, q3['p1'], q3['p3']):
                        spread['q3'] += 1
                    else:
                        spread['q4'] += 1
        return spread

    def fetch_metadata(self, table_area_dict, table_count_dict, order, analysis, rel_para_area, paras,
                       table_rel_centroid_dist_dict, table_cell_dict):
        page_metadata = {}
        page_metadata = {"order": [], "table": {}, "para_rel_area": {}}

        table_structure_details = self.extract_struct_details(table_cell_dict)
        for table_number in table_count_dict:
            page_metadata["table"][table_number] = {}
            # page_metadata[page_name]["table"][table_number] = table_centroid_dict[table_number]

            stats = [table_rel_centroid_dist_dict[table_number], table_area_dict[table_number]]
            page_metadata["table"][table_number]['Stats'] = stats

            page_metadata["table"][table_number]['ncols'] = table_structure_details[table_number]['ncols']
            page_metadata["table"][table_number]['nrows'] = table_structure_details[table_number]['nrows']
        #            stats = page_metadata["table"][table_number]['Stats']
        #            page_metadata["table"][table_number].append(table_area_dict[table_number])

        if len(table_count_dict) == 0:
            page_metadata["words"] = self.extract_words(analysis)
            page_metadata["spread"] = self.extract_spread()
        else:
            page_metadata["words"] = []
            page_metadata["spread"] = {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0}
        page_metadata["no_of_tables"] = len(page_metadata["table"])
        page_metadata["total_relative_table_area"] = sum(table_area_dict.values())

        page_metadata['para_rel_area'] = rel_para_area
        page_metadata['no_of_paras'] = len(paras)
        page_metadata['order'] = sorted(order, key=order.get)
        return page_metadata

    def final_json_para_corrections(self, temp):
        paragraphs = {}
        for para in temp:
            lines_all = []
            for lines in temp[para]:
                all_words = []
                for word in lines["words"]:
                    all_words.append({"text": word["text"], "boundingBox": {"p1": word["boundingBox"][0:2],
                                                                            "p3": word["boundingBox"][4:6]}})
                #                    print(para,word["text"],word["boundingBox"])
                lines_all.append(all_words)
            paragraphs.update({para: lines_all})
        return paragraphs
