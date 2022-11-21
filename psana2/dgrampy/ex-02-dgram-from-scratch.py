from psana.dgramedit import DgramEdit, AlgDef, DetectorDef
from psana.psexp import TransitionId
import numpy as np

def save_dgramedit(dg_edit, outbuf, outfile):
    """ Save dgram edit to output buffer and write to file"""
    dg_edit.save(outbuf)
    outfile.write(outbuf[:dg_edit.size])

if __name__ == "__main__":
    # NameId setup
    nodeId = 1 
    namesId = {
        "hsd": 0,
        "runinfo": 1,
        "scan": 2,
        "andor": 3,
        "epix": 4
    }
    det_name = "andor"
    det_type = "andor"
    det_id = 'detnum1234'
    segment = 1
    selected_timestamps = []

    # Creates buffer for writing
    obuf = bytearray(64000000)

    # Open output file for writing
    ofname = 'out.xtc2'
    xtc2file = open(ofname, "wb")

    
    # Create config, algorithm, and detector
    current_timestamp = 0
    ts_step = 10            # incrementing by this value  
    config = DgramEdit(transition_id=TransitionId.Configure, ts=current_timestamp)
    current_timestamp += ts_step
    
    alg = AlgDef("raw", 0, 0, 2)
    det = DetectorDef(det_name, det_type, det_id)

    # Required to be in this format exactly
    runinfo_alg = AlgDef("runinfo", 0, 0, 1)
    runinfo_det = DetectorDef("runinfo", "runinfo", "")
    
    scan_alg = AlgDef("raw", 0, 0 ,2)
    scan_det = DetectorDef("scan", "scan", "detnum1234") 


    # Define data formats
    datadef = {
        "calib": (np.float32, 2),
    }

    # Required to be in this format exactly
    runinfodef = {
        "expt": (str, 1),
        "runnum": (np.uint32, 0),
    }

    scandef = {
        "motor1": (np.float64, 0),
        "motor2": (np.float64, 0),
    }



    # Create detetors
    det = config.Detector(det, alg, datadef, nodeId=nodeId, namesId=namesId[det_name], segment=segment)
    runinfo = config.Detector(runinfo_det, 
                              runinfo_alg, 
                              runinfodef, 
                              nodeId=nodeId, 
                              namesId=namesId["runinfo"],
                              segment=segment,
                             )
    scan = config.Detector(scan_det, scan_alg, scandef, nodeId=nodeId, namesId=namesId["scan"], segment=segment)
    save_dgramedit(config, obuf, xtc2file)

    # Start writing out required transitions
    beginrun = DgramEdit(transition_id=TransitionId.BeginRun, config=config, ts=current_timestamp)
    if segment == 0:
        runinfo.runinfo.expt = "xpptut15"
        runinfo.runinfo.runnum = 1
        beginrun.adddata(runinfo.runinfo)
    save_dgramedit(beginrun, obuf, xtc2file)
    current_timestamp += ts_step

    n_steps = 2
    n_evt_per_step = 1000000
    for i in range(n_steps):
        beginstep = DgramEdit(transition_id=TransitionId.BeginStep, config=config, ts=current_timestamp)
        if segment == 0:
            scan.raw.motor1 = 42.0
            scan.raw.motor2 = 4200.0
            beginstep.adddata(scan.raw)
        save_dgramedit(beginstep, obuf, xtc2file)
        current_timestamp += ts_step
        
        enable = DgramEdit(transition_id=TransitionId.Enable, config=config, ts=current_timestamp)
        save_dgramedit(enable, obuf, xtc2file)
        current_timestamp += ts_step


        # Start saving L1Accept
        for j in range(n_evt_per_step):
            if current_timestamp in selected_timestamps or not selected_timestamps:
                d0 = DgramEdit(transition_id=TransitionId.L1Accept, config=config, ts=current_timestamp)
                det.raw.calib = np.ones([2,2], dtype=np.float32)
                d0.adddata(det.raw)
                save_dgramedit(d0, obuf, xtc2file)
            current_timestamp += ts_step

        disable = DgramEdit(transition_id=TransitionId.Disable, config=config, ts=current_timestamp)
        save_dgramedit(disable, obuf, xtc2file)
        current_timestamp += ts_step
        endstep = DgramEdit(transition_id=TransitionId.EndStep, config=config, ts=current_timestamp)
        save_dgramedit(endstep, obuf, xtc2file)
        current_timestamp += ts_step
    
    endrun = DgramEdit(transition_id=TransitionId.EndRun, config=config, ts=current_timestamp)
    save_dgramedit(endrun, obuf, xtc2file)
    current_timestamp += ts_step

    xtc2file.close()
