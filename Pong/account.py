from PyQt6 import QtCore, QtGui, QtWidgets
import config
import glob_func
import hub
import bcrypt

account_widget = {
    'userlabel': [],
    'guildlabel': [],
    'info': [],
    'usernamelabel': [],
    'username': [],
    'usernamebutton': [],
    'maillabel': [],
    'mail': [],
    'mailbutton': [],
    'passwordlabel': [],
    'password': [],
    'password2label': [],
    'password2': [],
    'passwordbutton': [],
    'back': []
}


def username_change():
    change_info()
    new_user = account_widget['username'][-1].text()

    if config.login_params['username'] == new_user:
        change_info('Username is the same!', 'red')
        return

    try:
        query = f"SELECT * FROM users WHERE nick='{str(new_user)}'"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    if dbdata:
        change_info('Username is already taken!', 'red')
        return

    try:
        query = f"UPDATE users SET nick='{str(new_user)}' WHERE user_id='{str(config.login_params['userID'])}'"
        glob_func.insert_into_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    change_info('Username changed!', 'green')
    config.login_params['username'] = new_user
    account_widget['userlabel'][-1].setText(config.login_params['username'])


def mail_change():
    change_info()
    new_email = account_widget['mail'][-1].text()

    if config.login_params['email'] == new_email:
        change_info('E-mail is the same!', 'red')
        return

    try:
        query = f"SELECT * FROM users WHERE email='{str(new_email)}'"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    if dbdata:
        change_info('E-mail is already taken!', 'red')
        return

    try:
        query = f"UPDATE users SET email='{str(new_email)}' WHERE user_id='{str(config.login_params['userID'])}'"
        glob_func.insert_into_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    change_info('E-mail changed!', 'green')
    config.login_params['email'] = new_email


def password_change():
    change_info()
    pas1 = account_widget['password'][-1].text()
    pas2 = account_widget['password2'][-1].text()

    if pas1 == '' or pas2 == '':
        change_info('Enter correct data!', 'red')
        return

    if pas1 != pas2:
        change_info('Passwords are not the same!', 'red')
        return

    try:
        query = f"SELECT password FROM users WHERE user_id='{str(config.login_params['userID'])}'"
        dbdata = glob_func.get_from_db(query)
        dbdata = dbdata[0][0]
    except:
        change_info('Error during connection with DB', 'red')
        return

    if bcrypt.checkpw(pas1.encode('utf-8'), dbdata.encode('utf-8')):
        change_info('Old and new passwords are the same!', 'red')
        return

    hash_pas = bcrypt.hashpw(pas1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        query = f"UPDATE users SET password='{str(hash_pas)}' WHERE user_id='{str(config.login_params['userID'])}'"
        glob_func.insert_into_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    change_info('Password changed!', 'green')
    config.login_params['password'] = hash_pas


def change_info(text='', color='black'):
    account_widget['info'][-1].show()
    account_widget['info'][-1].setText(text)
    account_widget['info'][-1].setStyleSheet(f"color: {color};")


def line_edit_account(text, func, tab, tab_name):
    le = QtWidgets.QLineEdit()
    #le.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    le.setText(text)
    le.setMaximumWidth(config.glob_params['windows_width'] / 3)
    le.returnPressed.connect(func)
    # le.setStyleSheet(
    #     "margin: 0 380px;"
    # )
    tab[tab_name].append(le)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def label_account(text, align, tab, tab_name):
    label = QtWidgets.QLabel(text)
    label.setAlignment(align)
    tab[tab_name].append(label)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def account_ui():

    # User and Guild
    us = QtWidgets.QLabel(config.login_params['username'])
    us.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    account_widget['userlabel'].append(us)
    account_widget['userlabel'][-1].show()
    config.glob_grid.addWidget(account_widget['userlabel'][-1], 0, 2, QtCore.Qt.AlignmentFlag.AlignCenter)

    guil = QtWidgets.QLabel(config.login_params['guild'])
    guil.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    account_widget['guildlabel'].append(guil)
    account_widget['guildlabel'][-1].show()
    config.glob_grid.addWidget(account_widget['guildlabel'][-1], 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)

    # Info
    infl = label_account('', QtCore.Qt.AlignmentFlag.AlignLeft, account_widget, 'info')
    config.glob_grid.addWidget(infl, 3, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Username
    userl = label_account('Username:', QtCore.Qt.AlignmentFlag.AlignRight, account_widget, 'usernamelabel')
    config.glob_grid.addWidget(userl, 4, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    userle = line_edit_account(config.login_params['username'], username_change, account_widget, 'username')
    userle.setMaxLength(20)
    config.glob_grid.addWidget(userle, 4, 1)

    userb = glob_func.button_main('Save', username_change, account_widget, 'usernamebutton')
    config.glob_grid.addWidget(userb, 4, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Mail
    maill = label_account('E-mail:', QtCore.Qt.AlignmentFlag.AlignRight, account_widget, 'maillabel')
    config.glob_grid.addWidget(maill, 5, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    maille = line_edit_account(config.login_params['email'], mail_change, account_widget, 'mail')
    maille.setMaxLength(256)
    config.glob_grid.addWidget(maille, 5, 1)

    mailb = glob_func.button_main('Save', mail_change, account_widget, 'mailbutton')
    config.glob_grid.addWidget(mailb, 5, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Password
    pasl = label_account('Password:', QtCore.Qt.AlignmentFlag.AlignRight, account_widget, 'passwordlabel')
    config.glob_grid.addWidget(pasl, 6, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    pasle = line_edit_account('', password_change, account_widget, 'password')
    pasle.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pasle.setMaxLength(40)
    config.glob_grid.addWidget(pasle, 6, 1)

    pas2l = label_account('Repeat password:', QtCore.Qt.AlignmentFlag.AlignRight, account_widget, 'password2label')
    config.glob_grid.addWidget(pas2l, 7, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    pas2le = line_edit_account('', password_change, account_widget, 'password2')
    pas2le.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pas2le.setMaxLength(40)
    config.glob_grid.addWidget(pas2le, 7, 1)

    pasb = glob_func.button_main('Save', password_change, account_widget, 'passwordbutton')
    config.glob_grid.addWidget(pasb, 6, 2, 2, 1, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Back button
    backb = glob_func.button_main('Back', lambda: glob_func.go_to(account_widget, hub.hub_ui), account_widget, 'back')
    config.glob_grid.addWidget(backb, 9, 2, QtCore.Qt.AlignmentFlag.AlignCenter)

    config.glob_grid.setRowStretch(2, 1)
    config.glob_grid.setRowStretch(8, 1)
    config.glob_grid.setRowStretch(10, 1)