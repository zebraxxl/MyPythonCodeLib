# -*- coding: utf-8 -*-
from StringIO import StringIO
import os
import sys
import math

__author__ = 'zebraxxl'
__CSI = '\033['
__escape_end = 'm'
__all_to_default = __CSI + '0;39;49' + __escape_end

__escape_flags = {
    'bold': '1',
    'dim': '2',
    'italic': '3',
    'underline': '4',
    'blink': '5',
    'reverse': '7',
    'hidden': '8',
    'strike': '9',
}

__colors = {
    'black': '0',
    'red': '1',
    'green': '2',
    'yellow': '3',
    'brown': '3',
    'purple': '5',
    'cyan': '6',
    'grey': '7',
    'white': '8',
    'default': '9',
}


def __color_hex_2_int(v):
    try:
        return int(v, 16)
    except:
        return 0


def __make_color(color):
    # TODO: gray scale support
    if color[0] == '#':
        color = color[1:]
        if len(color) == 6:
            r = __color_hex_2_int(color[:2])
            g = __color_hex_2_int(color[2:4])
            b = __color_hex_2_int(color[4:])
        elif len(color) == 3:
            r = __color_hex_2_int(color[0]) << 8
            g = __color_hex_2_int(color[1]) << 8
            b = __color_hex_2_int(color[2]) << 8
        else:
            return __colors['default']
        if r == g == b:
            return '8;05;' + str((15 if r > 239 else math.floor(r / 10)) + 232)
        return '8;05;' + str(int(16 + 36 * math.floor(r / 51.0) + 6 * math.floor(g / 51.0) + math.floor(b / 51.0)))
    else:
        if color in __colors:
            return __colors[color]
    return __colors['default']


def __make_escape(format_string, mode):
    if mode == 'flat':
        return ''

    params = format_string.split(',')
    result = list()
    for flag in __escape_flags:
        if flag in params:
            result.append(__escape_flags[flag])
    for p in params:
        param = p.strip()
        if param[0] == 'f':
            result.append('3' + __make_color(param[1:]))
        elif param[0] == 'b':
            result.append('4' + __make_color(param[1:]))

    return __CSI + ';'.join(result) + 'm'


# "Text{bold,dim,}Text"
# "{fred,#ff0011}"
def color_output(v, output=sys.stdout, force_color=False):
    tmp = StringIO()

    if force_color:
        mode = '256'
    else:
        if hasattr(output, 'isatty') and not output.isatty():
            mode = 'flat'
        elif '256color' in os.environ.get('TERM', ''):
            mode = '256'
        else:
            mode = '16'  # flat, 16 or 256

    i = 0
    while i < len(v):
        if v[i] == '{':
            i += 1
            if v[i] == '{':
                tmp.write('{')
                i += 1
            else:
                end = v.find('}', i)
                if end == -1:
                    tmp.write('{')
                else:
                    format_string = v[i:end]
                    tmp.write(__make_escape(format_string.lower(), mode))
                    i = end + 1
        else:
            tmp.write(v[i])
            i += 1

    sufix = __all_to_default if mode != 'flat' else ''
    output.write(tmp.getvalue() + sufix)
