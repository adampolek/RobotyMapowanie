import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QColorConstants, QBrush, QMouseEvent
from PyQt5.QtWidgets import QGroupBox


class MyCanvas(QGroupBox):
    def __init__(self):
        super().__init__("Map Visualization")

        self.grid = []
        self.figures = []
        self.pos1 = (0, 0)
        self.pos2 = (0, 0)
        self.start_point = (0, 0)
        self.is_start = False

    def paintEvent(self, event):
        width = int(self.width() / 30) * 30
        height = int(self.height() / 30) * 30
        qp = QPainter()
        qp.begin(self)
        for index in range(int(width / 30) + 1):
            qp.drawLine(index * 30, 0, index * 30, height)
            qp.drawLine(0, index * 30, width, index * 30)
        if self.start_point != (0, 0):
            qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            qp.drawEllipse(self.start_point[0], self.start_point[1], 15, 15)
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.darkCyan, Qt.SolidPattern))
        for figure in self.figures:
            qp.drawRect(figure['point'][0], figure['point'][1], figure['width'], figure['height'])
        qp.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pos1 = (int(event.pos().x() / 30) * 30, int(event.pos().y() / 30) * 30)
        elif event.button() == Qt.RightButton:
            for index, figure in enumerate(self.figures):
                if figure['point'][0] < event.pos().x() < figure['point'][0] + figure['width'] and figure['point'][1] < event.pos().y() < figure['point'][1] + figure['height']:
                    self.figures.pop(index)
                    self.update()
                    break

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_start:
                self.start_point = (int(event.pos().x() / 30) * 30 + 8, int(event.pos().y() / 30) * 30 + 8)
                self.is_start = False
                self.update()
                self.repaint()
                return

            self.pos2 = (math.ceil(event.pos().x() / 30) * 30, math.ceil(event.pos().y() / 30) * 30)

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
        pass

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
