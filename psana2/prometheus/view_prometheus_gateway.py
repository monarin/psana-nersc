from monitor import MetricDisplay
import os, sys
from datetime import datetime, timedelta

if __name__ == "__main__":
    stop = datetime.now()
    start = stop - timedelta(minutes=2)
    jobid = sys.argv[1]

    
    srvurl = os.environ.get("DM_PROM_SERVER", "http://psmetric03:9090") 
    md = MetricDisplay(srvurl, start, stop, jobid)
    md.show_counter('evts_transmit_total', query_type="rate", verbose_level=0, ignore_ranks=[])
