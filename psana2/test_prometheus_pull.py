import os
import sys
import time
from datetime import datetime, timedelta

import dmmon.promquery as pq
import jmespath
import numpy as np


# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, "w")


# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__


class MetricDisplay(object):
    def __init__(self, srvurl, start, stop, jobid):
        self.start = start
        self.stop = stop
        self.srvurl = srvurl
        self.jobid = jobid

    def get_rate(self, metric_name):
        blockPrint()  # block promequery print
        data = pq.get_data_prom(
            self.srvurl,
            'rate(%s{jobid="%s"}[15s])' % (metric_name, self.jobid),
            self.start.timestamp(),
            self.stop.timestamp(),
            step="5s",
        )
        enablePrint()
        return data


def main(srvurl, jobid, start=None, step_seconds=15):

    if not start:
        # Default is the last step_seconds
        stop = datetime.now()
        start = stop - timedelta(seconds=step_seconds)
    else:
        # Or query from start with query window = step_seconds
        stop = start + timedelta(seconds=step_seconds)

    print(f"QUERY FROM {start} TO {stop} ")
    print(f"STEP={step_seconds}s")

    md = MetricDisplay(srvurl, start, stop, jobid)
    data = md.get_rate("psana_bd_wait_eb_total")
    print(data)


if __name__ == "__main__":
    jobid = sys.argv[1]
    start = None
    if len(sys.argv) > 2:
        start = datetime.fromtimestamp(int(sys.argv[2]))
    srvurl = os.environ.get("DM_PROM_SERVER", "http://psmetric03:9090")

    print("Using server", srvurl, " jobid:", jobid)
    main(srvurl, jobid, start=start)
