import sys

from PyQt5 import QtWidgets

from gui.main_window import MyWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
