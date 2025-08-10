#!/bin/bash
set -e

SCRIPTHOME=$(dirname "$(realpath "$0")")

if [ "$#" -ne 2 ]; then
  echo "usage: create.patchset.sh NUM_OFPS NUM_WHITE_BLACK"
  exit 1
fi

OFPS=$1
WB=$2

BASENAME=ac_${OFPS}_wb${WB}

TARGEN_CMD="targen -v -d2 -G -e${WB} -B${WB} -f${OFPS} ${BASENAME}"

if [ -f ${BASENAME}.ti1 ] || [ -f ${BASENAME}.txt ]; then
  echo "output files ${BASENAME}.ti1/.txt already exists"
  exit 1
fi

echo "${TARGEN_CMD}"
eval "${TARGEN_CMD}"

"${SCRIPTHOME}/scaleti1rgb.py" -o ${BASENAME}.txt ${BASENAME}.ti1
