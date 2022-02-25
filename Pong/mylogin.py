from PyQt6 import QtCore, QtGui, QtWidgets
import config
import hub

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


def flogin():
    print(login_widget['username'][-1].text())
    print(login_widget['password'][-1].text())
    login_clear()
    hub.hub_ui(config.window)
    pass


def fsignin():
    print(login_widget['username'][-1].text())
    print(login_widget['password'][-1].text())
    print(login_widget['password2'][-1].text())
    print(login_widget['mail'][-1].text())
    show_info('test', 'yellow')
    #login_clear()
    #hub.hub_ui(config.window)
    pass


def show_info(text, color):
    login_widget['info'][-1].show()
    login_widget['info'][-1].setText(text)
    login_widget['info'][-1].setStyleSheet(f"color: {color};")


def hide_info():
    login_widget['info'][-1].show()
    login_widget['info'][-1].setText('')


def draw_login():
    login_clear()

    #config.glob_grid.setRowStretch(0, 1)
    #config.glob_grid.setRowStretch(5, 1)

    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    login_widget['info'].append(inf)
    login_widget['info'][-1].show()
    #login_widget['info'][-1].setText('')
    config.glob_grid.addWidget(login_widget['info'][-1], 1, 0, QtCore.Qt.AlignmentFlag.AlignTop)

    logf = QtWidgets.QLineEdit(config.window)
    logf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logf.setPlaceholderText("Username")
    logf.returnPressed.connect(flogin)
    logf.setStyleSheet(
        "margin: 0 380px;"
    )
    login_widget['username'].append(logf)
    login_widget['username'][-1].show()
    config.glob_grid.addWidget(login_widget['username'][-1], 2, 0)

    logf2 = QtWidgets.QLineEdit(config.window)
    logf2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logf2.setPlaceholderText("Password")
    logf2.returnPressed.connect(flogin)
    logf2.setStyleSheet(
        "margin: 0 380px;"
    )
    login_widget['password'].append(logf2)
    login_widget['password'][-1].show()
    config.glob_grid.addWidget(login_widget['password'][-1], 3, 0)

    loginb = create_login_button("Login")
    loginb.clicked.connect(flogin)
    login_widget['login'].append(loginb)
    login_widget['login'][-1].show()
    config.glob_grid.addWidget(login_widget['login'][-1], 4, 0)

    signinb = create_login_button("Sign in")
    signinb.clicked.connect(draw_signin)
    login_widget['signin'].append(signinb)
    login_widget['signin'][-1].show()
    config.glob_grid.addWidget(login_widget['signin'][-1], 5, 0)

    config.glob_grid.setRowStretch(0, 1)
    config.glob_grid.setRowStretch(6, 1)


def draw_signin():
    login_clear()
    #login_widget['grid'][-1] = QtWidgets.QGridLayout()

    # Info
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    login_widget['info'].append(inf)
    login_widget['info'][-1].show()
    # login_widget['info'][-1].setText('')
    config.glob_grid.addWidget(login_widget['info'][-1], 1, 0, QtCore.Qt.AlignmentFlag.AlignTop)

    # Username
    logf = QtWidgets.QLineEdit(config.window)
    logf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logf.setPlaceholderText("Username")
    logf.returnPressed.connect(fsignin)
    logf.setStyleSheet(
        "margin: 0 380px;"
    )
    login_widget['username'].append(logf)
    login_widget['username'][-1].show()
    config.glob_grid.addWidget(login_widget['username'][-1], 2, 0)

    # Password
    logf2 = QtWidgets.QLineEdit(config.window)
    logf2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logf2.setPlaceholderText("Password")
    logf2.returnPressed.connect(fsignin)
    logf2.setStyleSheet(
        "margin: 0 380px;"
    )
    login_widget['password'].append(logf2)
    login_widget['password'][-1].show()
    config.glob_grid.addWidget(login_widget['password'][-1], 3, 0)

    # Password 2
    logf3 = QtWidgets.QLineEdit(config.window)
    logf3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logf3.setPlaceholderText("Repeat password")
    logf3.returnPressed.connect(fsignin)
    logf3.setStyleSheet(
        "margin: 0 380px;"
    )
    login_widget['password2'].append(logf3)
    login_widget['password2'][-1].show()
    config.glob_grid.addWidget(login_widget['password2'][-1], 4, 0)

    # Email
    logf4 = QtWidgets.QLineEdit(config.window)
    logf4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    logf4.setPlaceholderText("Email")
    logf4.returnPressed.connect(fsignin)
    logf4.setStyleSheet(
        "margin: 0 380px;"
    )
    login_widget['mail'].append(logf4)
    login_widget['mail'][-1].show()
    config.glob_grid.addWidget(login_widget['mail'][-1], 5, 0)

    # Sign In
    signinb = create_login_button("Sign in")
    signinb.clicked.connect(fsignin)
    login_widget['signin'].append(signinb)
    login_widget['signin'][-1].show()
    config.glob_grid.addWidget(login_widget['signin'][-1], 6, 0)

    back = create_login_button("Back")
    back.clicked.connect(draw_login)
    login_widget['back'].append(back)
    login_widget['back'][-1].show()
    config.glob_grid.addWidget(login_widget['back'][-1], 7, 0)

    config.glob_grid.setRowStretch(0, 1)
    config.glob_grid.setRowStretch(8, 1)




def create_login_button(text):
    button = QtWidgets.QPushButton(text)
    button.setStyleSheet(
        "margin: 0 420px;"
    )

    return button


def login_clear():
    for h in login_widget:
        if login_widget[h] != []:
            login_widget[h][-1].deleteLater()
        for i in range(len(login_widget[h])):
            login_widget[h] = []
    config.glob_grid.setRowStretch(0, 0)
    config.glob_grid.setRowStretch(6, 0)
    config.glob_grid.setRowStretch(8, 0)


def login_ui():
    draw_login()