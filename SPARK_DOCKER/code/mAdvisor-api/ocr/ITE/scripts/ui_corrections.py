# -*- coding: utf-8 -*-
import base64
import re
import sys
import numpy as np
from collections import OrderedDict
import cv2
import os
import matplotlib as mpl
from PIL import ImageFont, ImageDraw, Image
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ocr/ITE/My_ProjectOCR_2427.json"
if os.environ.get('DISPLAY', '') == '':
    mpl.use('Agg')

"""Recursive dept expansion required for recursive functions i.e fonttunning()"""
sys.setrecursionlimit(10 ** 9)


def fonttunning(text, font, fontsize, width):
    """Estimation of font size reduction by reducing 0.001 in each iteration until no overlap for OPENCV plots"""
    textSize = cv2.getTextSize(text=text, fontFace=font, fontScale=fontsize, thickness=1)  # ((61, 22), 10)
    if width < textSize[0][0]:
        fontsize = fontsize - (textSize[0][0] - width) * 0.001
        return fonttunning(text, font, fontsize, width)
    else:
        return fontsize


class ui_corrections:

    def __init__(self, mask, final_json, image_path=None, image_directory_name=None,
                 database_path=None):
        self.mask = mask
        self.final_json = final_json
        # self.google_response = self.optimised_fetch_google_response(image_path, image_directory_name, database_path)
        # self.google_response = google_response
        # self.google_response2 = google_response2
        self.image_name = image_directory_name

    def check_if_centroid_inbetween_p1_p3(self, centroid, p1, p3):
        if p1[0] <= centroid[0] <= p3[0] and p1[1] <= centroid[1] <= p3[1]:
            return True
        else:
            return False

    def all_words(self, analysis):

        loi = []
        for line in analysis['lines']:
            for word in line['words']:
                if word['confidence'] < 0.8:
                    try:
                        loi.append({word['text']: [word['boundingBox'][:2], word['boundingBox'][4:6]]})
                    except:
                        pass
        return loi

    def calculate_centroid(self, p1, p3):
        x_centroid = ((p1[0] + p3[0]) * 0.5)
        y_centroid = ((p1[1] + p3[1]) * 0.5)
        return x_centroid, y_centroid

    def adjust_gamma(self, image, gamma):  # TODO: Give Abishek's Autogamma correction code also.
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)

    def toPercentage(self, x1, y1, x2, y2, x3, y3, x4, y4, height, width):
        x1p = round(x1 / width, 2)  # play with the round of parameter for better pricision
        x2p = round(x2 / width, 2)
        x3p = round(x3 / width, 2)
        x4p = round(x4 / width, 2)
        y1p = round(y1 / height, 3)
        y2p = round(y2 / height, 3)
        y3p = round(y3 / height, 3)
        y4p = round(y4 / height, 3)
        # def toImCoord(im1, x1p,y1p,x2p,y2p):
        w, h = 700, 800
        p1 = int(x1p * w)
        p2 = int(y1p * h)
        p3 = int(x2p * w)
        p4 = int(y2p * h)
        p5 = int(x3p * w)
        p6 = int(y3p * h)
        p7 = int(x4p * w)
        p8 = int(y4p * h)

        return p1, p2, p3, p4, p5, p6, p7, p8

    def confidence_filter(self, analysis, user_input):  # 90
        loi = []
        for line in analysis['lines']:
            for word in line['words']:
                if word['confidence'] < user_input:
                    try:
                        loi.append({word['text']: [word['boundingBox'][:2], word['boundingBox'][4:6]]})
                    except:
                        pass
        return loi

    def default_all_words_flag_to_false(self, final_json):
        for para in final_json["paragraphs"]:
            for line in final_json["paragraphs"][para]:
                for word in line:
                    word.update({"flag": False, "color": None})
        #            print(word)
        for table in final_json["tables"]:
            for cell in final_json["tables"][table]:
                for word in final_json["tables"][table][cell]["words"]:
                    word.update({"flag": False, "color": None})
        return final_json

    def flag_words_to_plot(self, final_json, needed_words, mode):
        u1 = []
        for k in final_json["paragraphs"]:
            for l in final_json["paragraphs"][k]:
                for m in l:
                    p1 = m['boundingBox']["p1"]
                    p3 = m['boundingBox']["p3"]

                    #            print(p1,p3)
                    for i in needed_words:
                        x, y = self.calculate_centroid(list(i.values())[0][0], list(i.values())[0][1])
                        if mode:
                            if (self.check_if_centroid_inbetween_p1_p3([x, y], p1, p3) and (
                                    m['text'] == list(i.keys())[0])):
                                m['flag'] = True
                                break
                            elif (self.check_if_centroid_inbetween_p1_p3([x, y], p1, p3) and (
                                    m['text'] != list(i.keys())[0])):
                                m['flag'] = True
                                temp_dict = {m['text']: [p1, p3]}
                                if temp_dict not in u1: u1.append(temp_dict)
                            else:
                                m['flag'] = False
                        #                                temp_dict = {list(m.keys())[0]: [p1,p3]}
                        #                                if temp_dict not in u1: u1.append(temp_dict)

                        else:
                            if (self.check_if_centroid_inbetween_p1_p3([x, y], p1,
                                                                       p3)):  # and (list(m.keys())[0]==list(i.keys())[0])):
                                m['flag'] = True
                                break
                            else:
                                m['flag'] = False
        for k in final_json["tables"]:
            for l in final_json["tables"][k]:
                for m in final_json["tables"][k][l]["words"]:
                    p1 = m["boundingBox"]["p1"]
                    p3 = m["boundingBox"]["p3"]
                    for i in needed_words:
                        x, y = self.calculate_centroid(list(i.values())[0][0], list(i.values())[0][1])
                        if mode:
                            if (self.check_if_centroid_inbetween_p1_p3([x, y], p1, p3) and (
                                    m["text"] == list(i.keys())[0])):
                                m.update({"flag": True})
                                break
                            elif (self.check_if_centroid_inbetween_p1_p3([x, y], p1, p3) and (
                                    m["text"] != list(i.keys())[0])):
                                m.update({"flag": True})
                                temp_dict = {m["text"]: [p1, p3]}
                                if temp_dict not in u1: u1.append(temp_dict)
                            else:
                                m.update({"flag": False})
                        #                                    temp_dict = {m["text"]: [p1,p3]}
                        #                                    if temp_dict not in u1: u1.append(temp_dict)
                        else:
                            if (self.check_if_centroid_inbetween_p1_p3([x, y], p1,
                                                                       p3)):  # and (m["text"]==list(i.keys())[0])):
                                m.update({"flag": True})
                                break
                            else:
                                m.update({"flag": False})

        upd = {'U1': u1}
        # update_u1(upd, image_name)
        return upd, final_json

    def flag_words_to_plot_custom(self, final_json, metadata):
        final_dict = {}
        for field in metadata['custom_fields']:
            p1, p3 = metadata['custom_fields'][field]['BoundingBox']

            final_dict[field] = []
            for k in final_json["paragraphs"]:
                for l in final_json["paragraphs"][k]:
                    for m in l:
                        p1w = m['boundingBox']["p1"]
                        p3w = m['boundingBox']["p3"]
                        p2w = [p3[0], p1[1]]
                        p4w = [p1[0], p3[1]]
                        bb = p1w + p2w + p3w + p4w
                        x, y = self.calculate_centroid(p1w, p3w)

                        if self.check_if_centroid_inbetween_p1_p3([x, y], p1, p3):
                            m['flag'] = True
                            final_dict[field].append((m['text'], bb))
                        elif 'flag' in list(m.keys()):
                            pass
                        else:
                            m['flag'] = False

            for k in final_json["tables"]:
                for l in final_json["tables"][k]:
                    for m in final_json["tables"][k][l]["words"]:
                        p1w = m['boundingBox']["p1"]
                        p3w = m['boundingBox']["p3"]
                        p2w = [p3[0], p1[1]]
                        p4w = [p1[0], p3[1]]
                        bb = p1w + p2w + p3w + p4w
                        x, y = self.calculate_centroid(p1w, p3w)

                        if self.check_if_centroid_inbetween_p1_p3([x, y], p1, p3):
                            m['flag'] = True
                            final_dict[field].append((m['text'], bb))
                        elif 'flag' in list(m.keys()):
                            pass
                        else:
                            m['flag'] = False

        for label in final_dict:

            words = final_dict[label]
            label_final = []

            #            depths = list(map(lambda x : x[1][1] , words))
            depths = list(map(lambda x: int((x[1][1] + x[1][5]) * 0.5), words))
            groups_formed = dict(enumerate(grouper(depths), 1))

            for group in groups_formed:
                sub_line = []
                for word in words:
                    #                    if word[1][1] in groups_formed[group]:
                    if int((word[1][1] + word[1][5]) * 0.5) in groups_formed[group]:
                        sub_line.append(word[0])
                    else:
                        pass
                label_final.append(' '.join(sub_line))

            final_dict[label] = '\n'.join(label_final)
        return final_dict, final_json

    def highlight_word(self, img, text, cord, fontScale,
                       font):  # text = "Some text in a box!"  img = np.zeros((500, 500))

        #        font_scale = 0.7
        #        font = cv2.FONT_HERSHEY_PLAIN
        #        print('FONT : ' ,font)
        # set the rectangle background to Yellow
        rectangle_bgr = (0, 255, 255)  # [255,255,0] (255, 255, 0)

        # get the width and height of the text box
        (text_width, text_height) = cv2.getTextSize(text, fontFace=2, fontScale=fontScale, thickness=1)[0]
        # set the text start position
        text_offset_x = cord[0]
        text_offset_y = cord[1]  # org=(p1[0],int((p3[1]+p1[1])*0.5))
        # make the coords of the box with a small padding of two pixels
        box_coords = (
            (text_offset_x, text_offset_y), (int(text_offset_x + (text_width) * 1.01), text_offset_y - text_height - 2))
        # print("text : ", text, "box_coords : ", box_coords)
        cv2.rectangle(img, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
        image_final = cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale=fontScale,
                                  color=(0, 0, 0), thickness=1)

        return image_final

    def get_optimal_params(self, bb_height, ratio, area):  ## bb width,page size, number of letters to print

        if ratio > 11:
            font = cv2.FONT_HERSHEY_DUPLEX
        #            font = cv2.FONT_HERSHEY_COMPLEX
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
        #            font = cv2.FONT_HERSHEY_COMPLEX_SMALL

        if area > (1000 * 1000):  ## ABOVE THRESHOLD QUALITY IMAGES
            if bb_height > 70:
                fontscale = 1
            elif bb_height > 60:
                fontscale = 0.92
            elif bb_height > 50:
                fontscale = 0.85
            elif bb_height > 40:
                fontscale = 0.78
            elif bb_height > 30:
                fontscale = 0.71
            elif bb_height > 20:
                fontscale = 0.62
            else:
                fontscale = 0.5
        else:
            fontscale = area / (1000 * 1000)  ## DYNAMIC FONT SCALE
            font = cv2.FONT_HERSHEY_SIMPLEX
            #            print(fontscale)

            if bb_height > 20 and ratio > 8:  # BIG TEXT BUT NOT CONJUSTED
                pass

            elif bb_height > 15 and ratio > 8:  # BIG TEXT BUT NOT CONJUSTED
                fontscale = 0.45

            elif bb_height > 15:  # BIG TEXT BUT CONJUSTED
                fontscale = 0.32

            elif ratio > 8:  ##  SMALL TEXT BUT NOT CONJUSTED
                fontscale = 0.35

            elif fontscale < 0.35:
                pass
            else:
                fontscale = 0.35

        #        fontscale_final = (fontScale_default+fontscale)*0.5
        return fontscale, font

    """def render_flagged_image(self, final_json_to_flag, mask, gen_image):  # plain_mask = False

        #        texted_image = self.adjust_gamma(texted_image, gamma=0.2)
        height, width, _ = mask.shape
        area = height * width
        #        fontScale = 0.6
        #        print (fontScale)
        #        print(final_json_to_flag)
        #        print('RESULT: ',sum([len(final_json_to_flag["tables"][table]) for table in final_json_to_flag["tables"]]))
        # if ((len(final_json_to_flag["tables"]) == 0) or (sum(
        #         [len(final_json_to_flag["tables"][table]) for table in final_json_to_flag["tables"]]) == 0)) and min(
        #     height, width) < 700:  # or plain_mask == True:
        #     white_canvas = 255 * np.ones(mask.shape).astype(mask.dtype)
        #     mask = white_canvas.copy()
        # else:
        #     pass

        if 'paragraphs' in final_json_to_flag:
            for k in final_json_to_flag["paragraphs"]:
                for l in final_json_to_flag["paragraphs"][k]:
                    for m in l:
                        p1 = m['boundingBox']["p1"]
                        p3 = m['boundingBox']["p3"]
                        p2 = [p3[0], p1[1]]
                        p4 = [p1[0], p3[1]]
                        text = m['text']
                        #
                        #                        print('WORD : ',text , ' BoundingBox Height : ',abs(p3[1]-p1[1]))
                        #                        print('WORD : ',text , ' BoundingBox Width / len of word : ',abs(p3[0]-p1[0])/len(text))
                        #
                        #                        print('*'*10)
                        #
                        height, ratio = abs(p3[1] - p1[1]), abs(p3[0] - p1[0]) / len(text)
                        fontScale, font = self.get_optimal_params(height, ratio, area)
                        #                        print('FONT : ',font)
                        if m['flag'] == True:
                            mask = self.highlight_word(mask, text, (p4[0] + 3, int((p4[1] + p1[1]) * 0.5)), fontScale,
                                                       font)
                        else:
                            cv2.putText(mask, text, (p4[0] + 3, int((p4[1] + p1[1]) * 0.5)), font, fontScale, (0, 0, 0),
                                        1, cv2.LINE_AA)
        else:
            pass

        if 'tables' in final_json_to_flag:
            for k in final_json_to_flag["tables"]:
                for l in final_json_to_flag["tables"][k]:
                    for m in final_json_to_flag["tables"][k][l]["words"]:
                        p1 = m["boundingBox"]["p1"]
                        p3 = m["boundingBox"]["p3"]
                        p2 = [p3[0], p1[1]]
                        p4 = [p1[0], p3[1]]
                        text = m["text"]
                        vertices = [p1, p2, p3, p4]

                        #                        print('WORD : ',text , ' BoundingBox Height : ',abs(p3[1]-p1[1]))
                        #                        print('WORD : ',text , ' BoundingBox Width / len of word : ',abs(p3[0]-p1[0])/len(text))
                        #
                        #                        print('*'*10)

                        height, ratio = abs(p3[1] - p1[1]), abs(p3[0] - p1[0]) / len(text)
                        fontScale, font = self.get_optimal_params(height, ratio, area)
                        #                        print('FONT : ',font)
                        if m['flag'] == True:
                            mask = self.highlight_word(mask, text, (p4[0] + 3, int((p4[1] + p1[1]) * 0.5)), fontScale,
                                                       font)
                        else:
                            cv2.putText(mask, text, (p4[0] + 3, int((p4[1] + p1[1]) * 0.5)), font, fontScale, (0, 0, 0),
                                        1, cv2.LINE_AA)
        else:
            pass

        #        int((p4[1]+p1[1])*0.5)

        if area < 1000 * 1000:
            pass

        else:
            mask = self.adjust_gamma(mask, gamma=0.4)
        mask = dynamic_cavas(mask)
        cv2.imwrite(gen_image, mask)
        return"""

    def render_flagged_image2(self, final_json, mask, gen_image_path, language_input):

        #        texted_image = self.adjust_gamma(texted_image, gamma=0.2)
        height, width = mask.shape[:2]
        #        area = height * width

        language_fonts = {"Korean": 'gulim.ttf', 'Chinese-1': 'simsun.ttc', 'Japanese': 'TakaoGothic.ttf'}
        if language_input in language_fonts.keys():
            fontpath = "ocr/ITE/fonts/" + language_fonts[language_input]
        else:
            fontpath = "ocr/ITE/fonts/FreeMono.ttf"

        font = ImageFont.truetype(fontpath, 12)

        img_pil = Image.fromarray(mask)
        draw = ImageDraw.Draw(img_pil)
        b, g, r, a = 0, 0, 0, 0

        if 'paragraphs' in final_json:
            for k in final_json["paragraphs"]:
                for l in final_json["paragraphs"][k]:
                    for m in l:
                        p1 = m['boundingBox']["p1"]
                        p3 = m['boundingBox']["p3"]
                        p2 = [p3[0], p1[1]]
                        p4 = [p1[0], p3[1]]
                        text = m['text']

                        draw.text((p1[0] + 3, p1[1]), text, font=font, fill=(b, g, r, a))


        else:
            pass

        if 'tables' in final_json:
            for k in final_json["tables"]:
                for l in final_json["tables"][k]:
                    for m in final_json["tables"][k][l]["words"]:
                        p1 = m["boundingBox"]["p1"]
                        p3 = m["boundingBox"]["p3"]
                        p2 = [p3[0], p1[1]]
                        p4 = [p1[0], p3[1]]
                        text = m["text"]

                        draw.text((p1[0] + 3, p1[1]), text, font=font, fill=(b, g, r, a))
        else:
            pass
        mask = np.array(img_pil)
        mask = self.adjust_gamma(mask, gamma=0.4)
        mask = dynamic_cavas(mask)

        cv2.imwrite(gen_image_path, mask)
        return

    def render_flagged_image(self, final_json_to_flag, mask, gen_image_path):
        words_with_special_characters = []
        #        texted_image = self.adjust_gamma(texted_image, gamma=0.2)
        height, width = mask.shape[:2]
        area = height * width
        font = cv2.FONT_HERSHEY_SIMPLEX

        if 'paragraphs' in final_json_to_flag:
            for k in final_json_to_flag["paragraphs"]:
                for l in final_json_to_flag["paragraphs"][k]:
                    for m in l:
                        p1 = m['boundingBox']["p1"]
                        p3 = m['boundingBox']["p3"]
                        p2 = [p3[0], p1[1]]
                        p4 = [p1[0], p3[1]]
                        text = m['text']
                        x = re.findall(r'[^\x00-\x7F]', text)
                        if x:
                            words_with_special_characters.append(m)
                        else:
                            heightoftext = p4[1] - p1[1]
                            widthoftext = p2[0] - p1[0]
                            fontScale = (heightoftext / 4.5) * 0.1
                            fontScale = fonttunning(text, font, fontScale, widthoftext)
                            textSize = cv2.getTextSize(text=text, fontFace=font, fontScale=fontScale, thickness=1)
                            anchorX = p4[0] + 3
                            anchorY = int((p4[1] + p1[1]) * 0.5)
                            anchorXforcleaning = (anchorX, anchorY - 1 - textSize[0][1])
                            anchorYforcleaning = (anchorX + textSize[0][0], anchorY + 5)
                            cv2.rectangle(mask, anchorXforcleaning, anchorYforcleaning, (255, 255, 255), -1)
                            # height, ratio = abs(
                            #     p3[1] - p1[1]), abs(p3[0] - p1[0]) / len(text)
                            # fontScale, font = self.get_optimal_params(
                            #     height, ratio, area)
                            #                        print('FONT : ',font)
                            if m['flag']:
                                mask = self.highlight_word(
                                    mask, text, (anchorX, anchorY), fontScale, font)
                            else:
                                cv2.putText(mask,
                                            text,
                                            (anchorX, anchorY),
                                            font,
                                            fontScale,
                                            (0,
                                             0,
                                             0),
                                            1,
                                            cv2.LINE_AA)


        else:
            pass

        if 'tables' in final_json_to_flag:
            for k in final_json_to_flag["tables"]:
                for l in final_json_to_flag["tables"][k]:
                    for m in final_json_to_flag["tables"][k][l]["words"]:
                        p1 = m["boundingBox"]["p1"]
                        p3 = m["boundingBox"]["p3"]
                        p2 = [p3[0], p1[1]]
                        p4 = [p1[0], p3[1]]
                        text = m["text"]
                        #                        print(text)
                        vertices = [p1, p2, p3, p4]

                        x = re.findall(r'[^\x00-\x7F]', text)
                        if x:
                            words_with_special_characters.append(m)
                        else:
                            heightoftext = p4[1] - p1[1]
                            widthoftext = p2[0] - p1[0]
                            fontScale = (heightoftext / 4.5) * 0.1
                            fontScale = fonttunning(text, font, fontScale, widthoftext)
                            textSize = cv2.getTextSize(text=text, fontFace=font, fontScale=fontScale, thickness=1)
                            anchorX = p4[0] + 3
                            anchorY = int((p4[1] + p1[1]) * 0.5)
                            anchorXforcleaning = (anchorX, anchorY - 1 - textSize[0][1])
                            anchorYforcleaning = (anchorX + textSize[0][0], anchorY + 5)
                            cv2.rectangle(mask, anchorXforcleaning, anchorYforcleaning, (255, 255, 255), -1)

                            if m['flag']:
                                mask = self.highlight_word(
                                    mask, text, (anchorX, anchorY), fontScale, font)
                            else:
                                cv2.putText(mask,
                                            text,
                                            (anchorX, anchorY),
                                            font,
                                            fontScale,
                                            (0,
                                             0,
                                             0),
                                            1,
                                            cv2.LINE_AA)
        else:
            pass

        #        int((p4[1]+p1[1])*0.5)

        if area < 1000 * 1000:
            pass

        else:
            mask = self.adjust_gamma(mask, gamma=0.4)
        if len(words_with_special_characters) > 0:
            img_pil = Image.fromarray(mask)
            draw = ImageDraw.Draw(img_pil)
            for except_word in words_with_special_characters:
                # print(words_with_special_characters)
                b, g, r, a = 0, 0, 0, 0
                fontpath = os.path.join(os.getcwd(), "ocr", "ITE", "fonts", "DejaVuSans.ttf")
                p1 = except_word['boundingBox']["p1"]
                p3 = except_word['boundingBox']["p3"]
                p2 = [p3[0], p1[1]]
                p4 = [p1[0], p3[1]]
                heightofbox = p4[1] - p1[1]
                widthofbox = p2[0] - p1[0]
                if heightofbox != 0:
                    font_size = int(heightofbox * .65)
                else:
                    font_size = 7
                text = except_word['text']
                font_custom = ImageFont.truetype(fontpath, font_size)
                # yanchor_cord = int(p1[1])-int(heightofbox/4)
                if except_word['flag'] == True:
                    draw.text((p4[0] + 3, int((p4[1] + p1[1]) * 0.5)), text, fill=(0, 0, 0), font=font_custom,
                              anchor="ls", stroke_fill=(0, 255, 255, 255), stroke_width=5)
                else:
                    # draw.rectangle(((p1[0],p1[1]),(p3[0],p3[1])),fill=(0, 255, 255, 255))
                    draw.text((p4[0] + 3, int((p4[1] + p1[1]) * 0.5)), text, fill=(0, 0, 0), font=font_custom,
                              anchor="ls")
                # img_pil.show()
            mask = np.array(img_pil)
        else:
            pass
        mask = dynamic_cavas(mask)
        cv2.imwrite(gen_image_path, mask)
        return

    def document_confidence(self, analysis):
        word_count, error = 0, 0
        for line in analysis['lines']:

            for word in line['words']:
                word_count = word_count + 1

                if word['confidence'] < 0.8:
                    error = error + 1
                else:
                    pass
        try:
            document_accuracy = round((word_count - error) / word_count, 2)
        except ZeroDivisionError:
            document_accuracy = 0
        return document_accuracy, word_count

    def document_fields_count(self, analysis):
        word_count = 0
        for line in analysis['lines']:

            for word in line['words']:
                word_count = word_count + 1
        return word_count


def ui_flag_v2(mask, final_json, gen_image, analysis, percent=1):
    mask = mask
    final_json = final_json

    uc_obj = ui_corrections(mask, final_json)

    final_json = uc_obj.default_all_words_flag_to_false(final_json)
    doc_accuracy, total_words = uc_obj.document_confidence(analysis)

    if percent == 1:
        mode = "default"
        needed_words = uc_obj.all_words(analysis)
    else:
        mode = None
        needed_words = uc_obj.confidence_filter(analysis, percent)
    upd, fj = uc_obj.flag_words_to_plot(final_json, needed_words, mode)

    uc_obj.render_flagged_image(fj, uc_obj.mask, gen_image)
    # cv2.imwrite(gen_image, texted_image)
    with open(gen_image, mode='rb') as file:
        img = file.read()
    gen_image = base64.encodebytes(img)
    return gen_image, doc_accuracy, total_words


def ui_flag_v3(mask, final_json, gen_image, analysis, percent=1):
    mask = mask
    final_json = final_json

    uc_obj = ui_corrections(mask, final_json)

    final_json = uc_obj.default_all_words_flag_to_false(final_json)
    doc_accuracy, total_words = uc_obj.document_confidence(analysis)

    if percent == 1:
        mode = "default"
        needed_words = uc_obj.all_words(analysis)
    else:
        mode = None
        needed_words = uc_obj.confidence_filter(analysis, percent)
    upd, fj = uc_obj.flag_words_to_plot(final_json, needed_words, mode)

    uc_obj.render_flagged_image(fj, uc_obj.mask, gen_image)
    return gen_image, doc_accuracy, total_words


def ui_flag_v4(mask, final_json, gen_image_path, analysis, language_input):
    mask = mask
    final_json = final_json
    uc_obj = ui_corrections(mask, final_json)
    #    final_json = uc_obj.default_all_words_flag_to_false(final_json)
    total_words = uc_obj.document_fields_count(analysis)
    #    if percent == 1:
    #        mode = "default"
    #        needed_words = uc_obj.all_words(analysis)
    #    else:
    #        mode = None
    #        needed_words = uc_obj.confidence_filter(analysis, percent)
    #    upd, fj = uc_obj.flag_words_to_plot(final_json, needed_words, mode)

    uc_obj.render_flagged_image2(final_json, uc_obj.mask, gen_image_path, language_input)

    return gen_image_path, total_words


def check_if_centroid_inbetween_p1_p3(centroid, p1, p3):
    if p1[0] <= centroid[0] <= p3[0] and p1[1] <= centroid[1] <= p3[1]:
        return True
    else:
        return False


def fetch_click_word_from_final_json(final_json, click_coordinate):
    if "paragraphs" in final_json.keys():
        for para in final_json["paragraphs"]:
            for line in final_json["paragraphs"][para]:
                for word in line:

                    p1 = word['boundingBox']['p1']
                    p3 = word['boundingBox']['p3']
                    print(p1, p3)
                    if check_if_centroid_inbetween_p1_p3(click_coordinate, p1, p3):
                        return True, word['text']
    if "tables" in final_json.keys():
        for k in final_json["tables"]:
            for l in final_json["tables"][k]:
                for m in final_json["tables"][k][l]["words"]:
                    p1 = m["boundingBox"]["p1"]
                    p3 = m["boundingBox"]["p3"]
                    if check_if_centroid_inbetween_p1_p3(click_coordinate, p1, p3):
                        return True, m['text']

    return False, ""


def update_user_changes_to_from_final_json(final_json, click_coordinate, user_input):
    """
    click coordinate is a list where the word has to be updated
    user input is a string that  user provides
    """
    for k in final_json["paragraphs"]:
        for l in final_json["paragraphs"][k]:
            for m in l['words']:
                #                print(m)
                p1 = list(m.values())[0][0:2]
                p3 = list(m.values())[0][4:6]
                if check_if_centroid_inbetween_p1_p3(click_coordinate, p1, p3):
                    m['text'] = user_input
                    return True, final_json

    for k in final_json["tables"]:
        for l in final_json["tables"][k]:
            for m in final_json["tables"][k][l]["words"]:
                p1 = m["boundingBox"]["p1"]
                p3 = m["boundingBox"]["p3"]
                if check_if_centroid_inbetween_p1_p3(click_coordinate, p1, p3):
                    m['text'] = user_input
                    return True, final_json
    return False, final_json


def offset(dev_click_cord, image_size, dim):
    x, y = dev_click_cord[0], dev_click_cord[1]
    x_offseted = int(x * (image_size[1] / dim[1]))
    y_offseted = int(y * (image_size[0] / dim[0]))

    return [x_offseted, y_offseted]


def cleaned_final_json(final_json):
    clean_final_json = final_json.copy()

    if 'paragraphs' in final_json.keys():
        for i in range(len(final_json['paragraphs'])):

            lines = {}
            for j, line in enumerate(final_json['paragraphs']['p_' + str(i + 1)]):
                lines['line_' + str(j + 1)] = ' '.join([word['text'] for word in line])

            clean_final_json['paragraphs']['p_' + str(i + 1)] = lines
    else:
        pass

    if 'tables' in final_json.keys():
        for i in range(len(final_json['tables'])):

            for cell in final_json['tables'][str(i + 1)]:
                cell_content = {}
                for j, word in enumerate(clean_final_json['tables'][str(i + 1)][cell]['words']):
                    cell_content[j + 1] = clean_final_json['tables'][str(i + 1)][cell]['words'][j]['text']

                clean_final_json['tables'][str(i + 1)][cell] = cell_content
    else:
        pass

    return clean_final_json


def sort_json(final_json):
    sorted_json = {}
    for key in final_json.keys():
        if key not in ['tables', 'paragraphs']:
            sorted_json[key] = final_json[key]

    if 'paragraphs' in final_json.keys():
        para_order = sorted(final_json['paragraphs'], key=lambda x: int(x.split('_')[1]))

        paras = []
        for para in para_order:
            paras.append((para, final_json['paragraphs'][para]))

        sorted_json['paragraphs'] = OrderedDict(paras)

    if 'tables' in final_json.keys():
        sorted_json['tables'] = {}
        for table in final_json['tables']:
            cell_order = sorted(final_json['tables'][table], key=lambda x: int(x.split('r')[0].split('c')[-1]))

            cells = []
            for cell in cell_order:
                cells.append((cell, final_json['tables'][table][cell]))

            sorted_json['tables'][table] = OrderedDict(cells)

    return sorted_json


def dynamic_cavas(image):
    height, width = image.shape[:2]

    if max(height, width) > 2000:  # 35% size reduction
        scale_percent = 65  # percent of original size

    elif max(height, width) > 1500:
        scale_percent = 75



    elif max(height, width) > 1000:
        scale_percent = 85

    else:
        scale_percent = 100

    width_scaled = int(image.shape[1] * scale_percent / 100)
    height_scaled = int(image.shape[0] * scale_percent / 100)

    dim = (width_scaled, height_scaled)
    # resize image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized


def dynamic_cavas_size(shape):
    height, width = shape

    if max(height, width) > 2000:  # 35% size reduction
        scale_percent = 65  # percent of original size

    elif max(height, width) > 1500:
        scale_percent = 75

    elif max(height, width) > 1000:
        scale_percent = 85

    else:
        scale_percent = 100

    width_scaled = int(shape[1] * scale_percent / 100)
    height_scaled = int(shape[0] * scale_percent / 100)

    dim = height_scaled, width_scaled

    return dim


def custom_field(analysis, cords):  ##[p1,p3]

    final_dict = {}
    wc = []
    for i, line in enumerate(analysis["lines"]):
        wc.append([(word['boundingBox'], word['text']) for word in line['words']])

    p1, p3 = cords
    p2 = [p3[0], p1[1]]
    p4 = [p1[0], p3[1]]
    bb = [p1, p2, p3, p4]
    tp = Polygon(bb)

    final_dict['label'] = []
    for line in wc:
        for word in line:
            bb = word[0]
            centroid = Point(int((bb[0] + bb[2]) * 0.5), int((bb[1] + bb[5]) * 0.5))
            if tp.contains(centroid):
                if (list(set(word[1])) != ['.']) and (list(set(word[1])) != ['.', ' ']):
                    final_dict['label'].append((word[1], word[0]))
                else:
                    pass
            else:
                pass

    for label in final_dict:

        words = final_dict[label]
        label_final = []

        depths = list(map(lambda x: int((x[1][1] + x[1][5]) * 0.5), words))
        groups_formed = dict(enumerate(grouper(depths), 1))

        for group in groups_formed:
            sub_line = []
            for word in words:
                if int((word[1][1] + word[1][5]) * 0.5) in groups_formed[group]:
                    sub_line.append(word[0])
                else:
                    pass
            label_final.append(' '.join(sub_line))

        final_dict[label] = '\n'.join(label_final)

    return final_dict['label']


# def custom_fields_adapter(p1, p3, **labels):
#     custom_fields_new = dict()
#     if labels:
#         custom_fields_new[]


def update_meta(data, metadata):  ## FOR EACH SELECTION

    # data = {'label': 'default_label' , 'BoundingBox': [p1,p3] , 'Type' : 'Alpha'}
    if 'custom_fields' not in list(metadata.keys()):
        metadata['custom_fields'] = {}

    if len(metadata['custom_fields']) == 0:

        if data['label'] == 'default_label':
            custom_field = 'label1'
        else:
            custom_field = data['label']
    else:
        if data['label'] == 'default_label':
            default_labels = [x for x in list(metadata['custom_fields'].keys()) if 'label' in x]
            if len(default_labels) == 0:
                custom_field = 'label1'
            else:
                custom_field = 'label' + str(int(sorted(default_labels)[-1][-1]) + 1)
        else:
            custom_field = data['label']

    metadata['custom_fields'][custom_field] = {}

    for key in data:
        if key != 'label':
            metadata['custom_fields'][custom_field][key] = data[key]

    return metadata


def grouper(iterable):
    prev = None
    group = []
    for item in iterable:
        if not prev or item - prev <= 10:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group


def ui_flag_custom(mask, final_json, gen_image_path, analysis, metadata):
    uc_obj = ui_corrections(mask, final_json)
    final_json = uc_obj.default_all_words_flag_to_false(final_json)
    doc_accuracy, total_words = uc_obj.document_confidence(analysis)

    if 'custom_fields' in metadata.keys():
        custom_words, fj = uc_obj.flag_words_to_plot_custom(final_json, metadata)

        uc_obj.render_flagged_image(fj, uc_obj.mask, gen_image_path)

    else:
        print('No custom Field info found in metadata')
    return gen_image_path, doc_accuracy, total_words, custom_words
