from psana import DataSource

#ds = DataSource(files='multirun_w_new_config.xtc2')

xtc_dir= '/cds/home/m/monarin/psana-nersc/psana2/dgrampy/multirun_w_new_config'
ds = DataSource(exp="xpptut15", run=1, dir=xtc_dir)

for run in ds.runs():
    print(f'**NEW RUN:{run.runnum}')
    if run.runnum == 1:
        det = run.Detector('hsd')
    else:
        det = run.Detector('andor')

    for evt in run.events():
        print(f'    evt={evt.timestamp} calib={det.raw.calib(evt).shape}')

