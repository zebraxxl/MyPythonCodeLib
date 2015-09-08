# -*- coding: utf-8 -*-
import sys
from terminal_size import get_terminal_size

__author__ = 'zebraxxl'


class ProgressBar(object):
    def __redraw(self):
        position = float(self.__value - self.__min) / float(self.__max - self.__min)
        if self.__show_as_percents:
            line_end = '%3s%%' % int(position * 100.0)
        else:
            max_length = len(str(self.__max))
            line_end = '%' + str(max_length) + 's / %s'
            line_end = line_end % (self.__value, self.__max)

        # String format: " |*******      | line_end "
        progress_width = self.__term_width - len(line_end) - 5     # Tree spaces and two line
        fill_count = int(position * progress_width)
        spaces_count = progress_width - fill_count

        self.__output.write(' [%s%s] %s\r' % ('#' * fill_count, ' ' * spaces_count, line_end))

    def __init__(self, min_value=0, max_value=100, start_value=None, show_as_percents=True, output=sys.stderr):
        self.__min = min_value
        self.__max = max_value
        self.__value = start_value if start_value is not None else min_value
        self.__show_as_percents = show_as_percents
        self.__output = output
        self.__term_width = get_terminal_size()[1]

    def start(self):
        self.__redraw()

    def update(self, new_value):
        self.__value = new_value
        self.__redraw()

    def end(self, hide_progress=False):
        if not hide_progress:
            self.__output.write('\n')
        else:
            self.__output.write(' ' * self.__term_width + '\r')
