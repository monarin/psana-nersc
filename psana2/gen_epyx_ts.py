n = 100000
with open('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/out', 'r') as f:
    for row in f:
        if n == 100000:
            cols = row.split()
            ts = cols[3].split('.')
            nsecs = float('0.'+ts[1].split(',')[0])
            print(ts[0], int(nsecs * 1e9))
            n = 0
        n += 1




