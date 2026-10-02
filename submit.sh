#!/bin/bash
#PBS -N mega
#PBS -l select=4:ncpus=16:mpiprocs=16:mem=20gb
#PBS -l place=scatter
#PBS -l walltime=03:00:00
#PBS -o job.out
#PBS -e job.err
#PBS -P ioe.che.rousan.1
#PBS -m bea
#PBS -M che252200@iitd.ac.in

cd $PBS_O_WORKDIR

NP=64

mpirun -np $NP pw.x  < Voxy.in > vo1.out
