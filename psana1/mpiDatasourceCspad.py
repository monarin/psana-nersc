from psana import *

dsource = MPIDataSource('exp=cxic0515:run=83:smd')
det = Detector('DsdCsPad')

smldata = dsource.small_data('cxic0515_run83.h5',gather_interval=10)

partial_run_sum = None
for nevt,evt in enumerate(dsource.events()):
   calib = det.calib(evt)
   if calib is None: continue
   epix_sum = calib.sum()      # number
   epix_roi = calib[0][0][3:5] # array
   if partial_run_sum is None:
      partial_run_sum = epix_roi
   else:
      partial_run_sum += epix_roi

   # save per-event data
   smldata.event(epix_sum=epix_sum,epix_roi=epix_roi)

   if nevt == 100: break

# get "summary" data
run_sum = smldata.sum(partial_run_sum)
# save HDF5 file, including summary data
smldata.save(run_sum=run_sum)
