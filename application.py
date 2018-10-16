import time
import os
import sys
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, disconnect, emit
import time
import multiprocessing
import serial
import serial.threaded
import serialworker

SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 9600

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
clients = []
ser = None

input_queue = multiprocessing.Queue()
output_queue = multiprocessing.Queue()

@app.route('/')
def root():
    return render_template('index.html')

@socketio.on('message', namespace='/webapp')
def handle_message(message):
    print('received message: ' + message)
    #input_queue.put(message)
    ser.write(message.encode('utf-8'))

@socketio.on('connect', namespace='/webapp')
def test_connect():
    emit("message", "hello client")
    print('new connection')


@socketio.on('disconnect', namespace='/webapp')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on_error(namespace='/webapp')
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))

if __name__ == '__main__':
    print("running")
    #sp = serialworker.SerialProcess(input_queue, output_queue)
    #sp.daemon = True
    #sp.start()
    # connect to serial port

    ser = serial.serial_for_url(SERIAL_PORT, do_not_open=True)
    ser.baudrate = SERIAL_BAUDRATE
    try:
        ser.open()
    except serial.SerialException as e:
        sys.stderr.write('Could not open serial port {}: {}\n'.format(ser.name, e))
        sys.exit(1)

    ser_to_net = serialworker.SerialToNet()
    ser_to_net.socket = socketio
    serial_worker = serial.threaded.ReaderThread(ser, ser_to_net)
    serial_worker.start()

    socketio.run(app, debug=True)
