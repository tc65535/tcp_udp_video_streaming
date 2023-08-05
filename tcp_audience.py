import socket
import cv2
import numpy as np
import base64
import threading
import os


class Audience:
    def __init__(self):
        self.audienceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddr = ("15.152.30.6", 9991)
        # self.serverAddr = ("127.0.0.1", 9991)
        self.buffer = b""

    def connectToServer(self):
        try:
            self.audienceSocket.connect(self.serverAddr)
            print("Connected to:", self.serverAddr)
            return True
        except Exception as e:
            print("Server reject connection")
            return False

    def receiveFromServer(self):
        print("Receiving Video...")
        while True:
            try:
                data = self.audienceSocket.recv(1400)
                self.buffer += data
                if len(self.buffer) > 655350:
                    bIndex = self.buffer.find(b"*")
                    if bIndex > -1:
                        tmpData = self.buffer[:bIndex]
                        self.buffer = self.buffer[bIndex + 1:]

                        decodeData = tmpData.decode()
                        data = base64.b64decode(decodeData, " /")
                        data = np.frombuffer(data, dtype=np.uint8)
                        frame = cv2.imdecode(data, 1)
                        cv2.imshow(os.path.basename(__file__), frame)
                        cv2.waitKey(1)
            except Exception as e:
                continue


client = Audience()
if client.connectToServer():
    threads = [
        threading.Thread(target=client.receiveFromServer),
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
