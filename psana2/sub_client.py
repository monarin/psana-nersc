import sys
import zmq
import time

port = "5556"
if len(sys.argv) > 1:
    port = int(sys.argv[1])
    
if len(sys.argv) > 2:
    port1 = int(sys.argv[2])

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect ("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

# Subscribe to zipcode, default is NYC, 10001
topicfilter = "10001"
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

# Wait
wait_sec = 10
print(f'waiting for {wait_sec}s...')
time.sleep(wait_sec)

st = time.time()
string = socket.recv_string()
en = time.time()
topic, messagedata = string.split()
print(topic, messagedata, f'recv took:{en-st:.2f}s.')

      

