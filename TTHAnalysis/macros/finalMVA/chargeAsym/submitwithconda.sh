#!/bin/bash
WORK=$1; shift
cd $WORK
source /t3home/sesanche/.conda.sh; 
conda activate pytorch_1.13
exec $*
