from PyQt6 import QtCore, QtGui, QtWidgets
import config
import mysql.connector
import platform
import socket as sock


def get_from_db(query):
    connection = mysql.connector.connect(**config.db_params)
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    connection.close()
    return result


def insert_into_db(query):
    connection = mysql.connector.connect(**config.db_params)
    cur = connection.cursor()
    cur.execute(query)
    connection.commit()
    cur.close()
    connection.close()


def grid_clear(tab):
    for i in range(config.glob_grid.rowCount()):
        config.glob_grid.setRowStretch(i, 0)
    for i in range(config.glob_grid.columnCount()):
        config.glob_grid.setColumnStretch(i, 0)
        config.glob_grid.setColumnMinimumWidth(i, 0)

    for h in tab:
        if tab[h] != []:
            tab[h][-1].deleteLater()
        for i in range(len(tab[h])):
            tab[h] = []


def button_back(func, tab, tab_name):
    button = QtWidgets.QPushButton("Back")
    # back.setStyleSheet(
    #     "margin: 0px 10px;" +
    #     "padding: 10px 10px;"
    # )
    button.clicked.connect(func)
    tab[tab_name].append(button)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def button_main(text, func, tab, tab_name, style=""):
    button = QtWidgets.QPushButton(text)
    button.setStyleSheet(style)
    button.clicked.connect(func)
    tab[tab_name].append(button)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def label_box(text, tab, tab_name):
    label = QtWidgets.QLabel(text)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    label.setStyleSheet(
        "font: bold 20px;"
    )
    tab[tab_name].append(label)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def table_create(name, data, tab, back_pos, back_func):
    # Database
    db = QtWidgets.QTableWidget()
    db.setRowCount(0)
    db.setColumnCount(len(data))
    # db.setColumnHidden(len(data) - 1, True)
    db.setHorizontalHeaderLabels(data)

    db.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

    header = db.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    tab['db_view'].append(db)
    tab['db_view'][-1].show()
    config.glob_grid.addWidget(tab['db_view'][-1], 2, 0, back_pos-1, 1)

    # Name
    nam = QtWidgets.QLabel(name)
    nam.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    nam.setStyleSheet(config.table_header)
    tab['namelabel'].append(nam)
    tab['namelabel'][-1].show()
    config.glob_grid.addWidget(tab['namelabel'][-1], 0, 0, 2, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)

    # User and Guild
    us = QtWidgets.QLabel(config.login_params['username'])
    us.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    tab['userlabel'].append(us)
    tab['userlabel'][-1].show()
    config.glob_grid.addWidget(tab['userlabel'][-1], 0, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

    guil = QtWidgets.QLabel(config.login_params['guild'])
    guil.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    tab['guildlabel'].append(guil)
    tab['guildlabel'][-1].show()
    config.glob_grid.addWidget(tab['guildlabel'][-1], 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)


    # Back button
    config.glob_grid.addWidget(button_main('Back', back_func, tab, 'back'), back_pos, 1)


def load_db(query, tab, tab_name='db_view'):
    tab[tab_name][-1].clearContents()
    tab[tab_name][-1].setRowCount(0)
    try:
        result = get_from_db(query)
    except:
        print('ERROR')
        return

    for row_number, row_data in enumerate(result):
        tab[tab_name][-1].insertRow(row_number)
        for column_number, data in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(data))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable)
            tab[tab_name][-1].setItem(row_number, column_number, item)


def logout_func():
    connection = mysql.connector.connect(**config.db_params)
    cur = connection.cursor()
    os, os_version=platform.platform().split('-')[0:2]
    ip = sock.gethostbyname(sock.gethostname())
    val = (os, os_version, ip, config.login_params['userID'], config.login_datetime)
    cur.callproc('add_login_event', val)
    connection.commit()
    cur.close()
    connection.close()


def go_to(to_clean, to_open):
    grid_clear(to_clean)
    to_open()


def le_search(text, func, tab, tab_name, style=""):
    le = QtWidgets.QLineEdit()
    le.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    le.setStyleSheet(style)
    le.setPlaceholderText(text)
    le.setMaximumWidth(100)
    le.returnPressed.connect(func)
    le.textChanged.connect(func)
    tab[tab_name].append(le)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def search_func(query, querySTD, tab, tab_name):
    search = tab[tab_name][-1].text()

    if search == '':
        load_db(querySTD, tab)
        return

    load_db(query.format(search), tab)
