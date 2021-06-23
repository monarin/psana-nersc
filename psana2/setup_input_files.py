import subprocess
import shutil

def setup_input_files(tmp_path):
    xtc_dir = tmp_path / 'xtcdata' 
    xtc_dir.mkdir()
    smd_dir = xtc_dir / 'smalldata'
    smd_dir.mkdir()
    
    n_files = 60
    for i in range(n_files):
        # segments 0,1 and "counting" timestamps for event-building
        filename = 'data-r0001-s%s.xtc2'%(str(i).zfill(2))
        smd_filename = 'data-r0001-s%s.smd.xtc2'%(str(i).zfill(2))
        s01file = str(xtc_dir / filename)
        
        # ask for 100 steps (-m) with 100k events per step (-n) with every 1M events, one SlowUpdate inserted (-e).
        subprocess.call(['xtcwriter','-f',s01file,'-t','-n','100000','-s',str(i*2),'-e','1000000','-m','100','-i', str(i)]) 
        #subprocess.call(['xtcwriter','-f',s01file,'-t','-n','10','-s',str(i*2),'-i', str(i)]) 
        
        subprocess.call(['smdwriter','-f',s01file,'-o',str(smd_dir / smd_filename)])


if __name__ == "__main__":
    import pathlib
    setup_input_files(pathlib.Path('.'))
