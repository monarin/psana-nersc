import logging

#logging.basicConfig(level=logging.DEBUG)

from psana.pscalib.calib.MDBWebUtils import calib_constants
det_str="cspad_0002"
#x = calib_constants(det_str, exp="cxid9114", ctype='pedestals', run=95, url="http://login3:6749/calib_ws")
x = calib_constants(det_str, exp="cxid9114", ctype='pedestals', run=95)
print(x)
