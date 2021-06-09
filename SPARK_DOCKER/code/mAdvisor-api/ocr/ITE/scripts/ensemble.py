#import json
#import requests


############################### FINAL JSON

#with open('/home/user/ITE/ITE_APP_DEV/Intelligent-Text-Extraction/database/02 (1)_page_25_V_2_OA_page_1/final_json.json','r') as f:
#    final_json  = json.load(f)
#    
#cleaned = cleaned_final_json(final_json)

#########################  ADD AZURE CONF




from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from statistics import mean
from scipy.spatial import distance
def calculate_centroid( p1, p3):
    x_centroid = int((p1[0] + p3[0]) * 0.5)
    y_centroid = int((p1[1] + p3[1]) * 0.5)
    return (x_centroid, y_centroid)



#with open('/home/user/ITE/Backups/fj_conf.json','w+') as f:    
#    json.dump(final_json_new,f)


def add_azure_conf(final_json, analysis):  ## ADDS AZURE CONFIDENCE KEY
    wc = {}
    for i,line in enumerate(analysis["lines"]):
        wc[i+1] = [(word['boundingBox'],word['text'],word['confidence'],line['appearance']['style']) for word in line['words']]
    
    manual =False
    for line in wc:
        for word in wc[line]:
            updated = False
            bb = word[0]
            cord = calculate_centroid(bb[:2],bb[4:6])
            conf = word[2]
            style = word[3]
            
            if len(final_json['paragraphs'])>0 :
                updated,final_json = check_update_paras_conf(final_json, cord, conf, style)
            if not updated and len(final_json['tables'])>0:
                updated,final_json = check_update_tables_conf(final_json, cord, conf, style)
            
            if updated:
                print('update done')
                pass
            else:
                print('Update fault')
#                manual = True
    
#    if manual:
#        final_json = manual_fill_flags_az(final_json)
            
    return final_json
            


def check_update_paras_conf(final_json, cord, conf, style):
    for i in range(len(final_json['paragraphs'])):
        for j, line in enumerate(final_json['paragraphs']['p_'
                                                          + str(i + 1)]):
            # j th line
            for k, d in enumerate(final_json['paragraphs']['p_' +
                                                           str(i + 1)][j]):
                # k th word
                bb = d['boundingBox']['p1'] + d['boundingBox']['p3']
#                if (cord[0] in range(bb[0], bb[2])) and (cord[1] in range(bb[1], bb[3])):
                if cord[0] in range(min(bb[0],bb[2])\
                       , max(bb[0],bb[2])) and \
                       cord[1] in range(min(bb[1],bb[3]) , \
                           max(bb[1],bb[3])):
                    text = final_json['paragraphs']['p_' + str(i + 1)][j][k]['text'] 
                    final_json['paragraphs']['p_' + str(i + 1)][j][k]['az_text'] = text
                    final_json['paragraphs']['p_' + str(i + 1)][j][k]['azure_conf'] = conf
                    final_json['paragraphs']['p_' + str(i + 1)][j][k]['style'] = style
                    return True, final_json
                else:
                    pass

 

    return False, final_json

 

def check_update_tables_conf(final_json, cord, conf, style):
    
    update = True
    p = Point(cord)
    
    for i in range(len(final_json['tables'])):
        # CURRENTLY ONLY 4 SIDED TABLES 
        
        # str table number********* when saved
        p1, p3 = final_json['table_coordinates'][i + 1][:2],\
                    final_json['table_coordinates'][i + 1][2:]
        p2 = [p3[0], p1[1]]
        p4 = [p1[0], p3[1]]
        polygon_coordinates_list = [p1, p2, p3, p4]
        temp_polygon = Polygon(polygon_coordinates_list)

 

        if temp_polygon.contains(p):
            for cell in final_json['tables'][i + 1]:
                bb = final_json['tables'][i + 1][cell]['boundingBox']

 

                if cord[0] in range(bb['p1'][0], bb['p3'][0]) and cord[1] in range(bb['p1'][1], bb['p3'][1]):
                    words_bb = final_json['tables'][i + 1][cell]['words']

 

                    for j, bb in enumerate([el['boundingBox'] for el in words_bb]):
                        if cord[0] in range(min(bb['p1'][0],bb['p3'][0])\
                               , max(bb['p1'][0],bb['p3'][0])) and \
                               cord[1] in range(min(bb['p1'][1],bb['p3'][1]) , \
                                   max(bb['p1'][1],bb['p3'][1])):
                            text  = final_json['tables'][i + 1][cell]['words'][j]['text'] 
                            final_json['tables'][i + 1][cell]['words'][j]['az_text'] = text
                            final_json['tables'][i + 1][cell]['words'][j]['azure_conf'] = conf
                            final_json['tables'][i + 1][cell]['words'][j]['style'] = style
                            
                            update = True
#                            return True, final_json

 

                        else:
                            pass
                else:
                    pass
        else:
            pass
        
    if not update:
        return False, final_json
    else: 
        return True, final_json
    
    

def manual_fill_flags_az(final_json):

    if len(final_json['paragraphs'])>0 :
                
        for i in range(len(final_json['paragraphs'])):
            for j, line in enumerate(final_json['paragraphs']['p_'
                                                              + str(i + 1)]):
                # j th line
                for k, d in enumerate(final_json['paragraphs']['p_' +
                                                               str(i + 1)][j]):
                    # k th word
                    if 'azure_conf' not in list(d.keys()):
                        final_json['paragraphs']['p_' + str(i + 1)][j][k]['azure_conf'] = 0.0
                        final_json['paragraphs']['p_' + str(i + 1)][j][k]['style'] = 'NA'
                    else:
                        pass    
    
    if len(final_json['tables'])>0:
        for i in range(len(final_json['tables'])):
            for cell in final_json['tables'][i + 1]:
                words = final_json['tables'][i + 1][cell]['words']
    
                for j, word in enumerate(words):
                    if 'azure_conf' not in list(word.keys()):
                        final_json['tables'][i + 1][cell]['words'][j]['azure_conf'] = 0.0
                        final_json['tables'][i + 1][cell]['words'][j]['style'] = 'NA'
    
                    else:
                        pass
                        

    return final_json

    





###########   VISION  #####################################



def extract_polygons_from_response(response):  #90
   polygons = []
   for page in response["full_text_annotation"]["pages"]:
       for block in page["blocks"]:
           for paragraph in block["paragraphs"]:
               for word in paragraph["words"]:
                   word_text = ''.join([symbol["text"] for symbol in word["symbols"]])
                   try:
                       polygons.append(([
                           word["bounding_box"]["vertices"][0]["x"], word["bounding_box"]["vertices"][0]["y"],
                           word["bounding_box"]["vertices"][1]["x"], word["bounding_box"]["vertices"][1]["y"],
                           word["bounding_box"]["vertices"][2]["x"], word["bounding_box"]["vertices"][2]["y"],
                           word["bounding_box"]["vertices"][3]["x"], word["bounding_box"]["vertices"][3]["y"]],word_text,word["confidence"]))
                   except:
                        pass
   return polygons



def check_gv_word_in_azure(gv_info,azure_info):
    poly_coordinates = [tuple(azure_info["boundingBox"]["p1"]),
    (azure_info["boundingBox"]["p3"][0],azure_info["boundingBox"]["p1"][1]),
    tuple(azure_info["boundingBox"]["p3"]),
    (azure_info["boundingBox"]["p1"][0],azure_info["boundingBox"]["p3"][1])]
    point_coordinates = (int((gv_info[0]+gv_info[2])/2),
                         int((gv_info[1]+gv_info[5])/2))
    point = Point(point_coordinates)
    polygon = Polygon(poly_coordinates)
#    print(polygon.contains(point))
    return polygon.contains(point)


def check_gv_word_in_azure_intersection(gv_info,azure_info):
    poly_coordinates = [tuple(azure_info["boundingBox"]["p1"]),
    (azure_info["boundingBox"]["p3"][0],azure_info["boundingBox"]["p1"][1]),
    tuple(azure_info["boundingBox"]["p3"]),
    (azure_info["boundingBox"]["p1"][0],azure_info["boundingBox"]["p3"][1])]
    point_coordinates = [gv_info[i:i + 2] for i in range(0, len(gv_info), 2)] 
    point = Polygon(point_coordinates)
    polygon = Polygon(poly_coordinates)
#    print(polygon.contains(point))
    return polygon.intersects(point)

def add_gv_conf_text(text_json,data,analysis):
    
    gv_polygons_response = extract_polygons_from_response(text_json)

    if len(data['paragraphs'])>0 :
        for para in data["paragraphs"]:
        #    print(data["paragraphs"][para])
            for word in data["paragraphs"][para]:
                for ind_word in word:
#                    print(ind_word["text"])
                    words_to_combine = []
                    for gv_word in reversed(gv_polygons_response):
                        if check_gv_word_in_azure(gv_word[0],ind_word):
                            words_to_combine.append(gv_word)
                            gv_polygons_response.remove(gv_word)
                    words_to_combine.sort(key = lambda x:x[0][0])
                    if words_to_combine:
                        gv_text_to_update = " ".join([i[1] for i in words_to_combine])
                        gv_conf_to_update = mean([i[2] for i in words_to_combine])
                    else:
                        gv_text_to_update = ""
                        gv_conf_to_update = 0
                    ind_word.update({"gv_text":gv_text_to_update,"gv_conf":gv_conf_to_update})


    if len(data['tables'])>0:               
        for table in data["tables"]:
            for row in data["tables"][table]:
                for word in data["tables"][table][row]["words"]:
#                    print(word["text"])
                    words_to_combine = []
                    for gv_word in reversed(gv_polygons_response):
                        if check_gv_word_in_azure(gv_word[0],word):
                            words_to_combine.append(gv_word)
                            gv_polygons_response.remove(gv_word)
                    words_to_combine.sort(key = lambda x:x[0][0])
                    if words_to_combine:
                        gv_text_to_update = "".join([i[1] for i in words_to_combine])
                        gv_conf_to_update = mean([i[2] for i in words_to_combine])
                    else:
                        gv_text_to_update = ""
                        gv_conf_to_update = 0
                    word.update({"gv_text":gv_text_to_update,"gv_conf":gv_conf_to_update})
    
    filterd_gv_polygons = filter_gv_words(gv_polygons_response , analysis)
    data = add_gv_words(data,filterd_gv_polygons)
    
    return data

 

 

def check_vicinity(gv_bb,bb):

 

    point_coordinates = [gv_bb[i:i + 2] for i in range(0, len(gv_bb), 2)] 
    polygon_gv = Polygon(point_coordinates)

 

    p1 = bb[:2][0]-5 , bb[:2][1]-5
    p2 = bb[2:4][0]+5 , bb[2:4][1]-5
    p3 = bb[4:6][0]+5 , bb[4:6][1]+5
    p4 = bb[6:][0]-5 , bb[6:][1]+5
    
    poly_coordinates = [p1,p2,p3,p4]
    polygon_az = Polygon(poly_coordinates)
#    print(polygon.contains(point))
    return polygon_gv.intersects(polygon_az)

 

def filter_gv_words(gv_polygons_response , analysis):
    
    wc = {}
    for i,line in enumerate(analysis["lines"]):
        wc[i+1] = [(word['boundingBox'],word['text'],word['confidence'],line['appearance']['style']) for word in line['words']]
    
    filterd_gv_polygons = gv_polygons_response.copy()
    
    for gv_word in gv_polygons_response:
        
        for line in wc:
            for word in wc[line]:
                
                bb_az = word[0]
                bb_gv = gv_word[0]
                
                cen1 = calculate_centroid(bb_az[:2],bb_az[4:6])
                cen2 = calculate_centroid(bb_gv[:2],bb_gv[4:6])
                
                if distance.euclidean(cen1,cen2) <=100 :
                    if check_vicinity(bb_gv,bb_az):
                        print('removed')
                        
                        if gv_word in filterd_gv_polygons:
                            filterd_gv_polygons.remove(gv_word)
                    else:
                        pass
                else:
                    pass
    
    return filterd_gv_polygons

 

 

def add_gv_words(data,gv_polygons_response):

 

    if len(data['tables'])>0:
        for table in data["tables"]:
            for row in data["tables"][table]:
                for gv_word in reversed(gv_polygons_response):
                    if (check_gv_word_in_azure(gv_word[0],data["tables"][table][row])):
                        data["tables"][table][row]["words"].append({"gv_text":gv_word[1],"gv_conf":gv_word[2],
                                                                    "text":"","boundingBox":{"p1":gv_word[0][0:2],"p3":gv_word[0][4:6]},"azure_conf":0,
                                                                    "style":'NA'})
                        gv_polygons_response.remove(gv_word)
    
    
    #len(data["paragraphs"])
    if len(data['paragraphs'])>=0 :
        for gv_word in reversed(gv_polygons_response):
            para_info = [[{"gv_text":gv_word[1],
                             "boundingBox":{"p1":gv_word[0][0:2],"p3":gv_word[0][4:6]},
                             "gv_conf":gv_word[2],
                             "text":"",
                             "azure_conf":0,
                             "style":"NA"}]]
            data["paragraphs"].update({"p_"+str(len(data["paragraphs"])+1):para_info})
            gv_polygons_response.remove(gv_word)

 

    return data



#img_path = '/home/user/ITE/ITE_APP_DEV/02 (1)_page_25.png'
#final_json_az_gv = add_gv_conf_text(img_path,final_json_az)

###############  ENSEMBLE JSON




def ensemble_final_json(final_json):
    
    ensemble_json = final_json.copy()

    if 'paragraphs' in final_json.keys():
        for i in range(len(final_json['paragraphs'])):
            for j, line in enumerate(
                    final_json['paragraphs']['p_' + str(i + 1)]):

                for k, word in enumerate(line):
                    try:
                        if ((word['azure_conf'] > word['gv_conf']) and word['style'] != 'print') or (word["gv_text"] == ""):
                            pass
                        else:
                            text = final_json['paragraphs']['p_' + str(i + 1)][j][k]['gv_text']
                            ensemble_json['paragraphs']['p_' + str(i + 1)][j][k]['text'] = text
                    except Exception as e:
                        print(e)
                        print('## Exception in para: ','p_' + str(i + 1) )
                        pass
#                        print('## Exception in para: ','p_' + str(i + 1) )
#                        print('**',word , '\n')
                        
    else:
        pass

    if 'tables' in final_json.keys():
        for i in final_json['tables']:
#            print(i)
            for cell in final_json['tables'][i]:
            
                for j, word in enumerate(
                        final_json['tables'][i][cell]['words']):
                    try:
                        if ((word['azure_conf'] > word['gv_conf']) and word['style'] != 'print') or (word["gv_text"] == ""):
                            pass
                        else:
                            text = final_json['tables'][i][cell]['words'][j]['gv_text']
                            ensemble_json['tables'][i][cell]['words'][j]['text'] = text
                    
                    except Exception as e:
                        pass
#                        print(e)
#                        print('## Exception in table number: ', i)
#                        print('**',word , '\n')
                        
    else:
        pass

    return ensemble_json




def ensemble_main(final_json,analysis,text_resp):
    
    final_json_az = add_azure_conf(final_json,analysis)
    final_json_az_gv = add_gv_conf_text(text_resp,final_json_az,analysis)
    ens_json = ensemble_final_json(final_json_az_gv)
    
    return ens_json
