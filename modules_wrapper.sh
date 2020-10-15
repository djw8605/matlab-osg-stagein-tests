#!/bin/bash

RUNTIME=$1
RUNDIR=$2
OUTFILE=$3
# Another option: condor_status -ads .job.ad -af ClusterID
now_date=$(date +%s)
condor_chirp ulog "MODULE Load Start $now_date" &
module_pid=$!
module load matlab
RUNDIR=/cvmfs/connect.opensciencegrid.org/modules/packages/linux-rhel7-x86_64/gcc-6.4.0spack/matlab-R2018b-cg5ysgn5gb2waoe73lv5ooteg4ntah46/v95
#time tar -xzf $RUNTIME
# STAGE-IN Complete
now_date=$(date +%s)
condor_chirp ulog "STAGE-IN Complete $now_date" &
stagein_in_pid=$!
echo "STAGE-IN Complete: $now_date" >> $OUTFILE
time ./run_matrix.sh $RUNDIR

now_date=$(date +%s)
condor_chirp ulog "EXECUTION Complete $now_date" &
execution_pid=$!
echo "EXECUTION Complete: $now_date" >> $OUTFILE

# Wait for the chirps to complete
wait $execution_pid
wait $stagein_in_pid
wait $module_pid
