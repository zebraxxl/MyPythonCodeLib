# -*- coding: utf-8 -*-
import sys

__author__ = 'zebraxxl'


class TablePrint(object):
    def __write_line(self, fill_symbol, split_symbol, output):
        output.write(split_symbol + ''.join(
            [fill_symbol + (fill_symbol * x) + fill_symbol + split_symbol for x in self.__rows_widths]
        ) + '\n')

    def __init__(self, field_names=None, max_width=None, rows_widths=None):
        self.__field_names = field_names
        self.__max_width = max_width
        self.__rows = list()
        self.__rows_widths = rows_widths
        self.__columns = len(field_names) if field_names is not None else 0
        self.__total_width = None

    def add_row(self, row):
        self.__rows.append(row)
        self.__columns = max(self.__columns, len(row))

    def write(self, output=sys.stdout, draw_blank_line=False):
        if self.__rows_widths is None:
            if self.__max_width is None:
                self.__max_width = 0xffffffff
            self.__rows_widths = [0] * self.__columns
            if self.__field_names is not None:
                for i in range(len(self.__field_names)):
                    self.__rows_widths[i] = len(str(self.__field_names[i]))
            for row in self.__rows:
                for i in range(len(row)):
                    self.__rows_widths[i] = max(self.__rows_widths[i], len(str(row[i])))
            total_width = sum(self.__rows_widths) + len(self.__rows_widths) * 2 + 2
            if total_width > self.__max_width:
                real_max_width = self.__max_width - len(self.__rows_widths) * 2 - 2
                rows_weight = [float(x) / float(real_max_width) for x in self.__rows_widths]
                for i in range(len(self.__rows_widths)):
                    self.__rows_widths[i] = int(float(self.__rows_widths[i]) * rows_weight[i])
                for i in range(len(self.__rows_widths)):
                    if self.__rows_widths[i] < 1:
                        self.__rows_widths[i] = 1
                        self.__rows_widths[self.__rows_widths.index(max(self.__rows_widths))] -= 1

        self.__total_width = sum(self.__rows_widths) + len(self.__rows_widths) * 2 + 2
        self.__write_line('-', '+', output)
        if self.__field_names is not None:
            if draw_blank_line:
                self.__write_line(' ', '|', output)
            for i in range(self.__columns):
                if i != 0:
                    output.write(' ')
                output.write('| ')
                if i < len(self.__field_names):
                    fmt = '{:^' + str(self.__rows_widths[i]) + '}'
                    output.write(fmt.format(str(self.__field_names[i])))
                else:
                    output.write(' ' * self.__rows_widths[i])
            output.write(' |\n')
            if draw_blank_line:
                self.__write_line(' ', '|', output)
            self.__write_line('-', '+', output)

        for row in self.__rows:
            if draw_blank_line:
                self.__write_line(' ', '|', output)
            for i in range(self.__columns):
                if i != 0:
                    output.write(' ')
                output.write('| ')
                if i < len(row):
                    fmt = '{:^' + str(self.__rows_widths[i]) + '}'
                    output.write(fmt.format(str(row[i])))
                else:
                    output.write(' ' * self.__rows_widths[i])
            output.write(' |\n')

            if draw_blank_line:
                self.__write_line(' ', '|', output)
            self.__write_line('-', '+', output)
