import socket
import select
import sys


client_recv=[0]
i=0
l=0
noempty_parts=[]

class Socket_Teleop:
	def __init__(self): #객체가 생성될 때 자동으로 생성됨
		global sc

		HOST = ''					#서버의 주소=어떠한 주소에서든 접속을 허용함
		PORT = 50007 				#서버가 사용하는 포트 번호

		sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sc.bind((HOST, PORT)) 
		sc.listen() 

		print("server is starting")

		self.client_number=input("HOW MANY CLIENT? ")

		self.client_info = {}		#client의 mac 주소를 저장할 딕셔너리
		self.readsocks = [sc]		#읽기 가능한 소켓 리스트에 서버 소켓 추가
		self.readsocks = [sock for sock in self.readsocks if sock.fileno() >=0]
		self.readables,_,_ = select.select(self.readsocks,[],[])




	def register(self): #클라이언트를 등록하는 메서드->새 클라이언트의 연결을 처리
		for sock in self.readables:
			if sock == sc: 
				#새로운 클라이언트 소켓을 반환함
				newsock, addr = sc.accept() 
				self.readsocks.append(newsock)

				#addr: client의 주소를 나타내는 튜플
				#sock: 소켓 객체
				self.client_info[addr]={'sock': newsock,'mac': None, 'station': None}
				print(f"new connection from {addr}\n")

	def receive(self): #클라이언트로부터 데이터를 수신함
		for sock in self.readables:
			if sock != sc:
				return sock.recv(1024).decode()



if __name__ == '__main__': #python 파일이 직접 실행될 때만 내부의 코드가 실행됨

	server_sc = Socket_Teleop() #클래스의 인스턴스를 생성
	client_101=[0]#101 받은 갯수 세는 배열

	while 1:
		data = server_sc.receive()	
		if data:
			if ',' in data:
				#데이터가 mac이랑 client_infostation인 경우
				client_mac, client_station = data.split(",")
				server_sc.client_info[addr].update({'mac': client_mac, 'station': int(client_station)})
				client_mac=""
				client_recv=0
		else:
			print("no received data\n")
			break
		if len(server_sc.client_info)==server_sc.client_number:
			for addr, info in server_sc.client_info.items():
				print("address: {addr}, mac: {info['mac']}, station: {info['station']}\n")
			sorted_info=sorted(server_sc.client_info.items(), ey=lambda x: x[1]['station'])

			for addr, info in sorted_info.items():
				print("sorted infomation address: {addr}, mac: {info['mac']}, station: {info['station']}\n")	

			for addr, info in sorted_info:
				k=info['sock']
				try:
					k.sendall("100".encode())
					print(f"{l}th send command 100 to {addr}")
					l=l+1
					data101=server_sc.receive()
					q=0
					client_101.insert(q,data101)
					q=q+1
					data101=0

				except socket.error as e:
					print(f"error {e}")
			
			if len(client_101)==server_sc.client_number:
				print(f"confirmation received from 101: tbs are landing")
			else:
				print(f"unexpected result from tbs")