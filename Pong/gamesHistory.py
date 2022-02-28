from PyQt6 import QtCore, QtGui, QtWidgets
import config
import glob_func
import hub
import mysql.connector

gh_widget = {
    'db_view': [],
    'namelabel': [],
    'userlabel': [],
    'guildlabel': [],
    'back': []
}


test = [('Antoni','15.02','15.02','192.158.1.1','Windows 10'),('Artur','15.06.2021 15:38:15','15.06.2021 18:40:38','125.135.186.200','Windows 10')]

def load_db():
    result = test
    for row_number, row_data in enumerate(result):
        gh_widget['db_view'][-1].insertRow(row_number)
        for column_number, data in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(data))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            gh_widget['db_view'][-1].setItem(row_number, column_number, item)


def gh_ui():

    data = ['User 1', 'User 2', 'Score 1/2', 'Start', 'End', 'Game ID']
    glob_func.table_create('Games History', data, gh_widget, 3, lambda: glob_func.go_to(gh_widget, hub.hub_ui))
    gh_widget['db_view'][-1].hideColumn(len(data)-1)
    gh_widget['db_view'][-1].horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

    query = f"SELECT p1n, p2n, sc, g.start_time, g.end_time, g.game_id " \
            f"FROM games g " \
            f"LEFT JOIN (SELECT p1.nick as p1n, p2.nick as p2n, CONCAT(p1.score, '/',p2.score) as sc, p1.game_id " \
            f"FROM (SELECT IFNULL(nick, CONCAT('UID(',user_id,')')) as nick, score, user_id, game_id " \
            f"FROM participants " \
            f"LEFT JOIN users " \
            f"USING (user_id)) p1 " \
            f"LEFT JOIN (SELECT IFNULL(nick, CONCAT('UID(',user_id,')')) as nick, score, user_id, game_id " \
            f"FROM participants " \
            f"LEFT JOIN users " \
            f"USING (user_id)) p2 " \
            f"USING (game_id) " \
            f"WHERE p1.user_id < p2.user_id " \
            f"ORDER BY game_id) p " \
            f"USING (game_id)"
    glob_func.load_db(query, gh_widget)
    # load_db()

    config.glob_grid.setRowStretch(2, 1)
