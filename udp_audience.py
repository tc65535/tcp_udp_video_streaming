import socket
import cv2
import numpy as np
import base64


class Audience:
    def __init__(self):
        self.audienceSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverAddr = ("15.152.30.6", 9991)
        # self.serverAddr = ("127.0.0.1", 9991)

    def connect(self):
        self.audienceSocket.sendto(b"CONNECT_AUDIENCE", self.serverAddr)

    def receive(self):
        while True:
            data, serverAddr = self.audienceSocket.recvfrom(65507)
            data = base64.b64decode(data, ' /')
            data = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(data, 1)
            cv2.imshow("Live Streaming", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.audienceSocket.close()
                break


audience = Audience()
audience.connect()
audience.receive()
