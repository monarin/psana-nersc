# This takes no. of nodes and core per node
# then generates erf input (host file) for mpi

import sys

N = int(sys.argv[1])  # no. of nodes
n = int(sys.argv[2])  # no. of cores per node
m = int(sys.argv[3])  # no. of openmp threads
e = int(sys.argv[4])  # no. of eventbuilder cores

t = 4  # no. of threds per core


def get_binding(b):
    binding = ""
    if b <= 21:
        for i in range(b):
            st = i * t
            en = i * t + 3
            binding += f"{{{st}-{en}}}"
            if i < b - 1:
                binding += f","
    else:
        for i in range(21):
            st = i * t
            en = i * t + 3
            binding += f"{{{st}-{en}}},"

        # the second socket threads start on 88
        for i in range(21, b):
            st = i * t
            en = i * t + 3
            binding += f"{{{st}-{en}}}"
            if i < b - 1:
                binding += f","

    return binding


for i in range(N):
    if i == 0:
        txt = f"1 : {{host: 1; cpu: {{0-{m}}}}}"
    elif i == 1:
        txt = f"{e}: {{host: 2; cpu: {get_binding(e)}}}"
    else:
        txt = f"{n}: {{host: {i+1}; cpu: {get_binding(n)}}}"

    print(txt)
