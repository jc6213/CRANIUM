#!/bin/bash

#SBATCH --cpus-per-task=1
#SBATCH --mem=25000
#SBATCH --array=1-17%8

module load python/3.8.8
module load py-virtualenv/16.4.1-python-3.8.8
module load jdk

read startimage stopimage < <(sed -n ${SLURM_ARRAY_TASK_ID}p Plate001_lookup.txt )

. /home/jessecohn/env/bin/activate
cellprofiler -p /scratch/rmlab/1/Jesse/Plate001/output_folder/Batch_data.h5 -c -r -f ${startimage} -l ${stopimage}
