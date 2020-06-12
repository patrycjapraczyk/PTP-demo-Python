#!/usr/bin/env python3

import socket, threading, time
import struct
from GlobalConstants import GlobalConstants

counter = 0
lock = threading.Lock()

class Slave(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def change_counter(self, val):
        global counter
        lock.acquire()
        counter += val
        lock.release()

    def receive_sync(self):
        sync = self.s.recv(32)
        t1 = None
        if sync == b'AA':
            t1 = counter
            self.s.send(GlobalConstants.SYNC_RECEIVED.encode())
        return t1

    def delay_request(self):
        self.s.send(GlobalConstants.DELAY_REQ.encode())
        return counter

    def receive_data(self):
        return self.s.recv(32)

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((GlobalConstants.HOST, GlobalConstants.PORT))

        while(True):
            t1 = None
            while not t1:
                t1 = self.receive_sync()

            print('-------------')
            print("t1: ", t1)

            # receive sync_follow
            t2 = None
            while not t2:
                t2 = struct.unpack('f', self.receive_data())[0]

            print("t2: ", t2)

            MS_difference = t2 - t1
            self.change_counter(MS_difference)
            # measure data transfer delay
            t3 = self.delay_request()
            print("t3: ", t3)
            t4 = None
            while not t4:
                t4 = struct.unpack('f', self.receive_data())[0]

            print("t4 ", t4)
            transfer_delay = (t4 - t3) / 2
            self.change_counter(transfer_delay)

            print("delay", transfer_delay)
            print("conter :", counter)


class Counter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global counter
        while True:
            lock.acquire()
            if counter < GlobalConstants.MAX_COUNT:
                counter += 1
            lock.release()


def main():
    c = Counter()
    c.start()
    m = Slave()
    m.start()


if __name__ == "__main__":
    main()