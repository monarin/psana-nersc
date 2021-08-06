import sys, os
import matplotlib.pyplot as plt

filename = sys.argv[1]
nodetype = sys.argv[2]
unit = sys.argv[3]

if nodetype == 'smd0':
    #sum_t = {1.0: 0, 2.0: 0, 3.0: 0, 4.0:0, 3.1: 0}
    #cn = {1.0: 0, 2.0: 0, 3.0: 0, 4.0:0, 3.1: 0}
    #label = {1.0: 'SMD0GOTCHUNK', 
    #        2.0: 'SMD0GOTEB', 
    #        3.0: 'SMD0GOTREPACK', 
    #        3.1: 'SMD0GOTSTEP', 
    #        4.0:'SMD0DONEWITHEB', 
    #        }
    sum_t = {1.0: 0, 2.0: 0, 3.0: 0, 4.0:0, 2.1: 0, 2.2: 0}
    cn = {1.0: 0, 2.0: 0, 3.0: 0, 4.0:0, 2.1: 0, 2.2: 0}
    label = {1.0: 'SMD0GOTCHUNK', 
            2.0: 'SMD0GOTEB', 
            2.1: 'SMD0GOTSTEPHIST', 
            2.2: 'SMD0STEPHISTUPDATED', 
            3.0: 'SMD0GOTREPACK', 
            4.0:'SMD0DONEWITHEB', 
            }
elif nodetype == 'eb':
    sum_t = {5.0: 0, 6.0: 0, 7.0: 0}
    cn = {5.0: 0, 6.0: 0, 7.0: 0}
    label = {5.0: 'EBSENDREQTOSMD0', 
            6.0: 'EBDONESENDREQ', 
            7.0: 'EBRECVDATA'}
elif nodetype == 'smd0_chunk':
    sum_t = {1.0: 0, 2.0: 0, 3.0: 0}
    cn = {1.0: 0, 2.0: 0, 3.0: 0}
    label = {1.0: 'STARTCHUNK',
            2.0: 'DONECREATEVIEW', 
            3.0: 'DONEREAD'}

prev_ts = 0
first_ts = 0
data = []
view_task_id = 3.0
with open(filename, 'r') as f:
    for i, line in enumerate(f):
        cols = line.split()
        task_id = float(cols[-3])
        ts = float(cols[-1])
        if prev_ts == 0:
            first_ts = ts
            prev_ts = ts
            delta = 0
        else:
            delta = ts - prev_ts
            prev_ts = ts
            if task_id in sum_t:
                sum_t[task_id] += delta
                cn[task_id] += 1
            else:
                print(line)
            if task_id == view_task_id:
                if unit == 'ms':
                    data.append(delta*1e3)
                else:
                    data.append(delta)

    
    sum_all_t = 0

    print(f'TASK/ TOTAL TIME ({unit})/ #OCCUR/ TIME ({unit}) per Occ.')
    for key, val in sum_t.items():
        val_by_unit = val
        if unit == 'ms':
            val_by_unit = val * 1e3
        print(f'{label[key]} {val_by_unit:.2f} {cn[key]} ') #{val_by_unit/cn[key]:.2f}')
        sum_all_t += val
    print(f'total: {sum_all_t*1e3:.2f} {(ts-first_ts)*1e3:.2f}')

    #plt.hist(data)
    #plt.title(f'Histogram of {label[view_task_id]} #cn:{cn[view_task_id]} total:{sum_t[view_task_id]*1e3:.2f} {unit}')
    #plt.xlabel(unit)
    #plt.show()
