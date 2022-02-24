from PyQt6 import QtCore, QtGui, QtWidgets
import config
import hub

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
    print(account_widget['username'][-1].text())
    show_info('testting', 'green')
    refresh_user()


def mail_change():
    print(account_widget['mail'][-1].text())
    show_info('Reddddddd', 'red')


def password_change():
    print(account_widget['password'][-1].text())
    print(account_widget['password2'][-1].text())


def to_hub():
    account_clear()
    hub.hub_ui(config.window)


def show_info(text, color):
    account_widget['info'][-1].show()
    account_widget['info'][-1].setText(text)
    account_widget['info'][-1].setStyleSheet(f"color: {color};")


def hide_info():
    account_widget['info'][-1].show()
    account_widget['info'][-1].setText('')


def refresh_user():
    account_widget['userlabel'][-1].setText(config.login_params['username'])


def draw():
    account_clear()

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
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    account_widget['info'].append(inf)
    account_widget['info'][-1].show()
    config.glob_grid.addWidget(account_widget['info'][-1], 3, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Username
    userl = QtWidgets.QLabel('Username:')
    userl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    account_widget['usernamelabel'].append(userl)
    account_widget['usernamelabel'][-1].show()
    config.glob_grid.addWidget(account_widget['usernamelabel'][-1], 4, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    userbox = QtWidgets.QLineEdit(config.window)
    #userbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    userbox.setText(config.login_params['username'])
    userbox.setMaximumWidth(config.glob_params['windows_width'] / 3 - 15)
    account_widget['username'].append(userbox)
    account_widget['username'][-1].show()
    config.glob_grid.addWidget(account_widget['username'][-1], 4, 1)

    usern = QtWidgets.QPushButton("Save")
    usern.clicked.connect(username_change)
    account_widget['usernamebutton'].append(usern)
    account_widget['usernamebutton'][-1].show()
    config.glob_grid.addWidget(account_widget['usernamebutton'][-1], 4, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Mail
    maill = QtWidgets.QLabel('E-mail:')
    maill.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    account_widget['maillabel'].append(maill)
    account_widget['maillabel'][-1].show()
    config.glob_grid.addWidget(account_widget['maillabel'][-1], 5, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    mailbox = QtWidgets.QLineEdit(config.window)
    # mailbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    mailbox.setText(config.login_params['email'])
    mailbox.setMaximumWidth(config.glob_params['windows_width'] / 3 - 15)
    account_widget['mail'].append(mailbox)
    account_widget['mail'][-1].show()
    config.glob_grid.addWidget(account_widget['mail'][-1], 5, 1)

    mailb = QtWidgets.QPushButton("Save")
    mailb.clicked.connect(mail_change)
    account_widget['mailbutton'].append(mailb)
    account_widget['mailbutton'][-1].show()
    config.glob_grid.addWidget(account_widget['mailbutton'][-1], 5, 2, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Password
    passl = QtWidgets.QLabel('Password:')
    passl.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    account_widget['passwordlabel'].append(passl)
    account_widget['passwordlabel'][-1].show()
    config.glob_grid.addWidget(account_widget['passwordlabel'][-1], 6, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    passbox = QtWidgets.QLineEdit(config.window)
    # passbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    passbox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    passbox.setMaximumWidth(config.glob_params['windows_width'] / 3 - 15)
    account_widget['password'].append(passbox)
    account_widget['password'][-1].show()
    config.glob_grid.addWidget(account_widget['password'][-1], 6, 1)

    pass2l = QtWidgets.QLabel('Repeat password:')
    pass2l.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    account_widget['password2label'].append(pass2l)
    account_widget['password2label'][-1].show()
    config.glob_grid.addWidget(account_widget['password2label'][-1], 7, 0, QtCore.Qt.AlignmentFlag.AlignRight)

    pass2box = QtWidgets.QLineEdit(config.window)
    # pass2box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    pass2box.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    pass2box.setMaximumWidth(config.glob_params['windows_width'] / 3 - 15)
    account_widget['password2'].append(pass2box)
    account_widget['password2'][-1].show()
    config.glob_grid.addWidget(account_widget['password2'][-1], 7, 1)

    passb = QtWidgets.QPushButton("Save")
    passb.clicked.connect(password_change)
    account_widget['passwordbutton'].append(passb)
    account_widget['passwordbutton'][-1].show()
    config.glob_grid.addWidget(account_widget['passwordbutton'][-1], 6, 2, 2, 1, QtCore.Qt.AlignmentFlag.AlignLeft)

    # Back button
    back = QtWidgets.QPushButton("Back")
    back.clicked.connect(to_hub)
    account_widget['back'].append(back)
    account_widget['back'][-1].show()
    config.glob_grid.addWidget(account_widget['back'][-1], 9, 2, QtCore.Qt.AlignmentFlag.AlignCenter)


    config.glob_grid.setRowStretch(2, 1)
    config.glob_grid.setRowStretch(8, 1)
    config.glob_grid.setRowStretch(10, 1)


def account_clear():
    for h in account_widget:
        if account_widget[h] != []:
            account_widget[h][-1].deleteLater()
        for i in range(len(account_widget[h])):
            account_widget[h] = []
    config.glob_grid.setRowStretch(2, 0)
    config.glob_grid.setRowStretch(8, 0)
    config.glob_grid.setRowStretch(10, 0)


def account_ui():
    draw()