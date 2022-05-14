from dgrampy import DgramPy, AlgDef, DetectorDef
from psana.psexp import TransitionId
import numpy as np

if __name__ == "__main__":
    # NameId setup
    nodeId = 1 
    namesId = {
        "hsd": 0,
        "runinfo": 1,
        "andor": 2,
        "epix": 3
    }
    det_name = "epix"
    det_type = "epix"
    det_id = 'detnum1234'
    segment = 2
    selected_timestamps = [10,20]


    # Open output file for writing
    ofname = 'out.xtc2'
    xtc2file = open(ofname, "wb")

    
    # Create config, algorithm, and detector
    current_timestamp = 0
    config = DgramPy(transition_id=TransitionId.Configure, ts=current_timestamp)
    current_timestamp += 1
    
    alg = AlgDef("raw", 0, 0, 2)
    det = DetectorDef(det_name, det_type, det_id)

    runinfo_alg = AlgDef("runinfo", 0, 0, 1)
    runinfo_det = DetectorDef("runinfo", "runinfo", "")


    # Define data formats
    datadef = {
        "calib": (np.float32, 2),
    }

    runinfodef = {
        "expt": (str, 1),
        "runnum": (np.uint32, 0),
    }

    # Create detetors
    det = config.Detector(det, alg, datadef, nodeId=nodeId, namesId=namesId[det_name], segment=segment)
    runinfo = config.Detector(runinfo_det, 
                              runinfo_alg, 
                              runinfodef, 
                              nodeId=nodeId, 
                              namesId=namesId["runinfo"]
                             )
    config.save(xtc2file)

    beginrun = DgramPy(transition_id=TransitionId.BeginRun, config=config, ts=current_timestamp)
    runinfo.runinfo.expt = "xpptut15"
    runinfo.runinfo.runnum = 1
    beginrun.adddata(runinfo.runinfo)
    beginrun.save(xtc2file)
    current_timestamp += 1

    beginstep = DgramPy(transition_id=TransitionId.BeginStep, config=config, ts=current_timestamp)
    beginstep.save(xtc2file)
    current_timestamp += 1
    
    enable = DgramPy(transition_id=TransitionId.Enable, config=config, ts=current_timestamp)
    enable.save(xtc2file)
    current_timestamp += 1


    # Start saving L1Accept
    for i in range(17):
        if current_timestamp in selected_timestamps or not selected_timestamps:
            d0 = DgramPy(transition_id=TransitionId.L1Accept, config=config, ts=current_timestamp)
            det.raw.calib = np.ones([2,2], dtype=np.float32) * i
            d0.adddata(det.raw)
            d0.save(xtc2file)
        current_timestamp += 1

    disable = DgramPy(transition_id=TransitionId.Disable, config=config, ts=current_timestamp)
    disable.save(xtc2file)
    current_timestamp += 1
    endstep = DgramPy(transition_id=TransitionId.EndStep, config=config, ts=current_timestamp)
    endstep.save(xtc2file)
    current_timestamp += 1
    endrun = DgramPy(transition_id=TransitionId.EndRun, config=config, ts=current_timestamp)
    endrun.save(xtc2file)
    current_timestamp += 1

    xtc2file.close()
