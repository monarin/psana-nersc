import zmq
import random
import sys
import time
import zlib, pickle

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
    wait_sec = 5
    print(f'waiting for {wait_sec}s...')
    time.sleep(wait_sec)
    calib_const = wu.calib_constants_all_types(det_uniqueid, exp=expt, run=runnum, dbsuffix=dbsuffix)
    send_zipped_pickle(socket, calib_const)
    print(f"sent {calib_const['pedestals'][0][0,1]=}")

def send_zipped_pickle(zmq_socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    p = pickle.dumps(obj, protocol)
    z = zlib.compress(p)
    return zmq_socket.send(z, flags=flags)

if __name__ == "__main__":
    port = "5556"
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    socket = pub_bind(port)
    pub_send(socket)
