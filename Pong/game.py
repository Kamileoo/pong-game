from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsEllipseItem, QPushButton
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from main import *
import main
import hub
import time


threads = []


game_widget = {
    'startbutton': [],
    'endbutton': [],
    'myscore': [],
    'enscore': [],
    'myline': [],
    'enline': [],
    'ball': [],
    'result': []
}

game_val = {
    'my_pos': 0,    # 0 - 100
    'en_pos': 0,    # 0 - 100
    'ball_x': 0,    # 0 - 200
    'ball_y': 0,    # 0 - 100
    'my_score': 0,
    'en_score': 0,
    'is_game': 0,
    'key': 0,
    'esckey': 0
}

game_opt = {
    'line_len': 160,
    'line_wid': 20,
    'ball_rad': 10,
    'from_border': 10
}


# When Press Start
def is_ready():
    game_widget['startbutton'][-1].hide()
    game_val['is_game'] = 1
    game()


# When Press End
def is_end(win):
    game_clear(win)
    hub.hub_ui(win)


# After the Game Ends
def game_is_over():
    game_val['is_game'] = 0
    game_widget['endbutton'][-1].show()
    game_widget['ball'][-1].hide()
    res = 'You Won!' if game_val['my_score'] > game_val['en_score']\
        else 'You Lost!' if game_val['my_score'] < game_val['en_score'] \
        else 'It is a Tie'
    game_widget['result'][-1].setText(res)
    game_widget['result'][-1].show()


# Clearing the window
def game_clear(win):
    win.setStyleSheet("background-color: #ffffff;")
    for h in game_widget:
        if game_widget[h] != []:
            game_widget[h][-1].deleteLater()
        for i in range(len(game_widget[h])):
            game_widget[h] = []
    for v in game_val:
        game_val[v] = 0


# Keyboard
def keyHandler(event, status):
    if status == 'P':
        if not event.isAutoRepeat():
            if event.key() == QtCore.Qt.Key.Key_W:
                game_val['key'] = 1
            elif event.key() == QtCore.Qt.Key.Key_S:
                game_val['key'] = -1
            elif event.key() == QtCore.Qt.Key.Key_Escape:
                game_val['esckey'] = 1
    elif status == 'R':
        if not event.isAutoRepeat():
            game_val['key'] = 0
        pass
    else:
        pass


# Drawing Palettes, scores and ball
def draw():
    game_widget['myscore'][-1].setText(str(game_val['my_score']))
    game_widget['myscore'][-1].show()

    game_widget['enscore'][-1].setText(str(game_val['en_score']))
    game_widget['enscore'][-1].show()

    game_widget['ball'][-1].setGeometry(QtCore.QRect((main.glob_params['windows_width'] - 2 * game_opt['ball_rad']) * game_val['ball_x'] / 200,
                                                     (main.glob_params['windows_height'] - 2 * game_opt['ball_rad']) * game_val['ball_y'] / 100,
                                                     2 * game_opt['ball_rad'], 2 * game_opt['ball_rad']))
    game_widget['ball'][-1].show()

    game_widget['myline'][-1].setGeometry(QtCore.QRect(game_opt['from_border'],
                                                    (main.glob_params['windows_height'] - game_opt['line_len']) * game_val['my_pos'] / 100,
                                                    game_opt['line_wid'], game_opt['line_len']))
    game_widget['myline'][-1].show()

    game_widget['enline'][-1].setGeometry(QtCore.QRect(main.glob_params['windows_width']-game_opt['from_border']-game_opt['line_wid'],
                                                       (main.glob_params['windows_height'] - game_opt['line_len']) * game_val['en_pos'] / 100,
                                                       game_opt['line_wid'], game_opt['line_len']))
    game_widget['enline'][-1].show()


# Game
def game():
    #game_is_over()
    pass


# Drawing and setting the window
def game_ui(win):
    game_val['my_pos'] = 50
    game_val['en_pos'] = 50
    game_val['ball_x'] = 100
    game_val['ball_y'] = 50

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

    # My Palette
    my_line = QtWidgets.QFrame(win)
    my_line.setLineWidth(0)
    my_line.setMidLineWidth(game_opt['line_wid'])
    my_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    my_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    game_widget['myline'].append(my_line)

    # Enemy Palette
    en_line = QtWidgets.QFrame(win)
    en_line.setLineWidth(0)
    en_line.setMidLineWidth(game_opt['line_wid'])
    en_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    en_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
    game_widget['enline'].append(en_line)

    # Ball
    ball = QtWidgets.QLabel(win)
    ball.setStyleSheet(
        "background: white;" +
        f"border-radius: {game_opt['ball_rad']}px;"
    )
    game_widget['ball'].append(ball)

    # Score text
    endscore = QtWidgets.QLabel(win)
    endscore.setStyleSheet(
        "font-size: 40px;" +
        "color: 'white';" +
        "background: transparent;"
    )
    endscore.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    endscore.setGeometry(QtCore.QRect(0,main.glob_params['windows_height']/4 , main.glob_params['windows_width'], 40))
    game_widget['result'].append(endscore)
    game_widget['result'][-1].hide()

    # Draw Palettes, Ball and Scores
    draw()

# Game itself
class myGame(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    pass