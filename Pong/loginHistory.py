from PyQt6 import QtCore, QtGui, QtWidgets
import config
import hub
import mysql.connector

lg_widget = {
    'db_view': [],
    'userlabel': [],
    'guildlabel': [],
    'back': [],

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


def back_button():
    lg_clear()
    hub.hub_ui(config.window)

test = [('Antoni','15.02','15.02','192.158.1.1','Windows 10'),('Artur','15.06.2021 15:38:15','15.06.2021 18:40:38','125.135.186.200','Windows 10')]

def load_db():
    # connection = mysql.connector.connect(
    #     host=config.db_params['host'],
    #     user=config.db_params['user'],
    #     password=config.db_params['password'],
    #     database=config.db_params['database'],
    # )
    # query = "SELECT X FROM Y"
    # cur = connection.cursor()
    # cur.execute(query)
    # result = cur.fetchall()
    result = test
    print(test)
    for row_number, row_data in enumerate(result):
        lg_widget['db_view'][-1].insertRow(row_number)
        for column_number, data in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(data))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            #item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable)
            lg_widget['db_view'][-1].setItem(row_number, column_number, item)

    # cur.close()


def lg_clear():
    for h in lg_widget:
        if lg_widget[h] != []:
            lg_widget[h][-1].deleteLater()
        for i in range(len(lg_widget[h])):
            lg_widget[h] = []
    config.glob_grid.setRowStretch(2, 0)




def lg_ui():

    # Database
    db = QtWidgets.QTableWidget()
    db.setRowCount(0)
    db.setColumnCount(5)
    db.setHorizontalHeaderLabels(['User', 'Date In', 'Date Out', 'IP', 'System Version'])

    # db.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    header = db.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    lg_widget['db_view'].append(db)
    lg_widget['db_view'][-1].show()
    config.glob_grid.addWidget(lg_widget['db_view'][-1], 0, 0, 5, 1)

    load_db()

    # User and Guild
    us = QtWidgets.QLabel(config.login_params['username'])
    us.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    lg_widget['userlabel'].append(us)
    lg_widget['userlabel'][-1].show()
    config.glob_grid.addWidget(lg_widget['userlabel'][-1], 0, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

    guil = QtWidgets.QLabel(config.login_params['guild'])
    guil.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    lg_widget['guildlabel'].append(guil)
    lg_widget['guildlabel'][-1].show()
    config.glob_grid.addWidget(lg_widget['guildlabel'][-1], 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

    # Back button
    back = QtWidgets.QPushButton("Back")
    # back.setStyleSheet(
    #     "margin: 0px 10px;" +
    #     "padding: 10px 10px;"
    # )
    back.clicked.connect(back_button)
    lg_widget['back'].append(back)
    lg_widget['back'][-1].show()
    config.glob_grid.addWidget(lg_widget['back'][-1], 4, 1)

    config.glob_grid.setRowStretch(2, 1)

    pass