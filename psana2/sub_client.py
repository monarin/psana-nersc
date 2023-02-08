import sys
import zmq
import time
import zlib, pickle


def sub_connect(ipaddr, port):
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from weather server...")
    socket.connect ("tcp://%s:%s" % (ipaddr, port))

    # Subscribe to all
    topicfilter = ""
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    return socket

def sub_recv(socket):
    # Wait
    wait_sec = 10
    print(f'waiting for {wait_sec}s...')
    time.sleep(wait_sec)

    st = time.time()
    calib_const = recv_zipped_pickle(socket)
    en = time.time()
    assert calib_const['pedestals'][0][0,1] == 12
    print(f"{calib_const['pedestals'][0][0,1]=} recv took:{en-st:.2f}s.")

def recv_zipped_pickle(zmq_socket, flags=0, protocol=-1):
    """inverse of send_zipped_pickle"""
    z = zmq_socket.recv(flags)
    p = zlib.decompress(z)
    return pickle.loads(p)
      
if __name__ == "__main__":
    ipaddr = "localhost"
    port = "5556"
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    socket = sub_connect(ipaddr, port)
    sub_recv(socket)

