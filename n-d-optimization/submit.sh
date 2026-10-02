#!/bin/bash
#PBS -N mega
#PBS -l select=4:ncpus=16:mpiprocs=16:mem=20gb
#PBS -l place=scatter
#PBS -l walltime=03:00:00
#PBS -o job.out
#PBS -e job.err

cd $PBS_O_WORKDIR

NP=64

mpirun -np $NP pw.x -npool 4 < rel22.in > vcrel22.out
