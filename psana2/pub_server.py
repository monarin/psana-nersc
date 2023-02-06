import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

wait_sec = 40
print(f'waiting for {wait_sec}s...')
time.sleep(wait_sec)

topic = 10001
messagedata = random.randrange(1,215) - 80
print("%d %d" % (topic, messagedata))
socket.send_string("%d %d" % (topic, messagedata))
