# client.py
import socket
import threading
from time import time
from flask import Flask, render_template

HEADER = 128
FORMAT = 'utf-8'
PORT = 5050
DISCONNECT = '#EXIT#'

startt = 0
messages = []

def send(msg, live_server):
    global startt
    endt = int(time() * 1000)
    if endt - startt >= 500 or startt == 0:
        msg += '\n'
        msg_to_send = msg.encode(FORMAT)
        msg_len = len(msg_to_send)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        live_server.send(send_len)
        live_server.send(msg_to_send)
        startt = int(time() * 1000)

def receive(live_server):
    """Receive messages from server"""
    while True:
        try:
            msg_len = live_server.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len.strip())
                msg = live_server.recv(msg_len).decode(FORMAT)
                messages.append(msg)
                print(msg)
        except:
            break

def client():
    ADDR = (input('address: '), PORT)
    live_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    live_server.connect(ADDR)

    receive_thread = threading.Thread(target=receive, args=(live_server,))
    receive_thread.start()
    receive_thread.join()

    gui =  threading.Thread(target=html, args=(messages,))
    gui.start()

    name = '#NAME# ' + input('Név: ')
    send(name, live_server)
    
    usr_input = ''
    while usr_input != DISCONNECT:
        usr_input = input(': ') + '\n'
        send(usr_input, live_server)

def html(msg):
    

    app = Flask(__name__)

    @app.route("/")
    def index(msg):
        return render_template("index.html", msg = str(msg))

    if __name__ == "__main__":
        app.run()

if __name__ == '__main__':
    client()
