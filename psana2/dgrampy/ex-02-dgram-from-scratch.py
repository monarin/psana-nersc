from psana.dgrampy import DgramPy, AlgDef, DetectorDef
from psana.psexp import TransitionId
import numpy as np

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
    selected_timestamps = [40, 70, 130, 160]


    # Open output file for writing
    ofname = 'out.xtc2'
    xtc2file = open(ofname, "wb")

    
    # Create config, algorithm, and detector
    current_timestamp = 0
    ts_step = 10            # incrementing by this value  
    config = DgramPy(transition_id=TransitionId.Configure, ts=current_timestamp)
    current_timestamp += ts_step
    
    alg = AlgDef("raw", 0, 0, 2)
    det = DetectorDef(det_name, det_type, det_id)

    runinfo_alg = AlgDef("runinfo", 0, 0, 1)
    runinfo_det = DetectorDef("runinfo", "runinfo", "")
    
    scan_alg = AlgDef("raw", 0, 0 ,2)
    scan_det = DetectorDef("scan", "scan", "detnum1234") 


    # Define data formats
    datadef = {
        "calib": (np.float32, 2),
    }

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
    config.save(xtc2file)

    beginrun = DgramPy(transition_id=TransitionId.BeginRun, config=config, ts=current_timestamp)
    if segment == 0:
        runinfo.runinfo.expt = "xpptut15"
        runinfo.runinfo.runnum = 1
        beginrun.adddata(runinfo.runinfo)
    beginrun.save(xtc2file)
    current_timestamp += ts_step

    n_steps = 2
    n_evt_per_step = 5
    for i in range(n_steps):
        beginstep = DgramPy(transition_id=TransitionId.BeginStep, config=config, ts=current_timestamp)
        if segment == 0:
            scan.raw.motor1 = 42.0
            scan.raw.motor2 = 4200.0
            beginstep.adddata(scan.raw)
        beginstep.save(xtc2file)
        current_timestamp += ts_step
        
        enable = DgramPy(transition_id=TransitionId.Enable, config=config, ts=current_timestamp)
        enable.save(xtc2file)
        current_timestamp += ts_step


        # Start saving L1Accept
        for j in range(n_evt_per_step):
            if current_timestamp in selected_timestamps or not selected_timestamps:
                d0 = DgramPy(transition_id=TransitionId.L1Accept, config=config, ts=current_timestamp)
                det.raw.calib = np.ones([2,2], dtype=np.float32) * (i*n_evt_per_step + j)
                d0.adddata(det.raw)
                d0.save(xtc2file)
            current_timestamp += ts_step

        disable = DgramPy(transition_id=TransitionId.Disable, config=config, ts=current_timestamp)
        disable.save(xtc2file)
        current_timestamp += ts_step
        endstep = DgramPy(transition_id=TransitionId.EndStep, config=config, ts=current_timestamp)
        endstep.save(xtc2file)
        current_timestamp += ts_step
    
    endrun = DgramPy(transition_id=TransitionId.EndRun, config=config, ts=current_timestamp)
    endrun.save(xtc2file)
    current_timestamp += ts_step

    xtc2file.close()
