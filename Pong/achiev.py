from PyQt6 import QtCore, QtGui, QtWidgets
import config
import glob_func
import hub

ach_widget = {
    'db_view': [],
    'namelabel': [],
    'userlabel': [],
    'guildlabel': [],
    'edit': [],
    'back': []
}


def ach_ui():
    data = ['Achievement', 'Unlock Date']
    glob_func.table_create('Achievements', data, ach_widget, 5, lambda: glob_func.go_to(ach_widget, hub.hub_ui))

    query = f"SELECT achivement_name, date FROM got_achivements WHERE user_id='{str(config.login_params['userID'])}'"
    glob_func.load_db(query, ach_widget)

    config.glob_grid.setRowStretch(2, 1)
    config.glob_grid.setRowStretch(4, 1)
