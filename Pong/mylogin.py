from PyQt6 import QtCore, QtGui, QtWidgets
import config
import glob_func
import hub
import bcrypt
from datetime import datetime

login_widget = {
    'login': [],
    'signin': [],
    'back': [],
    'username': [],
    'password': [],
    'password2': [],
    'mail': [],
    'info': []
}


def login_func():
    change_info()
    user = login_widget['username'][-1].text()
    pas = login_widget['password'][-1].text()

    if user == '' or pas == '':
        change_info('Enter correct data!', 'red')
        return

    try:
        query = f"SELECT user_id, password, admin, email, guild FROM users WHERE nick = convert('{str(user)}' using utf8mb4) collate utf8mb4_bin"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    if not dbdata:
        change_info('User does not exist!', 'red')
        return
    else:
        id, dbpass, isAdmin, email, guild = dbdata[0]

    if bcrypt.checkpw(pas.encode('utf-8'),dbpass.encode('utf-8')):
        config.login_params['userID'] = id
        config.login_params['username'] = user
        config.login_params['password'] = dbpass
        config.login_params['email'] = email
        config.login_params['guild'] = guild if guild else None
        config.login_params['isAdmin'] = isAdmin

        glob_func.grid_clear(login_widget)
        config.login_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        hub.hub_ui()
    else:
        change_info('Incorrect password!', 'red')
        return


def signin_func():
    change_info()
    user = login_widget['username'][-1].text()
    pas1 = login_widget['password'][-1].text()
    pas2 = login_widget['password2'][-1].text()
    email = login_widget['mail'][-1].text()

    # Poprawność danych
    if user == '' or pas1 == '' or pas2 == '' or email == '':
        change_info('Enter correct data!', 'red')
        return

    # Sprawdzenie obecności w bazie
    try:
        query = f"SELECT nick, email FROM users WHERE nick = '{str(user)}' OR email='{str(email)}'"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    # Jeżeli istnieje
    if len(dbdata) == 2:
        change_info('Username and email are already taken!', 'red')
        return
    elif len(dbdata) == 1:
        if dbdata[0][0] == user and dbdata[0][1] == email:
            change_info('Username and email are already taken!', 'red')
            return
        elif dbdata[0][0] == user:
            change_info('Username is already taken!', 'red')
            return
        else:
            change_info('Email already used!', 'red')
            return

    # Poprawność haseł
    if pas1 != pas2:
        change_info('Passwords are different!', 'red')
        return

    # Wpisywanie do bazy
    hashPas = bcrypt.hashpw(pas1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        query = f"INSERT INTO users(email, nick, password) VALUES ('{str(email)}','{str(user)}','{str(hashPas)}')"
        glob_func.insert_into_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    # Odbieranie danych z bazy
    try:
        query = f"SELECT user_id, password, admin, email FROM users WHERE nick = convert('{str(user)}' using utf8mb4) collate utf8mb4_bin"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    if not dbdata:
        change_info('Error during adding a user', 'red')
        return
    else:
        id, dbpass, isAdmin, email = dbdata[0]

    config.login_params['userID'] = id
    config.login_params['username'] = user
    config.login_params['password'] = dbpass
    config.login_params['email'] = email
    config.login_params['guild'] = None
    config.login_params['isAdmin'] = isAdmin

    glob_func.grid_clear(login_widget)
    config.login_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    hub.hub_ui()


def change_info(text='', color='black'):
    login_widget['info'][-1].show()
    login_widget['info'][-1].setText(text)
    login_widget['info'][-1].setStyleSheet(f"color: {color};")


def line_edit_login(text, func, tab, tab_name):
    le = QtWidgets.QLineEdit()
    le.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    le.setPlaceholderText(text)
    le.returnPressed.connect(func)
    le.setStyleSheet(
        "margin: 0 380px;"
    )
    tab[tab_name].append(le)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def login_ui():
    # Info
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    login_widget['info'].append(inf)
    login_widget['info'][-1].show()
    config.glob_grid.addWidget(login_widget['info'][-1], 1, 0)

    # Username
    logle = line_edit_login('Username', login_func, login_widget, 'username')
    logle.setMaxLength(20)
    config.glob_grid.addWidget(logle, 2, 0)

    # Password
    pasle = line_edit_login('Password', login_func, login_widget, 'password')
    pasle.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pasle.setMaxLength(40)
    config.glob_grid.addWidget(pasle, 3, 0)

    # Login button
    logb = glob_func.button_main('Login', login_func, login_widget, 'login', config.login_buttons)
    config.glob_grid.addWidget(logb, 4, 0)

    # Sign In button
    signb = glob_func.button_main('Sign In', lambda: glob_func.go_to(login_widget, signin_ui), login_widget, 'signin', config.login_buttons)
    config.glob_grid.addWidget(signb, 5, 0)

    config.glob_grid.setRowStretch(0, 1)
    config.glob_grid.setRowStretch(6, 1)


def signin_ui():
    # Info
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    login_widget['info'].append(inf)
    login_widget['info'][-1].show()
    config.glob_grid.addWidget(login_widget['info'][-1], 1, 0, QtCore.Qt.AlignmentFlag.AlignTop)

    # Username
    logle = line_edit_login('Username', signin_func, login_widget, 'username')
    logle.setMaxLength(20)
    config.glob_grid.addWidget(logle, 2, 0)

    # Password
    pas1le = line_edit_login('Password', signin_func, login_widget, 'password')
    pas1le.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pas1le.setMaxLength(40)
    config.glob_grid.addWidget(pas1le, 3, 0)

    # Password 2
    pas2le = line_edit_login('Repeat password', signin_func, login_widget, 'password2')
    pas2le.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pas2le.setMaxLength(40)
    config.glob_grid.addWidget(pas2le, 4, 0)

    # Email
    emle = line_edit_login('Email', signin_func, login_widget, 'mail')
    emle.setMaxLength(256)
    config.glob_grid.addWidget(emle, 5, 0)

    # Sign In button
    sigb = glob_func.button_main('Sign in', signin_func, login_widget, 'signin', config.login_buttons)
    config.glob_grid.addWidget(sigb, 6, 0)

    # Back button
    backb = glob_func.button_main('Back', lambda: glob_func.go_to(login_widget, login_ui), login_widget, 'back',
                                  config.login_buttons)
    config.glob_grid.addWidget(backb, 7, 0)

    config.glob_grid.setRowStretch(0, 1)
    config.glob_grid.setRowStretch(8, 1)
