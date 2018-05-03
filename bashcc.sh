#!/bin/bash --login

#SBATCH -N 1-1   
#SBATCH --tasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH -t 44:00:00

module load /app/modules/languages/python/2.7.11

for ((i=1; i<=4; i+=1))
do
    python hpcdecoderTester.py 12 5000 $i 0.02 0.08 0 &
    python hpcdecoderTester.py 12 5000 $i 0.02 0.08 1 &
    python hpcdecoderTester.py 12 5000 $i 0.02 0.08 2 &
done
 

wait
