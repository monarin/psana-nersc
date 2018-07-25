## Copyright (c) 2017, Los Alamos National Security, LLC.
## All rights reserved.
import lanl.setup_env as lanl_config
from lanl.setup_env import get_launchpad
from lanl.demo import per_run, general

lp = get_launchpad()
db = lp.db

for run in list(db.run_log.find()):
    run_num = run['run_num']
    if 'dc_queued' in run and 'dc_start' in run and 'dc_stop' in run:
        dc_queued = run['dc_queued']
        dc_start = run['dc_start']
        dc_stop = run['dc_stop']
        print 'run number %d: data check queue time=%d seconds, run time=%d seconds' % (run_num, int(dc_start)-int(dc_queued),
                                                                                        int(dc_stop)-int(dc_start))
    if 'int_queued' in run and 'int_start' in run and 'int_stop' in run:
        int_queued = run['int_queued']
        int_start = run['int_start']
        int_stop = run['int_stop']
        print 'run number %d: integrate queue time=%d seconds, run time=%d seconds' % (run_num, int(int_start)-int(int_queued),
                                                                                       int(int_stop)-int(int_start))
        print 'run number %d: total process time=%d seconds' % (run_num, int(int_stop)-int(dc_queued))

    print '------------------------------------------------'
    print ''

merge_prefix = general['merge_prefix']
merge_bundles = general['merge_bundles']
pickled = db.merge_log.find_one({'pickled' : 'Exafel Demo'})
for m in range(0,len(merge_bundles)):
    merge_tag = '%s_%s' % (merge_prefix, str(m))
    mqueued = 'merge_queued_%s' % merge_tag
    mstart = 'merge_start_%s' % merge_tag
    mstop = 'merge_stop_%s' % merge_tag
    if merge_tag in pickled:
        runs = pickled[merge_tag]['runs']
        run_num = (runs.keys())[0]
        run_id = runs[str(run_num)][0]
        run = db.run_log.find_one({'run_id' : run_id})
        if run and mqueued in run and mstart in run and mstop in run:
            merge_queued = run['merge_queued']
            merge_start = run['merge_start']
            merge_stop = run['merge_stop']
            print 'merge %s: queue time=%d seconds, run time=%d seconds' % (merge_tag, int(merge_start)-int(merge_queued),
                                                                            int(merge_stop)-int(merge_start))
            print 'total time including merge %s=%d seconds' % (merge_tag, int(merge_stop)-int(dc_queued))


