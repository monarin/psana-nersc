import zmq
import random
import sys
import time

# Request util for contacting the db
import psana.pscalib.calib.MDBWebUtils as wu

# Parameters required in the request
expt = 'xpptut15'
det_uniqueid = 'cspad_detnum1234'
runnum = 1
dbsuffix = ''

def pub_bind(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    return socket

def pub_send(socket):
    wait_sec = 10
    print(f'waiting for {wait_sec}s...')
    time.sleep(wait_sec)

    topic = 10001
    messagedata = random.randrange(1,215) - 80
    print("%d %d" % (topic, messagedata))
    socket.send_string("%d %d" % (topic, messagedata))

if __name__ == "__main__":
    port = "5556"
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    socket = pub_bind(port)
    pub_send(socket)
