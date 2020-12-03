import math
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QColorConstants, QBrush, QMouseEvent
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
        self.is_start = False

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
        is_first_check = False
        self.generate_grid()
        print('\n\n\n')
        self.grid_map = [[Tile() for j in range(32)] for i in range(22)]
        row, column = self.start_point[1] + 1, self.start_point[0] + 1
        distance = 4
        movement_direction = Direction.DOWN
        # self.counter = 0
        while True:
            self.__update_grid_map(column, distance, row, movement_direction)
            # if self.counter != 0 and self.counter != 2:
            row_temp = row + 1 if movement_direction == Direction.DOWN else row - 1 if movement_direction == Direction.UP else row
            column_temp = column + 1 if movement_direction == Direction.RIGHT else column - 1 if movement_direction == Direction.LEFT else column

            if self.grid_map[row_temp][column_temp].value >= 3:
                # self.counter = 0
                movement_direction = movement_direction.next()
                row = row + 1 if movement_direction == Direction.DOWN else row - 1 if movement_direction == Direction.UP else row
                column = column + 1 if movement_direction == Direction.RIGHT else column - 1 if movement_direction == Direction.LEFT else column
            else:
                row = row_temp
                column = column_temp
            # self.counter += 1
            for r in self.grid_map:
                print(r)
            print("cokolwiek")

    def __update_grid_map(self, column, distance, row, movement_direction):
        if row - distance >= 0 and movement_direction.get_bum() != Direction.UP:
            self.grid_map[row - distance][column].update_value("+")
            for i in range(1, distance):
                if self.grid[row - i][column] != 1:
                    self.grid_map[row - i][column].update_value("-")
        if row + distance < len(self.grid_map) and movement_direction.get_bum() != Direction.DOWN:
            self.grid_map[row + distance][column].update_value("+")
            for i in range(1, distance):
                if self.grid[row + i][column] != 1:
                    self.grid_map[row + i][column].update_value("-")
        if column - distance >= 0 and movement_direction.get_bum() != Direction.LEFT:
            self.grid_map[row][column - distance].update_value("+")
            for i in range(1, distance):
                if self.grid[row][column - i] != 1:
                    self.grid_map[row][column - i].update_value("-")
        if column + distance < len(self.grid_map[0]) and movement_direction.get_bum() != Direction.RIGHT:
            self.grid_map[row][column + distance].update_value("+")
            for i in range(1, distance):
                if self.grid[row][column + i] != 1:
                    self.grid_map[row][column + i].update_value("-")

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

    def generate_grid(self):
        self.grid = [[1 if i == 0 or i == 21 or j == 0 or j == 31 else 0 for j in range(32)] for i in range(22)]
        for figure in self.figures:
            for width in range(figure['width']):
                for height in range(figure['height']):
                    self.grid[figure['point'][1] + height + 1][figure['point'][0] + width + 1] = 1
        self.grid[self.start_point[1] + 1][self.start_point[0] + 1] = 2
        for g in self.grid:
            print(g)

    # def __get_mask(self, row, column):
    #     return [
    #         [
    #             0 if row - 1 < 0 else 0 if column - 1 < 0 else self.grid_map[row - 1][column - 1].value,
    #             0 if row - 1 < 0 else self.grid_map[row - 1][column].value,
    #             0 if row - 1 < 0 else 0 if column + 1 >= len(self.grid_map[0]) else self.grid_map[row - 1][
    #                 column + 1].value
    #         ],
    #         [
    #             0 if column - 1 < 0 else self.grid_map[row][column - 1].value,
    #             self.grid_map[row][column].value,
    #             0 if column + 1 >= len(self.grid_map[0]) else self.grid_map[row][column + 1].value
    #         ],
    #         [
    #             0 if row + 1 >= len(self.grid_map) else 0 if column - 1 < 0 else self.grid_map[row + 1][
    #                 column - 1].value,
    #             0 if row + 1 >= len(self.grid_map) else self.grid_map[row + 1][column].value,
    #             0 if row + 1 >= len(self.grid_map) else 0 if column + 1 >= len(self.grid_map[0]) else
    #             self.grid_map[row + 1][column + 1].value
    #         ]
    #     ]
