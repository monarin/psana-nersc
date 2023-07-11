## TMO Hutch Psana2/AMI Build Instruction
We build both software packages on psbuild-rhel7-01 under tmoopr user.
```
ssh psbuild-rhel7-01 -l tmoopr
cd ~/git
git clone https://github.com/slac-lcls/lcls2.git lcls2_mmddyy
cd lcls2_mmddyy
source setup_env.sh
./build_all.sh
cd ..
git clone https://github.com/slac-lcls/ami.git ami_mmddyy
cd ami_mmddyy
./build_all.sh
cd ..
```
Create a softlink under tmo's work directory (where all the .cnf files are) to point to this new build. 
```
cd /cds/group/pcds/dist/pds/tmo/scripts
ln -s /cds/home/opr/tmoopr/git/lcls2_ddmmyy/setup_env.sh setup_env.sh
```

