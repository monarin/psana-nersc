"""
USAGE: python gen_slurm_hostfile.py drp-srcf-cmp[001-023,025-033,036-056],drp-srcf-eb[005-011],drp-srcf-mon[002-007,009-019] 5 2

output:
drp-srcf-cmp001
drp-srcf-cmp002
drp-srcf-cmp002
drp-srcf-cmp003
drp-srcf-cmp003

From sinfo output: 
drp-srcf-cmp[001-023,025-033,036-056],drp-srcf-eb[005-011],drp-srcf-mon[002-007,009-019]

and Input Parameters:
    1) n_ranks
    2) n_ranks_per_node

Create and output for SLURM_HOSTFILE with
rank 0 on the first node
rank 1 to n_ranks - 1 spread over no. of nodes where there can only be
n_bd_per_node on one node.
"""
import sys

node_text = sys.argv[1]
n_req_ranks = int(sys.argv[2])
n_ranks_per_node = int(sys.argv[3])

# get all nodes available
node_gobs = node_text.split('],')
nodes = {}
for node_gob in node_gobs:
    node_grp_name, node_grp_list = node_gob.split('[')
    node_no_list = []
    for node_grp in node_grp_list.split(','):
        node_grp = node_grp.replace(']','')
        node_from_to = node_grp.split('-')
        if len(node_from_to) == 1:
            node_no_list += node_from_to
        else:
            node_st, node_en = map(int, node_from_to) # e.g. 018-023
            node_no_list += list(range(node_st, node_en+1))
    nodes[node_grp_name] = node_no_list


# Try to put smd0 on drp-srcf-eb or drp-srcf-mon (1000 Gb link)
txt_out = ''
if 'drp-srcf-eb' in nodes:
    txt_out += f'drp-srcf-eb{str(nodes["drp-srcf-eb"].pop()).zfill(3)}'
elif 'drp-srcf-mon' in nodes:
    txt_out += f'drp-srcf-mon{str(nodes["drp-srcf-mon"].pop()).zfill(3)}'
else:
    txt_out += f'drp-srcf-cmp{str(nodes["drp-srcf-cmp"].pop()).zfill(3)}'

cn_ranks = 1 # smd0 count

# Spread over nodes - each node limits to n_ranks_per_node
def spread_on(cluster_name, n_asking):
    if cluster_name not in nodes:
        return 0, ""

    node_list = nodes[cluster_name]
    cn_ranks = 0
    n_used_nodes = 0
    txt_out = ''
    while cn_ranks < n_asking and n_used_nodes < len(node_list):
        current_node = node_list[n_used_nodes]
        for i in range(n_ranks_per_node):
            txt_out += f'\n{cluster_name}{str(current_node).zfill(3)}'
            cn_ranks += 1
            if cn_ranks == n_asking:
                break
        n_used_nodes += 1
    return cn_ranks, txt_out


# 1st Priority to drp-srcf-eb
n_asking = n_req_ranks - 1
if n_asking > 0:
    got_ranks, txt_ = spread_on('drp-srcf-eb', n_asking)
    n_asking -= got_ranks
    txt_out += txt_

# 2nd Priority to drp-srcf-mon
if n_asking > 0:
    got_ranks, txt_ = spread_on('drp-srcf-mon', n_asking)
    n_asking -= got_ranks
    txt_out += txt_

# 3rd Priority to drp-srcf-cmp
if n_asking > 0:
    got_ranks, txt_ = spread_on('drp-srcf-cmp', n_asking)
    n_asking -= got_ranks
    txt_out += txt_

print(txt_out)
if n_asking > 0:
    print(f'ERROR NOT ENOUGH NODE TO FULFILL THIS REQUEST')



