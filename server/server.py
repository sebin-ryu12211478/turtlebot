import socket
import select
import sys
import pandas as pd

STRING_DIVIDER = "\n\n" + "=" * 50 + "\n\n"

class SocketTeleop:
    def __init__(self):  # 객체가 생성될 때 자동으로 생성됨
        HOST = ''  # 서버의 주소=어떠한 주소에서든 접속을 허용함
        PORT = 50007  # 서버가 사용하는 포트 번호

        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sc.bind((HOST, PORT))
        self.sc.listen()
        self.client_sockets = []

        self.CLIENT_NUM = 2
        self.df = pd.DataFrame(
            columns = ["SOCK","MAC", "ARR. STATION"]
        )

        print("server is starting")

    def update_information(self, sock, client_mac, client_sation):
        self.df.loc[self.df["SOCK"] == sock, ["MAC", "ARR. STATION"]] = [client_mac,int(client_sation)]


    def order_cmd(self, cmd):
        for tb, addr in self.df[["SOCK", "MAC"]].values:
            try:
                tb.sendall(cmd.encode())
                print("[{}] send command {}.".format(addr, cmd))

                data = str(tb.recv(1024).decode())

                print("[{}] received command {}.".format(addr, data))


            except socket.error as e:
                print(f"error {e}")



if __name__ == '__main__':  # python 파일이 직접 실행될 때만 내부의 코드가 실행됨

    server_sc = SocketTeleop()  # 클래스의 인스턴스를 생성
    readsocks = [server_sc.sc]  # 읽기 가능한 소켓 리스트에 서버 소켓 추가

    while 1:
        valid_socks = [sock for sock in readsocks if sock.fileno() >= 0]

        if not valid_socks:
            print("not valid sockets. program exit")
            sys.exit(1)

        readables, _, _ = select.select(readsocks, [], [])

        for sock in readables:
            if sock == server_sc.sc:
                newsock, addr = server_sc.sc.accept()
                readsocks.append(newsock)
                server_sc.client_sockets.append(newsock)

                server_sc.df.loc[len(server_sc.df)] = [newsock, None, 0]
                print(f"new connection from {addr}")

            else:
                data = sock.recv(1024).decode()
                print(data)

                if ',' in data:
                    # 데이터가 mac이랑 station인 경우
                    client_mac, client_station = data.split(",")

                    server_sc.update_information(sock, client_mac, client_station)

                    client_mac = ""

                else:
                    print(f"no received data {data}")
                    server_sc.client_sockets.remove(sock)
                    sock.close()

                # 모든 기기가 접속을 하면
                if len(server_sc.df) == server_sc.CLIENT_NUM:
                    print(STRING_DIVIDER)

                    # 역 번호에 따라 정렬
                    server_sc.df = server_sc.df.sort_values("ARR. STATION", ascending=False)
                    print(server_sc.df[["MAC", "ARR. STATION"]], end=STRING_DIVIDER)
                    server_sc.order_cmd("100")

                    # 하차 상황에서는 역 정렬
                    server_sc.df = server_sc.df.sort_values("ARR. STATION", ascending=True)
                    server_sc.order_cmd("102")

                    print(f"confirmation received from 101: tbs are landing")

                    for client_socket in server_sc.client_sockets:
                        try:
                            client_socket.sendall(str(333).encode())
                            client_socket.close()

                        except socket.error as e:
                            print(f"error send 333 to client: {e}")

                    server_sc.client_sockets.clear()
                    server_sc.sc.close()
                    readsocks.remove(sock)
                    sys.exit(1)
