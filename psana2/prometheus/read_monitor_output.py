import sys

filename = sys.argv[1]
batch_size = int(sys.argv[2])
query_start = int(sys.argv[3])
t = ""
with open(filename, 'r') as f:
    for line in f:
        #if line.find('CHECKPOINT TIMESTAMP') == 0:
            #print(t)
        if line.find('SMD0') == 0:
            _ = next(f) # DISK READING
            next_line = next(f) 
            smd0_read_mbs = float(next_line.split()[3])
            #print(smd0_read_mbs)
            _ = next(f) # SEND RATE
            next_line = next(f)
            smd0_send_mbs = float(next_line.split()[1])
            #print(smd0_send_mbs)
            _ = next(f) # batches
            next_line = next(f)
            smd0_send_khz = float(next_line.split()[1])/1000
            #print(smd0_send_khz)
            _ = next(f) # MPI WAITING TIME
            next_line = next(f)
            smd0_wait_sec = float(next_line.split()[2])
            #print(smd0_wait_sec)
        
        elif line.find('EVENTBUILDER(S)') == 0:
            _ = next(f) # SEND RATE
            next_line = next(f)
            eb_send_mbs = float(next_line.split()[1])
            #print(eb_send_mbs)
            _ = next(f) # batches/s
            next_line = next(f)
            eb_send_khz = float(next_line.split()[1])/1000
            #print(eb_send_khz)
        elif line.find('TIME (s) WAITING FOR SMD0') == 0:
            next_line = next(f)
            eb_wait_smd0_sec = float(next_line.split()[2])
            #print(eb_wait_smd0_sec)
        elif line.find('TIME (s) WAITING FOR BIGDATA CORES') == 0:
            next_line = next(f)
            eb_wait_bd_sec = float(next_line.split()[2])
            #print(eb_wait_bd_sec)
        elif line.find('BIGDATA') == 0:
            _ = next(f) # DISK READING
            next_line = next(f)
            bd_read_mbs = float(next_line.split()[3])
            #print(bd_read_mbs)
            next_line = next(f)
            bd_read_avg_s = float(next_line.split()[1])
            _ = next(f) # PROCESSING RATE
            next_line = next(f) 
            bd_process_khz = float(next_line.split()[1])/1000
            #print(bd_process_khz)
            next_line = next(f)
            bd_gen_smd_batch = float(next_line.split()[1])
            #print(bd_gen_smd_batch)
            next_line = next(f)
            bd_gen_evt = float(next_line.split()[1])
            #print(bd_gen_evt)
        elif line.find('TIME (s) BD WAITING FOR EVENTBUILDER') == 0:
            next_line = next(f)
            bd_mpi_sec = float(next_line.split()[2])
            #print(bd_mpi_sec)

print(query_start, smd0_read_mbs, smd0_send_mbs, smd0_send_khz, smd0_wait_sec, eb_send_mbs, eb_send_khz, eb_wait_smd0_sec, eb_wait_bd_sec, bd_read_mbs, bd_process_khz, bd_read_avg_s, bd_gen_smd_batch, batch_size*bd_gen_evt, bd_mpi_sec)