from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsEllipseItem, QPushButton
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from main import *
import hub

# min 0 max 512-line_len=352

game_widget = {
    'startbutton': [],
    'endbutton': [],
    'myscore': [],
    'enscore': [],
    'myline': [],
    'enline': [],
    'ball': []
}

game_val = {
    'my_pos': 0,
    'en_pos': 0,
    'ball_x': 0,
    'ball_y': 0,
    'my_score': 0,
    'en_score': 0
}

game_opt = {
    'line_len': 160,
    'line_wid': 20,
    'ball_rad': 10
}


def is_ready():
    game_widget['startbutton'][-1].hide()
    game()


def is_end(win):
    game_clear(win)
    hub.hub_ui(win)


def game_clear(win):
    win.setStyleSheet("background-color: #ffffff;")
    for h in game_widget:
        if game_widget[h] != []:
            game_widget[h][-1].deleteLater()
        for i in range(len(game_widget[h])):
            game_widget[h] = []
    for v in game_val:
        game_val[v] = 0


def game():
    #while 1:
    #    game_widget['myscore'][-1].setText[str(game_val['my_score'])]
    #    game_widget['enscore'][-1].setText[str(game_val['en_score'])]
    game_widget['endbutton'][-1].show()
    pass


def game_ui(win):
    game_val['my_pos'] = (512 - game_opt['line_len']) / 2
    game_val['en_pos'] = (512 - game_opt['line_len']) / 2

    win.setStyleSheet("background-color: #363636;")

    # Start button
    startbutton = QtWidgets.QPushButton("Start", win)
    startbutton.setGeometry(QtCore.QRect(462, 320, 100, 40))
    startbutton.setObjectName("Start")
    startbutton.setStyleSheet(
        "color: 'white'"
    )
    startbutton.clicked.connect(is_ready)
    game_widget['startbutton'].append(startbutton)
    game_widget['startbutton'][-1].show()

    # My score
    myscore = QtWidgets.QLabel(str(game_val['my_score']), win)
    myscore.setStyleSheet(
        "font-size: 30px;" +
        "color: 'white';" +
        "background: transparent;"
    )
    myscore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    myscore.setGeometry(QtCore.QRect(462, 0, 35, 30))
    game_widget['myscore'].append(myscore)
    game_widget['myscore'][-1].show()

    # Enemy score
    enscore = QtWidgets.QLabel(str(game_val['en_score']), win)
    enscore.setStyleSheet(
        "font-size: 30px;" +
        "color: 'white';" +
        "background: transparent;"
    )
    enscore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    enscore.setGeometry(QtCore.QRect(527, 0, 35, 30))
    game_widget['enscore'].append(enscore)
    game_widget['enscore'][-1].show()

    # End button
    endbutton = QtWidgets.QPushButton("End", win)
    endbutton.setGeometry(QtCore.QRect(462, 320, 100, 40))
    endbutton.setObjectName("End")
    endbutton.setStyleSheet(
        "color: 'white'"
    )
    endbutton.clicked.connect(lambda: is_end(win))
    game_widget['endbutton'].append(endbutton)
    game_widget['endbutton'][-1].hide()

    #ball = QGraphicsEllipseItem()
    #ball.setRect(0,0,5,5)

    my_line = QtWidgets.QFrame(win)
    my_line.setGeometry(QtCore.QRect(10, game_val['my_pos'], game_opt['line_wid'], game_opt['line_len']))
    my_line.setLineWidth(0)
    my_line.setMidLineWidth(game_opt['line_wid'])
    my_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    my_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    game_widget['myline'].append(my_line)
    game_widget['myline'][-1].show()

    en_line = QtWidgets.QFrame(win)
    en_line.setGeometry(QtCore.QRect(1024-10-game_opt['line_wid'], game_val['en_pos'], game_opt['line_wid'], game_opt['line_len']))
    en_line.setLineWidth(0)
    en_line.setMidLineWidth(game_opt['line_wid'])
    en_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    en_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    game_widget['enline'].append(en_line)
    game_widget['enline'][-1].show()

    ball = QtWidgets.QLabel(win)
    ball.setGeometry(QtCore.QRect((1024-2*game_opt['ball_rad'])/2, (512-2*game_opt['ball_rad'])/2, 2*game_opt['ball_rad'], 2*game_opt['ball_rad']))
    ball.setStyleSheet(
        "background: white;" +
        f"border-radius: {game_opt['ball_rad']}px;"
    )
    game_widget['ball'].append(ball)
    game_widget['ball'][-1].show()
