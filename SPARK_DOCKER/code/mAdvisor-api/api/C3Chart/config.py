
# Chart
PADDING_TOP = 40
CHART_HEIGHT = 340
CHART_WIDTH = 200

# Title
TITLE = None

# Data
DEFAULT_CHART_TYPE = 'line'
CHART_TYPE_SCATTER = 'scatter'
CHART_TYPE_PIE = 'pie'
CHART_TYPE_DONUT = 'donut'
DEFAULT_DATA_TYPE = 'columns'
DATA_TYPE_JSON = 'json'

# X axis
X_DEFAULT_TYPE = 'category'
X_TYPE_TIMESERIES = 'timeseries'
X_TYPE_INDEX = 'index'
X_AXIS_HEIGHT = 55
X_TICKS_ROTATION = -45
X_TICK_MULTILNE = False
X_LABEL_DEFAULT_POSITION = 'outer-center'
X_LABEL_DEFAULT_TEXT = ''
X_COLUMN_NAME = 'x'
X_EXTENT_DEFAULT = 10
X_TICK_FIT = False


# Y axis
Y_LABEL_DEFAULT_TEXT = ''
Y_LABEL_DEFAULT_POSITION = 'outer-middle'
Y_TICK_MULTILNE = True
# Y2 axis
Y2_LABEL_DEFAULT_TEXT = ''
Y2_LABEL_DEFAULT_POSITION = 'outer-middle'
Y2_TICK_MULTILNE = True

# Point
POINT_RADIUS = 3
MIN_DATA_COUNT = 30

# Subchart
SUBCHART_X_TICK_THRESHOLD = 14

# Colors
PATTERN1 = [
    '#00AEB3', '#f47b16', '#7c5bbb',
    '#dd2e1f', '#00a0dc', '#efb920',
    '#e2247f', '#7cb82f', '#86898c',
    '#0fc4b5' , '#005662' , '#148071' , '#6cba86' , '#bcf3a2'
]


PATTERN = ['#0fc4b5' , '#005662' , '#148071' , '#6cba86' , '#bcf3a2']
SECOND_FLIP_PATTERN = ['#005662' , '#0fc4b5', '#148071' , '#6cba86' , '#bcf3a2']

COLOR_MAPPING = {
    'red': 'red_x',
    'blue': 'blue_x',
    'green': 'green_x',
    'orange': 'orange_x',
    'yellow': 'yellow_x'
}

# tooltip
FUNCTION_TOOLTIP = "set_toolip"
FUNCTION_NEGATIVE_COLOR = "set_negative_color"
FUNCTION_COLOR = "set_color"

# d3.format
D3_FORMAT_EMPTY = ''
D3_FORMAT_MILLION = '.2s'
D3_FORMAT_DOLLAR = '$'

# bar width
SMALL_BAR_WIDTH = 40
SMALL_BAR_RATIO = 0.2
DEFAULT_BAR_WIDTH = 0.5

USE_MULTILINE_LABELS = False

METADATA_CHART_LEVEL_COUNT = 100
