## CNF -l (lane) flag
There are 8 lanes (4 per PGP/ 2 PGPs per node) connected to a node. We connect an instrument to one of this lanes.  
1 2 3 4 5 6 7 8

The lane number is represented by a bitmask. For example,  
LANE#1 is 00000001 = 2^0 = 1  
LANE#2 is 00000010 = 2^1 = 2  
and  
LANE#5 is 00010000 = 2^4 = 16  

The option flag -l in cnf files takes a hexadecimal value wo we need to convert base 10 of the bitmask representation to hex.  
1 --hex(1)-> 0x1  
2 --hex(2)-> 0x2  
and  
16 --hex(16)-> 0x10  


