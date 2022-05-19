# echosender.py

from socket import *
import struct
import time

def recv_all(sock,size):
    '''
    Receive an exact amount of data on a socket
    '''
    chunks = []
    while size > 0:
        chunk = sock.recv(size)
        if not chunk:
            raise IOError("Incomplete message")
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)

def send_test(addr, nmessages, msgsize):
    '''
    Blast a stream of size-prefixed messages at someone.
    '''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(addr)
    sock.setsockopt(SOL_TCP, TCP_NODELAY, 1)
    msg = struct.pack("!I", msgsize) + b'x'*msgsize
    start = time.time()
    nmsg = nmessages
    while nmessages > 0:
        sock.send(msg)
        resp = recv_all(sock,len(msg))
#        assert resp == msg
        nmessages -=1
        time.sleep(0.001)
    sock.send(struct.pack("!I",0))
    sock.close()
    end = time.time()
    print("%d messages sent in %f seconds" % (nmsg, end-start))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: %s nmessages msgsize" % sys.argv[0])
        raise SystemExit(1)
    send_test(("localhost",15000),int(sys.argv[1]),int(sys.argv[2]))


        

    
