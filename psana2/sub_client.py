import sys
import zmq
import time


def sub_connect(ipaddr, port):
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from weather server...")
    socket.connect ("tcp://%s:%s" % (ipaddr, port))

    # Subscribe to zipcode, default is NYC, 10001
    topicfilter = "10001"
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    return socket

def sub_recv(socket):
    # Wait
    wait_sec = 20
    print(f'waiting for {wait_sec}s...')
    time.sleep(wait_sec)

    st = time.time()
    string = socket.recv_string()
    en = time.time()
    topic, messagedata = string.split()
    print(topic, messagedata, f'recv took:{en-st:.2f}s.')

      
if __name__ == "__main__":
    ipaddr = "localhost"
    port = "5556"
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    socket = sub_connect(ipaddr, port)
    sub_recv(socket)

