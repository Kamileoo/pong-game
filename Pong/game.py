from PyQt6 import QtCore, QtGui, QtWidgets
import hub
import gameLogic
import config


threads = []
objects = []


game_widget = {
    'startbutton': [],
    'endbutton': [],
    'myscore': [],
    'enscore': [],
    'myline': [],
    'enline': [],
    'ball': [],
    'result': [],
    'central_line': []
}

game_val = {
    'move_x':0,
    'my_pos_x': 0,
    'my_pos_y': 0,# 0 - 100
    'en_pos_x': 0,
    'en_pos_y': 0,# 0 - 100
    'ball_x': 0,    # 0 - 200
    'ball_y': 0,
    'ball_radius': 0,# 0 - 100
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
    'from_border': 10,
    'im_width': 2000,
    'im_height': 1000
}


# When Press Start
def is_ready():
    game_widget['startbutton'][-1].hide()
    game_widget['central_line'][-1].show()
    game_val['is_game'] = 1
    game()


# When Press End
def is_end(win):
    game_clear(win)
    hub.hub_ui()


# After the Game Ends
def game_is_over():
    game_val['is_game'] = 0
    game_widget['central_line'][-1].hide()
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
    threads = []
    objects = []


# Keyboard
def keyHandler(event, status):
    if status == 'P':
        if event.key() == QtCore.Qt.Key.Key_W:
            game_val['move_x'] -=8
        if event.key() == QtCore.Qt.Key.Key_S:
            game_val['move_x'] +=8
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

    game_widget['ball'][-1].setGeometry(QtCore.QRect((config.glob_params['windows_width'] - 2 * game_opt['ball_rad']) * game_val['ball_x'] / game_opt['im_width'],
                                                     (config.glob_params['windows_height'] - 2 * game_opt['ball_rad']) * game_val['ball_y'] / game_opt['im_height'],
                                                     2 * game_opt['ball_rad'], 2 * game_opt['ball_rad']))
    game_widget['ball'][-1].show()

    game_widget['myline'][-1].setGeometry(QtCore.QRect(game_opt['from_border'],
                                                    (config.glob_params['windows_height'] - game_opt['line_len']) * game_val['my_pos_x'] / game_opt['im_height'],
                                                    game_opt['line_wid'], game_opt['line_len']))
    game_widget['myline'][-1].show()

    game_widget['enline'][-1].setGeometry(QtCore.QRect(config.glob_params['windows_width']-game_opt['from_border']-game_opt['line_wid'],
                                                       (config.glob_params['windows_height'] - game_opt['line_len']) * game_val['en_pos_x'] / game_opt['im_height'],
                                                       game_opt['line_wid'], game_opt['line_len']))
    game_widget['enline'][-1].show()


# Create imaginary numbers
def imagine():
    game_val['my_pos_x'] = game_opt['im_height'] / 2
    game_val['en_pos_x'] = game_opt['im_height'] / 2
    game_val['ball_x'] = game_opt['im_width'] / 2
    game_val['ball_y'] = game_opt['im_height'] / 2

    tmp_my = game_opt['from_border'] + game_opt['line_wid']/2
    game_val['my_pos_y'] = tmp_my / config.glob_params['windows_width'] * game_opt['im_width']

    tmp_en = config.glob_params['windows_width'] - game_opt['from_border'] + game_opt['line_wid'] / 2
    game_val['en_pos_y'] = tmp_en / config.glob_params['windows_width'] * game_opt['im_width']

    game_val['ball_radius'] = game_opt['ball_rad'] / config.glob_params['windows_width'] * game_opt['im_width']


# Game
def game():
    thread = QtCore.QThread()
    gameObject = gameLogic.MyGame()
    gameObject.moveToThread(thread)
    thread.started.connect(gameObject.run)
    gameObject.finished.connect(thread.quit)
    gameObject.finished.connect(gameObject.deleteLater)
    thread.finished.connect(thread.deleteLater)

    threads.append(thread)
    objects.append(gameObject)

    threads[-1].start()


# Drawing and setting the window
def game_ui(win=config.window):
    imagine()

    win = config.window
    win.setStyleSheet("background-color: #363636;")

    # Dotted line
    central_line = QtWidgets.QFrame(win)
    central_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    central_line.setStyleSheet(
        "background: transparent;" +
        f"border: {game_opt['line_wid']/2}px white;" +
        "border-style: dotted;"
    )
    central_line.setGeometry(
        QtCore.QRect((config.glob_params['windows_width'] - game_opt['line_wid']/2) / 2, 0,
                     game_opt['line_wid']/2, config.glob_params['windows_height']))
    game_widget['central_line'].append(central_line)
    game_widget['central_line'][-1].hide()

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
    my_line.setLineWidth(game_opt['line_wid'])
    my_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    my_line.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
    my_line.setStyleSheet(
        "color: 'white';"
    )
    game_widget['myline'].append(my_line)

    # Enemy Palette
    en_line = QtWidgets.QFrame(win)
    en_line.setLineWidth(game_opt['line_wid'])
    en_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
    en_line.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
    en_line.setStyleSheet(
        "color: 'white';"
    )
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
    endscore.setGeometry(QtCore.QRect(0,config.glob_params['windows_height']/4 , config.glob_params['windows_width'], 40))
    game_widget['result'].append(endscore)
    game_widget['result'][-1].hide()


    # Draw Palettes, Ball and Scores
    draw()

