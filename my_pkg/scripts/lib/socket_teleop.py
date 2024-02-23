import socket
import getmac 

class Socket_Teleop:
    def __init__(self):
        HOST = '192.168.0.21'
        PORT = 50007

        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sc.connect((HOST, PORT))

        #숫자가 작을수록 먼 역
        self.station=3202
        self.MAC = getmac.get_mac_address()
        self.sc.sendall(str("{},{}".format(self.MAC, self.station)).encode())

    def close_connection(self):
        self.sc.close()

    def receive(self):
        return self.sc.recv(1024).decode().strip()

    def send_cmd(self, cmd):
        self.sc.sendall(format(cmd).encode())

    def debug_mode(self):
        print("DEBUG")

        self.receive()
        input("INPUT ANY KEY")
        self.send_all(101)

        self.receive()
        input("INPUT ANY KEY")
        self.send_all(103)

