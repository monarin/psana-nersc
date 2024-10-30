import os
import sys

filename = sys.argv[1]
hosts = {}
cn_hosts = 0
cn_ranks = 0
with open(filename, "r") as f:
    for line in f:
        cols = line.split()
        hostname = cols[8]
        if hostname in hosts:
            hosts[hostname] += 1
        else:
            hosts[hostname] = 1
            cn_hosts += 1
        cn_ranks += 1

print(f"#hosts: {len(hosts.keys())} {cn_hosts} {cn_ranks}")
print(hosts)
