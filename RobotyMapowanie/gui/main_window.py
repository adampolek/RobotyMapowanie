from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QMenuBar

from gui.my_canvas import MyCanvas


class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__set_settings()
        widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.canvas = MyCanvas()
        self.main_layout.addWidget(self.canvas)
        clear = QPushButton()
        clear.setText("CLEAR")
        clear.clicked.connect(self.canvas.clear_figures)
        self.main_layout.addWidget(clear)
        run = QPushButton()
        run.setText("RUN")
        run.clicked.connect(self.canvas.run)
        start = QPushButton()
        start.setText("SET START POINT")
        start.clicked.connect(self.canvas.set_start)
        end = QPushButton()
        end.setText("SET END POINT")
        end.clicked.connect(self.canvas.set_end)
        self.main_layout.addWidget(run)
        self.main_layout.addWidget(start)
        self.main_layout.addWidget(end)
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.show()
        self.__create_menubar()

    def __set_settings(self):
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("Mapowanie")

    def __create_menubar(self):
        self.menuBar = QMenuBar(self)
        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction("Save")
        fileMenu.addAction("Load")
        self.menuBar.show()