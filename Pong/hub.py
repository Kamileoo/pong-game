from PyQt6 import QtCore, QtGui, QtWidgets
import game
import config
import account
import loginHistory

hub_widget = {
    'startbutton': [],
    'player': [],
    'guilds': [],
    'achievements': [],
    'statistics': [],
    'loginhistory': [],
    'gameshistory': [],
    'account': [],
    'spacers': []
}

def start_game(win):
    hub_clear()
    game.game_ui(win)


def guilds():
    pass


def achievements():
    pass


def statistics():
    pass

def gameshistory():
    pass


def loginhistory():
    hub_clear()
    loginHistory.lg_ui()
    pass



def account_func():
    hub_clear()
    account.draw()


def hub_clear():
    for h in hub_widget:
        if hub_widget[h] != []:
            hub_widget[h][-1].deleteLater()
        for i in range(len(hub_widget[h])):
            hub_widget[h] = []
    config.glob_grid.setColumnMinimumWidth(0, 0)
    config.glob_grid.setRowStretch(2, 0)
    config.glob_grid.setRowStretch(9, 0)


def create_main_button(text):
    button = QtWidgets.QPushButton(text)
    # button.setStyleSheet(
    #     "margin: 0px 10px;" +
    #     "padding: 10px 10px;"
    # )

    return button


def hub_ui(win):

    # Nickname
    #player = QtWidgets.QLabel("Player")
    player = QtWidgets.QLabel(config.login_params['username'])
    player.setMaximumHeight(20)
    player.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    hub_widget['player'].append(player)
    hub_widget['player'][-1].show()
    config.glob_grid.addWidget(hub_widget['player'][-1], 0, 2, QtCore.Qt.AlignmentFlag.AlignTop)

    # Account
    acc = QtWidgets.QPushButton("Account")
    acc.setStyleSheet(
        "margin: 0px 80px;"
    )
    acc.clicked.connect(account_func)
    hub_widget['account'].append(acc)
    hub_widget['account'][-1].show()
    config.glob_grid.addWidget(hub_widget['account'][-1], 1, 2)

    # Game start
    startb = create_main_button("Start")
    startb.clicked.connect(lambda: start_game(win))
    hub_widget['startbutton'].append(startb)
    hub_widget['startbutton'][-1].show()
    config.glob_grid.addWidget(hub_widget['startbutton'][-1], 3, 1)

    # Guilds
    gul = create_main_button("Guilds")
    gul.clicked.connect(guilds)
    hub_widget['guilds'].append(gul)
    hub_widget['guilds'][-1].show()
    config.glob_grid.addWidget(hub_widget['guilds'][-1], 4, 1)

    # Achievements
    ach = create_main_button("Achievements")
    ach.clicked.connect(achievements)
    hub_widget['achievements'].append(ach)
    hub_widget['achievements'][-1].show()
    config.glob_grid.addWidget(hub_widget['achievements'][-1], 5, 1)

    # Statistics
    stat = create_main_button("Statistics")
    stat.clicked.connect(statistics)
    hub_widget['statistics'].append(stat)
    hub_widget['statistics'][-1].show()

    config.glob_grid.addWidget(hub_widget['statistics'][-1], 6, 1)
    # Games History
    gam = create_main_button("Games History")
    gam.clicked.connect(gameshistory)
    hub_widget['gameshistory'].append(gam)
    hub_widget['gameshistory'][-1].show()
    config.glob_grid.addWidget(hub_widget['gameshistory'][-1], 7, 1)

    # Login History
    log = create_main_button("Login History")
    log.clicked.connect(loginhistory)
    hub_widget['loginhistory'].append(log)
    if config.login_params['isAdmin']:
        hub_widget['loginhistory'][-1].show()
    else:
        hub_widget['loginhistory'][-1].hide()
    config.glob_grid.addWidget(hub_widget['loginhistory'][-1], 8, 1)

    # Spacers
    config.glob_grid.setColumnMinimumWidth(0,config.glob_params['windows_width']/3)
    config.glob_grid.setRowStretch(2, 1)
    config.glob_grid.setRowStretch(9, 1)
