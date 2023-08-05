import socket
from datetime import datetime

import cv2
import imutils
import base64


class Streamer:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        self.streamerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverAddr = ("15.152.30.6", 9991)
        # self.serverAddr = ("127.0.0.1", 9991)

    def connect(self):
        self.streamerSocket.sendto(b"CONNECT_STREAMER", self.serverAddr)

    def send(self):
        now = datetime.now()
        while self.video.isOpened():
            delta = (datetime.now() - now).total_seconds()
            delta = format(delta, ".3f")

            img, frame = self.video.read()
            frame = cv2.putText(frame, delta, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            frame = imutils.resize(frame, width=600)
            encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            message = base64.b64encode(buffer)
            self.streamerSocket.sendto(message, self.serverAddr)

            cv2.imshow("Streamer", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                self.streamerSocket.close()
                break


streamer = Streamer()
streamer.connect()
streamer.send()
