import sys, os
import matplotlib.pyplot as plt

filename = sys.argv[1]
nodetype = sys.argv[2]
unit = sys.argv[3]
show_plot = 0
if len(sys.argv) > 4:
    show_plot = int(sys.argv[4])

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
    sum_t = {5.0: 0, 6.0: 0, 7.0: 0, 8.0:0, 9.0:0, 10.0:0, 11.0:0, 12.0:0, 12.1:0}
    cn = {5.0: 0, 6.0: 0, 7.0: 0, 8.0:0, 9.0:0, 10.0:0, 11.0:0, 12.0:0, 12.1:0}
    label = {5.0: 'EB1SENDREQTOSMD0',
            6.0: 'EB1DONESENDREQ', 
            7.0: 'EB1RECVDATA',
            8.0: 'EB1DONEBUILDINGEVENTS',
            9.0: 'EB1REQBD',
            10.0: 'EB1GOTBD2FROMREQ',
            11.0: 'EB1SENDDATATOBD2',
            12.0: 'EB1DONESENDDATATOBD2',
            12.1: 'EB1DONEALLBATCHES'}
elif nodetype == 'smd0_chunk':
    sum_t = {1.0: 0, 2.0: 0, 3.0: 0}
    cn = {1.0: 0, 2.0: 0, 3.0: 0}
    label = {1.0: 'STARTCHUNK',
            2.0: 'DONECREATEVIEW', 
            3.0: 'DONEREAD'}
elif nodetype == 'bd_node':
    sum_t = {13.0: 0, 14.0: 0, 15.0: 0}
    cn = {13.0: 0, 14.0: 0, 15.0: 0}
    label = {13.0: 'BD2SENDREQTOEB',
            14.0: 'BD2DONESENDREQTOEB', 
            15.0: 'BD2RECVDATA'}
elif nodetype == 'bd_event':
    sum_t = {1.0:0, 2.0:0, 3.0:0, 4.0:0, 5.0:0, 6.0:0}
    cn = {1.0:0, 2.0:0, 3.0:0, 4.0:0, 5.0:0, 6.0:0}
    label = {1.0: 'GETOFFSETANDSIZE',
            2.0: 'DONEGETOFFSET',
            3.0: 'DONEFILLBUF',
            4.0:'STARTCREATEDGRAMS', 
            5.0:'DONECREATEDGRAMS',
            6.0: 'DONECREATEEVENT'}
elif nodetype == 'bd_hsd':
    sum_t = {0.0: 0, 0.1:0, 0.2:0, 0.3:0,
            1.0:0, 2.0:0, 3.0:0, 4.0:0, 5.0:0, 0.10:0, 0.11:0, 0.12:0, 
            4.1:0, 4.2:0, }
    cn = {0.0: 0, 0.1:0, 0.2:0, 0.3:0,
            1.0:0, 2.0:0, 3.0:0, 4.0:0, 5.0:0, 0.10:0, 0.11:0, 0.12:0, 
            4.1:0, 4.2:0, }
    label = {
            0.0: 'START',
            0.1: 'STARTPARSE',
            0.2: 'ENDPARSE',
            0.3: 'END',
            0.10: 'STARTPARSEEVT',
            0.11: 'DONEINITHSDSEG',
            0.12: 'DONEINITEVT',
            1.0: 'STARTSEG',
            2.0: 'STARTCHAN',
            3.0: 'DONEPYCHAN',
            4.0: 'DONEWAVEFORM',
            4.1: 'DONEPEAKINIT',
            4.2: 'DONEPEAKDICT',
            5.0:'DONEPEAKLIST', 
            }



prev_ts = 0
first_ts = 0
data = []
view_task_id = 2.0
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
                #print(task_id, delta)
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
        print(f'{label[key]} {val_by_unit:.2f} {cn[key]} {val_by_unit/cn[key]:.2f}')
        sum_all_t += val

    sum_all_by_unit = sum_all_t
    chk_all_by_unit = ts-first_ts
    if unit == 'ms':
        sum_all_by_unit *= 1e3
        chk_all_by_unit *= 1e3
    print(f'total: {sum_all_by_unit:.2f} {chk_all_by_unit:.2f}')

    if show_plot:
        plt.hist(data)
        plt.title(f'Histogram of {label[view_task_id]} #cn:{cn[view_task_id]} total:{sum_t[view_task_id]*1e3:.2f} {unit}')
        plt.xlabel(unit)
        plt.show()
