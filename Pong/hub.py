from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsEllipseItem, QPushButton
from PyQt6 import QtCore, QtGui, QtWidgets
import sys

import main
from main import *
import game
#from game import game_ui

hub_widget = {
    'grid': [],
    'startbutton': [],
    'player': []
}

def start_game(win):
    hub_clear()
    game.game_ui(win)


def hub_clear():
    for h in hub_widget:
        if hub_widget[h] != []:
            hub_widget[h][-1].deleteLater()
        for i in range(len(hub_widget[h])):
            hub_widget[h] = []


def create_main_button(text):
    button = QtWidgets.QPushButton(text)
    button.setStyleSheet(
        "margin: 0 300px;"
    )
    #button.setObjectName(text)

    return button


def hub_ui(win):
    grid = QtWidgets.QGridLayout(win)

    player = QtWidgets.QLabel("Player")
    player.setMaximumHeight(20)
    player.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    hub_widget['player'].append(player)
    grid.addWidget(hub_widget['player'][-1], 0, 0, QtCore.Qt.AlignmentFlag.AlignTop)


    startb = create_main_button("Start")
    startb.clicked.connect(lambda: start_game(win))
    hub_widget['startbutton'].append(startb)
    grid.addWidget(hub_widget['startbutton'][-1], 1, 0, QtCore.Qt.AlignmentFlag.AlignTop)

    hub_widget['grid'].append(grid)