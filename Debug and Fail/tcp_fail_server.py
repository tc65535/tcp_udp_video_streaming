import socket
import threading


class Server:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverAddr = ("172.31.36.242", 9991)
        # self.serverAddr = ("127.0.0.1", 9991)
        self.users = {}

    def startServer(self):
        try:
            self.serverSocket.bind(self.serverAddr)
            self.serverSocket.listen(5)
            print("Server Started:", self.serverAddr)
            return True
        except Exception as e:
            print("Server fail to start")
            return False

    def acceptConnection(self):
        print("Waiting for connection...")
        while True:
            try:
                clientSocket, addr = self.serverSocket.accept()
                self.users[addr] = clientSocket
                print("User Connected, Total:{}".format(len(self.users)), list(self.users.keys()))
            except:
                pass

    def receiveVideo(self):
        print("Receiving Video Stream...")
        while True:
            try:
                users = self.users.copy()
                if len(users) >= 1:
                    streamer = list(users.keys())[0]
                    streamerConn = users[streamer]
                    msg = streamerConn.recv(655350)
                    self.broadcast(users, msg)
            except Exception as e:
                pass

    def broadcast(self, users, message):
        keys = list(users.keys())[1:]
        for key in keys:
            singleConn = self.users.copy()[key]
            try:
                singleConn.sendall(message)
            except Exception as e:
                del self.users[key]
                singleConn.close()
                print("Disconnect:", key)


server = Server()
if server.startServer():
    threads = [
        threading.Thread(target=server.acceptConnection),
        threading.Thread(target=server.receiveVideo),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
