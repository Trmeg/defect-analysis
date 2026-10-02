#!/bin/bash
#PBS -N vo
#PBS -l select=8:ncpus=8:mpiprocs=8
#PBS -l place=scatter
#PBS -l walltime=60:00:00
#PBS -o o.out
#PBS -e e.err
#PBS -P ioe.che.rousan.1
#PBS -m bea
#PBS -M che252200@iitd.ac.in

cd $PBS_O_WORKDIR

mpirun -np 64  ph.x -in phvo.in > ph.out 

mpirun -np 4 dynmat.x < dynmat.in > dynmat.out
