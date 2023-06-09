import socket
import pickle
import yaml

class Network:
    def __init__(self) -> None:
        with open('config.yml', 'r') as f:
            config = yaml.safe_load(f)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = config['ip']
            self.port = config['port']
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