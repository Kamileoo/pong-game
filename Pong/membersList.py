from PyQt6 import QtCore, QtGui, QtWidgets
import config
import glob_func
import guildsList

members_widget = {
    'db_view': [],
    'namelabel': [],
    'userlabel': [],
    'guildlabel': [],
    'back': []
}


def members_ui(name):
    data = ['User', 'No games', 'Wins', 'Losses', 'Ties', 'E-mail', 'Is Admin', 'User ID']
    glob_func.table_create(name, data, members_widget, 3, lambda: glob_func.go_to(members_widget, guildsList.guild_ui))
    members_widget['db_view'][-1].setColumnHidden(len(data) - 1, True)

    query = f"SELECT nick, no_games, no_wins, no_loses, no_ties, email, admin, user_id FROM users WHERE guild='{str(name)}'"
    glob_func.load_db(query, members_widget)

    config.glob_grid.setRowStretch(2, 1)
