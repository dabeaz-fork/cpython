# receiver.py

import struct
from socket import *
import threading
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

def recv_msg(sock):
    '''
    Receive a size-prefixed message.
    '''
    size = recv_all(sock,4)
    msglen, = struct.unpack("!I",size)
    return recv_all(sock,msglen)

def recv_benchmark(addr):
    '''
    Timing benchmark.
    '''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
    sock.bind(addr)
    sock.listen(1)
    client, addr = sock.accept()
    client.setsockopt(SOL_TCP, TCP_NODELAY, 1)
    num_messages = 0
    num_bytes = 0
    start = time.time()
    while True:
        try:
            msg = recv_msg(client)
            if not len(msg):
                break
            num_messages += 1
            num_bytes += len(msg)
            client.sendall(struct.pack("!I",len(msg)))
            client.sendall(msg)
        except IOError:
            break
    end = time.time()
    print("%d messages received in %0.4f seconds (%f bytes/sec)" % 
          (num_messages, end-start, num_bytes/(end-start)))
    client.close()
    sock.close()

def spinner():
    '''
    Spin endlessly
    '''
    import sys
    if hasattr(sys, 'setholiness'):
        sys.setholiness(True)
    print("Spinning")
    n = 0
    while True:
        n += 1
        
if __name__ == '__main__':
    import sys
    import threading
    if len(sys.argv) == 2:
        nthread = int(sys.argv[1])
    else:
        nthread = 0

    while nthread > 0:
        t = threading.Thread(target=spinner, daemon=True)
        t.start()
        nthread -=1
        
    while True:
        recv_benchmark(("",15000))

            
            
    

        
