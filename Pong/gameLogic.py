
from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsEllipseItem, QPushButton
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket
import sys
import main
import game
import time


# Game itself
class MyGame(QtCore.QObject):

    finished = QtCore.pyqtSignal()

    def run(self):
        print("RUN")
        socket = QTcpSocket()
        socket.connected.connect(lambda: print("POlączono z serwerem"))
        socket.disconnected.connect(lambda: print("Disconnected"))
        ip=main.glob_params['ip']
        port=int(main.glob_params['port'])
        socket.connectToHost(ip, port, protocol=QAbstractSocket.NetworkLayerProtocol.IPv4Protocol)
        socket.waitForConnected(-1)
        socket.waitForReadyRead(-1)

        game_val=game.game_val
        base = list('00000')
        while 1:
            game_val = game.game_val
            socket.waitForReadyRead(-1)
            buff = socket.readLine(20).decode("ascii")
            print(buff)
            positions = [int(elem) for elem in buff.split(',')]
            print(positions)
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
