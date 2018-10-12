from psana import DataSource
import sys

exp = sys.argv[1]
run = sys.argv[2]
detname = sys.argv[3]

xtc_dir = "/reg/d/psdm/xpp/xpptut15/scratch/mona/%s"%(exp)
ds = DataSource('exp=%s:run=%s:dir=%s'%(exp, run, xtc_dir))
det = eval('ds._configs[0].software.%s'%(detname))
dettype = det.dettype
detid = det.detid
print(dettype, detid)
