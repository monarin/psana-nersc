## CNF -l (lane) flag (DAQ Control)
devGui and DAQ Control both count from 0. 
There are 8 lanes (4 per PGP/ 2 PGPs per node) connected to a node. We connect an instrument to one of this lanes.  
0 1 2 3 4 5 6 7

The lane number is represented by a bitmask. For example,  
LANE#0 is 00000001 = 1<<0 = 2^0 = 1  
LANE#1 is 00000010 = 1<<1 = 2^1 = 2  
LANE#2 is 00000100 = 1<<2 = 2^2 = 4
and  
LANE#5 is 00100000 = 1<<5 = 2^5 = 32

The option flag -l in cnf files takes a hexadecimal value wo we need to convert base 10 of the bitmask representation to hex.  
1 --hex(1)-> 0x1  
2 --hex(2)-> 0x2  
4 --hex(4)-> 0x4  
and  
32 --hex(32)-> 0x20  


