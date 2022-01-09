from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import login
import game
import hub


app = QtWidgets.QApplication(sys.argv)
win = QtWidgets.QWidget()
win.setWindowTitle("Pong")
#win.resize(1024, 512)
win.setFixedSize(1024, 512)

#game.game_ui(win)
hub.hub_ui(win)


win.show()
sys.exit(app.exec())