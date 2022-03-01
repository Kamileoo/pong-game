from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import config
import glob_func
import hub
import membersList
import bcrypt

guild_widget = {
    'db_view': [],
    'namelabel': [],
    'userlabel': [],
    'guildlabel': [],
    'back': [],
    'search_le': [],
    'join': [],
    'leave': [],
    'members': [],
    'create': [],
    'change': [],
    'delete': []
}

new_win = {
    'new_window': [],
    'grid': [],
    'info': [],
    'line1': [],
    'line2': [],
    'line3': [],
    'save': [],
    'cancel': [],
    'info2': []
}


class New_Window(QtWidgets.QWidget):
    def __init__(self):
        super(New_Window, self).__init__()

    def closeEvent(self, event):
        # self.close()
        cleaner()


def cleaner():
    for h in new_win:
        if new_win[h] != []:
            new_win[h][-1].deleteLater()
        for i in range(len(new_win[h])):
            new_win[h] = []


def change_info(text='', color='black'):
    new_win['info'][-1].show()
    new_win['info'][-1].setText(text)
    new_win['info'][-1].setStyleSheet(f"color: {color};")


def line_edit_login(text, place_text, func, tab, tab_name):
    le = QtWidgets.QLineEdit()
    le.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    le.setText(text)
    le.setPlaceholderText(place_text)
    le.returnPressed.connect(func)
    # le.setStyleSheet(
    #     "margin: 0 380px;"
    # )
    tab[tab_name].append(le)
    tab[tab_name][-1].show()
    return tab[tab_name][-1]


def join_button():
    change_info()
    guild = new_win['line1'][-1].text()
    pas = new_win['line2'][-1].text()

    if guild == '' or pas == '':
        change_info('Enter correct data!', 'red')
        return

    try:
        query = f"SELECT name, password FROM guilds WHERE name ='{str(guild)}'"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    if not dbdata:
        change_info('Guild does not exist!', 'red')
        return
    else:
        guild, dpas = dbdata[0]

    if bcrypt.checkpw(pas.encode('utf-8'),dpas.encode('utf-8')):
        try:
            query = f"UPDATE users SET guild='{str(guild)}' WHERE user_id ='{str(config.login_params['userID'])}'"
            dbdata = glob_func.insert_into_db(query)
        except:
            change_info('Error during connection with DB', 'red')
            return

        config.login_params['guild'] = guild
        glob_func.grid_clear(guild_widget)
        guild_ui()
        new_win['new_window'][-1].close()
    else:
        change_info('Incorrect password!', 'red')
        return


def join_func():
    if new_win['new_window']:
        return

    cleaner()

    win = New_Window()
    win.setWindowTitle("Join")
    win.setFixedSize(320, 220)
    new_win['new_window'].append(win)
    new_win['new_window'][-1].show()

    grid = QtWidgets.QGridLayout(new_win['new_window'][-1])
    new_win['grid'].append(grid)

    # Info
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
    new_win['info'].append(inf)
    new_win['info'][-1].show()
    new_win['grid'][-1].addWidget(new_win['info'][-1], 1, 0, 1, 2)

    # Guild name
    row = guild_widget['db_view'][-1].currentRow()
    if row == -1:
        gname = ''
    else:
        gname = guild_widget['db_view'][-1].item(row, 0).text()

    gn = line_edit_login(gname, 'Guild name',  join_button, new_win, 'line1')
    gn.setMaxLength(20)
    new_win['grid'][-1].addWidget(gn, 2, 0, 1, 2)

    gp = line_edit_login('', 'Password', join_button, new_win, 'line2')
    gp.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    gp.setMaxLength(40)
    new_win['grid'][-1].addWidget(gp, 3, 0, 1, 2)

    sv = glob_func.button_main('Join', join_button, new_win, 'save')
    new_win['grid'][-1].addWidget(sv, 4, 1)

    cl = glob_func.button_main('Cancel', new_win['new_window'][-1].close, new_win, 'cancel')
    new_win['grid'][-1].addWidget(cl, 4, 0)


    new_win['grid'][-1].setRowStretch(0,1)
    new_win['grid'][-1].setRowStretch(5, 1)


def create_new_button():
    change_info()
    guild = new_win['line1'][-1].text()
    pas = new_win['line2'][-1].text()
    pas2 = new_win['line3'][-1].text()

    if guild == '' or pas == '' or pas2 == '':
        change_info('Enter correct data!', 'red')
        return

    try:
        query = f"SELECT name FROM guilds WHERE name ='{str(guild)}'"
        dbdata = glob_func.get_from_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    if len(dbdata) >= 1:
        change_info('Guild already exist!', 'red')
        return

    # Poprawność haseł
    if pas != pas2:
        change_info('Passwords are different!', 'red')
        return

    has_pas = bcrypt.hashpw(pas.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Wpisywanie do bazy
    try:
        query = f"INSERT INTO guilds(name, password) VALUES ('{str(guild)}','{str(has_pas)}')"
        glob_func.insert_into_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    try:
        query = f"UPDATE users SET guild='{str(guild)}' WHERE user_id='{str(config.login_params['userID'])}'"
        glob_func.insert_into_db(query)
    except:
        change_info('Error during connection with DB', 'red')
        return

    config.login_params['guild'] = guild
    glob_func.grid_clear(guild_widget)
    guild_ui()
    new_win['new_window'][-1].close()


def create_new():
    if new_win['new_window']:
        return

    cleaner()

    win = New_Window()
    win.setWindowTitle("Create new")
    win.setFixedSize(320, 220)
    new_win['new_window'].append(win)
    new_win['new_window'][-1].show()

    grid = QtWidgets.QGridLayout(new_win['new_window'][-1])
    new_win['grid'].append(grid)

    # Info
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
    new_win['info'].append(inf)
    new_win['info'][-1].show()
    new_win['grid'][-1].addWidget(new_win['info'][-1], 1, 0, 1, 2)

    # Guild name
    gn = line_edit_login('', 'Guild name', create_new_button, new_win, 'line1')
    gn.setMaxLength(20)
    new_win['grid'][-1].addWidget(gn, 2, 0, 1, 2)

    gp = line_edit_login('', 'Password', create_new_button, new_win, 'line2')
    gp.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    gp.setMaxLength(40)
    new_win['grid'][-1].addWidget(gp, 3, 0, 1, 2)

    gp2 = line_edit_login('', 'Repeat password', create_new_button, new_win, 'line3')
    gp2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    gp2.setMaxLength(40)
    new_win['grid'][-1].addWidget(gp2, 4, 0, 1, 2)

    sv = glob_func.button_main('Create', create_new_button, new_win, 'save')
    new_win['grid'][-1].addWidget(sv, 5, 1)

    cl = glob_func.button_main('Cancel', new_win['new_window'][-1].close, new_win, 'cancel')
    new_win['grid'][-1].addWidget(cl, 5, 0)

    new_win['grid'][-1].setRowStretch(0, 1)
    new_win['grid'][-1].setRowStretch(6, 1)


def leave_func():
    try:
        query = f"UPDATE users SET guild=NULL WHERE user_id='{str(config.login_params['userID'])}'"
        glob_func.insert_into_db(query)
    except:
        print('Error')
        return

    config.login_params['guild']=None
    glob_func.grid_clear(guild_widget)
    guild_ui()


def members():
    row = guild_widget['db_view'][-1].currentRow()

    if row == -1:
        return
    name = guild_widget['db_view'][-1].item(row, 0).text()

    glob_func.go_to(guild_widget,lambda: membersList.members_ui(name))


def change_button():
    change_info()
    old = new_win['line1'][-1].text()
    new = new_win['line2'][-1].text()
    pas = new_win['line3'][-1].text()

    if old == '' or new == '':
        change_info('Enter correct data!', 'red')
        return

    if old == new and pas=='':
        change_info('Names are the same!', 'red')
        return

    if old == new and pas!='':
        hash_pas = bcrypt.hashpw(pas.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        try:
            query = f"UPDATE guilds SET password='{str(hash_pas)}' WHERE name='{str(old)}'"
            glob_func.insert_into_db(query)
        except:
            print('Error')
            return
        new_win['new_window'][-1].close()

    if old!=new:
        try:
            query = f"SELECT name FROM guilds WHERE name ='{str(new)}'"
            dbdata = glob_func.get_from_db(query)
        except:
            change_info('Error during connection with DB', 'red')
            return

        if len(dbdata) >=1:
            change_info('Guild with that name already exist!', 'red')
            return

        if pas=='':
            query = f"UPDATE guilds SET name='{str(new)}' WHERE name ='{str(old)}'"
        else:
            query = f"UPDATE guilds SET name='{str(new)}', password='{str(pas)}' WHERE name ='{str(old)}'"

        try:
            glob_func.insert_into_db(query)
        except:
            print('Error')
            return

        if old == config.login_params['guild']: config.login_params['guild'] = new
        glob_func.grid_clear(guild_widget)
        guild_ui()
        new_win['new_window'][-1].close()


def change_func():
    if new_win['new_window']:
        return

    cleaner()

    win = New_Window()
    win.setWindowTitle("Change")
    win.setFixedSize(360, 320)
    new_win['new_window'].append(win)
    new_win['new_window'][-1].show()

    grid = QtWidgets.QGridLayout(new_win['new_window'][-1])
    new_win['grid'].append(grid)

    # Info
    inf = QtWidgets.QLabel('')
    inf.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
    new_win['info'].append(inf)
    new_win['info'][-1].show()
    new_win['grid'][-1].addWidget(new_win['info'][-1], 1, 0, 1, 2)

    # Guild name and password
    row = guild_widget['db_view'][-1].currentRow()
    if row == -1:
        gname = ''
    else:
        gname = guild_widget['db_view'][-1].item(row, 0).text()

    # Old name
    gn = line_edit_login(gname, 'Old name', change_button, new_win, 'line1')
    gn.setMaxLength(20)
    new_win['grid'][-1].addWidget(gn, 2, 0, 1, 2)

    # New name
    gn2 = line_edit_login(gname, 'New name', change_button, new_win, 'line2')
    gn2.setMaxLength(20)
    new_win['grid'][-1].addWidget(gn2, 3, 0, 1, 2)

    # Password
    gp = line_edit_login('', 'New password', change_button, new_win, 'line3')
    gp.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    gp.setMaxLength(40)
    new_win['grid'][-1].addWidget(gp, 4, 0, 1, 2)

    # Info
    inf2 = QtWidgets.QLabel('Leave password empty to not change it')
    inf2.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
    new_win['info2'].append(inf2)
    new_win['info2'][-1].show()
    new_win['grid'][-1].addWidget(new_win['info2'][-1], 5, 0, 1, 2)

    sv = glob_func.button_main('Save', change_button, new_win, 'save')
    new_win['grid'][-1].addWidget(sv, 6, 1)

    cl = glob_func.button_main('Cancel', new_win['new_window'][-1].close, new_win, 'cancel')
    new_win['grid'][-1].addWidget(cl, 6, 0)

    new_win['grid'][-1].setRowStretch(0, 1)
    new_win['grid'][-1].setRowStretch(7, 1)


def del_func():
    row = guild_widget['db_view'][-1].currentRow()

    if row == -1:
        return

    gname = guild_widget['db_view'][-1].item(row, 0).text()

    try:
        query = f"DELETE FROM guilds WHERE name='{str(gname)}'"
        glob_func.insert_into_db(query)
    except:
        print('ERROR')
        return

    if gname == config.login_params['guild']: config.login_params['guild'] = None
    glob_func.grid_clear(guild_widget)
    guild_ui()


def guild_ui():

    data = ['Name', 'Number of players']
    glob_func.table_create('Guilds', data, guild_widget, 11, lambda: glob_func.go_to(guild_widget, hub.hub_ui))

    # Load to DB
    query = f"SELECT g.name, u.nr " \
            f"FROM guilds g " \
            f"LEFT JOIN (SELECT guild, COUNT(*) as 'nr' FROM users GROUP BY guild) u " \
            f"ON g.name = u.guild;"

    glob_func.load_db(query, guild_widget)

    # Search
    querySE = "SELECT g.name, u.nr " \
              "FROM guilds g " \
              "LEFT JOIN (SELECT guild, COUNT(*) as 'nr' FROM users GROUP BY guild) u " \
              "ON g.name = u.guild " \
              "WHERE g.name LIKE '%{}%';"
    search = glob_func.le_search('Name', lambda: glob_func.search_func(querySE, query, guild_widget, 'search_le'), guild_widget, 'search_le')
    config.glob_grid.addWidget(search, 3, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

    # Join
    jo = glob_func.button_main('Join', join_func, guild_widget, 'join')
    if config.login_params['guild'] is not None: jo.hide()
    config.glob_grid.addWidget(jo, 4, 1)

    # Leave
    le = glob_func.button_main('Leave', leave_func, guild_widget, 'leave')
    if config.login_params['guild'] is None: le.hide()
    config.glob_grid.addWidget(le, 4, 1)

    # Members
    mem = glob_func.button_main('Members', members, guild_widget, 'members')
    config.glob_grid.addWidget(mem, 5, 1)

    # Create new
    cn = glob_func.button_main('Create new', create_new, guild_widget, 'create')
    if config.login_params['guild'] is not None: cn.hide()
    config.glob_grid.addWidget(cn, 6, 1)

    # Change
    ch = glob_func.button_main('Change', change_func, guild_widget, 'change')
    if not config.login_params['isAdmin']: ch.hide()
    config.glob_grid.addWidget(ch, 8, 1)

    # Delete
    de = glob_func.button_main('Delete', del_func, guild_widget, 'delete')
    if not config.login_params['isAdmin']: de.hide()
    config.glob_grid.addWidget(de, 9, 1)


    config.glob_grid.setRowStretch(2, 2)
    if config.login_params['isAdmin']: config.glob_grid.setRowStretch(7, 1)
    config.glob_grid.setRowStretch(10, 2)
