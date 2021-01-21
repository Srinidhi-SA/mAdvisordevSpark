from __future__ import print_function
from __future__ import division

import hashlib

from future import standard_library
standard_library.install_aliases()
from builtins import zip
from builtins import map
from builtins import str
from builtins import range
from past.utils import old_div
from builtins import object
import time
from math import floor, log10
import datetime
import random
import requests
import base64
import simplejson as json
import re
import datetime

from django.conf import settings
import yarn_api_client
# from api.tasks import *
from config.settings.config_file_name_to_run import CONFIG_FILE_NAME
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule
import pytz

JOBSERVER = settings.JOBSERVER
THIS_SERVER_DETAILS = settings.THIS_SERVER_DETAILS


class JobserverDetails(object):
    @classmethod
    def get_jobserver_url(cls):
        protocol = "https://" if settings.USE_HTTPS else "http://"
        return protocol + JOBSERVER.get('host') + ":" + JOBSERVER.get('port')

    @classmethod
    def get_app(cls):
        return JOBSERVER.get('app-name')

    @classmethod
    def get_context(cls):
        return JOBSERVER.get('context')

    @classmethod
    def get_class_path(cls, name):
        if name not in JOBSERVER:
            raise Exception('No such class.')
        return JOBSERVER.get(name)

    @classmethod
    def get_config(cls,
                   slug,
                   class_name,
                   job_name=None,
                   message_slug=None,
                   app_id=None
                   ):

        job_type = {
            "metadata": "metaData",
            "master": "story",
            "model": "training",
            "score": "prediction",
            "robo": "robo",
            "subSetting": "subSetting",
            "stockAdvisor": "stockAdvisor"
        }

        if settings.USE_HTTPS:
            protocol = 'https'
        else:
            protocol = 'http'

        return {
            "job_config": {
                "job_type": job_type[class_name],
                "config_url": "{3}://{0}/api/job/{2}/get_config".format(THIS_SERVER_DETAILS.get('host'),
                                                                        THIS_SERVER_DETAILS.get('port'),
                                                                        slug, protocol),
                "job_url": "{3}://{0}/api/job/{2}/".format(THIS_SERVER_DETAILS.get('host'),
                                                           THIS_SERVER_DETAILS.get('port'),
                                                           slug, protocol),
                "kill_url": "{3}://{0}/api/job/{2}/rest_in_peace/".format(THIS_SERVER_DETAILS.get('host'),
                                                                          THIS_SERVER_DETAILS.get('port'),
                                                                          slug, protocol),
                "initial_messages": "{3}://{0}/api/job/{2}/dump_complete_messages/".format(
                    THIS_SERVER_DETAILS.get('host'),
                    THIS_SERVER_DETAILS.get('port'),
                    slug, protocol),
                "message_url": "{3}://{0}/api/messages/{2}/".format(THIS_SERVER_DETAILS.get('host'),
                                                                    THIS_SERVER_DETAILS.get('port'),
                                                                    message_slug, protocol),
                "xml_url": "{3}://{0}/api/xml/{2}/".format(THIS_SERVER_DETAILS.get('host'),
                                                           THIS_SERVER_DETAILS.get('port'),
                                                           slug, protocol),
                "error_reporting_url": "{3}://{0}/api/set_job_report/{2}/".format(THIS_SERVER_DETAILS.get('host'),
                                                                                  THIS_SERVER_DETAILS.get('port'),
                                                                                  slug, protocol),
                "job_name": job_name,
                "app_id": app_id,
                "get_config":
                    {
                        "action": "get_config",
                        "method": "GET"
                    },
                "set_result":

                    {
                        "action": "result",
                        "method": "PUT"
                    }
            }
        }

    @classmethod
    def print_job_details(cls, job):
        job_url = "{0}/jobs/{1}".format(cls.get_jobserver_url(), job.jobId)
        print("job_url: {0}".format(job_url))
        return job_url


def metadata_chart_conversion(data):
    output = {
        "data": {
            "columns": [
                [],
            ],
            "type": "bar",
        },
        "bar": {
            "width": {
                "ratio": 0.5
            }
        },
        "legend": {
            "show": False
        },
        "color": {
            "pattern": ['#0fc4b5', '#005662', '#148071', '#6cba86', '#bcf3a2']
        }
    }
    values = ["data1"]
    for obj in data:
        values.append(obj["value"])
    output["data"]["columns"] = [values]

    return output


def find_chart_data_and_replace_with_chart_data(data):
    output = metadata_chart_conversion(data)
    return output


chartData = {
    "data": {
        "columns": [
            ["data1", 30, 200, 100, 400, 150, 250],
            ["data2", 130, 100, 140, 200, 150, 50]
        ],
        "type": "bar",
    },
    "bar": {
        "width": {
            "ratio": 0.5
        },
        "color": {
            "pattern": ['#0fc4b5', '#005662', '#148071', '#6cba86', '#bcf3a2']
        }
    },
}


def remove_tooltip_format_from_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if 'tooltip' in chart_data['chart_c3']:
            del chart_data['chart_c3']['tooltip']
    return chart_data


def remove_chart_height_from_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if "size" in chart_data['chart_c3']:
            del chart_data['chart_c3']['size']
    return chart_data


def remove_chart_height_from_x_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if "axis" in chart_data['chart_c3']:
            if "x" in chart_data['chart_c3']["axis"]:
                if "height" in chart_data['chart_c3']["axis"]["x"]:
                    del chart_data['chart_c3']["axis"]["x"]["height"]
    return chart_data


def keep_bar_width_in_ratio(chart_data):
    count_x = 0
    if 'chart_c3' in chart_data:
        if 'data' in chart_data['chart_c3']:
            if 'columns' in chart_data['chart_c3']['data']:
                columns_data = chart_data['chart_c3']['data']['columns']
                count_x = len(columns_data[0])
        if 'bar' in chart_data['chart_c3']:
            if count_x < 5:
                chart_data['chart_c3']['bar'] = {
                    'width': 20
                }
            else:
                chart_data['chart_c3']['bar'] = {
                    "width": {
                        "ratio": 0.5
                    }
                }
    return chart_data


def remove_padding_from_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if "padding" in chart_data['chart_c3']:
            del chart_data['chart_c3']['padding']
    return chart_data


def add_side_padding_to_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        chart_data['chart_c3']['padding'] = {
            'right': 20
        }

    return chart_data


def remove_subchart_from_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if "subchart" in chart_data['chart_c3']:
            del chart_data['chart_c3']['subchart']
    return chart_data


def remove_legend_from_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if "legend" in chart_data['chart_c3']:
            del chart_data['chart_c3']['legend']
    return chart_data


def remove_grid_from_chart_data(chart_data):
    if 'chart_c3' in chart_data:
        if "grid" in chart_data['chart_c3']:
            del chart_data['chart_c3']['grid']
    return chart_data


def remove_xdata_from_chart_data(chart_data):
    if 'xdata' in chart_data:
        del chart_data['xdata']
    return chart_data


def limit_chart_data_length(chart_data, limit=None):
    if limit != None:
        if 'chart_c3' in chart_data:
            tempData = []
            if "columns" in chart_data["chart_c3"]["data"]:
                for row in chart_data["chart_c3"]["data"]["columns"]:
                    tempData.append(row[:limit + 1])
                    chart_data["chart_c3"]["data"]["columns"] = tempData

    return chart_data


def decode_and_convert_chart_raw_data(data, object_slug=None):
    if not check_chart_data_format(data):
        print("chart data format not matched")
        return {}
    from api.C3Chart.c3charts import C3Chart, ScatterChart, DonutChart, PieChart
    chart_type = data['chart_type']
    title = data.get('title', "None")
    axes = data['axes']
    label_text = data['label_text']
    legend = data['legend']
    types = data.get('types', None)
    axisRotation = data.get('axisRotation', None)
    yAxisNumberFormat = data.get('yAxisNumberFormat', None)
    y2AxisNumberFormat = data.get('y2AxisNumberFormat', None)
    showLegend = data.get('show_legend', True)
    hide_xtick = data.get('hide_xtick', False)
    if y2AxisNumberFormat == "":
        y2AxisNumberFormat = ".2s"
    subchart = data.get('subchart', True)
    rotate = data.get('rotate', False)

    c3_chart_details = dict()
    from api.models import SaveData
    sd = SaveData()
    if object_slug is not None:
        sd.object_slug = object_slug
    sd.save()
    if chart_type in ["bar", "line", "spline"]:
        chart_data = replace_chart_data(data['data'])
        c3_chart_details['table_c3'] = put_x_axis_first_chart_data(chart_data, axes.get('x', 'key'))
        sd.set_data(data=chart_data)
        c3_chart_details['download_url'] = sd.get_url()
        c3 = C3Chart(
            data=chart_data,
            chart_type=chart_type,
            x_column_name=axes.get('x', 'key'),
            title=title
        )
        c3.set_all_basics()

        if axes.get('y', None) is not None:
            c3.set_y_axis(
                y_name=axes.get('y')
            )
            if yAxisNumberFormat is not None:
                c3_chart_details["yformat"] = yAxisNumberFormat
            else:
                c3_chart_details["yformat"] = '.2s'

        if axes.get('y2', None) is not None:
            c3.set_another_y_axis(
                y2_name=axes.get('y2')
            )

            if y2AxisNumberFormat is not None:
                c3_chart_details["y2format"] = y2AxisNumberFormat
            else:
                c3_chart_details["y2format"] = '.2s'
            c3.set_d3_format_y2(c3_chart_details["y2format"])

        c3.set_axis_label_simple(
            label_text=label_text
        )

        c3.add_additional_grid_line_at_zero()
        if chart_type == "bar":
            c3.remove_vertical_grid_from_chart_data()

        if subchart is False:
            c3.hide_subchart()
        if showLegend is True and legend:
            c3.set_name_to_data(legend)
        else:
            c3.hide_basic_legends()

        if rotate is True:
            c3.rotate_axis()

        xdata = get_x_column_from_chart_data_without_xs(chart_data, axes)
        if len(xdata) > 1:
            c3_chart_details["xdata"] = get_x_column_from_chart_data_without_xs(chart_data, axes)
            c3.set_tick_format_x()
            c3.set_tooltip_format()

        if hide_xtick is True:
            c3.hide_x_tick()
        # c3.add_additional_grid_line_at_zero()

        c3_chart_details["chart_c3"] = c3.get_json()

        return c3_chart_details

    elif chart_type in ["combination"]:

        chart_data = replace_chart_data(data['data'])
        c3_chart_details['table_c3'] = put_x_axis_first_chart_data(chart_data, axes.get('x', 'key'))
        sd.set_data(data=chart_data)
        c3_chart_details['download_url'] = sd.get_url()
        c3 = C3Chart(
            data=chart_data,
            chart_type=chart_type,
            x_column_name=axes.get('x', 'key'),
            title=title
        )
        c3.set_all_basics()

        if axes.get('y', None) is not None:
            c3.set_y_axis(
                y_name=axes.get('y')
            )
            if yAxisNumberFormat is not None:
                c3_chart_details["yformat"] = yAxisNumberFormat
            else:
                c3_chart_details["yformat"] = '.2s'

        if axes.get('y2', None) is not None:
            c3.set_another_y_axis(
                y2_name=axes.get('y2')
            )

            if y2AxisNumberFormat is not None:
                c3_chart_details["y2format"] = y2AxisNumberFormat
            else:
                c3_chart_details["y2format"] = '.2s'
            c3.set_d3_format_y2(c3_chart_details["y2format"])

        c3.set_axis_label_simple(
            label_text=label_text
        )

        if types:
            c3.add_new_chart_on_a_data_list(types)

        if axisRotation:
            c3.rotate_axis()

        if hide_xtick is True:
            c3.hide_x_tick()

        if showLegend is True and legend:
            c3.set_name_to_data(legend)
        else:
            c3.hide_basic_legends()

        xdata = get_x_column_from_chart_data_without_xs(chart_data, axes)
        if len(xdata) > 1:
            c3_chart_details["xdata"] = get_x_column_from_chart_data_without_xs(chart_data, axes)
            c3.set_tick_format_x()
            c3.set_tooltip_format()
        c3.add_additional_grid_line_at_zero()

        from api.C3Chart import config
        c3.set_basic_color_pattern(config.SECOND_FLIP_PATTERN)

        if subchart is False:
            c3.hide_subchart()
        # c3.add_additional_grid_line_at_zero()

        c3_chart_details["chart_c3"] = c3.get_json()
        return c3_chart_details

    elif chart_type in ["scatter"]:
        data_c3 = data['data']
        chart_data, xs = replace_chart_data(data_c3, data['axes'])
        c3_chart_details['table_c3'] = chart_data
        sd.set_data(data=chart_data)
        c3_chart_details['download_url'] = sd.get_url()
        c3 = ScatterChart(
            data=chart_data,
            data_type='columns',
            title=title
        )
        c3.set_xs(xs)

        c3.set_axis_label_simple(
            label_text=label_text
        )

        if axes.get('y', None) is not None:
            c3.set_y_axis(
                y_name=axes.get('y')
            )
            if yAxisNumberFormat is not None:
                c3_chart_details["yformat"] = yAxisNumberFormat
            else:
                c3_chart_details["yformat"] = '.2s'
        c3_chart_details["yformat"] = '.2s'

        if axes.get('y2', None) is not None:
            c3.set_another_y_axis(
                y2_name=axes.get('y2')
            )

            if y2AxisNumberFormat is not None:
                c3_chart_details["y2format"] = y2AxisNumberFormat
            else:
                c3_chart_details["y2format"] = '.2s'
            c3.set_d3_format_y2(c3_chart_details["y2format"])

        if subchart is False:
            c3.hide_subchart()

        if showLegend is True and legend:
            c3.set_name_to_data(legend)
        else:
            c3.hide_basic_legends()

        c3.set_x_type_as_index()

        if hide_xtick is True:
            c3.hide_x_tick()
        # c3.add_additional_grid_line_at_zero()
        c3_chart_details["chart_c3"] = c3.get_json()
        return c3_chart_details

    elif chart_type in ["scatter_line", "scatter_bar"]:
        data_c3 = data['data']
        chart_data, xs = replace_chart_data(data_c3, data['axes'])

        c3_chart_details['table_c3'] = chart_data
        sd.set_data(data=chart_data)
        c3_chart_details['download_url'] = sd.get_url()
        if 'point' in data:
            c3 = ScatterChart(
                data=chart_data,
                data_type='columns',
                title=title,
                point=data['point']
            )
        else:
            c3 = ScatterChart(
                data=chart_data,
                data_type='columns',
                title=title,
            )
        c3.set_xs(xs)

        c3.set_axis_label_simple(
            label_text=label_text
        )

        if chart_type == "scatter_line":
            c3.set_line_chart()
        elif chart_type == "scatter_bar":
            c3.set_bar_chart()

        if axes.get('y', None) is not None:
            c3.set_y_axis(
                y_name=axes.get('y')
            )
            if yAxisNumberFormat is not None:
                c3_chart_details["yformat"] = yAxisNumberFormat
            else:
                c3_chart_details["yformat"] = '.2s'
        c3_chart_details["yformat"] = '.2s'

        if axes.get('y2', None) is not None:
            c3.set_another_y_axis(
                y2_name=axes.get('y2')
            )

            if y2AxisNumberFormat is not None:
                c3_chart_details["y2format"] = y2AxisNumberFormat
            else:
                c3_chart_details["y2format"] = '.2s'
            c3.set_d3_format_y2(c3_chart_details["y2format"])

        if subchart is False:
            c3.hide_subchart()

        if showLegend is True and legend:
            c3.set_name_to_data(legend)
        else:
            c3.hide_basic_legends()

        if hide_xtick is True:
            c3.hide_x_tick()
        # c3.add_additional_grid_line_at_zero()
        c3_chart_details["chart_c3"] = c3.get_json()
        return c3_chart_details

    elif chart_type in ['scatter_tooltip']:
        # take from old code. tooltip related with scatter. easier to get this data
        data_c3 = data['data']
        card3_data, xs = convert_column_data_with_array_of_category_into_column_data_stright_xy(data_c3, 3)
        c3_chart_details['table_c3'] = data_c3
        sd.set_data(data=data_c3)
        c3_chart_details['download_url'] = sd.get_url()
        c3 = ScatterChart(
            data=card3_data,
            data_type='columns',
            title=title
        )
        c3.set_xs(xs)

        c3.set_axis_label_simple(
            label_text=label_text
        )

        c3.set_x_type_as_index()

        c3.add_tooltip_for_scatter()

        if axes.get('y', None) is not None:
            c3.set_y_axis(
                y_name=axes.get('y')
            )
            if yAxisNumberFormat is not None:
                c3_chart_details["yformat"] = yAxisNumberFormat
            else:
                c3_chart_details["yformat"] = '.2s'
        c3_chart_details["yformat"] = '.2s'

        if axes.get('y2', None) is not None:
            c3.set_another_y_axis(
                y2_name=axes.get('y2')
            )

            if y2AxisNumberFormat is not None:
                c3_chart_details["y2format"] = y2AxisNumberFormat
            else:
                c3_chart_details["y2format"] = '.2s'
            c3.set_d3_format_y2(c3_chart_details["y2format"])

        if subchart is False:
            c3.hide_subchart()

        if showLegend is True and legend:
            c3.set_name_to_data(legend)
        else:
            c3.hide_basic_legends()

        if hide_xtick is True:
            c3.hide_x_tick()
        # c3.add_additional_grid_line_at_zero()
        c3_chart_details["chart_c3"] = c3.get_json()
        c3_chart_details["tooltip_c3"] = format_tooltip_data([data_c3[0], data_c3[1], data_c3[2]])
        return c3_chart_details
    elif chart_type in ['donut']:
        chart_data = replace_chart_data(data['data'])
        sd.set_data(data=chart_data)
        c3_chart_details['download_url'] = sd.get_url()
        # pie_chart_data = convert_chart_data_to_pie_chart(chart_data)
        pie_chart_data = chart_data
        c3 = DonutChart(data=pie_chart_data, title=title, yAxisNumberFormat=yAxisNumberFormat)
        c3.set_all_basics()

        # c3.show_basic_legends()
        c3.show_legends_at_right()

        # c3.hide_basic_legends()

        if yAxisNumberFormat is not None:
            c3_chart_details["yformat"] = yAxisNumberFormat
        else:
            c3_chart_details["yformat"] = '.2s'

        c3.set_d3_format_y(c3_chart_details["yformat"])
        c3.set_basic_tooltip()
        c3.set_tooltip_format('.2s')
        c3.remove_x_from_data()
        c3.add_tooltip_for_donut()
        if len(chart_data) >= 1:
            name_list = [i[0] for i in chart_data]
            try:
                name_list = sorted(name_list, key=lambda x: int(x.split("-")[0]), reverse=True)
            except:
                pass
            from api.C3Chart.config import PATTERN1
            color_list = PATTERN1
            length = len(name_list)
            c3_chart_details["legend_data"] = [{'name': name_list[i], 'color': color_list[i]} for i in range(length)]

        c3_chart_details['table_c3'] = pie_chart_data
        c3_chart_details["chart_c3"] = c3.get_json()

        return c3_chart_details

    elif chart_type in ['pie']:
        chart_data = replace_chart_data(data['data'])
        # pie_chart_data = convert_chart_data_to_pie_chart(chart_data)
        pie_chart_data = chart_data
        sd.set_data(data=chart_data)
        c3_chart_details['download_url'] = sd.get_url()
        c3 = PieChart(data=pie_chart_data, title=title, yAxisNumberFormat=yAxisNumberFormat)
        c3.set_all_basics()
        c3.show_basic_legends()
        if yAxisNumberFormat is not None:
            c3_chart_details["yformat"] = yAxisNumberFormat
        else:
            c3_chart_details["yformat"] = '.2s'
        c3.set_d3_format_y(c3_chart_details["yformat"])
        c3.set_basic_tooltip()
        c3.set_tooltip_format('.2s')
        c3.remove_x_from_data()
        c3.add_tooltip_for_pie()

        c3_chart_details['table_c3'] = pie_chart_data
        c3_chart_details["chart_c3"] = c3.get_json()
        return c3_chart_details


def replace_chart_data(data, axes=None):
    if isinstance(data, list):
        return convert_listed_dict_objects(data)
    elif isinstance(data, dict):
        return dict_to_list(data, axes)


def convert_chart_data_to_pie_chart(chart_data):
    pie_chart_data = list(zip(*chart_data))
    pie_chart_data = list(map(list, pie_chart_data))
    return pie_chart_data[1:]


def put_x_axis_first_chart_data(chart_data, x_column=None):
    import copy
    chart_data = copy.deepcopy(chart_data)
    if x_column is None:
        return chart_data
    index = 0
    i = 0
    for data in chart_data:
        if data[0] == x_column:
            index = i
            break
        i += 1

    if index == 0:
        return chart_data
    else:
        temp = chart_data[index]
        chart_data[index] = chart_data[0]
        chart_data[0] = temp

    return chart_data


def get_slug(name):
    from django.template.defaultfilters import slugify
    import string
    import random
    slug = slugify(str(name) + "-" + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
    return slug


def check_chart_data_format(data):
    keys = ['data', 'axes', 'label_text', 'legend', 'chart_type', 'types', 'axisRotation']

    data_keys = list(data.keys())

    if len(set(keys) - set(data_keys)) < 1:
        return True
    return False


def convert_according_to_legend_simple(chart_data, legend):
    for data in chart_data:
        name = legend.get(data[0], None)
        if name is not None:
            data[0] = name

    return chart_data


def convert_listed_dict_objects(json_data):
    """
    :param_json_data:  [
                        {
                            "value": 100062.04,
                            "key": "Jan-1998"
                        },
                        {
                            "value": 125248,
                            "key": "Jan-1999"
                        },
                        {
                            "value": 708180.8600000001,
                            "key": "Aug-1999"
                        },
                        {
                            "value": 1048392.7300000001,
                            "key": "Sep-1999"
                        }
                    ]
    :return: [
        ['key', "Jan-1998", "Jan-1999", "Aug-1999", "Sep-1999"],
        ['value', 100062.04, 125248, 708180.8600000001, 1048392.7300000001]
    ]
    """
    if not json_data or not json_data[0]:
        return []
    keys = list(json_data[0].keys())
    column_data = [[] for _ in range(len(keys))]
    item_index_dictionary = dict()
    for index, item in enumerate(keys):
        column_data[index].append(item)
        item_index_dictionary[item] = index

    for data in json_data:
        for item in list(data.keys()):
            column_data[item_index_dictionary[item]].append(data[item])
    return column_data


def convert_json_with_list_to_column_data_for_xs(data):
    """
    {
        'a' : [{
            'date':23,
            'value':5
        },
        {
            'date':24,
            'value':6
        }],
        'b' : [{
            'date':23,
            'value':4
        },
        {
            'date':24,
            'value':7
        }]
    }

    to

    [
        ['a_date', 23, 24],
        ['a', 5, 6],
        ['b_date', 23, 24],
        ['b', 4, 7]
    ]

    """

    all_key = list(data.keys())

    final_data = []
    xs = {}
    mapp = {}
    i = 0
    for d in all_key:
        final_data.append([d + '_x'])
        final_data.append([d])

        xs[d] = d + '_x'

        mapp[d + '_x'] = i
        i += 1
        mapp[d] = i
        i += 1

    for d in list(data.keys()):
        array_of_json = data[d]
        x_index = mapp[d + '_x']
        y_index = mapp[d]
        for snip in array_of_json:
            final_data[x_index].append(snip.get('date'))
            final_data[y_index].append(snip.get('val'))

    return final_data, xs


def inv_axes(axes):
    """

    :param axes:
                {
                "x": "key",
                "y": "a",
                }
    :return: {'a': 'y', 'key': 'x'}
    """
    ax = dict()
    for key in axes:
        ax[axes[key]] = key
    return ax


def dict_to_list(datas, axes=None):
    """
     {
        'a' : [{
            'date':23,
            'value':5
        },
        {
            'date':24,
            'value':6
        }],
        'b' : [{
            'date':23,
            'value':4
        },
        {
            'date':24,
            'value':7
        }]
    }

    to

    [
        ['a_date', 23, 24],
        ['a', 5, 6],
        ['b_date', 23, 24],
        ['b', 4, 7]
    ],

    {
        "a": "a_x",
        "b": "b_x"
    }

    :param datas:
    :param axes:
    :return:
    """
    ar = []
    xs = dict()
    if axes.get('x', None) is None:
        raise Exception("No x in axes.")
    inverted_axes = inv_axes(axes)
    for key in datas:
        chart_data = datas[key]
        convert_data = convert_listed_dict_objects(chart_data)
        x = ""
        y = ""
        for d in convert_data:
            if inverted_axes.get(d[0], None) == 'x':
                d[0] = key + '_x'
                x = key + '_x'
            else:
                d[0] = key
                y = key
        xs[y] = x
        ar += convert_data
    return ar, xs


def convert_column_data_with_array_of_category_into_column_data_stright_xy(columns_data, category_data_index):
    def get_all_unique(category_data_list):
        return list(set(category_data_list))

    category_data_list = columns_data[category_data_index]
    try:
        color_naming_scheme = columns_data[3]
    except:
        color_naming_scheme = None

    if isinstance(color_naming_scheme, dict):
        pass
    elif isinstance(color_naming_scheme, list) or color_naming_scheme is None:

        color_naming_scheme = {
            'red': 'Cluster0',
            'blue': 'Cluster1',
            'green': 'Cluster2',
            'orange': 'Cluster3',
            'yellow': 'Cluster4'
        }

    unique_category_name = get_all_unique(category_data_list)

    end_data = []
    name_indexs = dict()
    xs = dict()

    i = 0
    for name in unique_category_name:
        if name == columns_data[category_data_index][0]:
            continue

        # name_x = name
        name_x = name + '_'
        try:
            name_y = color_naming_scheme[name_x]
        except:
            # name_y = name + '_'
            name_y = name

        end_data.append([name_x])
        name_indexs[name_x] = i
        i += 1

        end_data.append([name_y])
        name_indexs[name_y] = i
        i += 1

        xs[name_y] = name_x

    for index, name in enumerate(columns_data[category_data_index][1:]):
        # name_x = name
        name_x = name + '_'
        try:
            name_y = color_naming_scheme[name_x]
        except:
            # name_y = name + '_'
            name_y = name

        end_data[name_indexs[name_x]].append(columns_data[0][index + 1])
        end_data[name_indexs[name_y]].append(columns_data[1][index + 1])

    return end_data, xs


def get_x_column_from_chart_data_without_xs(chart_data, axes):
    i = None
    for index, row in enumerate(chart_data):
        if row[0] == axes.get('x', 'key'):
            i = index
            break

    if i is not None:
        return chart_data[i][1:]
    else:
        return []


from celery.decorators import task
from celery_once import QueueOnce, AlreadyQueued


def get_db_object(model_name, model_slug):
    from django.apps import apps
    mymodel = apps.get_model('api', model_name)
    obj = mymodel.objects.get(slug=model_slug)
    return obj


@task(base=QueueOnce, name='get_job_from_yarn', queue=CONFIG_FILE_NAME + '_yarn')
def get_job_from_yarn(model_name=None, model_slug=None):
    try:
        model_instance = get_db_object(model_name=model_name,
                                       model_slug=model_slug
                                       )
        if model_instance.job == None:
            return 1
        if model_instance.job.url == '':
            return model_instance.status
    except:
        print(model_instance)
        return

    try:
        ym = yarn_api_client.resource_manager.ResourceManager(address=settings.YARN.get("host"),
                                                              port=settings.YARN.get("port"),
                                                              timeout=settings.YARN.get("timeout"))
        app_status = ym.cluster_application(model_instance.job.url)
        YarnApplicationState = app_status.data['app']["state"]
    except:
        YarnApplicationState = "FAILED"

    readable_live_status = settings.YARN_STATUS.get(YarnApplicationState, "FAILED")
    model_instance.job.status = YarnApplicationState
    model_instance.job.save()

    if readable_live_status is 'SUCCESS' and model_instance.analysis_done is False:
        model_instance.status = 'FAILED'
    else:
        model_instance.status = readable_live_status

    model_instance.save()
    return model_instance.status


def get_job_status_from_yarn(instance=None):
    try:
        ym = yarn_api_client.resource_manager.ResourceManager(address=settings.YARN.get("host"),
                                                              port=settings.YARN.get("port"),
                                                              timeout=settings.YARN.get("timeout"))
        app_status = ym.cluster_application(instance.job.url)

        # YarnApplicationState = (
        # (ACCEPTED, 'Application has been accepted by the scheduler.'),
        # (FAILED, 'Application which failed.'),
        # (FINISHED, 'Application which finished successfully.'),
        # (KILLED, 'Application which was terminated by a user or admin.'),
        # (NEW, 'Application which was just created.'),
        # (NEW_SAVING, 'Application which is being saved.'),
        # (RUNNING, 'Application which is currently running.'),
        # (SUBMITTED, 'Application which has been submitted.'),
        # )

        YarnApplicationState = app_status.data['app']["state"]

        # YARN_STATUS = {"RUNNING": "INPROGRESS",
        #                "ACCEPTED": "INPROGRESS",
        #                "NEW": "INPROGRESS",
        #                "NEW_SAVING": "INPROGRESS",
        #                "SUBMITTED": "INPROGRESS",
        #                "ERROR": "FAILED",
        #                "FAILED": "FAILED",
        #                "killed": "FAILED",
        #                "FINISHED": "SUCCESS",
        #                "KILLED": "FAILED",
        #                }
    except:
        YarnApplicationState = "FAILED"
    readable_live_status = settings.YARN_STATUS.get(YarnApplicationState, "FAILED")

    try:
        instance.job.status = YarnApplicationState
        instance.job.save()
    except:
        pass

    if readable_live_status is 'SUCCESS' and instance.analysis_done is False:
        instance.status = 'FAILED'
    else:
        instance.status = readable_live_status

    instance.save()
    return instance.status


def get_job_status_from_jobserver(instance=None):
    if instance is None:
        return "no instance ---!!"

    if instance.job is None:
        return ""
    job_url = instance.job.url
    if instance.status in ['SUCCESS', 'FAILED']:
        return instance.status
    try:
        live_status = return_status_of_job_log(job_url)
        instance.status = live_status
        instance.save()
        return live_status
    except Exception as err:
        return err


def get_job_status(instance=None):
    if instance.status in ['SUCCESS', 'FAILED']:
        return instance.status
    else:
        if instance.job:
            if instance.job.status in ['SUCCESS', 'FAILED']:
                instance.status = instance.job.status
                instance.save()
                return instance.status

    if settings.SUBMIT_JOB_THROUGH_YARN:
        try:
            get_job_from_yarn.delay(
                type(instance).__name__,
                instance.slug
            )
            print("JobStatusCheck QUEUED ---> {0} | {1}".format(type(instance).__name__, instance.slug))
        except AlreadyQueued:
            print("JobStatusCheck ALREADY EXISTING ---> {0} | {1}".format(type(instance).__name__, instance.slug))
            pass
        except Exception as err:
            print("JobStatusCheck..")
            print(err)
    else:
        get_job_status_from_jobserver(instance)


def normalize_job_status_for_yarn(status):
    if "RUNNING" == status:
        return settings.job_status.RUNNING
    elif "ERROR" == status:
        return settings.job_status.ERROR
    elif "FAILED" == status:
        return settings.job_status.ERROR
    elif "FINISHED" == status:
        return settings.job_status.SUCCESS


def return_status_of_job_log(job_url):
    import urllib.request, urllib.parse, urllib.error, json
    final_status = "RUNNING"
    check_status = urllib.request.urlopen(job_url)
    data = json.loads(check_status.read())
    if data.get("status") == "FINISHED":
        final_status = data.get("status")
    elif data.get("status") == "ERROR" and "startTime" in list(data.keys()):
        final_status = data.get("status")
    elif data.get("status") == "RUNNING":
        final_status = data.get("status")
    elif data.get("status") == "KILLED":
        final_status = data.get("status")
    else:
        pass

    jobserver_status = settings.JOBSERVER_STATUS

    return jobserver_status.get(final_status)


def convert_json_object_into_list_of_object(datas, order_type='dataset'):
    from django.conf import settings
    order_dict = settings.ORDER_DICT
    analysis_list = settings.ANALYSIS_LIST
    order_by = order_dict[order_type]

    brief_name = settings.BRIEF_INFO_CONFIG

    list_of_objects = []
    for key in order_by:
        if key in datas:
            temp = dict()
            temp['name'] = key
            temp['displayName'] = brief_name[key]

            if key in ['analysis_list', 'analysis list']:
                temp['value'] = [analysis_list[item] for item in datas[key]]
            else:
                temp['value'] = datas[key]
            list_of_objects.append(temp)

    return list_of_objects


def convert_to_humanize(size):
    size_name = {
        1: 'B',
        2: 'KB',
        3: 'MB',
        4: 'GB',
        5: 'TB'
    }
    i = 1
    while old_div(size, 1024) > 0:
        i += 1
        size = old_div(size, 1024)

    return str(size) + " " + size_name[i]


def convert_to_GB(size):
    count = 3

    while count > 0:
        size = float(size) / 1024
        count -= 1

    return size


def format_tooltip_data(datas):
    for data in datas:
        for index, value in enumerate(data):
            if type(value) in ['int', 'float']:
                data[index] = round_sig(value)

    return datas


def round_sig(x, sig=3):
    try:
        if abs(x) >= 1:
            x = round(x, sig)
        else:
            x = round(x, sig - int(floor(log10(abs(x)))) - 1)
    except:
        pass
    return x


def calculate_percentage(message_log, stock, messages):
    percentage = 0
    msg_log = json.loads(message_log)
    # index = None
    # for d in msg_log:
    #     msg = msg_log[d]
    #     print(msg_log[d])
    #     if stock in msg:
    #         index = d
    #         break
    # index = int(index) -1
    # number_of_stocks = len(msg_log) - 2
    # if index == 0:
    #     percentage = 10
    # else:
    #     percentage = 80/number_of_stocks
    # actual_percentage = messages[-1]['globalCompletionPercentage'] + percentage

    if messages[-1]['globalCompletionPercentage'] == 0:
        percentage = 10
    else:
        number_of_stocks = len(msg_log) - 2
        percentage = 80/number_of_stocks
    actual_percentage = messages[-1]['globalCompletionPercentage'] + percentage
    return actual_percentage


def update_stock_sense_message(job_instance, stock):
    message = json.loads(job_instance.messages)
    percentage = None
    if stock == "ml-work":
        info = "Performing analysis"
        percentage = 80
    else:
        info = "Fetching news articles and NLU for {0}".format(stock)
        percentage = calculate_percentage(job_instance.message_log, stock, message)
        import math
        percentage = math.floor(percentage)

    print("!!!!!!!!!!! @@@@@@@@@@ PERCENTAGE {0}".format(percentage))
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest_message = {
        "analysisName": "stockAdvisor",
        "display": True,
        "stageName": "custom",
        "shortExplanation": info,
        "messageType": "info",
        "globalCompletionPercentage": percentage,
        "gmtDateTime": time_stamp,
        "stageCompletionPercentage": percentage
    }
    message.append(latest_message)
    return json.dumps(message)


def create_message_log_and_message_for_stocksense(stock_symbols):
    message_log = dict()
    message_log[0] = "Fetching stock data"
    stock_symbols = json.loads(stock_symbols)
    for index, (key, value) in enumerate(stock_symbols.items()):
        print(index, key, value)
        message_log[index+1] = "Fetching news articles and NLU for "+value

    message_log[len(stock_symbols) + 1] = "Performing analysis"
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = [
        {
            "analysisName": "stockAdvisor",
            "display": True,
            "stageName": "custom",
            "shortExplanation": message_log[0],
            "messageType": "info",
            "globalCompletionPercentage": 0,
            # "gmtDateTime": "2020-04-07 11:55:15",
            "gmtDateTime": time_stamp,
            "stageCompletionPercentage": 0
        },
    ]
    message_log = json.dumps(message_log)
    message = json.dumps(message)
    return message_log, message


def get_message(instance):
    if instance is None:
        return None
    from api.redis_access import AccessFeedbackMessage
    import simplejson as json
    ac = AccessFeedbackMessage()
    message_log = json.loads(instance.message_log)
    data = None
    if message_log is None or len(message_log) <= 0:
        data = get_message_for_job_status(instance.status)
        if data is not None:
            data = ac.append_using_key(instance.slug, data)
            instance.message_log = json.dumps(data)
            instance.save()
    else:
        keep_in_API = True
        for msg_log in message_log:
            if msg_log['analysisName'] != 'before_script':
                keep_in_API = False
                break

        last_message = message_log[-1]
        if 'analysisName' in last_message and keep_in_API:
            if last_message['analysisName'] == 'before_script':
                data = get_message_for_job_status(instance.status)
                if data is not None:
                    data = ac.append_using_key(instance.slug, data)
                    instance.message_log = json.dumps(data)
                    instance.save()

    if data is None:
        data = message_log

    prev_true_message = None
    for d in data:
        if d['display'] == True:
            prev_true_message = d['shortExplanation']
    data[-1]['shortExplanation'] = prev_true_message
    data[-1]['display'] = True

    return [data[-1]]


def get_message_for_job_status(status=""):
    job_status_message = settings.JOB_STATUS_MESSAGE
    import copy
    job_message_json_format = copy.deepcopy(settings.JOB_MESSAGE_JSON_FORMAT)
    if status == "":
        status = "EMPTY"
    job_message_json_format['messageType'] = status
    job_message_json_format['shortExplanation'] = job_status_message[status]

    return job_message_json_format


from django.http import JsonResponse


def auth_for_ml(func):
    def another_function(*args, **kwargs):
        request = args[0]
        key1 = request.GET['key1']
        key2 = request.GET['key2']
        signature = request.GET['signature']
        generationTime = float(request.GET['generated_at'])
        currentTime = time.time()
        timeDiff = currentTime - generationTime
        if timeDiff < settings.SIGNATURE_LIFETIME:
            json_obj = {
                "key1": key1,
                "key2": key2
            }
            generated_key = generate_signature(json_obj)
            if signature == generated_key:
                return func(*args, **kwargs)
            else:
                return JsonResponse({'Message': 'Auth failed'})
        else:
            return JsonResponse({'Message': 'Signature Expired'})

    return another_function


def generate_signature(json_obj):
    """
    json_obj = json obj with {"key1":"DSDDD","key2":"DASDAA","signature":None}
    secretKey = secret key kknown to ML and API Codebase
    """
    secretKey = settings.ML_SECRET_KEY
    existing_key = json_obj["key1"] + "|" + json_obj["key2"] + "|" + secretKey
    # newhash = md5.new() # python2.7
    # newhash.update(existing_key) # python2.7
    # value = newhash.hexdigest() # python2.7

    newhash = hashlib.md5()
    newhash.update(existing_key)
    value = newhash.hexdigest()  # python3
    return value


def generate_pmml_name(slug):
    return slug + "_" + 'pmml'


def encrypt_url(url):
    from cryptography.fernet import Fernet
    cipher_suite = Fernet(settings.HDFS_SECRET_KEY)
    bytes_url = url.encode()
    # if isinstance(bytes_url, bytes):
    #     pass
    # else:
    #     bytes_url = base64.urlsafe_b64decode(url)
    cipher_text = cipher_suite.encrypt(bytes_url)
    return cipher_text


def encrypt_for_kylo(username, password_encrypted):
    # newhash = md5.new() # python2.7
    existing_key = username + password_encrypted
    # newhash.update(existing_key) # python2.7
    # value = newhash.hexdigest() # python2.7

    # newhash = hashlib.md5()
    # newhash.update(existing_key)
    # value = newhash.hexdigest()  # python3
    value = hashlib.sha256(existing_key.encode('utf-8')).hexdigest()  # python3
    return value
    # return value



def convert_fe_date_format(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d').strftime('%d/%m/%Y')


def get_timing_details(timing_type=None):
    timing_details = {
        "type": "crontab",
        "crontab": {
            "minute": "*",
            "hour": "*",
            "day_of_week": "*",
            "day_of_month": "*",
            "month_of_year": "*",
            "timezone": "Asia/Calcutta"
        },
        "interval": {
            "every": 60,
            "period": "seconds"
        }
    }
    if timing_type == 'daily':
        timing_details['crontab']['hour'] = 24
    if timing_type == 'weekly':
        timing_details['crontab']['day_of_week'] = 1
    elif timing_type == 'monthly':
        timing_details['crontab']['day_of_month'] = 1
    elif timing_type == 'hourly':
        timing_details['crontab']['hour'] = 1
    elif timing_type == 'every 15 minutes':
        timing_details['type'] = "interval"
        timing_details['interval']['every'] = 60 * 15  # 15 minutes in seconds
    elif timing_type == 'every 10 minutes':
        timing_details['type'] = "interval"
        timing_details['interval']['every'] = 60 * 10  # 15 minutes in seconds
    else:
        timing_details['type'] = "interval"

    return timing_details


def get_schedule(timing_type=None):
    timing_details = get_timing_details(timing_type)

    if timing_details['type'] == 'crontab':
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=timing_details['crontab'].get('minute', '*'),
            hour=timing_details['crontab'].get('hour', '*'),
            day_of_week=timing_details['crontab'].get('day_of_week', '*'),
            day_of_month=timing_details['crontab'].get('day_of_month', '*'),
            month_of_year=timing_details['crontab'].get('month_of_year', '*'),
            timezone=pytz.timezone(timing_details['crontab'].get('timezone', 'Asia/Calcutta'))
        )
        return schedule, 'crontab'
    else:
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=timing_details['interval'].get('every', 600),
            period=timing_details['interval'].get('period', 'seconds')
        )
        return schedule, 'interval'


def get_a_random_slug(num=5):
    import string
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(num))


def get_random_model_id(algo_name):
    algo_map = {
        "Random Forest": "RF",
        "XG Boost": "XG",
        "XGBoost": "XG",
        "Xgboost": "XG",
        "Logistic Regression": "LG",
        "Naive Bayes": "NB",
        "Decision Tree": "DT",
        "GBTree Regression": "GB",
        "Random Forest Regression": "RFR",
        "Linear Regression": "LR",
        "Neural Network (Sklearn)": "NN",
        "Neural Network (TensorFlow)": "TF",
        "Neural Network (PyTorch)": "PT",
        "LightGBM": "LGBM",
        "Ensemble": "EN",
        "Adaboost": "ADAB"
    }
    get_a_random_number = get_a_random_slug()
    return ''.join([algo_map[algo_name], '_', get_a_random_number])


def check_email_id(email=None):
    try:
        import re
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if (re.search(regex, email)):
            print("Valid Email")
            return True
        else:
            print("Invalid Email")
            return False
    except Exception as e:
        print(e)


def get_mails_from_outlook():
    # ###############################################################################################################
    # r = get_outlook_auth(settings.OUTLOOK_AUTH_CODE, settings.OUTLOOK_REFRESH_TOKEN, settings.OUTLOOK_DETAILS)
    # ###############################################################################################################
    from api.models import OutlookToken
    token = OutlookToken.objects.first()
    try:
        # result = r.json()
        # refresh_token = result['refresh_token']
        # access_token = result['access_token']

        print("Access token received.", token.access_token)
        ### Trigger mail receive action  ###
        result_message = get_outlook_mails(token.access_token)
        if 'status' in result_message:
            print("result message not found.")
            return {'status': 'FAILED', 'err': result_message['err']}
        else:
            print("got result message")
            return result_message
    except Exception as err:
        return {'status': 'FAILED', 'err': err}

def get_outlook_auth(auth_code, refresh_token, outlook_data):
    token_url = 'https://login.microsoftonline.com/' + outlook_data['tenant_id'] + '/oauth2/v2.0/token'

    print(token_url)

    post_data_auth_code = {
        'grant_type': 'authorization_code',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        'code': auth_code,
        'redirect_uri': outlook_data['redirect_uri'],
        'scope': settings.OUTLOOK_SCOPES,
        'client_id': outlook_data['client_id'],
        'client_secret': outlook_data['client_secret']
    }
    post_data_refresh_token = {'grant_type': 'refresh_token',
                               # 'code': auth_code,
                               'redirect_uri': outlook_data['redirect_uri'],
                               'scope': 'https://graph.microsoft.com/.default',
                               'refresh_token': refresh_token,
                               'client_id': outlook_data['client_id'],
                               'client_secret': outlook_data['client_secret']
                               }
    if refresh_token is not None:
        r = requests.post(token_url, data=post_data_refresh_token)
    else:
        r = requests.post(token_url, data=post_data_auth_code)

    return r


def get_outlook_mails(access_token):
    # access_token = access_token
    # If there is no token in the session, redirect to home
    try:
        if not access_token:
            print("Access token not found")
            return None
        else:
            info_dict = {}
            from datetime import datetime, timedelta
            import time
            t1 = time.time()
            last_seen = time_conversion(t1)
            info_dict = get_my_messages(access_token, info_dict, last_seen)
            return info_dict
    except Exception as err:
        print(err)
        return {'status': 'FAILED', 'err': err}

def time_conversion(t1):
    from datetime import datetime, timedelta
    import time
    dt_object = datetime.fromtimestamp(t1)
    print(dt_object)
    dt_object = dt_object - timedelta(hours=0, minutes=10)
    dt_object = str(dt_object)
    dt_object = dt_object.replace(' ', 'T')
    dt_object = dt_object[:-7]
    dt_object = dt_object + 'Z'
    return dt_object


def get_my_messages(access_token, info_dict, last_seen=None, message_id=None, id_element=None):
    # get_messages_url = graph_endpoint.format('/me/messages?$select=sender,subject')
    graph_endpoint = 'https://graph.microsoft.com/v1.0'
    if message_id is None and id_element is None:
        get_messages_url = graph_endpoint + '/me/messages/'
    else:
        get_messages_url = graph_endpoint + '/me/messages/' + str(message_id) + '/attachments'

    # get_messages_url = graph_endpoint+'/me/messages/AAMkADI5ODU5MDllLTM5ZmQtNDk1Zi1iNzcxLTRmN2JlZjk2Zjc4NQBGAAAAAADGdZQ1rmo2RYpnFmn4OfBhBwAMw_MOyTI_RbDqXK9C1L0dAAAA4WFOAAB_HCNKDCWjR5dEFB9ADyJdAAEafcuCAAA=/attachments'
    # Use OData query parameters to control the results
    #  - Only first 10 results returned
    #  - Only return the ReceivedDateTime, Subject, and From fields
    #  - Sort the results by the ReceivedDateTime field in descending order
    '''
    it is taking Only top 10 or all since given time
    '''
    if last_seen is None:
        query_parameters = {
            # '$top': '1',
            # '$filter': 'isRead eq false',
            # '$select': 'receivedDateTime,subject,from',
            # '$orderby': 'receivedDateTime DESC'
        }
        # '$select': 'receivedDateTime,subject,from',
        # '$orderby': 'receivedDateTime DESC'}
    else:
        query_parameters = {
            # '$top': '1',
            '$filter': 'isRead eq false and  receivedDateTime gt ' + last_seen,
            # '$select': 'receivedDateTime,subject,from',
            # '$orderby': 'receivedDateTime DESC'
        }
        # '$select': 'receivedDateTime,subject,from',
        # '$orderby': 'receivedDateTime DESC'}

    r = make_api_call('GET', get_messages_url, access_token, parameters=query_parameters)
    # settings.OUTLOOK_LAST_SEEN=str(datetime.datetime.now())
    # print r.text
    try:
        if r.status_code == requests.codes.ok:
            if message_id is None and id_element is None:
                jsondata = r.json()
                for i in range(len(jsondata['value'])):
                    if jsondata['value'][i]['hasAttachments']:
                        u_id = str(datetime.datetime.now())
                        info_dict[u_id] = {}
                        info_dict[u_id]['subject'] = jsondata['value'][i]['subject']
                        info_dict[u_id]['mail'] = jsondata['value'][i]['bodyPreview']
                        info_dict[u_id]['mail'] = info_dict[u_id]['mail'].replace('\r', '').replace('\n', '||')
                        info_dict[u_id]['emailAddress'] = jsondata['value'][i]['from']
                        id = jsondata['value'][i]['id']

                        if ('sub-label')or('Sub-label') and ('target')or('Target') in info_dict[u_id]['mail']:
                            # check = re.search(r'sub-label: (\S+)',info_dict[u_id]['mail'].lower())
                            # if check:
                            # info_dict[u_id]['sub_target'] = check.group(1).replace('"','')
                            # info_dict[u_id]['sub_target'] = check.group(1).replace("'","")
                            for info in info_dict[u_id]['mail'].split('||'):
                                if 'sub-label' in info:
                                    info_dict[u_id]['sub_target'] = info.replace('sub-label', '').replace(':', '').strip()
                                elif 'Sub-label' in info:
                                    info_dict[u_id]['sub_target'] = info.replace('Sub-label', '').replace(':', '').strip()
                                elif 'target' in info:
                                    info_dict[u_id]['target'] = info.replace('target', '').replace(':', '').strip()
                                elif 'Target' in info:
                                    info_dict[u_id]['target'] = info.replace('Target', '').replace(':', '').strip()
                        '''if 'target' in info_dict[u_id]['mail'].lower():
                            # check = re.search(r'target: (\S+)',info_dict[u_id]['mail'].lower())
                            # if check:
                            # info_dict[u_id]['target'] = check.group(1).replace('"','')
                            # info_dict[u_id]['target'] = info_dict[u_id]['target'].replace("'","")
                            info_dict[u_id]['target'] = info_dict[u_id]['mail'].split('||')[0].replace('target: ',
                                                                                                     '').strip()'''
                        '''
                        if 'sub-label' in info_dict[u_id]['mail'].lower():
                            check = re.search(r'sub-label: (\S+)', info_dict[u_id]['mail'].lower())
                            if check:
                                info_dict[u_id]['sub_target'] = check.group(1).replace('"', '')
                                info_dict[u_id]['sub_target'] = check.group(1).replace("'", "")

                        if 'target' in info_dict[u_id]['mail'].lower():
                            check = re.search(r'target: (\S+)', info_dict[u_id]['mail'].lower())
                            if check:
                                info_dict[u_id]['target'] = check.group(1).replace('"', '')
                                info_dict[u_id]['target'] = info_dict[u_id]['target'].replace("'", "")
                        '''
                        get_my_messages(access_token, info_dict, message_id=id, id_element=u_id)
                    else:
                        u_id = str(datetime.datetime.now())
                        info_dict[u_id] = {}
                        info_dict[u_id]['subject'] = jsondata['value'][i]['subject']
                        info_dict[u_id]['mail'] = jsondata['value'][i]['bodyPreview']
                        if 'from' in list(jsondata['value'][i].keys()):
                            info_dict[u_id]['emailAddress'] = jsondata['value'][i]['from']
                        else:
                            info_dict[u_id]['emailAddress'] = 'External Sender'
            else:
                print("Downloading Attachments .")
                jsondata = r.json()
                try:
                    for i in range(len(jsondata['value'])):

                        # subject = jsondata['value'][i]['subject']
                        # mail = jsondata['value'][i]['bodyPreview']
                        # emailAddress = jsondata['value'][i]['emailAddress']
                        # print subject, mail, emailAddress
                        if jsondata['value'][i]["name"][-3:] == 'csv':
                            f = open('config/media/datasets/' + id_element + '_' + jsondata['value'][i]["name"], 'w+b')
                            f.write(base64.b64decode(jsondata['value'][i]['contentBytes']))
                            f.close()
                            if 'train' in jsondata['value'][i]["name"].lower():
                                info_dict[id_element]['train_dataset'] = id_element + '_' + jsondata['value'][i]["name"]
                            if 'test' in jsondata['value'][i]["name"].lower():
                                info_dict[id_element]['test_dataset'] = id_element + '_' + jsondata['value'][i]["name"]

                except Exception as e:
                    print(e)
            return info_dict
        else:
            return None
            # return "{0}: {1}".format(r.status_code, r.text)
    except Exception as err:
        print(err)
        return {'status': 'FAILED', 'err': err}


# Generic API Sending
def make_api_call(method, url, token, payload=None, parameters=None):
    '''
    establishes connection with the API
  '''
    # Send these headers with all API calls
    headers = {'Authorization': 'Bearer %s' % (token)}
    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    # request_id = str(uuid.uuid4())
    # instrumentation = { 'client-request-id' : request_id,
    #                   'return-client-request-id' : 'true' }

    # headers.update(instrumentation)
    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers=headers, params=parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers=headers, params=parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(url, headers=headers, data=json.dumps(payload), params=parameters)
    elif (method.upper() == 'POST'):
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, data=json.dumps(payload), params=parameters)

    return response


def generate_word_cloud_image(slug, temp_articles_list, date):
    import pandas as pd
    import collections
    from wordcloud import WordCloud, STOPWORDS
    import os
    articles_df = pd.DataFrame(temp_articles_list)
    articles_df = articles_df.sort_values(by='date', ascending=False)

    articles_df['date'] = articles_df.date.apply(lambda x: x[0:4] + "-" + x[4:6] + "-" + x[6:8])
    temp_date_list = articles_df['date'].tolist()
    temp_date_list = list(dict.fromkeys(temp_date_list))
    temp_date_list.sort(reverse=True)

    enddate = str(date)
    index_of_end_date = temp_date_list.index(enddate)
    start_date = temp_date_list[index_of_end_date + 1]
    pandasDf1 = articles_df[(articles_df.date >= start_date) & (articles_df.date <= enddate)]
    pandasDf1.reset_index(drop=True, inplace=True)

    words_freq_positive = []
    words_freq_negative = []
    words_freq_neutral = []

    if pandasDf1 is not None and len(pandasDf1) > 0:
        for index, datarow in pandasDf1.iterrows():
            for textrow in datarow["keywords"]:
                if textrow["sentiment"]["label"] == 'positive':
                    words_freq_positive.append(textrow['text'])
                elif textrow["sentiment"]["label"] == 'negative':
                    words_freq_negative.append(textrow['text'])
                elif textrow["sentiment"]["label"] == 'neutral':
                    words_freq_neutral.append(textrow['text'])
                else:
                    pass

        words_freq_positive = collections.Counter(words_freq_positive)
        words_freq_positive = sorted(words_freq_positive.items(), key=lambda x: x[1], reverse=True)
        words_freq_positive = dict(words_freq_positive)

        words_freq_negative = collections.Counter(words_freq_negative)
        words_freq_negative = sorted(words_freq_negative.items(), key=lambda x: x[1], reverse=True)
        words_freq_negative = dict(words_freq_negative)

        words_freq_neutral = collections.Counter(words_freq_neutral)
        words_freq_neutral = sorted(words_freq_neutral.items(), key=lambda x: x[1], reverse=True)
        words_freq_neutral = dict(words_freq_neutral)

        final_dict = words_freq_positive.copy()
        final_dict.update(words_freq_negative.items())
        words_freq = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)
        words_freq = dict(words_freq[:25])
        word_to_color = dict()

        pos_words = list(words_freq_positive.keys())
        for word in pos_words:
            word_to_color[word] = '#00ff00'  # green

        neg_words = list(words_freq_negative.keys())
        for word in neg_words:
            word_to_color[word] = '#ff0000'  # red

        def color_func(word, *args, **kwargs):
            try:
                color = word_to_color[word]
            except KeyError:
                color = '#000000'
            return color

        wc = WordCloud(width=500, height=500, background_color='white', min_font_size=10, color_func=color_func)
        wc.generate_from_frequencies(words_freq)
        # path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + slug + "/wordcloud.png"
        try:
            os.mkdir(settings.MEDIA_ROOT + "/" + slug)
        except FileExistsError:
            pass
        path = settings.MEDIA_ROOT + "/" + slug + "/wordcloud.png"
        wc.to_file(path)
        return path
    else:
        return None
