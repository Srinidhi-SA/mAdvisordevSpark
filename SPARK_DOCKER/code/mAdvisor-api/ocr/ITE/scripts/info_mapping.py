import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Final_json:

    def __init__(self, final_json, history_json=None):
        self.json = final_json
        self.table_count = len(self.json['tables'])
        self.para_count = len(self.json['paragraphs'])
        self.history_json = history_json
        if history_json is None:
            self.present_update_key = 'U1'
        else:
            self.present_update_key = 'U' + str(len(self.history_json.keys()) + 1)
        self.history_json[self.present_update_key] = []

    def update_u1(self, upd):
        self.history_json = upd
        return self.history_json

    """
    def update_final_json(self, cord, inp):

        if len(self.json['tables']) > 0 and len(self.json['paragraphs']) > 0:
            if self.check_update_tables(self.json, cord, inp):
                print('Updated In table')
            elif self.check_update_paras(self.json, cord, inp):
                print('Updated In Paraaaaa')
            else:
                print("Couldn't Update")

        elif len(self.json['tables']) > 0:
            if self.check_update_tables(self.json, cord, inp):
                print('Updated In table')
            else:
                print("Couldn't Update")

        else:
            if self.check_update_paras(self.json, cord, inp):
                print('Updated In Paraaaaa')
            else:
                print("Couldn't Update")
        return self.json, self.history_json
    """

    def update_final_json(self, cord, inp):

        final_json = self.json
        if len(final_json['tables']) > 0 and len(final_json['paragraphs']) > 0:
            status, final_json = self.check_update_tables(final_json, cord, inp)
            if status:
                print('Updated In table')
            elif not status:
                status, final_json = self.check_update_paras(final_json, cord, inp)
                if status:
                    print('Updated In Paraaaaa')
                else:
                    print("Couldn't Update")
            else:
                pass


        elif len(final_json['tables']) > 0:
            status, final_json = self.check_update_tables(final_json, cord, inp)
            if status:
                print('Updated In table')
            else:
                print("Couldn't Update")

        else:
            status, final_json = self.check_update_paras(final_json, cord, inp)
            if status:
                print('Updated In Paraaaaa')
            else:
                print("Couldn't Update")
        return final_json, self.history_json

    """
    def check_update_paras(self, final_json, cord, inp):
        p = Point(cord)
        for i in range(len(final_json['paragraphs'])):
            for j, line in enumerate(final_json['paragraphs']['p_' + str(i + 1)]):
                polygon_coordinates_list = line['boundingBox'][:2], line['boundingBox'][2:4], line['boundingBox'][4:6], \
                                           line['boundingBox'][6:]
                temp_polygon = Polygon(polygon_coordinates_list)

                if temp_polygon.contains(p):
                    for k, d in enumerate(final_json['paragraphs']['p_' + str(i + 1)][j]['words']):
                        print(d)
                        bb = list(d.values())[0]
                        # print(list(d.values())[1])
                        if cord[0] in range(bb['p1'][0], bb['p3'][0]) and cord[1] in range(bb['p1'][1], bb['p3'][1]):
                            #                            old_key = list(d.keys())[0]
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k] = {}
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k][inp] = bb
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k]['flag'] = False
                            self.update_history(inp, bb)
                            return True
                        else:
                            pass
                else:
                    pass

        return False
        """

    """def check_update_paras(self, final_json, cord, inp):
        for i in range(len(final_json['paragraphs'])):
            for j, line in enumerate(final_json['paragraphs']['p_' + str(i + 1)]):
                for k, d in enumerate(final_json['paragraphs']['p_' + str(i + 1)][j]['words']):
                    bb = list(d.values())
                    for item in bb:
                        if isinstance(item, list):
                            bb = item
                    if (cord[0] in range(bb[0], bb[2])) and (cord[1] in range(bb[1], bb[5])):
                        print("ijk:", i, j, k)
                        print("before update:", final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k]['text'])
                        final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k]['text'] = inp
                        print("after update:", final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k]['text'])
                        # self.update_history(history_json,inp,bb)
                        return True, final_json
                    else:
                        pass

        return False, final_json"""

    def check_update_paras(self, final_json, cord, inp):
        for i in range(len(final_json['paragraphs'])):
            for j, line in enumerate(final_json['paragraphs']['p_' + str(i + 1)]):  ## j th line
                for k, d in enumerate(final_json['paragraphs']['p_' + str(i + 1)][j]):  ## k th word

                    bb = d['boundingBox']['p1'] + d['boundingBox']['p3']
                    if (cord[0] in range(bb[0], bb[2])) and (cord[1] in range(bb[1], bb[3])):
                        final_json['paragraphs']['p_' + str(i + 1)][j][k]['text'] = inp
                        return True, final_json
                    else:
                        pass

        return False, final_json

    """
    def check_update_paras(self, final_json, cord, inp):
        p = Point(cord)
        for i in range(len(final_json['paragraphs'])):
            for j, line in enumerate(final_json['paragraphs']['p_' + str(i + 1)]):  ## p_i contains a list of lines
                polygon_coordinates_list = line['boundingBox'][:2], line['boundingBox'][2:4], line['boundingBox'][4:6], \
                                           line['boundingBox'][6:]
                temp_polygon = Polygon(polygon_coordinates_list)

                if temp_polygon.contains(p):
                    for k, d in enumerate(
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words']):  ## d  is each word dict
                        # bb = list(d.values())[0]
                        # print(list(d.values())[1])
                        bb = d['boundingBox']

                        if cord[0] in range(bb[0], bb[4]) and cord[1] in range(bb[1], bb[5]):
                            old_key = list(d.keys())[0]
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k] = {}
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k][inp] = bb
                            final_json['paragraphs']['p_' + str(i + 1)][j]['words'][k]['flag'] = False
                            # self.update_history(inp, bb)
                            return True
                        else:
                            pass
                else:
                    pass

        return False
    """

    """def check_update_tables(self, final_json, cord, inp):
        p = Point(cord)
        for i in range(len(final_json['tables'])):  ## CURRENTLY ONLY 4 SIDED TABLES
            p1, p3 = final_json['table_coordinates'][str(i + 1)][:2], final_json['table_coordinates'][str(i + 1)][2:]
            p2 = [p3[0], p1[1]]
            p4 = [p1[0], p3[1]]
            polygon_coordinates_list = [p1, p2, p3, p4]
            temp_polygon = Polygon(polygon_coordinates_list)

            if temp_polygon.contains(p):
                for cell in final_json['tables'][str(i + 1)]:
                    bb = final_json['tables'][str(i + 1)][cell]['boundingBox']

                    if cord[0] in range(bb['p1'][0], bb['p3'][0]) and cord[1] in range(bb['p1'][1], bb['p3'][1]):
                        words_bb = final_json['tables'][str(i + 1)][cell]['words']

                        for j, bb in enumerate([el['boundingBox'] for el in words_bb]):
                            if cord[0] in range(bb['p1'][0], bb['p3'][0]) and cord[1] in range(bb['p1'][1],
                                                                                               bb['p3'][1]):

                                final_json['tables'][str(i + 1)][cell]['words'][j]['text'] = inp
                                final_json['tables'][str(i + 1)][cell]['words'][j]['flag'] = False
                                self.update_history(inp, bb)
                                return True

                            else:
                                pass
                    else:
                        pass
            else:
                pass

        return False"""

    def check_update_tables(self, final_json, cord, inp):
        p = Point(cord)
        for i in range(len(final_json['tables'])):  ## CURRENTLY ONLY 4 SIDED TABLES
            p1, p3 = final_json['table_coordinates'][str(i + 1)][:2], final_json['table_coordinates'][str(i + 1)][
                                                                      2:]
            p2 = [p3[0], p1[1]]
            p4 = [p1[0], p3[1]]
            polygon_coordinates_list = [p1, p2, p3, p4]
            temp_polygon = Polygon(polygon_coordinates_list)

            if temp_polygon.contains(p):
                for cell in final_json['tables'][str(i + 1)]:
                    bb = final_json['tables'][str(i + 1)][cell]['boundingBox']

                    if cord[0] in range(bb['p1'][0], bb['p3'][0]) and cord[1] in range(bb['p1'][1], bb['p3'][1]):
                        words_bb = final_json['tables'][str(i + 1)][cell]['words']

                        for j, bb in enumerate([el['boundingBox'] for el in words_bb]):
                            if cord[0] in range(bb['p1'][0], bb['p3'][0]) and cord[1] in range(bb['p1'][1],
                                                                                               bb['p3'][1]):

                                final_json['tables'][str(i + 1)][cell]['words'][j]['text'] = inp
                                print("ij", i, j)
                                # self.update_history(history_json,inp,bb)
                                return True, final_json

                            else:
                                pass
                    else:
                        pass
            else:
                pass

        return False, final_json

    def update_history(self, updated_word, bounding_box):
        self.history_json[self.present_update_key].append({updated_word: [bounding_box['p1'], bounding_box['p3']]})

    def write_back(self, image_name, final_json_updated, history_json_updated):  # SUBMIT BOTTON

        with open('./database/' + image_name + '/final_json.json', 'w') as fj:
            json.dump(final_json_updated, fj)
            fj.close()

        with open('./database/' + image_name + '/update_history.json', 'w')  as hj:
            json.dump(history_json_updated, hj)
            hj.close()


def update_u1(upd, image_name):  ##initial comparision is captured
    ##todo
    #    try:
    #        with open('./database/'+image_name+'/update_history.json','r') as his:
    #            hist = json.load(his)
    #            his.close()
    #    except:
    #        print("Couldn't find any update history on this Image")
    hist = upd
    with open('./database/' + image_name + '/update_history.json', 'w') as his:
        json.dump(hist, his)
        his.close()
