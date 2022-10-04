#!/bin/bash

# Parameters for smdtools
RUNNUM=${1}
QNAME=${2}
MAXEVENTS=${3}
CORES=${4}
N_EB_NODES=${5}
N_SRV_NODES=${6}


# Parameters for psana2
export PS_XTC_DIR="/cds/data/drpsrcf/users/monarin/rixl1013320/small320x"
export PS_EB_NODES=$N_EB_NODES
export PS_SRV_NODES=$N_SRV_NODES


# Call smalldata tool 
OUTDIR="/cds/data/drpsrcf/users/monarin/rixl1013320/output"
pushd smalldata_tools/arp_scripts
./submit_smd.sh -e rixl1013320 -r $RUNNUM -d ${OUTDIR} -n $MAXEVENTS -q ${QNAME} -c $CORES --epicsAll
popd


# Report
echo "Output saved to ${OUTDIR}"
