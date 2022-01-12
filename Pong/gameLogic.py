from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsEllipseItem, QPushButton
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import main
import game
import time


# Game itself
class myGame(QtCore.QObject):

    finished = QtCore.pyqtSignal()

    def run(self):
        while not game.game_val['esckey']:
            if game.game_val['key'] == 1 and game.game_val['my_pos_x'] <= game.game_opt['im_height']:
                game.game_val['my_pos_x'] +=1
            elif game.game_val['key'] == -1  and game.game_val['my_pos_x'] >= 0:
                game.game_val['my_pos_x'] -=1
            game.draw()
            time.sleep(0.001)
        game.game_is_over()
        self.finished.emit()