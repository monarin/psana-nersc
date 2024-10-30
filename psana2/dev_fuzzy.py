from psana import DataSource

xtc_dir = "/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2"
ds = DataSource("exp=xpptut15:run=1:dir=%s" % xtc_dir)
print(ds.run_dict)
