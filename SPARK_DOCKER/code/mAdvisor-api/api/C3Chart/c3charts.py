'''
C3Chart is a python wrapper for c3.js charts. It has no dependencies other than standard python libraries.

Usage:
=====

    import C3Chart
    C3Chart.generate(config)
'''
from __future__ import print_function
from __future__ import division

from builtins import str
from builtins import object
from past.utils import old_div
__author__ = 'Ankush Patel'

import json
from .config import *


class C3Chart(object):

    def __init__(self, **kwargs):
        self._bindto = '#{}'.format(kwargs.get('bindto', 'chart'))
        self._data = None
        self._axis = {}
        self._grid = None
        self._region = None
        self._legend = None
        self._tooltip = None
        self._subchart = None
        self._point = None
        self._zoom = None
        self._color = None
        self._size = {
            'height': CHART_HEIGHT,
            # 'width':
        }
        self._type = kwargs.get('chart_type', DEFAULT_CHART_TYPE)
        self._x_label_text = kwargs.get('x_label_text', X_LABEL_DEFAULT_TEXT)
        self._y_label_text = kwargs.get('y_label_text', Y_LABEL_DEFAULT_TEXT)
        self._x_column_name = kwargs.get('x_column_name', X_COLUMN_NAME)
        self._data_data = kwargs.get('data', None)
        self._data_type = kwargs.get('data_type', DEFAULT_DATA_TYPE)
        self._x_type = kwargs.get('x_type', X_DEFAULT_TYPE)
        self._x_height = X_AXIS_HEIGHT
        self._x_label_rotation = X_TICKS_ROTATION
        self._point_radius = POINT_RADIUS
        self._title = {'text': kwargs.get('title', TITLE)}
        self._x_index_in_column_data = None
        self._number_of_x_ticks = None
        self._number_of_y_data = None
        self._total_data_count = None
        self._donutChartFormat = kwargs.get('yAxisNumberFormat',".2s")
        self._pieChartFormat = kwargs.get('yAxisNumberFormat',".2s")

        self.point_details_passed_in_arguments = None
        if 'point' in kwargs:
            self.point_details_passed_in_arguments = kwargs.get('point')

        self.set_data_and_type()
        self.set_basic_chart_setting()

    def _set_title(self, title):
        self._title = {'text': title}

    def set_data_and_type(self):
        type = 'bar'
        if isinstance(self._type, tuple) or isinstance(self._type, list):
            type = self._type[0]
        elif isinstance(self._type, str):
            type = self._type
        self._data = {
            self._data_type: self._data_data,
            'type': type
        }
        if self._data_type == DEFAULT_DATA_TYPE:
            self._data['x'] = self._x_column_name
        self.other_useful_info()

    def other_useful_info(self):
        if self._data_type == DEFAULT_DATA_TYPE:
            self._x_index_in_column_data = self.find_x_index_in_column_data()
        self._x_max_string_length = self.find_and_set_length_of_max_string_in_x()
        self._number_of_x_ticks = self.find_and_set_number_of_x_ticks()
        self._number_of_y_data = self.find_and_set_number_of_y_data()
        self._total_data_count = self.find_and_set_total_data_count()

    def set_keys_in_data_field(self):
        keys = []
        for data in self._data_data:
            keys = list(set(keys + list(data.keys())))

        keys.remove(self._x_column_name)
        self._data['keys'] = {'value': keys, 'x':self._x_column_name}

    def set_x_axis(self,
                   column_name=X_COLUMN_NAME):
        self._data['x'] = column_name

    def hide_x_axis(self):
        self._data['x'] = None

    def hide_x_axis_line(self):

        if 'x' in self._axis:
            self._axis['x']['show'] = False
        else:
            self._axis['x'] = {
                "show": False
            }

    def set_basic_chart_setting(self,
                                padding_top=PADDING_TOP):
        self._padding = {
            'top': padding_top,
            # 'right': 100,
            # 'bottom': 40,
            # 'left': 100
        }

    def set_basic_axis(self):

        if USE_MULTILINE_LABELS:
            X_TICK_MULTILNE = True
        else:
            X_TICK_MULTILNE = False

        self._axis = {
            'x':
                {
                    'tick':
                        {
                            'fit': X_TICK_FIT,
                            'rotate': self._x_label_rotation,
                            'multiline': X_TICK_MULTILNE,
                            # 'count': 15
                        },
                    'height': self._x_height,
                    'label':
                        {
                            'text': self._x_label_text,
                            'position': X_LABEL_DEFAULT_POSITION
                        },
                    'type': self._x_type
                },
            'y':
                {
                    'tick':
                        {
                            'outer': False,
                            # 'count': 7,
                            'multiline': Y_TICK_MULTILNE
                        },
                    'label':
                        {
                            'text': self._y_label_text,
                            'position': Y_LABEL_DEFAULT_POSITION
                        }
                }
        }

        if self._data_type == DATA_TYPE_JSON:
            self.set_keys_in_data_field()

    def set_basic_legends(self):
        if self._number_of_y_data is None:
            self._number_of_y_data = self.find_and_set_number_of_y_data()

        if self._number_of_y_data > 1:
            self._legend = {
                'show': True
            }
        else:
            self.hide_basic_legends()

    def hide_basic_legends(self):
        self._legend = {
            'show': False
        }

    def show_basic_legends(self):
        self._legend = {
            'show': True
        }

    def show_legends_at_right(self):
        self._legend = {
            'show':True,
            'position':'right'
        }

    def set_basic_grid_lines(self):
        self._grid = {
            'y': {
                'show': True
            },
            'x': {
                'show': True,
            }
        }

    def set_basic_color_pattern(self,
                                pattern=PATTERN):
        self._color = {
            'pattern': pattern
        }

    def set_basic_subchart(self):
        self._subchart = {
            'show': True
        }
        self._axis['x']['extent'] = [0,X_EXTENT_DEFAULT]

        self._size = {
                  # 'height': CHART_HEIGHT + X_AXIS_HEIGHT
                  'height': CHART_HEIGHT + self._x_height + 60
                  # 'height': CHART_HEIGHT
                }

    def hide_subchart(self):
        self._subchart = None
        self._axis['x']['extent'] = None
        self._size = {
            'height': CHART_HEIGHT
        }

    def set_basic_tooltip(self):
        self._tooltip = {
            'show': True
        }

    def set_height_between_legend_and_x_axis(self):
        if USE_MULTILINE_LABELS:
            import math
            if self._x_max_string_length:
                self._x_height = abs(math.sin(math.radians(self._x_label_rotation))) * \
                                 5 * \
                                 self._x_max_string_length + X_AXIS_HEIGHT
            else:
                self._x_height = X_AXIS_HEIGHT
        else:
            self._x_height = X_AXIS_HEIGHT + 40

    def find_and_set_length_of_max_string_in_x(self):
        data = self._data_data
        if self._x_column_name and self._data_type == DATA_TYPE_JSON:
            return max([len(d.get(self._x_column_name)) for d in data])
        elif self._data_type == DEFAULT_DATA_TYPE:
            x_data = data[self._x_index_in_column_data]
            if len(x_data) > 0:
                first_item = x_data[1]
                import math
                if isinstance(first_item, int) or isinstance(first_item, float):
                    return len(str(int(abs(max([d for d in x_data[1:]])))))

            return max([len(str(d)) for d in x_data[1:]])

    def find_and_set_number_of_x_ticks(self):
        data = self._data_data
        if self._data_type == DATA_TYPE_JSON:
            return len(data)
        elif self._data_type == DEFAULT_DATA_TYPE:
            return len(data[self._x_index_in_column_data])

    def find_and_set_number_of_y_data(self):
        return len(self._data_data) - 1

    def find_and_set_total_data_count(self):
        count = 0
        for d in self._data_data:
            count += len(d)
        return count

    def find_x_extent(self):
        if self._number_of_x_ticks < X_EXTENT_DEFAULT:
            return [0,5]
        else:
            return [0, old_div(self._number_of_x_ticks,10)]

    def find_x_index_in_column_data(self):
        for index, data in enumerate(self._data_data):
            if data[0] == self._x_column_name:
                return index
        return 0

    def set_subchart_after(self):
        if self._number_of_x_ticks > SUBCHART_X_TICK_THRESHOLD:
            self.set_basic_subchart()

    def rotate_axis(self):
        if self._axis:
            self._axis['rotated'] = True
            self._axis['x']['label']['position'] = Y_LABEL_DEFAULT_POSITION
            # self._axis['x']['label']['text'] = Y_LABEL_DEFAULT_TEXT
            self._axis['x']['tick']['rotate'] = 0
            self._axis['x']['tick']['fit'] = True
            # self._axis['y']['label']['position'] = X_LABEL_DEFAULT_POSITION
            # self._axis['y']['label']['text'] = X_LABEL_DEFAULT_TEXT
            self.set_multiline_x()

    def set_y_axis(self, y_name='y'):
        if self._data:
            self._data['axes'] = {
                y_name: 'y',
            }

    def set_another_y_axis(self,
                           y2_name=None):
        if y2_name is None:
            raise Exception('Dual axis: Y2 axis has to be assigned a column.')

        if self._axis:
            self._axis['y2'] = {
                "show": True,
                "label": {
                    "text": Y2_LABEL_DEFAULT_TEXT,
                    "position": Y2_LABEL_DEFAULT_POSITION
                },
                "tick": {
                    "count": 7,
                    "multiline": True
                }
            }
        if self._data:
            self._data['axes'] = {
                y2_name: 'y2',
            }

    def set_x_type_to_timeseries(self):
        if self._axis:
            self._axis['x']['type'] = X_TYPE_TIMESERIES

    def set_x_type_as_index(self):
        if self._axis:
            self._axis['x']['type'] = X_TYPE_INDEX

    def set_axis_label_text(self,
                            x_label=X_LABEL_DEFAULT_TEXT,
                            y_label=Y_LABEL_DEFAULT_TEXT,
                            y2_label=Y2_LABEL_DEFAULT_TEXT):

        if self._axis:
            self._axis['x']['label']['text'] = x_label
            self._axis['y']['label']['text'] = y_label
            if 'y2' in list(self._axis.keys()):
                self._axis['y2']['label']['text'] = y2_label

    def set_axis_label_simple(self, label_text):

        axis_names = ['x', 'y', 'y2']

        for axis_name in axis_names:
            if axis_name in label_text:
                if axis_name in self._axis:
                    self._axis[axis_name]['label']['text'] = label_text.get(axis_name, "")

    def get_point_radius(self):

        if self.point_details_passed_in_arguments is not None:
            return self.point_details_passed_in_arguments

        if self._total_data_count is None:
            self._total_data_count = self.find_and_set_total_data_count()

        count = self._total_data_count
        if count < 30:
            return 10
        elif count < 60:
            return 8
        elif count < 120:
            return 6
        elif count < 240:
            return 5
        else:
            return 4

    def set_scatter_chart(self):

        self._point_radius = self.get_point_radius()

        self._point = {
            'r': self._point_radius
        }
        if self._data:
            self._data['type'] = CHART_TYPE_SCATTER

    def set_line_chart(self):
        if self._data:
            self._data['type'] = "line"

    def set_bar_chart(self):
        if self._data:
            self._data['type'] = "bar"

    def set_pie_chatter(self):
        if self._data:
            self._data['type'] = CHART_TYPE_PIE

    def set_donut_chart(self):
        if self._data:
            self._data['type'] = CHART_TYPE_DONUT

    def set_x_tick_rotation(self, rotation=X_TICKS_ROTATION):
        if self._axis:
            if self._axis['x']:
                self._axis['x']['tick']['rotate'] = rotation

    def set_multiline_x(self):
        if self._axis['x']:
            if 'tick' in list(self._axis.keys()):
                self._axis['x']['tick']['multiline'] = True
            else:
                self._axis['x']['tick'] = {
                    'multiline': True
                }

    def hide_multipline_x(self):
        pass

    # TODO: make it proper code. remove unnecessary checks. better ask from backend
    def add_additional_grid_line_at_zero(self, datas=None):

        negative = False
        if datas is None:
            datas = self._data_data
            for data in datas:
                for d in data:
                    if (isinstance(d, int) or isinstance(d, float)) and d < 0:
                        negative = True
                        break
        else:
            for d in datas:
                if (isinstance(d, int) or isinstance(d, float)) and d < 0:
                    negative = True
                    break

        if negative is False:
            return ""

        zero_data = {"value": 0, "text": '',"class":"zeroAxisGrid", 'position': 'start'}
        if self._grid:
            if 'y' in self._grid:
                if 'lines' in self._grid['y']:
                    if isinstance(self._grid['y']['lines'], list):
                        self._grid['y']['lines'].append(zero_data)
                    else:
                        self._grid['y']['lines'] = [zero_data]
                else:
                    self._grid['y']['lines'] = [zero_data]
            else:
                self._grid['y'] = {
                    "lines": [zero_data]
                }
        else:
            self._grid = {
                'y': {
                    "lines": [zero_data]
                }
            }
        # self.hide_x_axis_line()

    def remove_y_label_count(self):
        self._axis['y']['tick']['count'] = None

    def add_groups_to_data(self, list_of_y):
        self._data['groups'] = [list_of_y]

    # function related
    def add_tooltip_for_scatter(self):

        if self._tooltip:
            self._tooltip['contents'] = 'set_tooltip'
        else:
            self._tooltip = {
                'show': True,
                'contents': 'set_tooltip'
            }

    def set_tick_format_x(self, set_x=D3_FORMAT_MILLION):
        if 'x' in self._axis:
            if 'tick' in self._axis['x']:
                self._axis['x']['tick']['format'] = set_x
            else:
                self._axis['x']['tick'] = {
                    'format': set_x
                }

    def set_d3_format_y(self, set_y=D3_FORMAT_MILLION):
        self._axis['y']['tick']['format'] = set_y

    def set_d3_format_y2(self, set_y2=D3_FORMAT_MILLION):
        if self._axis['y2']:
            y2_json = self._axis['y2']
            tick_conf = y2_json['tick']
            new_tick_format = {
                'format': set_y2
            }
            tick_conf.update(new_tick_format)
            y2_json['tick'] = tick_conf
            self._axis['y2'] = y2_json

    def set_tooltip_format(self, set_format=D3_FORMAT_MILLION):
        if self._tooltip:
            if 'format' in self._tooltip:
                self._tooltip['format']['title'] = set_format
            else:
                self._tooltip['format'] = {
                    'title': set_format
                }

    def add_negative_color(self):
        self._data['color'] = FUNCTION_COLOR
        pass

    def add_new_chart_on_a_data(self, chart_type='line', data_y='y'):
        if self._data:
            self._data['types'] = {
                data_y: chart_type
            }
            pass

    def add_new_chart_on_a_data_list(self, types=None):
        if self._data:
            if types is not None:
                self._data['types'] = types

    def hide_label(self, axis='x'):
        if self._axis:
            self._axis[axis]['label'] = None

    def hide_x_tick(self):
        tick_data = {
            'values': []
        }
        if self._axis:
            if 'x' in self._axis:
                if 'tick' in self._axis['x']:
                    if 'values' in self._axis['x']['tick']:
                        self._axis['x']['tick']['values'] = []
                    else:
                        self._axis['x']['tick'] = tick_data
                else:
                    self._axis['x'] = {
                        'tick': tick_data
                    }
            else:
                self._axis = {
                    'x' : {
                        'tick': tick_data
                    }
                }

    def set_xs(self, xs):
        self._data['x'] = None
        self._data['xs'] = xs

    def remove_x_from_data(self):
        self._data['x'] = None

    def remove_vertical_grid_from_chart_data(self):
        self._grid['x']['show'] = False

    def set_x_type(self, to=X_DEFAULT_TYPE):
        self._x_type = to

    def set_name_to_data(self, legend):
        new_legend = {}
        changes = {
            'x': 'k1',
            'y': 'k2',
            'y2': 'k3'
        }

        for val in legend:
            if val in ['x', 'y', 'y2']:
                new_legend[changes[val]] = legend[val]

        new_legend.update(legend)
        if self._data:
            self._data['names'] = new_legend

    def set_basic_bar_chart(self, bar_width_ration=DEFAULT_BAR_WIDTH):

        if self._type == 'bar':
            if self._number_of_x_ticks is not None and \
                    self._number_of_y_data is not None:
                if self._number_of_x_ticks * self._number_of_y_data < 11:
                    bar_width_ration = SMALL_BAR_WIDTH
                    return {
                        'width': bar_width_ration
                    }
        return  {
            'width': {
                    'ratio': bar_width_ration
            }
        }

    def get_some_related_info_printed(self):
        print("x max string length", self._x_max_string_length)
        print("x length", self._x_height)
        print("chart", self._size)
        print("legend", self._legend)
        print("y_count", self._number_of_y_data)
        print("total", self._total_data_count)

    def set_all_basics(self):
        self.set_height_between_legend_and_x_axis()
        self.set_basic_axis()
        self.set_basic_legends()
        self.set_basic_grid_lines()
        self.set_basic_color_pattern()
        self.set_basic_tooltip()
        self.set_subchart_after()
        self.set_d3_format_y()

    def special_bar_chart(self):
        self.set_basic_axis()
        self.hide_basic_legends()
        self.set_basic_grid_lines()
        self.set_basic_color_pattern()
        self.set_basic_tooltip()
        self.set_x_tick_rotation(0)
        self.set_d3_format_y()

    def get_json(self):

        if self._title == 'Unnamed Chart' or self._title is None:
            return {
                'data': self._data,
                'axis': self._axis,
                'tooltip': self._tooltip,
                'grid': self._grid,
                'legend': self._legend,
                'color': self._color,
                'padding': self._padding,
                # 'title': self._title,
                'subchart': self._subchart,
                'point': self._point,
                'bar': self.set_basic_bar_chart(),
                'size': self._size
            }
        else:
            return {
                'data': self._data,
                'axis': self._axis,
                'tooltip': self._tooltip,
                'grid': self._grid,
                'legend': self._legend,
                'color': self._color,
                'padding': self._padding,
                'title': self._title,
                'subchart': self._subchart,
                'point': self._point,
                'bar': self.set_basic_bar_chart(),
                'size': self._size
            }

    def add_tooltip_for_donut(self):
        self._tooltip={
            'format':{
            'title':"",
            'value':'.2s'
            }
            }
    def add_tooltip_for_pie(self):
        self._tooltip={
            'format':{
            'title':"",
            'value':'.2s'
            }
            }


class ScatterChart(C3Chart):

    def __init__(self, **kwargs):
        super(ScatterChart, self).__init__(**kwargs)
        self.set_all_basics()
        self.set_scatter_chart()
        self.hide_subchart()

class BarChart(C3Chart):

    def __init__(self, **kwargs):
        super(BarChart, self).__init__(**kwargs)


class PieChart(C3Chart):

    def __init__(self, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.hide_x_axis()
        self.set_pie_chatter()
        self._pie = {
            'title': "",
            'label': {
                'show' : False,
                'format' : None
            }
        }
        if self._pieChartFormat != None:
            self._pie["label"]["format"] = self._pieChartFormat
        # if self._title != None:
        #     self._pie["title"] = self._title["text"]

    def get_json(self):
        return {
            'data': self._data,
            'legend': self._legend,
            'color': self._color,
            'padding': self._padding,
            'title': self._title,
            'size': self._size,
            'pie': self._pie,
            'tooltip':self._tooltip,
        }


class DonutChart(C3Chart):

    def __init__(self, **kwargs):
        super(DonutChart, self).__init__(**kwargs)
        self.hide_x_axis()
        self.set_donut_chart()
        self._donut = {
            'title': "",
            'label': {
                'show' : False,
                'format' : None
            },
            'width':20
        }
        if self._donutChartFormat != None:
            self._donut["label"]["format"] = self._donutChartFormat
        #if self._title != None:
            #self._donut["title"] = self._title["text"]

    def get_json(self):

        return {
            'data': self._data,
            'legend': self._legend,
            'color': self._color,
            'padding': self._padding,
            # 'title': self._title,
            'size': self._size,
            'donut': self._donut,
            'tooltip':self._tooltip,
        }

class BarChartColored(C3Chart):
    pass
