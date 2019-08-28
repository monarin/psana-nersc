import subprocess
import shutil

def setup_input_files(tmp_path):
    xtc_dir = tmp_path / '.tmp' 
    xtc_dir.mkdir()
    smd_dir = xtc_dir / 'smalldata'
    smd_dir.mkdir()
    
    n_files = 16
    for i in range(n_files):
        # segments 0,1 and "counting" timestamps for event-building
        filename = 'data-r0001-s%s.xtc2'%(str(i).zfill(2))
        smd_filename = 'data-r0001-s%s.smd.xtc2'%(str(i).zfill(2))
        s01file = str(xtc_dir / filename)
        subprocess.call(['xtcwriter','-f',s01file,'-t','-n','100000','-s',str(i*2),'-e','1000000','-m','100']) # ask for 10 events with every 4 events, one SlowUpdate inserted.
        subprocess.call(['smdwriter','-f',s01file,'-o',str(smd_dir / smd_filename)])


if __name__ == "__main__":
    import pathlib
    setup_input_files(pathlib.Path('.'))
