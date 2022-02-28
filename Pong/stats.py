from PyQt6 import QtCore, QtGui, QtWidgets
import config
import glob_func
import hub

stat_widget = {
    'db_view': [],
    'namelabel': [],
    'userlabel': [],
    'guildlabel': [],
    'delete': [],
    'makeadmin': [],
    'back': [],
    'search_le': []
}


def delete_button():
    row = stat_widget['db_view'][-1].currentRow()

    if row == -1:
        return

    user_id = stat_widget['db_view'][-1].item(row, stat_widget['db_view'][-1].columnCount()-1).text()

    try:
        query = f"DELETE FROM users WHERE user_id='{str(user_id)}'"
        glob_func.insert_into_db(query)
    except:
        print('ERROR')
        return

    glob_func.grid_clear(stat_widget)
    stat_ui()


def admin_switch_button():
    row = stat_widget['db_view'][-1].currentRow()

    if row == -1:
        return

    user_id = stat_widget['db_view'][-1].item(row, stat_widget['db_view'][-1].columnCount()-1).text()

    try:
        query = f"UPDATE users SET admin=ABS(admin-1) WHERE user_id='{str(user_id)}'"
        glob_func.insert_into_db(query)
    except:
        print('ERROR')
        return

    glob_func.grid_clear(stat_widget)
    stat_ui()


def stat_ui():

    data = ['User', 'No games', 'Wins', 'Losses', 'Ties', 'E-mail', 'Guild', 'Is Admin', 'User ID']
    glob_func.table_create('Statistics', data, stat_widget, 8, lambda: glob_func.go_to(stat_widget, hub.hub_ui))
    stat_widget['db_view'][-1].setColumnHidden(len(data) - 1, True)

    query = f"SELECT nick, no_games, no_wins, no_loses, no_ties, email, guild, admin, user_id FROM users"
    glob_func.load_db(query, stat_widget)

    # Search
    querySE = "SELECT nick, no_games, no_wins, no_loses, no_ties, email, guild, admin, user_id FROM users WHERE nick LIKE '%{}%'"
    search = glob_func.le_search('Username', lambda: glob_func.search_func(querySE, query, stat_widget, 'search_le'),
                                 stat_widget, 'search_le')
    config.glob_grid.addWidget(search, 3, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

    # Delete
    dele = glob_func.button_main('Delete', delete_button, stat_widget, 'delete')
    if not config.login_params['isAdmin']: dele.hide()
    config.glob_grid.addWidget(dele, 5, 1)

    # Switch Admin
    sa = glob_func.button_main('Switch Admin', admin_switch_button, stat_widget, 'makeadmin')
    if not config.login_params['isAdmin']: sa.hide()
    config.glob_grid.addWidget(sa, 6, 1)

    config.glob_grid.setRowStretch(2, 1)
    config.glob_grid.setRowStretch(4, 1)
    config.glob_grid.setRowStretch(7, 1)
