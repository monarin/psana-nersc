## Collection of debug tools
### gdb with mpi
To use with mpi run
```
mpirun -n 3 xterm -e gdb python
```
This will open three X terminals with gdb prompt, for each one run the python script e.g. `run test_live.py`.  
### valgrind 
For a single process with output piped to a file and memcheck performed,
```
PYTHONMALLOC=malloc mpirun -n 3 valgrind --log-file="v.txt" --tool=memcheck --leak-check=full --suppressions=valgrind-python.supp python -X faulthandler test_live.py tmoc00221 20 /sdf/data/lcls/drpsrcf/ffb
```
Note that you need to find a good suppression file for this to work.
### ef (Electric Fence)
```
ef python test_live.py
```
To skip empty malloc checking, 
```
EF_ALLOW_MALLOC_0=1 ef python test_live.py
```
If ef runs out of memory, you'll get `protect()` error. You can increase the amount of process memory by:
```
sudo bash
cat /proc/sys/vm/max_map_count > prev_max_map_count
echo 1000000 > /proc/sys/vm/max_map_count
exit
```

