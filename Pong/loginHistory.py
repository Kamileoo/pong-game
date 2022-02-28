from PyQt6 import QtCore, QtGui, QtWidgets
import config
import hub
import glob_func

lg_widget = {
    'db_view': [],
    'namelabel': [],
    'userlabel': [],
    'guildlabel': [],
    'back': [],
    'search_le': []
}


def lg_ui():
    data = ['User', 'Date In', 'Date Out', 'IP', 'System Version']
    glob_func.table_create('Login History', data, lg_widget, 5, lambda: glob_func.go_to(lg_widget, hub.hub_ui))

    query = f"SELECT nick, login_time, logout_time, ip_address, CONCAT(operating_system, ' ',system_version)" \
               f"FROM logins_history LEFT JOIN users USING (user_id)" \
               f"ORDER BY logout_time DESC"
    glob_func.load_db(query, lg_widget)

    config.glob_grid.setRowStretch(2, 1)
    config.glob_grid.setRowStretch(4, 1)

    # Search
    querySE = "SELECT nick, login_time, logout_time, ip_address, CONCAT(operating_system, ' ',system_version)" \
            "FROM logins_history LEFT JOIN users USING (user_id)" \
            "WHERE nick LIKE '%{}%'" \
            "ORDER BY nick, logout_time DESC "
    search = glob_func.le_search('Username', lambda: glob_func.search_func(querySE, query, lg_widget, 'search_le'), lg_widget, 'search_le')
    config.glob_grid.addWidget(search, 3, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

