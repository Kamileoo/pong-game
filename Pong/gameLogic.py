from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket
import config
import game
import mysql.connector
from datetime import datetime
# Game itself
class MyGame(QtCore.QObject):

    finished = QtCore.pyqtSignal()

    def run(self):
        print("RUN")
        my_id=config.login_params['userID']
        socket = QTcpSocket()
        socket.connected.connect(lambda: print("Polączono z serwerem"))
        socket.disconnected.connect(lambda: print("Disconnected"))
        ip=config.glob_params['ip']
        port=int(config.glob_params['port'])
        socket.connectToHost(ip, port, protocol=QAbstractSocket.NetworkLayerProtocol.IPv4Protocol)
        socket.waitForConnected(-1)
        #send your id to server
        socket.write(str(my_id).encode('ascii'))
        socket.waitForBytesWritten(-1)
        game_val=game.game_val
        game_val['my_score'] = 0
        game_val['en_score'] = 0
        base = list('00000')
        win=-1
        start_datetime=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        while 1:
            game_val = game.game_val
            socket.waitForReadyRead(-1)
            buff = socket.readLine(20).decode("ascii")
            positions = [int(elem) for elem in buff.split(',')]
            print(positions)
            if positions[:2]==[-1, -1]:
                win=positions[3]
                if win:
                    game_val['my_score']=1
                else:
                    game_val['en_score']=1
                break
            game_val['my_pos_x'] = positions[0]
            game_val['en_pos_x'] = positions[1]
            game_val['ball_x'] = positions[2]
            game_val['ball_y'] = positions[3]
            game.draw()
            move = game_val['move_x']
            if move != 0:
                sign='+' if move>=0 else '-'
                move=abs(move)
                move_string=str(move)
                offset=len(base)-len(move_string)-1
                for idx, elem in enumerate(move_string):
                    base[idx+offset]=elem
                base[-1]=sign
                print(''.join(base).encode('ascii'))
                socket.write(''.join(base).encode('ascii'))
                socket.waitForBytesWritten(-1)
                game_val['move_x']=0
                base = list('00000')
        if win==0:
            socket.waitForReadyRead(-1)
            buff=socket.readLine(20).decode("ascii")
            players_ids = [int(elem) for elem in buff.split(',')]
            winner_id=players_ids[0] if players_ids[1]==my_id else players_ids[1]
            end_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            try:
                connection = mysql.connector.connect(**config.db_params)
                cur = connection.cursor()
                val = (start_datetime, end_datetime, my_id, winner_id)
                cur.callproc('add_game', val)
                connection.commit()
            except Exception as e:
                print(e)
        game.game_is_over()
        # #fragment for login update
        # connection = mysql.connector.connect(
        #     user='user',
        #     host='192.168.0.12',
        #     password='123',
        #     database='pong')
        # cur = connection.cursor()
        # import platform
        # import socket as sock
        # os, os_version=platform.platform().split('-')[0:2]
        # ip = sock.gethostbyname(sock.gethostname())
        # val = (os, os_version, ip, my_id, login_datetime)
        # cur.callproc('add_login_event', val)
        # connection.commit()


