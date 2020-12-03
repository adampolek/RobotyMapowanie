import math
import time
from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QColorConstants, QBrush, QMouseEvent, QFont
from PyQt5.QtWidgets import QGroupBox

from tile import Tile


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_bum(self):
        if self.value == 0:
            return Direction(2)
        elif self.value == 1:
            return Direction(3)
        elif self.value == 2:
            return Direction(0)
        elif self.value == 3:
            return Direction(1)

    def next(self):
        v = self.value + 1
        if v > 3:
            return Direction(0)
        return Direction(v)

    def previous(self):
        v = self.value - 1
        if v < 0:
            return Direction(3)
        return Direction(v)


class MyCanvas(QGroupBox):
    def __init__(self):
        super().__init__("Map Visualization")

        self.grid = []
        self.grid_map = []
        self.figures = []
        self.pos1 = (0, 0)
        self.pos2 = (0, 0)
        self.start_point = (0, 0)
        self.row, self.column = 1, 1
        self.is_start = False
        self.movement_direction = Direction.DOWN

    def paintEvent(self, event):
        self.width_size = int(self.width() / 30)
        self.height_size = int(self.height() / 20)
        width = int(self.width() / self.width_size) * self.width_size
        height = int(self.height() / self.height_size) * self.height_size
        qp = QPainter()
        qp.begin(self)
        for index in range(int(width / 30) + 1):
            qp.drawLine(index * self.width_size, 0, index * self.width_size, height)
            qp.drawLine(0, index * self.height_size, width, index * self.height_size)
        if self.start_point != (0, 0):
            qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            qp.drawEllipse(self.start_point[0] * self.width_size + 8, self.start_point[1] * self.height_size + 8,
                           int(self.width_size / 2), int(self.height_size / 2))
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.darkCyan, Qt.SolidPattern))
        for figure in self.figures:
            qp.drawRect(figure['point'][0] * self.width_size, figure['point'][1] * self.height_size,
                        figure['width'] * self.width_size, figure['height'] * self.height_size)
        qp.setFont(QFont("Arial", 12))
        for index_row, row in enumerate(self.grid_map):
            for index_cell, cell in enumerate(row):
                if index_row == 0 or index_cell == 0 or index_row == len(self.grid_map) - 1 or index_cell == len(
                        row) - 1:
                    continue
                qp.drawText((index_cell - 1) * self.width_size + 2, (index_row - 1) * self.height_size + 2,
                            self.width_size - 4, self.height_size - 4, 1, str(cell.value))
        qp.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pos1 = (int(event.pos().x() / self.width_size), int(event.pos().y() / self.height_size))
        elif event.button() == Qt.RightButton:
            for index, figure in enumerate(self.figures):
                if figure['point'][0] * self.width_size < event.pos().x() < figure['point'][0] * self.width_size + \
                        figure['width'] * self.width_size and figure['point'][
                    1] * self.height_size < event.pos().y() < figure['point'][1] * self.height_size + figure[
                    'height'] * self.height_size:
                    self.figures.pop(index)
                    self.update()
                    break

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_start:
                self.start_point = (int(event.pos().x() / self.width_size), int(event.pos().y() / self.height_size))
                self.row, self.column = self.start_point[1] + 1, self.start_point[0] + 1
                self.is_start = False
                self.update()
                self.repaint()
                return

            self.pos2 = (math.ceil(event.pos().x() / self.width_size), math.ceil(event.pos().y() / self.height_size))

            width = self.pos2[0] - self.pos1[0]
            height = self.pos2[1] - self.pos1[1]

            self.figures.append({
                'point': self.pos1,
                'width': width,
                'height': height
            })

            if len(self.figures) > 3:
                self.figures.pop(0)

            self.update()

    def clear_figures(self):
        self.figures.clear()
        self.start_point = (0, 0)
        self.update()
        self.repaint()

    def run(self):
        self.generate_grid()
        self.grid_map = [[Tile() for j in range(32)] for i in range(22)]
        distance = 4
        while True:
            if self.check_if_occupied():
                self.__update_grid_map(distance, 'mask')
            else:
                self.__update_grid_map(distance, None)

            if self.check_grid_map() or self.check_if_occupied():
                self.row, self.column, self.movement_direction = self.check_grid()
            else:
                self.row, self.column = self.get_next_position(self.movement_direction)

            self.start_point = (self.column - 1, self.row - 1)
            self.update()
            self.repaint()
            time.sleep(0.1)

    def __update_grid_map(self, distance, with_mask):
        if self.movement_direction.get_bum() != Direction.UP:
            d = distance if self.row - distance >= 0 else self.row
            if self.row - distance >= 0:
                if with_mask is not None:
                    self.grid_map[self.row - distance][self.column].update_value(with_mask, self.__get_mask(self.row - distance, self.column))
                else:
                    self.grid_map[self.row - distance][self.column].update_value("+", None)
            for i in range(1, d):
                if self.grid[self.row - i][self.column] != 1:
                    self.grid_map[self.row - i][self.column].update_value("-", None)
        if self.movement_direction.get_bum() != Direction.DOWN:
            d = distance if self.row + distance < len(self.grid_map) else len(self.grid_map) - self.row
            if self.row + distance < len(self.grid_map):
                if with_mask is not None:
                    self.grid_map[self.row + distance][self.column].update_value(with_mask, self.__get_mask(self.row + distance, self.column))
                else:
                    self.grid_map[self.row + distance][self.column].update_value("+", None)
            for i in range(1, d):
                if self.grid[self.row + i][self.column] != 1:
                    self.grid_map[self.row + i][self.column].update_value("-", None)
        if self.movement_direction.get_bum() != Direction.LEFT:
            d = distance if self.column - distance >= 0 else self.column
            if self.column - distance >= 0:
                if with_mask is not None:
                    self.grid_map[self.row][self.column - distance].update_value(with_mask, self.__get_mask(self.row, self.column-distance))
                else:
                    self.grid_map[self.row][self.column - distance].update_value("+", None)
            for i in range(1, d):
                if self.grid[self.row][self.column - i] != 1:
                    self.grid_map[self.row][self.column - i].update_value("-", None)
        if self.movement_direction.get_bum() != Direction.RIGHT:
            d = distance if self.column + distance < len(self.grid_map[0]) else len(self.grid_map[0]) - self.column
            if self.column + distance < len(self.grid_map[0]):
                if with_mask is not None:
                    self.grid_map[self.row][self.column + distance].update_value(with_mask, self.__get_mask(self.row, self.column + distance))
                else:
                    self.grid_map[self.row][self.column + distance].update_value("+", None)
            for i in range(1, d):
                if self.grid[self.row][self.column + i] != 1:
                    self.grid_map[self.row][self.column + i].update_value("-", None)

    def set_start(self):
        self.is_start = True

    def get_figures(self):
        return {
            'start_point': self.start_point,
            'figures': self.figures
        }

    def load_figures(self, elements):
        self.start_point = elements['start_point']
        self.figures = elements['figures']
        self.row, self.column = self.start_point[1] + 1, self.start_point[0] + 1

    def generate_grid(self):
        self.grid = [[1 if i == 0 or i == 21 or j == 0 or j == 31 else 0 for j in range(32)] for i in range(22)]
        for figure in self.figures:
            for width in range(figure['width']):
                for height in range(figure['height']):
                    self.grid[figure['point'][1] + height + 1][figure['point'][0] + width + 1] = 1
        self.grid[self.start_point[1] + 1][self.start_point[0] + 1] = 2
        for g in self.grid:
            print(g)

    def check_grid(self):
        r, c = self.get_next_position(self.movement_direction)
        if self.grid[r][c] == 1:
            r, c = self.get_next_position(self.movement_direction.get_bum())
            return r, c, self.movement_direction.get_bum()
        return r, c, self.movement_direction.next()

    def check_if_occupied(self):
        r, c = self.get_next_position(self.movement_direction)
        return self.grid[r][c] == 1

    def check_grid_map(self):
        rows = []
        columns = []
        if self.movement_direction == Direction.UP:
            for i in range(1, 4):
                if self.row - i >= 0:
                    rows.append(self.row - i)
            columns = [self.column]
        if self.movement_direction == Direction.DOWN:
            for i in range(1, 4):
                if self.row + i < len(self.grid_map):
                    rows.append(self.row + i)
            columns = [self.column]
        if self.movement_direction == Direction.LEFT:
            for i in range(1, 4):
                if self.column - i >= 0:
                    columns.append(self.column - i)
            rows = [self.row]
        if self.movement_direction == Direction.RIGHT:
            for i in range(1, 4):
                if self.column + i < len(self.grid_map[0]):
                    columns.append(self.column + i)
            rows = [self.row]

        for r in rows:
            for c in columns:
                if self.grid_map[r][c].value % 3 == 0 and self.grid_map[r][c].value != 0:
                    return True

    def get_next_position(self, direction):
        mask = self.__get_mask(self.row, self.column)
        index_r, index_c = 0, 0
        min_value = 15
        for i_r, r in enumerate(mask):
            for i_c, c in enumerate(r):
                if (i_r == 1 and i_c % 2 == 0) or (i_c == 1 and i_r % 2 == 0):
                    if mask[i_r][i_c] <= min_value:
                        min_value = mask[i_r][i_c]
                        index_r = i_r
                        index_c = i_c
        change_r = (index_r - 1)
        change_c = (index_c - 1)
        # return self.row + change_r, \
        #        self.column + change_c, \
        #        Direction.UP if change_r == -1 else \
        #            Direction.DOWN if change_r == 1 else \
        #                Direction.RIGHT if change_c == 1 else \
        #                    Direction.LEFT
        return self.row + 1 if direction == Direction.DOWN else self.row - 1 if direction == Direction.UP else self.row, \
               self.column + 1 if direction == Direction.RIGHT else self.column - 1 if direction == Direction.LEFT else self.column

    def __get_mask(self, row_current, column_current):
        return [
            [
                0 if self.row - 1 < 0 else 0 if column_current - 1 < 0 else self.grid_map[row_current - 1][column_current - 1].value,
                0 if self.row - 1 < 0 else self.grid_map[row_current - 1][column_current].value,
                0 if self.row - 1 < 0 else 0 if column_current + 1 >= len(self.grid_map[0]) else self.grid_map[row_current - 1][
                    column_current + 1].value
            ],
            [
                0 if column_current - 1 < 0 else self.grid_map[row_current][column_current - 1].value,
                self.grid_map[row_current][column_current].value,
                0 if column_current + 1 >= len(self.grid_map[0]) else self.grid_map[row_current][column_current + 1].value
            ],
            [
                0 if row_current + 1 >= len(self.grid_map) else 0 if self.column - 1 < 0 else self.grid_map[row_current + 1][
                    column_current - 1].value,
                0 if row_current + 1 >= len(self.grid_map) else self.grid_map[row_current + 1][column_current].value,
                0 if row_current + 1 >= len(self.grid_map) else 0 if column_current + 1 >= len(self.grid_map[0]) else
                self.grid_map[row_current + 1][column_current + 1].value
            ]
        ]
