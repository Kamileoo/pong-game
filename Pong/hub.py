from PyQt6 import QtCore, QtGui, QtWidgets
import game
import config
import glob_func
import account
import loginHistory
import mylogin
import gamesHistory
import stats
import achiev
import guildsList

hub_widget = {
    'startbutton': [],
    'player': [],
    'guilds': [],
    'achievements': [],
    'statistics': [],
    'loginhistory': [],
    'gameshistory': [],
    'account': [],
    'guildlabel': [],
    'logout': []
}


def account_func():
    hub_clear()
    account.account_ui()


def logout_func():
    hub_clear()
    if config.login_datetime is not None: glob_func.logout_func()
    config.login_datetime = None
    mylogin.login_ui()


def hub_clear():
    for h in hub_widget:
        if hub_widget[h] != []:
            hub_widget[h][-1].deleteLater()
        for i in range(len(hub_widget[h])):
            hub_widget[h] = []
    config.glob_grid.setColumnMinimumWidth(0, 0)
    config.glob_grid.setRowStretch(4, 0)
    config.glob_grid.setRowStretch(11, 0)


def create_main_button(text):
    button = QtWidgets.QPushButton(text)
    # button.setStyleSheet(
    #     "margin: 0px 10px;" +
    #     "padding: 10px 10px;"
    # )

    return button


def hub_ui(win=config.window):

    # Nickname
    player = QtWidgets.QLabel(config.login_params['username'])
    player.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    hub_widget['player'].append(player)
    hub_widget['player'][-1].show()
    config.glob_grid.addWidget(hub_widget['player'][-1], 0, 2, QtCore.Qt.AlignmentFlag.AlignTop)

    guil = QtWidgets.QLabel(config.login_params['guild'])
    guil.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    hub_widget['guildlabel'].append(guil)
    hub_widget['guildlabel'][-1].show()
    config.glob_grid.addWidget(hub_widget['guildlabel'][-1], 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)

    # Account
    acc = glob_func.button_main('Account', lambda: glob_func.go_to(hub_widget, account.account_ui), hub_widget,
                                'account', config.account_buttons)
    config.glob_grid.addWidget(acc, 2, 2)

    # LogOut
    logout = glob_func.button_main('Logout', logout_func, hub_widget,
                                   'logout', config.account_buttons)
    config.glob_grid.addWidget(logout, 3, 2)

    # Game start
    startb = glob_func.button_main('Start', lambda: glob_func.go_to(hub_widget, game.game_ui), hub_widget,
                                    'startbutton')
    config.glob_grid.addWidget(startb, 5, 1)

    # Guilds
    gul = glob_func.button_main('Guilds', lambda: glob_func.go_to(hub_widget, guildsList.guild_ui), hub_widget,
                                'guilds')
    config.glob_grid.addWidget(gul, 6, 1)

    # Achievements
    ach = glob_func.button_main('Achievements', lambda: glob_func.go_to(hub_widget, achiev.ach_ui), hub_widget,
                                'achievements')
    config.glob_grid.addWidget(ach, 7, 1)

    # Statistics
    stat = glob_func.button_main('Statistics', lambda: glob_func.go_to(hub_widget, stats.stat_ui), hub_widget,
                                 'statistics')
    config.glob_grid.addWidget(stat, 8, 1)

    # Games History
    gam = glob_func.button_main('Games history', lambda: glob_func.go_to(hub_widget, gamesHistory.gh_ui), hub_widget,
                                'gameshistory')
    config.glob_grid.addWidget(gam, 9, 1)

    # Login History
    log = glob_func.button_main('Login history', lambda: glob_func.go_to(hub_widget, loginHistory.lg_ui), hub_widget,
                                'loginhistory')
    if not config.login_params['isAdmin']: log.hide()
    config.glob_grid.addWidget(log, 10, 1)

    # Spacers
    config.glob_grid.setColumnMinimumWidth(0,config.glob_params['windows_width']/3)
    config.glob_grid.setRowStretch(4, 1)
    config.glob_grid.setRowStretch(11, 2)
