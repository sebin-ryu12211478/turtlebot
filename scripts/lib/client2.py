import socket
import getmac 

 #숫자가 작을수록 먼 역
message=""


class Socket_Teleop:
	def __init__(self):
		global sc

		HOST = '192.168.0.246'
		PORT = 50007

		sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sc.connect((HOST, PORT))
		self.station=3208
		MAC = getmac.get_mac_address()

		sc.sendall("{},{},\0".format(MAC, self.station).encode()) #\0=널문자->메시지의 끝을 표시함

	
	def receive(self):
		ans = b""#수신된 데이터를 저장할 바이트 문자열을 초기화함
		while 1:
			chunk = sc.recv(1) #소켓으로부터 1바이트 데이터를 수신함
			print(chunk)
			if chunk == b'\0' or chunk == b'\n':
				break
			ans += chunk #수신된 데이터를 ans 변수에 추가
		return ans.decode().strip() #문자열로 디코딩하고, 앞뒤 공백을 제거한 후 반환


if __name__ == '__main__': #__main__ 스크립트가 실행될 때만 아래 코드가 실행

	client_sc = Socket_Teleop()
	while 1:
		ans = client_sc.receive()

		if ans != None:	
			print(int(ans))

			# 차량 승차 허가 플래그
			if int(ans) == 100:
				print(f"tb {MAC} received\n")

				# 승차 완료
				#input("INPUT ANY KEY")
				s.sendall(format(101).encode())
				print(f"get on success {client_sc.MAC} \n")

			# 차량 하차 허가 플래그
			#if int(ans) == 101:
			#	print(f"tb {MAC} received\n")

			# 하차 완료
				#input("INPUT ANY KEY")
				