from builtins import object
import simplejson as json
from rest_framework.utils import humanize_datetime
from django.conf import settings


def convert_to_string(data):

    keys = ['meta_data', 'datasource_details']

    for key in keys:
        if key in data:
            value = data[key]
            if isinstance(value, str):
                pass
            elif isinstance(value, dict):
                data[key] = json.dumps(value)

    return data


def convert_to_json(data):
    keys = ['meta_data', 'datasource_details', 'preview']

    for key in keys:
        if key in data:
            value = data[key]
            data[key] = json.loads(value)
    return data


def convert_time_to_human(data):

    keys = ['created_on', 'updated_on']

    for key in keys:
        if key in data:
            value = data[key]
            data[key] = humanize_datetime.humanize_strptime(value)
    return data


def convert_metadata_according_to_transformation_setting(meta_data=None, transformation_setting=None, user=None):

    if meta_data is not None:
        uiMetaData = meta_data
        #uiMetaData=get_metaData_after_checking_ignoreSuggestionFlag(meta_data=meta_data)
    else:
        return {}

    ts = transformation_setting
    metaData = uiMetaData.get("metaDataUI")
    sampleData = uiMetaData.get("sampleDataUI")
    headers = uiMetaData.get("headersUI")
    columnData = uiMetaData.get("columnDataUI")

    read_and_change_metadata(
        ts=ts,
        metaData=metaData,
        headers=headers,
        columnData=columnData,
        sampleData=sampleData,
        user=user
    )
    uiMetaData['transformation_settings'] = transformation_setting
    uiMetaData['modified'] = True

    varibaleSelectionArray = add_variable_selection_to_metadata(
        uiMetaData["columnDataUI"],
        uiMetaData['transformation_settings']
    )
    uiMetaData.update({"varibaleSelectionArray": varibaleSelectionArray})
    return uiMetaData

def get_metaData_after_checking_ignoreSuggestionFlag(meta_data):
    temp_columnDataUI=meta_data['meta_data']['uiMetaData']['columnDataUI']
    temp_varibaleSelectionArray=meta_data['meta_data']['uiMetaData']['varibaleSelectionArray']
    for iter in temp_columnDataUI:
        if(iter['ignoreSuggestionFlag']==True):
            for i in temp_varibaleSelectionArray:
                if(iter['slug']==i['slug']):
                    i['selected']=False

def read_and_change_metadata(ts, metaData, headers, columnData, sampleData, user=None):

    mdc = MetaDataChange(
        metaData=metaData,
        headers=headers,
        ts=ts,
        columnData=columnData,
        sampleData=sampleData,
        user=user
    )

    ts = ts.get('existingColumns')

    for col in ts:
        columnSetting_Temp = None
        uid_flag = False
        if "columnSetting" in col:
            columnSetting = col.get("columnSetting")

            for colset in columnSetting:
                # colset.get("status")=> get status of the actionitems
                if colset.get("status") == True:

                    if colset.get('actionName') == 'unique_identifier':
                        uid_flag = True

                    if colset.get("actionName") == "delete":

                        if 'modified' in colset:
                            if colset.get('modified') == True:
                                pass
                            else:
                                colset['modified'] = True
                                mdc.changes_on_delete(col.get("name"), type='delete')
                        else:
                            colset['modified'] = True
                            mdc.changes_on_delete(col.get("name"), type='delete')

                        colset['displayName'] = 'UnDelete Column'

                    if colset.get("actionName") == "rename":
                        colName = col.get('name')
                        newName = colset.get('newName')
                        col['name'] = newName
                        if 'modified' in colset:
                            if colset.get('modified') == True:
                                colset['prevName'] = newName
                        else:
                            colset['modified'] = True
                            colset['prevName'] = colName
                        mdc.changes_on_rename(
                            colName=colName,
                            newName=newName
                        )

                    if colset.get("actionName") == "data_type":
                        listOfActions = colset.get('listOfActions')
                        data_type = {}
                        for data in listOfActions:
                            if data.get('status') == True:
                                mdc.changes_on_data_type(
                                    colName=col.get('name'),
                                    type=data.get('name')
                                )

                    if colset.get('actionName') == 'replace':
                        colName = col.get('name')
                        replacementValues = colset.get('replacementValues')
                        mdc.replace_values(
                            colName=colName,
                            replace_match_array=replacementValues
                        )

                    if colset.get('actionName') == 'ignore_suggestion':
                        colName = col.get('name')
                        colset['displayName'] = 'Consider for Analysis'
                        mdc.changes_on_consider_column(colName, False)
                        if colset['previous_status'] != colset["status"]:
                            columnSetting_Temp = mdc.changes_in_column_data_if_column_is_ignore(colName)
                            colset['previous_status'] = colset["status"]
                            break
                # colset.get("status")=> get status of the actionitems
                elif colset.get("status") == False:

                    if colset.get("actionName") == "delete":

                        if 'modified' in colset:
                            if colset.get('modified') == True:
                                mdc.changes_on_delete(col.get("name"), type='undelete')
                                colset['modified'] = False
                        colset['displayName'] = 'Delete Column'

                    if colset.get('actionName') == 'ignore_suggestion':
                        colName = col.get('name')
                        colset['displayName'] = 'Ignore for Analysis'
                        mdc.changes_on_consider_column(colName, True)
                        if colset['previous_status'] != colset["status"]:
                            columnSetting_Temp = mdc.changes_in_column_data_if_column_is_considered(
                                                        colName,
                                                        uid_flag=uid_flag
                                                    )
                            colset['previous_status'] = colset["status"]
                            break

        if columnSetting_Temp is not None:
            col['columnSetting'] = columnSetting_Temp

    return metaData, headers


class MetaDataChange(object):

    def __init__(self, **kwargs):

        self.metaData = kwargs.get("metaData")
        self.headers = kwargs.get("headers")
        self.ts = kwargs.get("ts")
        self.columnData = kwargs.get("columnData")
        self.sampleData = kwargs.get("sampleData")
        self.user = kwargs.get('user')

    def changes_on_delete(self, colName=None, type='delete'):
        """
        metaData - *
        :return:
        """

        if colName is None:
            return

        self.change_col_from_noOfColumns(colName, type=type)
        self.changes_from_measure_or_dimension_or_timeDimension_also_count(colName, type=type)

    def change_col_from_noOfColumns(self, colName=None, type=None):

        for data in self.metaData:
            if data.get("name") == "noOfColumns":
                if type == 'delete':
                    data['value'] = data['value'] - 1
                elif type == 'undelete':
                    data['value'] = data['value'] + 1
                break

    def changes_from_measure_or_dimension_or_timeDimension_also_count(self, colName=None, type=None):
        indexes = {
            "measures": None,
            "dimensions": None,
            "timeDimension": None,
            "measureColumns": None,
            "dimensionColumns": None,
            "timeDimensionColumns": None

        }

        match_for_name = {
            "measure": 'measures',
            "dimension": 'dimensions',
            "timeDimension": 'timeDimension',
            "datetime":'timeDimension',
        }

        match_for_column = {
            "measures": 'measureColumns',
            "dimensions": 'dimensionColumns',
            "timeDimension": 'timeDimensionColumns',
            "measure": 'measureColumns',
            "dimension": 'dimensionColumns',
            "datetime":'timeDimensionColumns',
        }

        for i, data in enumerate(self.metaData):
            if data['name'] in indexes:
                indexes[data["name"]] = i

        measures_array = self.metaData[indexes["measureColumns"]].get("value")
        dimensions_array = self.metaData[indexes["dimensionColumns"]].get("value")
        time_dimensions_array = self.metaData[indexes["timeDimensionColumns"]].get("value")

        type_of_col = None
        if type == "undelete":
            for data in self.columnData:
                if data.get('name') == colName:
                    type_of_col = data.get('columnType')
                    break

        if type_of_col is not None:
            self.metaData[indexes[match_for_name[type_of_col]]]["value"] = self.metaData[indexes[match_for_name[type_of_col]]]["value"] + 1
            self.metaData[indexes[match_for_column[type_of_col]]]["value"].append(colName)
            return ""

        if colName in measures_array:
            if type == 'delete':
                measures_array.remove(colName)
                self.metaData[indexes["measures"]]["value"] = self.metaData[indexes["measures"]]["value"] - 1
        elif colName in dimensions_array:
            if type == 'delete':
                dimensions_array.remove(colName)
                self.metaData[indexes["dimensions"]]["value"] = self.metaData[indexes["dimensions"]]["value"] - 1
        elif colName in time_dimensions_array:
            if type == 'delete':
                time_dimensions_array.remove(colName)
                self.metaData[indexes["timeDimension"]]["value"] = self.metaData[indexes["timeDimension"]]["value"] - 1


    def changes_on_rename(self, colName=None, newName=None, type='name'):
        """
        metaData - *
        headers - *
        :return:
        """
        if colName is None:
            raise Exception("no col name>changes_on_rename")

        if newName is None:
            raise Exception("no new name>changes_on_rename")

        self.rename_in_measure_or_dimension_or_timeDimension(colName, newName)
        self.rename_in_headers(colName, newName)

    def rename_in_measure_or_dimension_or_timeDimension(self, colName=None, newName=None):
        if colName is None :
            raise Exception("no col name > rename_in_measure_or_dimension_or_timeDimension")

        if newName is None:
            raise Exception("no new name > rename_in_measure_or_dimension_or_timeDimension")

        indexes = {
            "measures": None,
            "dimensions": None,
            "timeDimension": None,
            "measureColumns": None,
            "dimensionColumns": None,
            "timeDimensionColumns": None
        }

        for i, data in enumerate(self.metaData):
            if data['name'] in indexes:
                indexes[data["name"]] = i

        measures_array = self.metaData[indexes["measureColumns"]].get("value")
        dimensions_array = self.metaData[indexes["dimensionColumns"]].get("value")
        time_dimensions_array = self.metaData[indexes["timeDimensionColumns"]].get("value")

        if colName in measures_array:
            for i, value in enumerate(measures_array):
                if value == colName:
                    measures_array[i] = newName
        elif colName in dimensions_array:
            for i, value in enumerate(dimensions_array):
                if value == colName:
                    dimensions_array[i] = newName
        elif colName in time_dimensions_array:
            for i, value in enumerate(time_dimensions_array):
                if value == colName:
                    time_dimensions_array[i] = newName

    def rename_in_headers(self, colName=None, newName=None):

        if colName is None or newName is None:
            raise Exception("no name")

        for head in self.columnData:

            if head.get('name') == colName:
                head['name'] = newName
                break

    def changes_on_data_type(self, colName=None, type=None):
        """
        metaData - *
        columnsData - *
        :return:
        """
        if colName is None or type is None:
            raise Exception("No colName or Type")

        match_in_columnstats = {
            'numeric': 'measure',
            'text': 'dimension'
        }

        for data in self.columnData:
            if data.get('name') == colName:
                if data['columnType'] == match_in_columnstats[type]:
                    return ""
                data['columnType'] = match_in_columnstats[type]
        if type == 'numeric':
            for data in self.metaData:
                if data.get('name') == 'measures':
                    data['value'] = data['value'] + 1
                if data.get('name') == 'measureColumns':
                    data['value'].append(colName)
                if data.get('name') == 'dimensions':
                    data['value'] = data['value'] - 1
                if data.get('name') == 'dimensionColumns':
                    if colName in data['value']:
                        data['value'].remove(colName)
        elif type == 'text':
            for data in self.metaData:
                if data.get('name') == 'measures':
                    data['value'] = data['value'] - 1
                if data.get('name') == 'measureColumns':
                    if colName in data['value']:
                        data['value'].remove(colName)
                if data.get('name') == 'dimensions':
                    data['value'] = data['value'] + 1
                if data.get('name') == 'dimensionColumns':
                    data['value'].append(colName)

    def replace_values(self, colName=None, replace_match_array=None):
        if replace_match_array is None:
            raise Exception('Nothing to replace. >> replace_values')
        if colName is None:
            raise Exception('No colname. >> replace_values')

        index = None
        for i, head in enumerate(self.headers):
            if head.get('name') == colName:
                index = i
                break

        for data in self.sampleData:
            for r in replace_match_array:
                replaceType = r.get('replaceType')
                if replaceType == "contains":
                    data[index] = data[index].replace(r['valueToReplace'], r['replacedValue'])
                elif replaceType == "startsWith":
                    if data[index].startswith(r['valueToReplace']):
                        data[index] = r['replacedValue']+data[index][len(r['valueToReplace']):]
                elif replaceType == "endsWith":
                    if data[index].endswith(r['valueToReplace']):
                        data[index] = data[index][:-len(r['valueToReplace'])]+r['replacedValue']
                elif replaceType == "equals":
                    if data[index] == r['valueToReplace']:
                        data[index] = data[index].replace(r['valueToReplace'], r['replacedValue'])
                elif replaceType == "":
                    pass

    def changes_on_consider_column(self, colName=None, make_it=None):
        for data in self.columnData:
            if data.get('name') == colName:
                data['consider'] = make_it
                # data['ignoreSuggestionFlag'] = not make_it
                break

    def changes_in_column_data_if_column_is_considered(self, colName, uid_flag=False):
        import copy
        from django.conf import settings

        signal_permission = self.user.has_perm('api.create_signal')

        for head in self.columnData:
            if head.get('name') == colName:
                transformation_settings = settings.TRANSFORMATION_SETTINGS_CONSTANT

                columnSettingCopy = copy.deepcopy(transformation_settings.get('columnSetting'))
                columnType = head.get('columnType')
                head_columnSetting = []

                if "dimension" == columnType:
                    if signal_permission is False:
                        head_columnSetting = columnSettingCopy[:1]
                    else:
                        head_columnSetting = columnSettingCopy[:4]
                elif "boolean" == columnType:
                    if signal_permission is False:
                        head_columnSetting = columnSettingCopy[:1]
                    else:
                        head_columnSetting = columnSettingCopy[:4]
                elif "measure" == columnType:
                    if signal_permission is False:
                        columnSettingTemp = columnSettingCopy[0:1] + columnSettingCopy[5:]
                        columnSettingTemp[1]['listOfActions'][0]["status"] = True
                        columnSettingTemp[2]['listOfActions'][0]["status"] = True
                        head_columnSetting = columnSettingTemp
                    else:
                        datatype_element = columnSettingCopy[4]
                        datatype_element['listOfActions'][0]["status"] = True
                        columnSettingCopy[5]['listOfActions'][0]["status"] = True
                        columnSettingCopy[6]['listOfActions'][0]["status"] = True

                        replace_element = columnSettingCopy[3]
                        replace_element['replaceTypeList'] = replace_element['replaceTypeList'][:1]
                        head_columnSetting = columnSettingCopy

                elif "datetime" == columnType:
                    if signal_permission is False:
                        head_columnSetting = columnSettingCopy[:1]
                    else:
                        head_columnSetting = columnSettingCopy[:3]

                transformation_settings_ignore = copy.deepcopy(settings.TRANSFORMATION_SETTINGS_IGNORE)
                transformation_settings_ignore['status'] = False
                transformation_settings_ignore['displayName'] = 'Ignore for Analysis'
                transformation_settings_ignore['previous_status'] = False

                if uid_flag is True:
                    for head_column in head_columnSetting:
                        if head_column.get('actionName') == 'unique_identifier':
                            head_column['status'] = True
                            break

                head_columnSetting.append(transformation_settings_ignore)
                head['consider'] = True

                return head_columnSetting

    def changes_in_column_data_if_column_is_ignore(self, colName):
        import copy
        from django.conf import settings
        signal_permission = self.user.has_perm('api.create_signal')
        for head in self.columnData:
            if head.get('name') == colName:
                transformation_settings = settings.TRANSFORMATION_SETTINGS_CONSTANT
                columnSettingCopy = copy.deepcopy(transformation_settings.get('columnSetting'))

                if signal_permission is False:
                    head_columnSetting = []
                else:
                    head_columnSetting = columnSettingCopy[1:3]

                transformation_settings_ignore = copy.deepcopy(settings.TRANSFORMATION_SETTINGS_IGNORE)
                transformation_settings_ignore['status'] = True
                transformation_settings_ignore['previous_status'] = True
                transformation_settings_ignore['displayName'] = 'Consider for Analysis'
                head_columnSetting.append(transformation_settings_ignore)
                head['consider'] = False
                return head_columnSetting

def add_possible_analysis_to_ui_metadata(meta_data):
    return settings.ANALYSIS_FOR_TARGET_VARIABLE


def add_metaData_to_ui_metadata(meta_data):
    # metaDataUI = []
    # if "metaData" in meta_data:
    #     metaKeysUI = ["noOfRows", "noOfColumns", "measures", "dimensions", "timeDimension",
    #                   "measureColumns", "dimensionColumns"]
    #     metaDataUI = [x for x in meta_data["metaData"] if x["name"] in metaKeysUI]
    if "metaData" in meta_data:
        return meta_data['metaData']
    return []

def collect_slug_for_percentage_columns(meta_data):
    metaData = meta_data['metaData']
    name_list = []
    slug_list = []
    for data in metaData:
        if 'percentageColumns' == data['name']:
            name_list = data['value']

    columnData = meta_data['columnData']
    for name in name_list:
        for data in columnData:
            if name == data['name']:
                slug_list.append(data['slug'])

    return slug_list


def get_advanced_setting(varibaleSelectionArray):

    things_to_add = dict()

    time_count = 0
    add_trend = False
    add_overview = True
    add_association = False
    add_prediction = False
    add_performance = False
    add_influencer = False
    target_column_name = None
    target_data_type = None
    dimension_count = 0
    dimension_list = []
    measure_count = 0
    measure_list = []
    datetime_count = 0
    datetime_list = []

    for data in varibaleSelectionArray:
        if data['dateSuggestionFlag'] is True or data['columnType'] == 'datetime':
            time_count += 1
        if data['targetColumn'] == True:
            target_column_name = data['name']
            target_data_type = data['columnType']

        if data['columnType'] == 'dimension':
            dimension_count += 1
            dimension_list.append(data['name'])

        if data['columnType'] == 'measure':
            measure_count += 1
            measure_list.append(data['name'])

        if data['columnType'] == 'datetime':
            datetime_count += 1
            datetime_list.append(data['name'])

    if time_count > 0:
        add_trend = True

    measure_count_without_target = measure_count
    dimension_count_without_target = dimension_count
    if target_data_type == 'measure':
        measure_count_without_target = measure_count - 1
    elif target_data_type == 'dimension':
        dimension_count_without_target = dimension_count - 1

    if measure_count_without_target + dimension_count_without_target >= 1:
        add_association = True
        add_prediction = True

    if measure_count_without_target > 0:
        add_influencer = True

    if dimension_count_without_target > 0:
        add_performance = True

    things_to_add = {
        'overview': add_overview,
        'trend': add_trend,
        'association': add_association,
        'performance': add_performance,
        'influencer': add_influencer,
        'prediction': add_prediction,
    }

    return add_trend_in_advanced_setting(things_to_add)


def add_trend_in_advanced_setting(things_to_add):
    import copy
    from django.conf import settings

    if things_to_add == dict():
        main_setting = copy.deepcopy(settings.ADVANCED_SETTINGS_FOR_POSSIBLE_ANALYSIS_WITHOUT_TREND)
        return main_setting
    trend_setting = copy.deepcopy(settings.ADANCED_SETTING_FOR_POSSIBLE_ANALYSIS_TREND)

    overview = copy.deepcopy(settings.ADVANCED_SETTINGS_OVERVIEW)
    association = copy.deepcopy(settings.ADVANCED_SETTINGS_ASSOCIATION)
    performance= copy.deepcopy(settings.ADVANCED_SETTINGS_PERFORMANCE)
    prediction= copy.deepcopy(settings.ADVANCED_SETTINGS_PREDICTION)
    influencer= copy.deepcopy(settings.ADVANCED_SETTINGS_INFLUENCER)
    trend= copy.deepcopy(settings.ADANCED_SETTING_FOR_POSSIBLE_ANALYSIS_TREND)
    # target_level= copy.deepcopy(settings.ADVANCED_SETTINGS_TARGET_LEVEL)
    # target_settings= copy.deepcopy(settings.ADVANCED_SETTINGS_TARGET_SETTINGS)

    match_ing = {
        'overview': overview,
        'association': association,
        'performance': performance,
        'prediction': prediction,
        'influencer': influencer,
        'trend': trend
    }

    measure_checklist = copy.deepcopy(settings.ADVANCED_SETTINGS_FOR_POSSIBLE_MEASURE_ANALYSIS_CHECK_LIST)
    dimension_checklist = copy.deepcopy(settings.ADVANCED_SETTINGS_FOR_POSSIBLE_DIMENSION_ANALYSIS_CHECK_LIST)

    raw_final_setting = copy.deepcopy(settings.ADVANCED_SETTINGS_FOR_POSSIBLE_ANALYSIS)

    for key in measure_checklist:
        if things_to_add[key]:
            raw_final_setting['measures']['analysis'].append(match_ing[key])

    for key in dimension_checklist:
        if things_to_add[key]:
            raw_final_setting['dimensions']['analysis'].append(match_ing[key])

    return raw_final_setting
    # if add_trend is True:
    #
    #     main_setting["dimensions"]["analysis"].insert(1, trend_setting)
    #     main_setting["measures"]["analysis"].insert(1, trend_setting)
    #     return main_setting
    # else:
    #     return settings.ADVANCED_SETTINGS_FOR_POSSIBLE_ANALYSIS_WITHOUT_TREND


def add_transformation_setting_to_ui_metadata(meta_data, permissions_dict=None):
    transformation_final_obj = {"existingColumns": None, "newColumns": None}
    transformation_data = []
    create_signal_permission = permissions_dict['create_signal']
    subsetting_dataset_permission = permissions_dict['subsetting_dataset']
    if 'columnData' in meta_data:
        columnData = meta_data['columnData']
        transformation_settings = settings.TRANSFORMATION_SETTINGS_CONSTANT

        percentage_slug_list = collect_slug_for_percentage_columns(meta_data)

        for head in columnData:
            import copy
            temp = dict()
            temp['name'] = head.get('name')
            temp['slug'] = head.get('slug')
            columnSettingCopy = copy.deepcopy(transformation_settings.get('columnSetting'))
            columnType = head.get('columnType')

            if "dimension" == columnType:
                if subsetting_dataset_permission is False:
                    temp['columnSetting'] = columnSettingCopy[:1]
                else:
                    temp['columnSetting'] = columnSettingCopy[:4]
            elif "boolean" == columnType:
                if subsetting_dataset_permission is False:
                    temp['columnSetting'] = columnSettingCopy[:1]
                else:
                    temp['columnSetting'] = columnSettingCopy[:4]
            elif "measure" == columnType:
                if subsetting_dataset_permission is False:
                    columnSettingTemp = columnSettingCopy[0:1] + columnSettingCopy[5:]
                    columnSettingTemp[1]['listOfActions'][0]["status"] = True
                    columnSettingTemp[2]['listOfActions'][0]["status"] = True
                    temp['columnSetting'] = columnSettingTemp
                else:
                    datatype_element = columnSettingCopy[4]
                    datatype_element['listOfActions'][0]["status"] = True
                    columnSettingCopy[5]['listOfActions'][0]["status"] = True
                    columnSettingCopy[6]['listOfActions'][0]["status"] = True

                    replace_element = columnSettingCopy[3]
                    replace_element['replaceTypeList'] = replace_element['replaceTypeList'][:1]
                    temp['columnSetting'] = columnSettingCopy

            elif "datetime" == columnType:
                if create_signal_permission is False:
                    temp['columnSetting'] = columnSettingCopy[:1]
                else:
                    temp['columnSetting'] = columnSettingCopy[:3]

            if head.get('ignoreSuggestionFlag') is True:
                transformation_settings_ignore = copy.deepcopy(settings.TRANSFORMATION_SETTINGS_IGNORE)
                transformation_settings_ignore['status'] = True
                transformation_settings_ignore['previous_status'] = True
                transformation_settings_ignore['displayName'] = 'Consider for Analysis'
                temp['columnSetting'].append(transformation_settings_ignore)
            else:
                transformation_settings_ignore = copy.deepcopy(settings.TRANSFORMATION_SETTINGS_IGNORE)
                transformation_settings_ignore['status'] = False
                transformation_settings_ignore['previous_status'] = False
                transformation_settings_ignore['displayName'] = 'Ignore for Analysis'
                temp['columnSetting'].append(transformation_settings_ignore)

            if head['slug'] in percentage_slug_list:
                for colSet in temp['columnSetting']:
                    if 'set_variable' == colSet['actionName']:
                        colSet['status'] = True
                        if 'listOfActions' in colSet:
                            for listAct in colSet['listOfActions']:
                                if 'percentage' == listAct['name']:
                                    listAct['status'] = True
                                else:
                                    listAct['status'] = False

            transformation_data.append(temp)
        transformation_final_obj["existingColumns"] = transformation_data
        transformation_final_obj["newColumns"] = transformation_settings.get('new_columns')
    return transformation_final_obj


def add_columnData_to_ui_metatdata(meta_data):
    columnDataUI = []
    if 'columnData' in meta_data:
        columnData = meta_data['columnData']

        for head in columnData:
            colDataUI = {}
            colDataUI["name"] = head["name"]
            colDataUI["slug"] = head["slug"]
            colDataUI["columnType"] = head["columnType"]
            colDataUI["dateSuggestionFlag"] = head["dateSuggestionFlag"]
            colDataUI["ignoreSuggestionFlag"] = head["ignoreSuggestionFlag"]
            if 'ignoreSuggestionPreviewFlag' in head:
                colDataUI["ignoreSuggestionPreviewFlag"] = head["ignoreSuggestionPreviewFlag"]
            else:
                colDataUI["ignoreSuggestionPreviewFlag"] = True
            colDataUI["ignoreSuggestionMsg"] = head["ignoreSuggestionMsg"]
            colDataUI["columnStats"] = head["columnStats"]
            if "actualColumnType" in head:
                colDataUI["actualColumnType"] = head["actualColumnType"]
            else:
                colDataUI["actualColumnType"] = None

            if head.get('ignoreSuggestionFlag') is True:
                colDataUI['consider'] = False
            else:
                colDataUI['consider'] = True

            columnDataUI.append(colDataUI)
    return columnDataUI


def add_sampleData_to_ui_metadata(meta_data):
    if 'sampleData' in meta_data:
        return meta_data['sampleData']


def add_modified_to_ui_metadata(value=False):
    return value


def add_headers_to_ui_metadata(meta_data):
    if 'headers' in meta_data:
        return meta_data['headers']
    return []


def add_ui_metadata_to_metadata(meta_data, permissions_dict=None):
    output = {
        'possibleAnalysis': add_possible_analysis_to_ui_metadata(meta_data),
        'transformation_settings': add_transformation_setting_to_ui_metadata(meta_data, permissions_dict),
        'metaDataUI': add_metaData_to_ui_metadata(meta_data),
        'columnDataUI': add_columnData_to_ui_metatdata(meta_data),
        'sampleDataUI': add_sampleData_to_ui_metadata(meta_data),
        'headersUI': add_headers_to_ui_metadata(meta_data),
        'modified': add_modified_to_ui_metadata()
    }
    varibaleSelectionArray = add_variable_selection_to_metadata(output["columnDataUI"], output['transformation_settings'])
    output.update({"varibaleSelectionArray":varibaleSelectionArray})
    output.update({'advanced_settings': get_advanced_setting(varibaleSelectionArray)})
    return output

def add_variable_selection_to_metadata(columnDataUI,transformation_settings):
    validcols = [ {"name":x["name"],"slug":x["slug"],"columnType":x["columnType"],"actualColumnType":x["actualColumnType"],"dateSuggestionFlag":x["dateSuggestionFlag"],"targetColumn":False,"targetColSetVarAs":None} for x in columnDataUI if x["consider"]==True]
    # validcols += [ {"name":x["name"],"slug":x["slug"],"columnType":x["columnType"],"actualColumnType":x["actualColumnType"],"dateSuggestionFlag":x["dateSuggestionFlag"],"targetColumn":False,"targetColSetVarAs":None} for x in columnDataUI if x["consider"]==False and x["ignoreSuggestionPreviewFlag"]==False]

    for x in columnDataUI:
        if 'ignoreSuggestionPreviewFlag' in x:
            if x["consider"] == False and x["ignoreSuggestionPreviewFlag"] == False :
                temp = {"name":x["name"],"slug":x["slug"],"columnType":x["columnType"],"actualColumnType":x["actualColumnType"],"dateSuggestionFlag":x["dateSuggestionFlag"],"targetColumn":False,"targetColSetVarAs":None}
                validcols.append(temp)

    timeDimensionCols = []
    dateSuggestionCols = []
    validcols1 = []
    for x in validcols:
        if x["columnType"] == "datetime":
            timeDimensionCols.append(x["slug"])
        if x["dateSuggestionFlag"] == True:
            dateSuggestionCols.append(x["slug"])
        if x["dateSuggestionFlag"] == True:
            x.update({"selected": False})
        else:
            if x["columnType"] == "datetime":
                x.update({"selected": False})
            else:
                x.update({"selected": True})

        validcols1.append(x)
    validcols = validcols1
    transformSetting = transformation_settings["existingColumns"]
    uidcols = []
    polarity = []
    setVarAs = []
    for obj in transformSetting:
        colset = obj["columnSetting"]
        uidobj = [{"name":obj["name"],"slug":obj["slug"]} for x in colset if x["actionName"] == "unique_identifier" and x["status"]==True]
        if len(uidobj) > 0:
            uidcols.append(uidobj[0])
        polarityCols = [x for x in colset if x["actionName"] == "set_polarity" and x["status"]==True]
        if len(polarityCols) >0:
            polarityActions = polarityCols[0]["listOfActions"]
            relevantAction = [x for x in polarityActions if x["status"]==True]
            if len(relevantAction) >0:
                polarity.append({"name":obj["name"],"slug":obj["slug"],"polarity":relevantAction[0]["name"]})

        setVarAsCols = [x for x in colset if x["actionName"] == "set_variable" and x["status"] == True]
        if len(setVarAsCols) > 0:
            setVarAsActions = setVarAsCols[0]["listOfActions"]
            relevantAction = [x for x in setVarAsActions if x["status"] == True]
            if len(relevantAction) > 0:
                setVarAs.append({"name": obj["name"], "slug": obj["slug"], "setVarAs": relevantAction[0]["name"]})

    ######
    output = []
    selctedDateSuggestedCol = None
    if len(timeDimensionCols) == 0:
        if len(dateSuggestionCols) > 0:
            selctedDateSuggestedCol = dateSuggestionCols[0]
    for obj in validcols:
        if selctedDateSuggestedCol != None:
            if obj["slug"]==selctedDateSuggestedCol:
                # obj.update({"selected":True})
                obj.update({"selected":False})
        uidFilter = [x for x in uidcols if x["slug"] == obj["slug"]]
        if len(uidFilter) > 0:
            obj.update({"uidCol": True})
        else:
            obj.update({"uidCol": False})

        polarityFilter = [x for x in polarity if x["slug"] == obj["slug"]]
        if len(polarityFilter) > 0:
            obj.update({"polarity": polarityFilter[0]["polarity"]})
        else:
            obj.update({"polarity": None})

        setVarAsFilter = [x for x in setVarAs if x["slug"] == obj["slug"]]
        if len(setVarAsFilter) > 0:
            obj.update({"setVarAs": setVarAsFilter[0]["setVarAs"]})
        else:
            obj.update({"setVarAs": None})
        output.append(obj)


    return output
