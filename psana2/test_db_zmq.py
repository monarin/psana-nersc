# Test sending calibration constant using zmq
# Usage: python test_db_zmq.py server_flag
# where server_flag=1 indicates that script is the server.
# Usecase scenario:
#   Pick a node for the server and check ip with ifconfig
#   Update the script so server_ip matches with the value from ifconfig
#   On that node run: 
#       python test_db_zmq.py 1
#   On other node run:
#       srun -N12 -n600 python test_db_zmq.py 0
#       This will ask 600 cores on 12 nodes to run as a client

import sys
import zmq
import zlib, pickle
import time
import socket

# Request util for contacting the db
import psana.pscalib.calib.MDBWebUtils as wu

# Parameters required in the request
expt = 'xpptut15'
det_uniqueid = 'cspad_detnum1234'
runnum = 1
dbsuffix = ''

# For zmq
max_clients = 600
server_ip = "172.21.152.100"
port_number = "5555"

def send_zipped_pickle(zmq_socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    p = pickle.dumps(obj, protocol)
    z = zlib.compress(p)
    return zmq_socket.send(z, flags=flags)

def recv_zipped_pickle(zmq_socket, flags=0, protocol=-1):
    """inverse of send_zipped_pickle"""
    z = zmq_socket.recv(flags)
    p = zlib.decompress(z)
    return pickle.loads(p)

if __name__ == "__main__":
    server_flag = int(sys.argv[1])

    context = zmq.Context()
    if server_flag:
        print(f"I'm the server")
        # retreive calibration constants
        calib_const = wu.calib_constants_all_types(det_uniqueid, exp=expt, run=runnum, dbsuffix=dbsuffix)
        # Initialize zmq server
        zmq_socket = context.socket(zmq.REP)
        zmq_socket.bind(f"tcp://*:{port_number}")
        # Keeps sending until no. of expected clients is reached
        n_clients = 0 
        st = time.time()
        while True:
            #  Wait for next request from client
            message = zmq_socket.recv()
            #print("Received request: %s" % message)

            #  Send reply back to client
            #zmq_socket.send(b"World")
            send_zipped_pickle(zmq_socket, calib_const)
            #print(f'client {n_clients} sent')
            n_clients += 1
            if n_clients == max_clients:
                break
        en = time.time()
        print(f'Done sent to {n_clients} clients. Elapsed Time: {en-st:.5f}s.')
    else:
        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname) 
        #print(f"I'm the client on {hostname} with ip: {IPAddr}")
        zmq_socket = context.socket(zmq.REQ)
        zmq_socket.connect(f"tcp://{server_ip}:{port_number}")
        zmq_socket.send(b"Hello")
        #message = zmq_socket.recv()
        calib_const = recv_zipped_pickle(zmq_socket)
        # pedestals array[0,1] is 12
        assert calib_const['pedestals'][0][0,1] == 12
        #print(f"I received {message}")

