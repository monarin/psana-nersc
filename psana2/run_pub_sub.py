from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

from pub_server import pub_bind, pub_send
from sub_client import sub_connect, sub_recv
import socket

if __name__ == "__main__":
    port = "5556"
    
    # Get a list of publishers' rank and IPaddr
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 
    n_pubs = 12
    if rank < n_pubs:
        pub_dict = {rank: IPAddr} 
    else:
        pub_dict = None 
    pub_dict = comm.allgather(pub_dict)

    # Convert list of dicts into one dict
    result = {}
    for pub in pub_dict:
        if pub:
            result.update(pub)
    pub_dict = result
    
    comm.Barrier()
    st = MPI.Wtime()

    if rank in pub_dict:
        print(f'publisher: {rank} IPAddr:{IPAddr}')
        pub_socket = pub_bind(port)
        pub_send(pub_socket)
    else:
        mypub_rank = rank % n_pubs
        print(f'subscriber: {rank} IPAddr:{IPAddr} {mypub_rank=} {pub_dict[mypub_rank]=}')
        ipaddr = pub_dict[mypub_rank] 
        sub_socket = sub_connect(ipaddr, port)
        sub_recv(sub_socket)
    
    comm.Barrier()
    en = MPI.Wtime()
    if rank == 0:
        print(f'{size=} {n_pubs=} TOTAL ELAPSED: {en-st:.5f}s.')
    

