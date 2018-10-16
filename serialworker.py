import socket
import serial
import serial.threaded
import time
import multiprocessing


class SerialToNet(serial.threaded.Protocol):
    """serial->socket"""

    def __init__(self):
        self.socket = None

    def __call__(self):
        return self

    def data_received(self, data):
        if self.socket is not None:
            print(data.decode('utf-8'))
            self.socket.emit("message", data)
