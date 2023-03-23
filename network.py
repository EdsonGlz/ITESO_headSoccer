import socket
import pickle

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "148.201.50.17"  #ITESO
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    def getP(self):
        ''' Obtiene al jugador que se conecto '''
        return self.p

    def connect(self):
        ''' Conexion con el servidor '''
        try: 
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            print("Excepcion...")

    def send(self, data):
        ''' Envia los datos al servidor '''
        try: 
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e) 