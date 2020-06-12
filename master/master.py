
import socket, threading
import time
import struct
from GlobalConstants import GlobalConstants

counter = 0
lock = threading.Lock()


class Master(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def send_sync(self):

        self.conn.send(GlobalConstants.SYNC_CODE.encode())
        return counter

    def send_sync(self):
        self.conn.send(GlobalConstants.SYNC_CODE.encode())
        return counter

    def receive_message(self, message):
        global counter
        data = b''
        while data.decode('ascii') != message:
            data = self.conn.recv(32)
        return counter

    def send_sync_follow(self, time):
        self.conn.send(time)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((GlobalConstants.HOST, GlobalConstants.PORT))
        print("listening:")
        s.listen()
        self.conn, addr = s.accept()
        print('Connected by', addr)

        while(True):
            t1 = self.send_sync()
            print("t1", t1)
            self.receive_message(GlobalConstants.SYNC_RECEIVED)
            print("approved")
            self.conn.send(struct.pack('f', t1))
            t4 = self.receive_message(GlobalConstants.DELAY_REQ)
            print("t4: ", t4)
            self.conn.send(struct.pack('f', t4))
            self.conn.send(struct.pack('f', t4))

            print('------------')
            time.sleep(2)


class Counter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global counter
        while True:
            lock.acquire()
            if counter < GlobalConstants.MAX_COUNT:
                counter += 1
            else:
                counter = 0
            lock.release()


def main():
    c = Counter()
    c.start()
    m = Master()
    m.start()

if __name__ == "__main__":
    main()