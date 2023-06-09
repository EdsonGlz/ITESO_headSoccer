import socket
from _thread import *
from player import Player 
import  yaml
import pickle

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

path = config['path']
server = config['ip']
port = config['port']

print(str(path) + " " + str(server) + " " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e: 
    str(e) 


s.listen(2)

print("Waiting for connection. Server started")


players = [Player(50,500,50,50,(255,0,0)), Player(900,500,50,50,(0,0,255))]

def threaded_client(conn, player):
    ''' Crea la conexion entre el cliente y el servidor '''
    print(player)
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True: 
        try: 
            data = pickle.loads(conn.recv(2048))
            players[player] = data
            #reply = data.decode("utf-8")

            if not data: 
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                #print("Received ", data)
                #print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break 

    print("Lost connection")
    conn.close()



currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("connected to", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1