Build docker image  
docker build -t monarin/psana2:latest .  
  
Deploy to shifter at NERSC  
* OBSOLUTE * (solved) 
2019-11-20 shifterimg -v pull command is broken. Mona got
this temp. script for deploying at NERSC.  
/usr/common/das/shifter/pull monarin/psana2:test
***


