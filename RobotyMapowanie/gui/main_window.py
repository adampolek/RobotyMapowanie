from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QMenuBar, QAction, QFileDialog

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
        self.main_layout.addWidget(run)
        self.main_layout.addWidget(start)
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
        self.__create_menubar()
        self.show()

    def __set_settings(self):
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("Mapowanie")

    def __create_menubar(self):
        save_action: QAction = QAction('Save file', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Saving file')
        save_action.triggered.connect(self.__save_map)

        load_action: QAction = QAction('Load file', self)
        load_action.setShortcut('Ctrl+L')
        load_action.setStatusTip('Load file')
        load_action.triggered.connect(self.__load_map)

        menu_bar: QMenuBar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

    def __save_map(self):
        file_name, _ = QFileDialog.getSaveFileName()
        if file_name:
            with open(file_name, 'w+') as f:
                f.write(str(self.canvas.get_figures()))

    def __load_map(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            with open(file_name, 'r') as f:
                self.canvas.load_figures(eval("\n".join(f.readlines())))
