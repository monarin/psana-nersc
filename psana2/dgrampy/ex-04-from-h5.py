"""
Create new xtc2 from data from hdf5 file.
"""
from psana.dgramedit import DgramEdit, AlgDef, DetectorDef
from psana.psexp import TransitionId
import numpy as np
import h5py
from psana import DataSource


def test_output(h5data):
    """Compares known data (saved to hdf5 by the push process) with read data."""
    pixel_position_reciprocal = h5data['pixel_position_reciprocal']
    pixel_index_map = h5data['pixel_index_map']
    intensities = h5data['intensities']

    n_test_events = 3
    ds = DataSource(files='out.xtc2')
    run = next(ds.runs())
    det = run.Detector('amopnccd')
    xtc2_pixel_position_reciprocal = run.beginruns[0].scan[0].raw.pixel_position_reciprocal
    xtc2_pixel_index_map = run.beginruns[0].scan[0].raw.pixel_index_map
    data_array = np.zeros([n_test_events,1,128,128], dtype=np.float32)

    for i,evt in enumerate(run.events()):
        if i == n_test_events: break
        data_array[i,:,:,:] = det.raw.calib(evt)

    assert np.array_equal(intensities[:n_test_events][:],data_array)
    assert np.array_equal(pixel_position_reciprocal, xtc2_pixel_position_reciprocal)
    assert np.array_equal(pixel_index_map, xtc2_pixel_index_map)

    print('TEST SUCCESS')

current_ts = -1
def get_next_ts():
    global current_ts
    current_ts += 1
    return current_ts


if __name__ == "__main__":
    flag_test = False

    # NameId setup
    nodeId = 1 
    namesId = {
        "amopnccd": 0,
        "runinfo": 1,
        "scan": 2,
    }


    # Open input hdf5 file
    h5f = h5py.File('/cds/data/drpsrcf/users/monarin/spinifel_3iyf/3iyf_sim_400k.h5', 'r')
    pixel_index_map = h5f['pixel_index_map'][:].astype(np.int16)
    pixel_position_reciprocal = h5f['pixel_position_reciprocal'][:].astype(np.float32)
    intensities = h5f['intensities']
    n_events = intensities.shape[0]
    print(f'Done opened h5 file n_events:{n_events}')
    

    # Open output file for writing
    ofname = 'out.xtc2'
    xtc2file = open(ofname, "wb")

    
    # Create config, algorithm, and detector
    config = DgramEdit(transition_id=TransitionId.Configure, ts=get_next_ts())
    alg = AlgDef("raw", 1, 2, 3)
    det = DetectorDef("amopnccd", "pnccd", "detnum1234")

    runinfo_alg = AlgDef("runinfo", 0, 0, 1)
    runinfo_det = DetectorDef("runinfo", "runinfo", "")

    scan_alg = AlgDef("raw", 2, 0, 0)
    scan_det = DetectorDef("scan", "scan", "detnum1234")


    # Define data formats
    datadef = {
        "calib": (np.float32, 3),
    }

    runinfodef = {
        "expt": (str, 1),
        "runnum": (np.uint32, 0),
    }

    scandef = {
        "pixel_position_reciprocal": (np.float32, 4),
        "pixel_index_map": (np.int16, 4),
    }


    # Create detetors
    pnccd = config.Detector(det, alg, datadef, nodeId=nodeId, namesId=namesId["amopnccd"])
    runinfo = config.Detector(runinfo_det, 
                              runinfo_alg, 
                              runinfodef, 
                              nodeId=nodeId, 
                              namesId=namesId["runinfo"]
                             )
    scan = config.Detector(scan_det,
                           scan_alg,
                           scandef,
                           nodeId=nodeId,
                           namesId=namesId["scan"]
                          )

    
    # Save xtc header transitions
    config.save(xtc2file)

    beginrun = DgramEdit(transition_id=TransitionId.BeginRun, config=config, ts=get_next_ts())
    runinfo.runinfo.expt = "xpptut15"
    runinfo.runinfo.runnum = 1
    beginrun.adddata(runinfo.runinfo)
    scan.raw.pixel_position_reciprocal = pixel_position_reciprocal
    scan.raw.pixel_index_map = pixel_index_map
    beginrun.adddata(scan.raw)
    beginrun.save(xtc2file)
    
    beginstep = DgramEdit(transition_id=TransitionId.BeginStep, config=config, ts=get_next_ts())
    beginstep.save(xtc2file)
    
    enable = DgramEdit(transition_id=TransitionId.Enable, config=config, ts=get_next_ts())
    enable.save(xtc2file)

    
    # Save L1 events
    for i_evt in range(n_events):
        d0 = DgramEdit(transition_id=TransitionId.L1Accept, config=config, ts=get_next_ts())
        pnccd.raw.calib = intensities[i_evt][:]
        d0.adddata(pnccd.raw)
        d0.save(xtc2file)
        if i_evt % 1000 == 0:
            print(f'Done saving L1 #processed: {i_evt}: events')

    
    # Save footer transitions
    disable = DgramEdit(transition_id=TransitionId.Disable, config=config, ts=get_next_ts())
    disable.save(xtc2file)
    endstep = DgramEdit(transition_id=TransitionId.EndStep, config=config, ts=get_next_ts())
    endstep.save(xtc2file)
    endrun = DgramEdit(transition_id=TransitionId.EndRun, config=config, ts=get_next_ts())
    endrun.save(xtc2file)

    xtc2file.close()

    if flag_test:
        h5data = {'pixel_index_map': pixel_index_map,
                  'pixel_position_reciprocal': pixel_position_reciprocal,
                  'intensities': intensities
                 }
        test_output(h5data)
