#!/bin/bash

RUNTIME=$1
RUNDIR=$2
OUTFILE=$3
# Another option: condor_status -ads .job.ad -af ClusterID
module load stashcache
stashcp /osgconnect/public/ckoch5/matlab-testing/r2018b.tar.gz ./
time tar -xzf $RUNTIME

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
