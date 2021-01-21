def parsing(news_data, imp_attributes):
    type_list, not_found_list = [], []
    for attr, data_type in imp_attributes.items():
        try:
            if type(news_data[attr]) not in ['', {}, None] + data_type:
                type_list.append(attr)
        except:
            not_found_list.append(attr)
    return type_list, not_found_list


class NewJsonParse(object):

    def __init__(self, news_json):
        self.data = news_json
        self.News_Attributes = {
            "stock": [str],
            "title": [str],
            "date": [str],
            "keywords": [list],
            "source": [str],
            "time": [str],
        }
        self.Sentiment_Attributes = {
            "document": [dict],
        }
        self.Keyword_Attributes = {
            "sentiment": [dict],
            "relevance": [float, int],
        }
        self.Keyword_Sentiment_Attributes = {
            "score": [float, int],
            "label": [str],
        }
        self.Document_Attributes = {
            "score": [float, int],
            "label": [str],
        }

    def senti_attr(self, sample_data, idx):
        senti_m = []
        type_list, not_found_list = parsing(sample_data, self.Sentiment_Attributes)
        if type_list + not_found_list != []:
            senti_m.append(idx)
            print("Sentiment_Attributes: record_number {0}".format(idx))
        else:
            type_list, not_found_list = parsing(sample_data['document'], self.Document_Attributes)
            if type_list + not_found_list != []:
                senti_m.append(idx)
                print("Sentiment_document_Attributes:{0} type_list:{1} not_found_list{2}".format(idx, type_list,
                                                                                                 not_found_list))
        return senti_m

    def key_attr(self, sample_data, idx):
        key_att_m = []
        for idx_keyw in range(len(sample_data)):
            type_list, not_found_list = parsing(sample_data[idx_keyw], self.Keyword_Attributes)
            if type_list + not_found_list != []:
                key_att_m.append(idx)
                print("Keyword_Attributes: type_list:{0} not_found_list{1}".format(type_list, not_found_list))
            else:
                type_list, not_found_list = parsing(sample_data[idx_keyw]['sentiment'],
                                                         self.Keyword_Sentiment_Attributes)
                if type_list + not_found_list != []:
                    key_att_m.append(idx_keyw)
                    print("Keyword_Sentiment_Attributes:{0} type_list:{1} not_found_list{2}".format(idx_keyw, type_list,
                                                                                                    not_found_list))
        return key_att_m

    def remove_attributes(self):
        print("length of news json BEFORE :{0}".format(len(self.data)))
        index = []
        for idx in range(len(self.data)):
            type_list, not_found_list = parsing(self.data[idx], self.News_Attributes)
            if type_list + not_found_list != []:
                index.append(idx)
                print("News_Attributes: Record number {0}".format(idx))
            else:
                senti_index = self.senti_attr(self.data[idx]["sentiment"], idx)
                if not senti_index:
                    key_att_index = self.key_attr(self.data[idx]['keywords'], idx)
                    if key_att_index:
                        index = index + [idx]

                #             if len(key_att_index)==len(self.data[idx]['keywords']):
                #                 index = index+[idx]
                #             else:
                #                 print(len(key_att_index,'B')
                else:
                    # print("senti_index", senti_index)
                    index = index + senti_index
        index = list(set(index))
        # print("index {0}".format(index))
        self.data = [i for j, i in enumerate(self.data) if j not in index]
        print("length of news json AFTER :{0}".format(len(self.data)))
        return self.data