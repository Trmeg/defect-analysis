#!/bin/bash
#PBS -N lda
#PBS -l select=8:ncpus=8:mpiprocs=8
#PBS -l place=scatter
#PBS -l walltime=24:00:00
#PBS -o job.out
#PBS -e job.err
#PBS -P ioe.che.rousan.1
#PBS -m bea
#PBS -M che252200@iitd.ac.in

cd $PBS_O_WORKDIR



mpirun -np 64 pw.x  < defse.in > v0sed.out
