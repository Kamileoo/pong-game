from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import login
import game
import hub


glob_params = {
    'windows_height': 512,
    'windows_width': 1024,
}


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

    def keyPressEvent(self, event):
        if game.game_val['is_game']:
            game.keyHandler(event, 'P')
    def keyReleaseEvent(self, event):
        if game.game_val['is_game']:
            game.keyHandler(event, 'R')

app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
win.setWindowTitle("Pong")
win.setFixedSize(1024, 512)

hub.hub_ui(win)

win.show()
sys.exit(app.exec())