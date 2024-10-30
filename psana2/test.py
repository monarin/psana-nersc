from psana import DataSource

# import logging
# logger = logging.getLogger('psana.psexp')
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)
ds = DataSource(exp="rixly5620", run=96, live=True)

for run in ds.runs():
    print(f"run={run.runnum}")
    for nevt, evt in enumerate(run.events()):
        print(nevt, evt.timestamp)
