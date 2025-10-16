# server.py
import socket
import threading

HEADER = 128
FORMAT = 'utf-8'
PORT = 5050
DISCONNECT = '#EXIT#'

hostname = socket.gethostname()
SERVER = socket.gethostbyname(hostname)
ADDR = (SERVER, PORT)

clients = []
client_names = {}

def broadcast(message, sender_conn=None):
    """Send message to all connected clients except sender"""
    for client in clients:
        if client != sender_conn:
            try:
                msg_encoded = message.encode(FORMAT)
                msg_len = str(len(msg_encoded)).encode(FORMAT)
                msg_len += b' ' * (HEADER - len(msg_len))
                client.send(msg_len)
                client.send(msg_encoded)
            except:
                clients.remove(client)

def manage_client(con, addr):
    print(f'{addr} fellépett!\n')
    
    connected = True
    client_name = str(addr)
    msg = ''
    
    while connected:
        try:
            msg_len = con.recv(HEADER).decode(FORMAT)
        except:
            msg = '###########'
        
        if msg != '###########':
            msg_len = int(msg_len)
            msg = con.recv(msg_len).decode(FORMAT)
        
            if '#NAME# ' in msg:
                client_name = msg.replace('#NAME# ', '')
                client_names[con] = client_name
                broadcast(f'{client_name} csatlakozott a chathez', con)
            
            else:
                print(f'{client_name}: {msg}')
                broadcast(f'\n{client_name}: {msg}', con)
        
        else:
            connected = False
            print(f'{client_name} Kilépett!')
            broadcast(f'\n {client_name} kilépett a chatből', con)
    
    if con in clients:
        clients.remove(con)
    if con in client_names:
        del client_names[con]
    con.close()

def start(live_server):
    live_server.listen()
    while True:
        con, addr = live_server.accept()
        clients.append(con)
        thread = threading.Thread(target=manage_client, args=(con, addr))
        thread.start()
        print(f'szerver méret: {threading.active_count() - 1}\n')

def server():
    live_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    live_server.bind(ADDR)
    print('Indul a szerver...')
    print(hostname, SERVER)
    start(live_server)

if __name__ == '__main__':
    server()
