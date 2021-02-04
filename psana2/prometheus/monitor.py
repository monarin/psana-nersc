#!/usr/bin/env python3

import os
import time
import jmespath
from datetime import datetime, timedelta
import dmmon.promquery as pq
import numpy as np
import sys, os

jobid = sys.argv[1]

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__


class MetricDisplay(object):
    def __init__(self, srvurl, start, stop):
        self.start  = start
        self.stop   = stop
        self.srvurl = srvurl

    def get_rate(self, metric_name):
        blockPrint()        # block promequery print
        data = pq.get_data_prom(self.srvurl,
                'irate(%s{}[10s])'%(metric_name),
                self.start.timestamp(), self.stop.timestamp(), 5)
        enablePrint()
        return data

    def get_raw(self, metric_name):
        blockPrint()
        data = pq.get_data_prom(self.srvurl,
                '%s{}'%(metric_name),
                self.start.timestamp(), self.stop.timestamp(), 5)
        enablePrint()
        return data

    def digest(self, data, iface=None, instance=None):
        result = {}
        for sample in  jmespath.search("data.result[*].[metric, values]", data):
            labels, values = sample
            if iface == "bash":
                if labels["instance"] == instance:
                    result_key = labels['instance']
                    result[result_key] = int(values[-1][0]), float(values[-1][1])

            elif 'jobid' in labels:
                if labels['jobid'] == jobid:
                    if 'unit' in labels:
                        result_key = (labels['rank'], labels['unit'], labels['endpoint'])
                    elif 'checkpoint' in labels:
                        result_key = (labels['rank'], labels['checkpoint'])
                    else:
                        result_key = (labels['rank'], 'seconds', 'None')
                    # report latest value: (ts, val)
                    result[result_key] = int(values[-1][0]), float(values[-1][1])
        return result

    def show_counter(self, metric_name, query_type="rate", verbose_level=0):
        if query_type == "rate":
            data = self.get_rate(metric_name)
        else:
            data = self.get_raw(metric_name)
        result = self.digest(data)
        prn_out = {}
        sum_by_ranks = {}
        sum_by_units = {}
        for (rank, unit, endpoint), (_, val) in result.items():
            txt = f"ENDPOINT {endpoint}: {val:.5f} {unit}\n" 
            if rank in prn_out:
                prn_out[rank] += txt
            else:
                prn_out[rank] = txt
            
            if rank in sum_by_ranks:
                unit_val_dict = sum_by_ranks[rank]
                if unit in unit_val_dict:
                    unit_val_dict[unit] += val
                else:
                    unit_val_dict[unit] = val
            else:
                sum_by_ranks[rank] = {unit: val}

            if unit in sum_by_units:
                sum_by_units[unit] += val
            else:
                sum_by_units[unit] = val
        
        for unit, sum_val in sum_by_units.items():
            print(f"{unit.ljust(20)} {sum_val:.5f}")
        
        for rank, prn in prn_out.items():
            unit_val_dict = sum_by_ranks[rank]
            if int(rank) > 0 and verbose_level > 0:
                print(f"RANK {rank} SUMMARY")
            for unit, sum_val in unit_val_dict.items():
                if query_type == "rate":
                    unit += "/s"
                if verbose_level > 0:
                    print(f"{unit.ljust(20)} {sum_val:.5f} ")
            
            if verbose_level > 1:
                print(prn)
    
    def show_summary(self, metric_partial_name):
        data = self.get_raw(f'{metric_partial_name}_sum')
        result_sum = self.digest(data)

        data = self.get_raw(f'{metric_partial_name}_count')
        result_count = self.digest(data)

        for ((rank, sum_unit, sum_endpoint), (_, sum_val)), \
                ((_, _, _), (_, cn_val)) \
                in zip(result_sum.items(), result_count.items()):
            
            if cn_val == 0: continue # skip if no data
            
            if int(rank) > 0:
                print(f"RANK {rank}")

            print(f"{'AVG'.ljust(20)} {sum_val/cn_val:.5f} s")
            print(f"{'TOTAL'.ljust(20)} {sum_val:.5f} s")
            print(f"{'COUNTS'.ljust(20)} {cn_val}")

    def show_gauge(self, metric_name, iface=None, instance=None, diff_with=None):
        data = self.get_raw(metric_name)
        result = self.digest(data, iface, instance)
        val = 0
        if iface == "bash":
            for instance, (prom_ts, val) in result.items():
                if diff_with:
                    diff = val - diff_with
                else:
                    diff = 0
                #print(f"instance: {instance} {metric_name} at {val} delta={diff:.5f}")
        else:
            group_by_checkpoints = {}
            for (rank, checkpoint), (prom_ts, val) in result.items():
                if diff_with:
                    diff = val - diff_with
                else:
                    diff = 0
                
                if checkpoint in group_by_checkpoints:
                    group_by_checkpoints[checkpoint].append(diff)
                else:
                    group_by_checkpoints[checkpoint] = [diff]
            
            for checkpoint, diffs in group_by_checkpoints.items():
                print(f"{checkpoint.ljust(20)} AVG={np.average(diffs):.2f} MIN={min(diffs):.2f} MAX={max(diffs):.2f} STD={np.std(diffs):.2f}")
        return val

    def show_ranking_counter(self, metric_name, rank_unit=None, q=95, show="top"):
        """Show top/bottom nth-tile performers (default is 95 percentile)
        For Counter, you can choose unit (etc. seconds) as the value for
        ranking and the results are grouped by the rank nos. Example usage:
        Smd0 waiting for EventBuilder cores (endpoint) or EventBuilder waiting
        for BigData cores (endpoint). For the latter, the print out is shown
        for each EventBuilder core.

        NOTE:
        - Counter labels: evts, batches, MB, seconds (used in rank_unit).
        - The perentile is calculated on the chosen rank_unit / batches 
        (no. of communications).
        """
        data = self.get_raw(f'{metric_name}')
        result = self.digest(data)
        
        if not result: return
        
        vals = []
        for (rank, unit, endpoint), (_, val) in result.items():
            if unit == rank_unit:
                if (rank, 'batches', endpoint) in result:
                    if result[(rank, 'batches', endpoint)][1] == 0: continue

                    vals.append(val/ result[(rank, 'batches', endpoint)][1])
                else:
                    vals.append(val)

        if not vals:
            print(f'NO DATA')
            return

        percentile = np.percentile(vals, q)
        print(f'{str(q)+"th percentile".ljust(18)} {percentile:.5f}')

        prn_out = {}
        for (rank, unit, endpoint), (_, val) in result.items():
            if unit != rank_unit: continue
            
            # convert value to rate (divided by no. of batches) if batches
            # were collected.
            if (rank, 'batches', endpoint) in result:
                if result[(rank, 'batches', endpoint)][1] == 0: continue
                val = val / result[(rank, 'batches', endpoint)][1] 
            
            txt = ""
            endpoint_str = f"ENDPOINT {endpoint}"
            if show == "top":
                if val >= percentile:
                    txt = f"{endpoint_str.ljust(20)} {val:.5f} {unit}\n"
            else:
                if val < percentile:
                    txt = f"{endpoint_str.ljust(20)} {val:.5f} {unit}\n"
            
            if rank in prn_out:
                prn_out[rank] += txt
            else:
                prn_out[rank] = txt
        
        for rank, prn in prn_out.items():
            if prn:
                print(f"RANK {rank} (/s)")
                print(prn)

    def show_ranking_summary(self, metric_partial_name, excluded_ranks=[], q=95, show="top"):
        """Show top/bottom nth-tile performers (default is 95 percentile)
        For Summary, ranking is done on the average values (*_sum/ *_count).
        """
        data = self.get_raw(f'{metric_partial_name}_sum')
        result_sum = self.digest(data)

        data = self.get_raw(f'{metric_partial_name}_count')
        result_count = self.digest(data)
        
        avgs = []
        for ((rank, sum_unit, sum_endpoint), (_, sum_val)), \
                ((_, _, _), (_, cn_val)) \
                in zip(result_sum.items(), result_count.items()):
            if cn_val == 0 or int(rank) in excluded_ranks: continue
            avgs.append(sum_val/ cn_val)
        
        if not avgs:
            print(f'NO DATA')
            return

        percentile = np.percentile(avgs, q)
        print(f'{str(q)+"th percentile".ljust(18)} {percentile:.5f}')
        for ((rank, unit, endpoint), (_, sum_val)), \
                ((_, _, _), (_, cn_val)) \
                in zip(result_sum.items(), result_count.items()):
            
            if cn_val == 0 or int(rank) in excluded_ranks: continue
           
            avg_val = sum_val/ cn_val
            rank_str = f"RANK {rank}"
            if show == "top":
                if avg_val >= percentile:
                    print(f"{rank_str.ljust(20)} {avg_val:.5f} {unit}")
            else:
                if avg_val < percentile:
                    print(f"{rank_str.ljust(20)} {avg_val:.5f} {unit}")


def main(srvurl):
    
    stop = datetime.now()
    start = stop - timedelta(minutes=5)

    q = 95 
    n_smd_nodes = 1
    
    md = MetricDisplay(srvurl, start, stop)
    
    print("CHECKPOINT TIMESTAMP")
    start_time = md.show_gauge('psana_start_time', iface="bash", instance="drp-srcf-cmp001")
    #md.show_gauge('psana_end_time', iface="bash", instance="drp-tst-dev011", diff_with=start_time)
    md.show_gauge('psana_timestamp', diff_with=start_time)

    print("SMD0\nDISK READING RATE")
    md.show_counter('psana_smd0_read_total', query_type="rate")

    print("SEND RATE")
    md.show_counter('psana_smd0_sent_total')
    
    print("DISK WAITING TIME")
    md.show_summary('psana_smd0_wait_disk')
    
    print("MPI WAITING TIME")
    md.show_ranking_counter('psana_smd0_sent_total', rank_unit='seconds', q=q)
    
    
    print("\nEVENTBUILDER(S)")
    print("SEND RATE")
    md.show_counter('psana_eb_sent_total')
    
    print("USER FILTER CALLBACK WAITING TIME")
    md.show_ranking_counter('psana_eb_filter_total', rank_unit='seconds', q=q)
    
    print("TIME (s) WAITING FOR SMD0")
    md.show_ranking_summary('psana_eb_wait_smd0', excluded_ranks=[0], q=q)

    print("TIME (s) WAITING FOR BIGDATA CORES")
    md.show_ranking_counter('psana_eb_sent_total', rank_unit='seconds', q=q)

    
    print("\nBIGDATA")
    print("DISK READING RATE")
    md.show_counter('psana_bd_read_total')
    
    print("TIME (s) WAITING FOR EVENTBUILDER")
    md.show_ranking_counter('psana_bd_wait_eb_total', rank_unit='seconds', q=q)

    print("AVERAGE DISK WAITING TIME")
    md.show_ranking_summary('psana_bd_wait_disk', excluded_ranks=range(n_smd_nodes+1), q=q) 
    
    print("AVERAGE ANALYSIS WAITING TIME")
    md.show_ranking_counter('psana_bd_ana_total', rank_unit='seconds', q=q)

    
if __name__ == "__main__":
    srvurl = os.environ.get("DM_PROM_SERVER", "http://psmetric03:9090") 

    print("Using server", srvurl)
    main(srvurl)
