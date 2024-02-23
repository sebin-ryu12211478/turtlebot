import socket
import getmac 

station=3210 #숫자가 작을수록 먼 역
message=""


class Socket_Teleop:
	def __init__(self):
		HOST = '192.168.0.21'
		PORT = 50007

		self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sc.connect((HOST, PORT))

	def close_connection(self):
		self.sc.close()

if __name__ == '__main__': #__main__ 스크립트가 실행될 때만 아래 코드가 실행

	client_sc = Socket_Teleop()
	MAC = getmac.get_mac_address()
	print(MAC)

	data=f"{MAC},{station}"
	client_sc.sc.sendall(str(data).encode())

	while 1:
		ans =client_sc.sc.recv(1024).decode().strip()

		if ans == "100":
			print("[{}] {} received".format(MAC, ans))

			# 승차 완료
			input("INPUT ANY KEY")

			client_sc.sc.sendall(format(101).encode())

		if ans == "102":
			print("[{}] {} received".format(MAC, ans))

			# 하차 완료
			input("INPUT ANY KEY")

			client_sc.sc.sendall(format(103).encode())

			client_sc.close_connection()
			break

