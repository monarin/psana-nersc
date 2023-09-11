## goal:
- keep track of run/psmon-node/psmon-port eventually in elog database
  (will need help from murali).  in the short term, make a fake "zmq"
  database and keep the info there.
- the "psplot" command would switch automatically to the most recent
  run, or to an older run if requested by the userc
- can keep psplot from different runs running at the same time.
- users kill the plots by [x] or possibly by command line (e.g. kill id)

See ~cpo/git/lcls2/andor.py.  Add code roughly like this:
```
if rank==4: # hack for now to eliminate use of publish.local below              
    publish.init()

# we will remove this for batch processing and use "psplot" instead             
# publish.local = True                                                          

# fake-server is a small standalone zmq python script                           
# fake_dbase_server='psanagpu109'                                               

def my_smalldata(data_dict):
    # if first_time:                                                            
    #    my_node = get_node_name                                                
    #    my_port = get_psmon_port_number                                        
    #    my_runno = get_runno                                                   
    #    zmq_send(fake_dbase_server, my_node, my_port, my_runno)                
```
