import socket
from datetime import datetime

import cv2
import imutils
import base64
import threading


class Streamer:
    def __init__(self):
        self.streamerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddr = ("15.152.30.6", 9991)
        # self.serverAddr = ("127.0.0.1", 9991)
        self.video = cv2.VideoCapture(0)

    def connectToServer(self):
        try:
            self.streamerSocket.connect(self.serverAddr)
            print("Connected to:", self.serverAddr)
            return True
        except Exception as e:
            print("Server reject connection")
            return False

    def sendToServer(self):
        print("Sending video...")
        i = 0
        try:
            now = datetime.now()
            while (self.video.isOpened()):
                if i == 3:
                    break
                i += 1
                delta = (datetime.now() - now).total_seconds()
                delta = format(delta, ".3f")

                img, frame = self.video.read()
                frame = imutils.resize(frame, width=600)
                frame = cv2.putText(frame, delta, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                message = base64.b64encode(buffer) + b"*"
                self.streamerSocket.sendall(message)
                print(len(message))
                # cv2.imshow("Streamer", frame)
                #
                # key = cv2.waitKey(1) & 0xFF
                # if key == ord("q"):
                #     self.streamerSocket.close()
                #     break
        except NameError:
            pass


streamer = Streamer()
if streamer.connectToServer():
    input("Press Enter To Start Streaming:")
    threads = [
        threading.Thread(target=streamer.sendToServer),
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
