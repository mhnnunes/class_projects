#!/bin/bash

CURDIR=`pwd`
echo $CURDIR

DATASETS=$HOME/git/class_projects/heuristics/implementation/dataset/
echo $DATASETS

RESULT_FILE=$CURDIR/out_time.log

# Clean out old result file
echo "" > $RESULT_FILE

# Begin test
for f in `find $DATASETS -name *.tsp| sort -V `;
do
  echo "Testing file: ${f}"

  # Pre-processing input file
  # Remove space between the word DIMENSION and ':'
  # sed -i "s/DIMENSION\ :/DIMENSION:/g" $f
  # head -n6 "${f}" | grep DIME
  # Verify if the first 6 lines of every file are header lines
  # head -n6 "${f}" | grep COORD
  # Verify the syntax of the lines denoting the distance type
  # head -n6 $f | grep WEIGHT
  # sed -i "s/EDGE_WEIGHT_TYPE\ :/EDGE_WEIGHT_TYPE:/g" $f

  # Execute and save results from program
  BNAME=`basename $f`
  TIME_START=`date +%s.%N`
  OUTPUT=`$CURDIR/tp4 < $f`
  TIME_END=`date +%s.%N`
  TIME_DIFF=`echo ${TIME_END} - ${TIME_START}| bc`
  echo "${OUTPUT} ${BNAME} ${TIME_DIFF}" >> $RESULT_FILE
done
