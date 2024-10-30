# We want to see what happen if around 600 processes try
# to access the database for calibration constants at
# the same time.
# This is an mpi script that all ranks will run this
# database query.

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Request util for contacting the db
import psana.pscalib.calib.MDBWebUtils as wu

# Parameters required in the request
expt = "xpptut15"
det_uniqueid = "cspad_detnum1234"
runnum = 1
dbsuffix = ""


def all_request():
    calib_const = wu.calib_constants_all_types(
        det_uniqueid, exp=expt, run=runnum, dbsuffix=dbsuffix
    )
    return calib_const


def single_request():
    if rank == 0:
        calib_const = wu.calib_constants_all_types(
            det_uniqueid, exp=expt, run=runnum, dbsuffix=dbsuffix
        )
    else:
        calib_const = None
    calib_const = comm.bcast(calib_const, root=0)
    return calib_const


if __name__ == "__main__":
    comm.Barrier()
    st = MPI.Wtime()
    # calib_const = all_request()
    calib_const = single_request()
    comm.Barrier()
    en = MPI.Wtime()

    # pedestals array[0,1] is 12
    assert calib_const["pedestals"][0][0, 1] == 12
    if rank == 0:
        print(f"no. of cores: {size} request took {en-st:.5f}s.")
