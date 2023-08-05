import socket
import threading


class BroadcastServer:
    def __init__(self):
        self.audiences = []

        self.broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcastSocketAddr = ("172.31.36.242", 9991)
        # self.broadcastSocketAddr = ("127.0.0.1", 9991)

    def start(self):
        self.broadcastSocket.bind(self.broadcastSocketAddr)
        print("Broadcast Server started!")
        self.receive()

    def receive(self):
        print("Waiting for connection...")
        while True:
            try:
                data, clientAddr = self.broadcastSocket.recvfrom(65507)
                if data:
                    if data == b"CONNECT_STREAMER":
                        print("Streamer connected:", clientAddr)
                    elif data == b"CONNECT_AUDIENCE":
                        print("Audience connected:", clientAddr)
                        self.audiences.append(clientAddr)
                    else:
                        self.broadcast(data)
            except Exception as e:
                pass

    def broadcast(self, packet):
        for audience in self.audiences:
            self.broadcastSocket.sendto(packet, audience)


broadcastServer = BroadcastServer()

threads = [
    threading.Thread(target=broadcastServer.start),
]
for t in threads:
    t.start()
for t in threads:
    t.join()
