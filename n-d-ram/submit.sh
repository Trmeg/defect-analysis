#!/bin/bash
#PBS -N ph
#PBS -l select=1:ncpus=4:mpiprocs=4
#PBS -l place=scatter
#PBS -l walltime=00:10:00
#PBS -o o.out
#PBS -e e.err
#PBS -P ioe.che.rousan.1
#PBS -m bea
#PBS -M che252200@iitd.ac.in

cd $PBS_O_WORKDIR

mpirun -np 4 dynmat.x < dynmat.in > dynmat.out
