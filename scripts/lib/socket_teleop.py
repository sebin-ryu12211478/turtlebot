import socket
import getmac

message=""


class Socket_Teleop:
    def __init__(self):
        global sc
        global MAC

        MAC = getmac.get_mac_address()
        HOST = '192.168.0.22'
        PORT = 50007
        self.station = "3011"

        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((HOST, PORT))

        sc.sendall(f"{MAC},{self.station}".encode())

    def send_all(self, msg):
        sc.sendall("{},{}".format(MAC,msg).encode())

    def close(self):
        sc.close()

    def receive(self):
            while 1:
                print("waiting...")
                ans = sc.recv(1024).decode().strip()

                if int(ans) == 100:
                    print("received 100")
                    return 1

                if int(ans) == 101:
                    print("received 101")
                    return 2
                

    def debug_mode(self):
        print("DEBUG")

        self.receive()
        input("INPUT ANY KEY")
        self.send_all(98)

        self.receive()
        input("INPUT ANY KEY")
        self.send_all(99)
