# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import numpy as np
import re
import pandas as pd

from ocr.ITE.scripts.domain_classification import Domain


class Transcript:

    def __init__(self):
        pass

    def extract_metadata_transcript(self, analysis, image_name):

        polygons = []
        polygons = [(line["boundingBox"], line["text"]) for line in analysis["lines"]]
        print(image_name)

        image = cv2.imread(image_name)

        h, w, z = image.shape
        result = self.check_template(polygons, w)
        if result:

            typ = '2 SIDED'
            pages = result

            cut = int(w / 2)
            arl1 = [bb for bb in analysis['lines'] if bb['boundingBox'][4] < int(cut)]
            arl2 = [bb for bb in analysis['lines'] if bb['boundingBox'][4] > int(cut)]

            wc_1, wc_2 = {}, {}
            for i, line in enumerate(arl1):
                wc_1[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

            for i, line in enumerate(arl2):
                wc_2[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]
            wc = [wc_1, wc_2]

            sem_info_list, p1_p3_list = self.extract_data(pages, type=2, wor_cor=wc, shape=image.shape, metadata=True)

            semesters = []
            header_cords = []
            headers_lines = []
            for i, page in enumerate(sem_info_list):
                page_sems = list(sem_info_list[i].keys())
                semesters = semesters + page_sems
                # print('sem_info[page]')
                # print(sem_info[page])
                # print('*'*50)
                # print('[list(sem_info[page].keys())')
                # print([list(sem_info[page].keys())])
                headers_lines.append(sem_info_list[i][page_sems[0]]['sem_header_1'][1])
                header_cords.append(
                    [p1_p3_list[i][line][0] if line == headers_lines[i][0] else p1_p3_list[i][line][1] for line in
                     headers_lines[i] if line in [headers_lines[i][0], headers_lines[i][-1]]])

            d = {}
            d['TYPE'] = typ
            d['No of Semesters:'] = len(semesters)
            d['Header Co-Ordinates'] = header_cords
            d['Header Centroids'] = [(np.array(header_cord[0]) + np.array(header_cord[1])) * 0.5 for header_cord in
                                     header_cords]


        else:

            typ = 'SINGLE SIDED'

            wc = {}

            for i, line in enumerate(analysis["lines"]):
                wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

            sem_info, p1_p3 = self.extract_data(polygons, type=1, wor_cor=None, shape=image.shape, metadata=True)
            #         print(typ,'\n',sem_info)
            #         return sem_info
            # print('*'*50,p1_p3,'*'*50)
            ## METADATA

            semesters = list(sem_info.keys())
            header_lines = sem_info[semesters[0]]['sem_header_1'][1]  ## FIRST SEMESTER FROM PAGE
            header_cord = [p1_p3[line][0] if line == header_lines[0] else p1_p3[line][1] for line in header_lines if
                           line in [header_lines[0], header_lines[-1]]]
            print('*' * 50)
            print('header_cord')
            print(header_cord)
            print('*' * 50)

            d = {}
            d['TYPE'] = typ
            d['No of Semesters:'] = len(semesters)
            d['Header Co-Ordinates'] = header_cord
            d['Header Centroid'] = (np.array(header_cord[0]) + np.array(header_cord[1])) * 0.5

        return d

    def check_template(self, polygons, w):

        cut = int(w / 2)
        pages = {1: {}, 2: {}}

        pages[1]['polygons'] = [polygon for polygon in polygons if polygon[0][2] < cut]  ## LEFT HALF OF THE PAGE
        pages[2]['polygons'] = [polygon for polygon in polygons if polygon[0][0] > cut]  ## RIGHT HALF OF THE PAGE

        ke_1_p = [pages[1]["polygons"][i][1] for i in range(len(pages[1]["polygons"]))]
        ke_2_p = [pages[2]["polygons"][i][1] for i in range(len(pages[2]["polygons"]))]

        wo = [words for words in list(set(ke_1_p) & set(ke_2_p)) if not re.findall(r"\d+\ *\.\ *\d+", words)]

        if len(wo) > 5:
            return pages
        else:
            return False

    def intermediate_1(self, analysis, image_name, return_sem_info=False):

        polygons = []
        polygons = [(line["boundingBox"], line["text"]) for line in analysis["lines"]]

        image = cv2.imread(image_name)
        image_name_only = image_name.split('/')[-1].split('.')[0]
        h, w, z = image.shape
        result = self.check_template(polygons, w)
        if result:
            pages = result

            cut = int(w / 2)
            arl1 = [bb for bb in analysis['lines'] if bb['boundingBox'][4] < int(cut)]
            arl2 = [bb for bb in analysis['lines'] if bb['boundingBox'][4] > int(cut)]

            wc_1, wc_2 = {}, {}
            for i, line in enumerate(arl1):
                wc_1[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

            for i, line in enumerate(arl2):
                wc_2[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

            full_info, transcript_info = self.extract_data(pages, wor_cor=[wc_1, wc_2], shape=image.shape)
            # print(full_info,transcript_info)
            # f = open('./database/' + image_name_only + '_transcript_data.txt', 'w+')
            # for l in full_info:
            #     f.writelines(str(l))
            # f.close()
            return full_info, transcript_info
        else:
            pages = {}
            pages[1] = polygons
            wc = {}
            for i, line in enumerate(analysis["lines"]):
                wc[i + 1] = [(word['boundingBox'], word['text']) for word in line['words']]

            full_info, transcript_info = self.extract_data(pages, wor_cor=[wc], shape=image.shape)
            # f = open('./database/' + image_name_only + '_transcript_data.txt', 'w+')
            # for l in full_info:
            #     f.writelines(str(l))
            # f.close()
            return full_info, transcript_info

    #############################################################################################################

    def extract_data(self, pages_or_polygons, wor_cor=None, shape=0, metadata=False):

        if len(wor_cor) > 1:
            full_info = []
            sem_info_list = []
            p1_p3_list = []
            transcript_info = {}

        for i, wc in enumerate(wor_cor):  ### PAGE WISE SEM_INFO

            sem_info = {}
            lines_api = {}
            cp_transcript_info = {}

            if len(wor_cor) > 1:
                current_page = pages_or_polygons[i + 1]['polygons'].copy()  ## i + 1 will be page number

            else:
                current_page = pages_or_polygons[i + 1]

            lines_api = {i: current_page[i - 1][1] for i in
                         range(1, len(current_page) + 1)}  # {line_number: Content of that line}
            starting_point = {line_number: current_page[line_number - 1][0][0] for line_number in
                              range(1, len(current_page) + 1)}

            p1_p3 = {}
            width_poly = {}
            for line_number, line in enumerate(current_page):
                line_number = line_number + 1
                p1_p3[line_number] = line[0][:2], line[0][4:6]
                width_poly[line_number] = line[0][2] - line[0][0]

            clubbed_lines = []
            current_depth = 0

            same_line = {}  ## ADDED NEW
            header = set(['Attempted', 'Scored', 'Points', 'Earned'])

            for line_number in p1_p3:

                if (line_number not in clubbed_lines):

                    current_depth = int((p1_p3[line_number][1][1] + p1_p3[line_number][0][1])*0.5)
                    cl = Domain().get_same_line_words_hori(p1_p3, line_number, current_depth, shape[0])
                    clubbed_lines = [line_number] + cl + clubbed_lines

                    sl = [line_number] + cl
                    d = {k: starting_point[k] for k in sl}
                    sl = sorted(d, key=d.get)  ## LINE NUMBERS
                    x = [lines_api[line_number] for line_number in sl]  ### LINE

                    if ([re.match(r'.*([2][0][0-9]{2})', line) for line in x] + [re.match(r'.*([1][9][0-9]{2})', line)
                                                                                 for line in x] != [None] * 2 * len(
                            x)) and ([re.match(r'.*(Fall|Spring|Summer|Term)', word) for word in x] != [None] * len(x)) \
                            and ([re.match(r'.*(/)', word) for word in x] == [None] * len(x)):
                        sem_info[' '.join(x)] = {}
                        i1, i2, i3 = 1, 1, 1


                    elif (len(x) == 1) and (':' in list(x[0])) and (len(sem_info.keys()) == 0):

                        info = x[0].split(':')
                        cp_transcript_info[info[0]] = info[1]

                    else:

                        try:
                            key = list(sem_info.keys())[-1]
                            joined = ' '.join(x)

                            if ([':' in list(word) for word in x] != [False] * len(x)) and (len(x) == 2):

                                k, v = joined.split(':')[0], joined.split(':')[1]
                                sem_info[key][k] = v

                            elif len(x) == 2:
                                sem_info[key][x[0]] = x[1]


                            elif re.findall(r'Total', joined) and ([w[0].isdigit() for w in x] != [False] * len(x)):
                                sem_info[key]['final_' + str(i1)] = [x, sl]
                                i1 = i1 + 1

                            elif len(header.intersection(set(joined.split()))) >= 2:
                                sem_info[key]['sem_header_' + str(i2)] = [x, sl]
                                i2 = i2 + 1

                            elif ([':' in list(word) for word in x] != [False] * len(x)):
                                k, v = joined.split(':')[0], joined.split(':')[1]
                                sem_info[key][k] = v

                            elif len(x) > 2 and ('Course Attributes' not in x):
                                sem_info[key]['data_' + str(i3)] = [x, sl]
                                i3 = i3 + 1
                            else:
                                pass

                        except:
                            joined = ' '.join(x)

                            if ([':' in list(word) for word in x] != [False] * len(x)) and (len(x) == 2):
                                cp_transcript_info[x[0][:-1]] = x[1]

                            elif (len(x) == 2):
                                cp_transcript_info[x[0]] = x[1]

                            elif len(x) > 3 and len(header.intersection(set(joined.split()))) >= 2:
                                cp_transcript_info['Global_header'] = x

            if metadata == True:
                sem_info_list.append(sem_info)
                p1_p3_list.append(p1_p3)

            if len(wor_cor) > 1:

                full_info.append(self.clean_info(sem_info, cp_transcript_info, lines_api, wc, p1_p3))
                # clean_info(self,sem_info,transcript_info,lines_api,wc,p1_p3):
                # full_info.append(sem_info)
                transcript_info.update(cp_transcript_info)
            else:
                return [self.clean_info(sem_info, cp_transcript_info, lines_api, wc,
                                        p1_p3)], cp_transcript_info  ## RESULTS FOR SINGLE SIDED
                # return sem_info,cp_transcript_info

        if metadata == True: return sem_info_list, p1_p3_list

        return full_info, transcript_info  ## RESULTS FOR 2 SIDED

    ##############################################################################
    def clean_info(self, sem_info, transcript_info, lines_api, wc, p1_p3):

        df_sem_list = []
        df_final_list = []
        final_scores = {}
        locations = {}  ## ADDED NEW

        for sem in sem_info:  ## SEMESTER WISE

            s = sem_info[sem].copy()  ## CURRENT SEMESTER

            data_rows = list(filter(lambda x: x[0:4] == 'data', list(s.keys())))
            final_rows = list(filter(lambda x: x[0:5] == 'final', list(s.keys())))
            roi = data_rows + final_rows

            ##################### CLEANING AND CAPTURING LOCATIONS OF LINES #################

            s, x1_x2_dict = self.clean_and_location(s, roi, wc, p1_p3, lines_api)

            ######################################### GETTING LOCATIONS OF HEADERS ##############################
            if 'Global_header' in transcript_info.keys():
                s['sem_header_1'] = ['Number', 'Title', 'Type', 'Grade', 'Attempted', 'Earned', 'GPA', 'Points']
            else:
                pass

            if len(s['sem_header_1'][0]) <= 6:

                s['sem_header_1'][0] = [x.split() for x in s['sem_header_1'][0]]
                s['sem_header_1'][0] = [item for sublist in s['sem_header_1'][0] for item in sublist]
            else:
                pass

            locations = {'sem_header_1': []}

            for header in s['sem_header_1'][0]:
                line_number = [x for x in s['sem_header_1'][1] if header in lines_api[x].split()][0]

                wc_line = wc[line_number]
                locations['sem_header_1'].append(
                    self.get_location_words(p1_p3, lines_api, header, line_number, wc_line)[0])

            if 'sem_header_2' in s.keys():

                locations['sem_header_2'] = []
                if len(s['sem_header_2'][0]) <= 3:
                    s['sem_header_2'][0] = [x.split() for x in s['sem_header_2'][0]]
                    s['sem_header_2'][0] = [item for sublist in s['sem_header_2'][0] for item in sublist]

                    if 'Units' in s['sem_header_2'][0]: s['sem_header_2'][0].remove('GPA')

                for header in s['sem_header_2'][0]:
                    line_number = [x for x in s['sem_header_2'][1] if header in lines_api[x].split()][0]
                    wc_line = wc[line_number]
                    locations['sem_header_2'].append(
                        self.get_location_words(p1_p3, lines_api, header, line_number, wc_line)[0])

            else:
                ## GETTING THE FINAL DATA DICTIONALRY FORMAT
                final_rows = list(filter(lambda x: x[0:5] == 'final', list(s.keys())))
                final_data = self.mapping(s, sem, x1_x2_dict, final_rows, None, 'final_no_df')
                final_scores = final_scores.update(final_data)  ## WORK TO BE DONE

            # print(locations)
            df_sem = pd.DataFrame(columns=s['sem_header_1'][0])
            df_sem = self.mapping(s, sem, x1_x2_dict, data_rows, locations, typ='data')
            df_sem_list.append(df_sem)

            final_scores = {}
            if 'final_data' not in locals():
                df = self.mapping(s, sem, x1_x2_dict, final_rows, locations, typ='final')
                df_final_list.append(df)

        if 'final_data' not in locals():
            return df_sem_list, df_final_list
        else:
            return df_sem_list, final_scores

    ######################################################

    ## CLEAN THE ROW AND LATER CALL THE MAPPING FUNCTION TO MAP IT TO DATAFRAME

    def clean_and_location(self, s, rows, wc, p1_p3, lines_api):

        x1_x2_dict = {}

        for row in rows:
            s[row][0] = [Transcript().clean(word) for word in s[row][0]]

            x1_x2 = []
            for pos, ls in enumerate(s[row][0]):

                line_number = s[row][1][pos]

                if len(s[row][0]) != len(s[row][1]): continue

                if len(ls) == 1:
                    x1, x2 = self.get_location_line(line_number, p1_p3)
                    x1_x2.append((x1, x2))

                if len(ls) > 1:
                    x1, x2 = p1_p3[line_number][0][0], p1_p3[line_number][1][0]
                    total_width = abs(x2 - x1)

                    if len(ls) == 2 and (ls[0] == ls[1]):
                        loc = [(x1, x1 + (total_width) * 0.5), (x1 + (total_width) * 0.5, x2)]

                    else:
                        wc_line = wc[line_number]
                        loc = []
                        for word in ls:
                            l, index = self.get_location_words(p1_p3, lines_api, word, line_number, wc_line)
                            loc.append(l)

                            if index != None: wc_line.remove(wc_line[index])

                        #                         loc = [get_location_words(p1_p3,lines_api,word,line_number,wc) for word in ls]

                        if None in loc:
                            word_len = total_width / len(ls)

                            for i, _ in enumerate(loc):
                                if loc[i] == None:
                                    if i == 0:
                                        loc[i] = (x1, x1 + word_len)
                                    else:
                                        loc[i] = (loc[i - 1][1], loc[i - 1][1] + word_len)
                                else:
                                    pass

                    x1_x2 = x1_x2 + loc
            x1_x2_dict[row] = x1_x2
            s[row][0] = [item for sublist in s[row][0] for item in sublist]

        return s, x1_x2_dict

    ## MAPPING OF THE PROCESSED ROW TO THE DATA FRAME
    def mapping(self, s, sem, x1_x2_dict, rows, locations, typ='data'):

        if locations == None:  ### NO HEADER FOR FINAL DATA

            final_scores = {}
            for row in rows:
                x1_x2 = x1_x2_dict[row]
                fr = row

                s[fr][0] = [Transcript().clean(x) for x in s[fr][0]]
                s[fr][0] = [item for sublist in s[fr][0] for item in sublist if item != '']

                final_scores[sem] = {}
                final_scores[sem][s[fr][0][0]] = s[fr][0][1]
                s['sem_header_2'] = ['Attempted', 'Earned', 'Points']
                d = {}
                try:
                    for i, header in enumerate(s['sem_header_2']):
                        d[header] = s[fr][0][i + 3]
                except:
                    pass
                final_scores[sem][s[fr][0][2]] = d

            return final_scores


        elif typ == 'data':
            df = pd.DataFrame(columns=s['sem_header_1'][0])
            for row in rows:
                x1_x2 = x1_x2_dict[row]
                data = row

                if ((s[data][0][1][0].isdigit()) or (s[data][0][1][0] == 'D')) and (len(s[data][0][1]) > 1) \
                        and ((len(s[data][0][0].split()) <= 1)) and (s[data][0][0][-1] != ':'):

                    s[data][0] = [s[data][0][0] + ' - ' + s[data][0][1]] + s[data][0][2:]
                    x1_x2.remove(x1_x2[1])
                else:
                    pass

                curr_row = {heading: 'NA' for heading in s['sem_header_1'][0]}

                if len(s[data][0]) == len(s['sem_header_1'][0]):
                    curr_row = {}
                    for i, heading in enumerate(s['sem_header_1'][0]):
                        curr_row[heading] = s[data][0][i]
                    df = df.append(curr_row, ignore_index=True)
                else:
                    curr_index = -1
                    for i, heading in enumerate(s['sem_header_1'][0]):

                        x1, x2 = locations['sem_header_1'][i]
                        for j, cord in enumerate(x1_x2):

                            if ((cord[0] in range(x1 - 15, x1 + 16)) or \
                                (cord[1] in range(x2 - 15, x2 + 16)) or (abs(sum(cord) - sum((x1, x2))) <= 25)) \
                                    and (j > curr_index):
                                curr_row[heading] = s[row][0][j]
                                curr_index = j
                                break

                    df = df.append(curr_row, ignore_index=True)

            return df

        else:

            df = pd.DataFrame(columns=s['sem_header_2'][0])
            for row in rows:
                x1_x2 = x1_x2_dict[row]
                fr = row

                curr_row = {heading: 'NA' for heading in s['sem_header_2'][0]}
                curr_index = -1

                for i, heading in enumerate(s['sem_header_2'][0]):
                    x1, x2 = locations['sem_header_2'][i]
                    found = False

                    for j, cord in enumerate(x1_x2):
                        if found == False:
                            if (cord[0] in range(x1 - 15, x1 + 16)) or (cord[1] in range(x2 - 15, x2 + 16)) \
                                    or (abs(sum(cord) - sum((x1, x2))) <= 25):
                                if j > curr_index: curr_row[heading] = s[fr][0][j]
                                curr_index = j
                                found = True
                        else:
                            pass

                if list(curr_row.values()).count('NA') >= 1:  ## IF NA COUNT IN ROW >1
                    ##SPECIFIC CASE
                    if ([w[0].isdigit() for w in s[fr][0][-4:]] == [True] * len(s['sem_header_2'][0])) and \
                            ('Grade' not in s['sem_header_2'][0]):

                        for i, heading in enumerate(s['sem_header_2'][0]):
                            curr_row[heading] = s[fr][0][-4:][i]
                            ##SPECIFIC CASE
                    elif ([w[0].isdigit() for w in s[fr][0][-4:]] == [True, True, False, True]) and \
                            ('Grade' in s['sem_header_2'][0]):
                        for i, heading in enumerate(s['sem_header_2'][0]):
                            curr_row[heading] = s[fr][0][-4:][i]

                    else:
                        pass

                ################### NAMES OF INDICES EXTRACTION #################################

                index_found = False
                index_place = -(len(s['sem_header_2'][0]) + 1)

                try:
                    if (not s[fr][0][index_place - 1][0].isdigit()) and (not s[fr][0][index_place].isdigit()):
                        row = pd.Series(curr_row, name=s[fr][0][index_place - 1] + ' ' + s[fr][0][index_place])
                        df = df.append(row)
                        index_found = True
                    else:
                        pass
                except:
                    pass

                if index_found == False:
                    try:
                        if not s[fr][0][index_place].isdigit():
                            row = pd.Series(curr_row, name=s[fr][0][index_place])
                            df = df.append(row)

                        else:
                            df = df.append(curr_row, ignore_index=True)
                    except:
                        df = df.append(curr_row, ignore_index=True)

            return df

        #########################################################

    def get_location_words(self, p1_p3, lines_api, word, line_number, wc_line):

        words = wc_line

        if lines_api[line_number] == word:
            return self.get_location_line(line_number, p1_p3), None

        for p, w in enumerate(words):
            try:
                if sum([list(w[1])[i] == list(word)[i] for i in range(len(word))]) == len(word):
                    return (w[0][0], w[0][2]), p

                elif sum([list(w[1])[i] == list(word)[i] for i in range(len(word))]) in range(len(word) - 2,
                                                                                              len(word) + 3):
                    return (w[0][0], w[0][2]), p

                else:
                    pass

                if (len(word) >= len(w) + 2) and (w in word) and (w not in ['.']):
                    return (w[0][0], w[0][2]), p

            except:
                pass

        return self.get_location_line(line_number, p1_p3), None

    def get_location_line(self, line_number, p1_p3):
        return (p1_p3[line_number][0][0], p1_p3[line_number][1][0])

    def clean(self, x):
        words = x.split()

        if len(words) == 1:
            # *****SPECIAL CASES****#
            reg = list(filter(None, re.split('(\d+)', x)))

            if (':' in x) and (x.split(':')[0].isdigit()) and (x.split(':')[1].isdigit()):
                return words

            elif (len(reg) > 1) and ('.' not in list(x)):  ## Splitting words and charecters
                return reg

            return words

        ## When Starts witha WORD Ends with A Word USUALLY SUBJECTS
        if (words[0][0].isdigit() == False and words[-1][0].isdigit() == False) and (
                len(words[0]) > 3 and len(words[-1]) > 3) and (len(words) > 2):
            return [x]

        ## ALL ALPHABATICAL WORDS (of ant length)
        if [word[0].isdigit() for word in words] == [False] * len(words):
            return [' '.join(words)]

        ## ALL ALPHABATICAL ONE NUMERIC WITH LEN 1

        numbers = [word for word in words if word.isdigit()]

        if len(numbers) == 1 and len(numbers[0]) == 1:
            return [' '.join(words)]

        if len(words) == 2:
            ## BOTH ARE NUMBERS AND '.' (present)

            if words[0].isdigit() and words[1].isdigit():
                return ['.'.join(words)]

            ## BOTH ARE NUMBERS AND '.' (present)
            elif ((words[0].isdigit() and words[1][1].isdigit()) or (
                    words[0][0].isdigit() and words[1].isdigit())) and (
                    (['.' in list(word) for word in words]) != [False] * len(words)):
                return [''.join(words)]

            ## ONE APLHABATIC AND ONE NUMERIC

            else:
                return words

        elif len(words) == 3:
            # **************************SPECIAL CASES************************************************** #

            ## MIX OF NUMBERS AND ALPHABET!!  '.' (present)   ALPHABET IN THE START
            if '.' in [words[0], words[2]]:
                words.remove('.')
                return words

            ## ALL ARE INDEPENDENT NUMBERS!!
            elif ([('.' in word) or (',' in word) or (';' in word) or (':' in word) for word in words] == [True] * len(
                    words)) and ([word[0].isdigit() for word in words] == [True] * len(words)):

                return [re.sub(r',|;|:', '.', word) for word in words]

            ## ALL ARE NUMBERS AND '.' (present)
            elif ([word[0].isdigit() for word in words] == [True] * len(words)) and (
                    (['.' in list(word) for word in words]) != [False] * len(words)):
                return [''.join(words)]


            ## ALL ARE NUMBERS AND '.' (absent)
            elif ([word[0].isdigit() for word in words] == [True] * len(words)):
                return [words[0] + '.' + ''.join(words[1:])]


            ## MIX OF NUMBERS AND ALPHABET!!  '.' (present)  ALPHABET IN THE START
            elif not words[0][0].isdigit() and ((['.' in list(word) for word in words]) != [False] * len(words)):
                return [words[0], ''.join(words[1:])]

            ## MIX OF NUMBERS AND ALPHABET!!  '.' (present)  ALPHABET IN THE END
            elif not words[2].isdigit() and ((['.' in list(word) for word in words]) != [False] * len(words)):
                return [''.join(words[:2]), words[2]]

            ## MIX OF NUMBERS AND ALPHABET!!  '.' (absent)  ALPHABET IN THE START
            elif not words[0].isdigit():
                return [words[0], ''.join(words[1:])]

            ## MIX OF NUMBERS AND ALPHABET!!  '.' (absent)  ALPHABET IN THE END
            elif not words[2].isdigit():
                return ['.'.join(words[:2]), words[2]]

            # ********************************************************************************************* #
            ## MIX OF NUMBERS AND ALPHABET!!  '.' (present)   ALPHABET IN THE START
            elif not words[2].isdigit() and ((['.' in list(word) for word in words]) != [False] * len(words)):
                return [''.join(words[:2]), words[2]]

            ## MIX OF NUMBERS AND ALPHABET!!  '.' (absent)   ALPHABET IN THE END
            elif not words[2].isdigit():
                return ['.'.join(words[:2]), words[2]]

            ##  TWO NUMBERS AND '.' in between

            elif words[2].isdigit() and words[0].isdigit() and words[1] == '.':
                return [''.join(words)]

            # ********************************************************************************************* #

            ## MIX OF NUMBERS AND ALPHABET!!  '.' (present)   ALPHABET IN THE START
            elif '.' in [words[0], words[2]]:
                words.remove('.')
                return words

        else:
            return words
