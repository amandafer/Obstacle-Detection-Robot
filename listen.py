import socket
import sys
import time

def main():
        if (len(sys.argv) != 3):
                print  'Usage: listen.py <ip> <port>'
                return

        UDP_IP = sys.argv[1]
        UDP_PORT = int(sys.argv[2])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        sock.settimeout(0.01)

        while True:
                try:
			time.sleep(3)
                        msg, addr = sock.recvfrom(100)

                        print 'Received message:', msg

                        if (msg == 'quit'):
                                break

                except socket.timeout:
                        print 'timed out'


if __name__ == "__main__":
        main()
