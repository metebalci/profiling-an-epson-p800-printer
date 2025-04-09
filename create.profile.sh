#!/bin/bash
set -ex

if [ "$#" -ne 3 ]; then
  echo 'usage: generate.profile.sh "PAPER" "matte/glossy" MEASUREMENTS'
  echo 'PAPER is included in the description tag'
  echo 'MEASUREMENTS_M0.txt and MEASUREMENTS_M2.txt is converted to .ti3 with txt2ti3 and used with colprof'
  echo 'output is MEASUREMENTS.icc'
  exit 1
fi

if ! command -v txt2ti3 2>&1 >/dev/null
then
  echo "txt2ti3 not found"
  exit 1
fi

if ! command -v colprof 2>&1 >/dev/null
then
  echo "colprof not found"
  exit 1
fi

PAPER="$1"

if [ "$2" = "matte" ]; then
ATTRIBUTES="mr"
elif [ "$2" = "glossy" ]; then
ATTRIBUTES="r"
else
  echo "invalid parameter: matte or glossy is allowed"
fi

MEASUREMENTS_M0_TXT="${3}_M0.txt"
# remove suffix
MEASUREMENTS_M0="${3}_M0"

MEASUREMENTS_M2_TXT="${3}_M2.txt"
# remove suffix
MEASUREMENTS_M2="${3}_M2"

INFO="Epson SC-P800"
COPYRIGHT="Copyright(C) Mete Balci. 2025"

AdobeRGB1998="../refs/AdobeRGB1998.icc"

QUALITY="h"
SOURCE_GAMUT="-S ${AdobeRGB1998}"

# M0

txt2ti3 "$MEASUREMENTS_M0_TXT" "$MEASUREMENTS_M0"

# M0, without FWA compensation

colprof -D "$INFO M0 $PAPER" -C "$COPYRIGHT" \
        -Z $ATTRIBUTES -q $QUALITY -a l \
        -i D50 -o 1931_2 -v \
        $SOURCE_GAMUT -cmt -dpp \
        "$MEASUREMENTS_M0"

# M0, with FWA compensation
# overrides default output filename to not overwrite non-FWA icc output

colprof -D "$INFO M0 FWA $PAPER" -C "$COPYRIGHT" \
        -Z $ATTRIBUTES -q $QUALITY -a l \
        -f -i D50 -o 1931_2 -v \
        $SOURCE_GAMUT -cmt -dpp \
        -O "${MEASUREMENTS_M0}_FWA.icc" \
        "$MEASUREMENTS_M0"

# M2=UV cut, no FWA compensation
txt2ti3 "$MEASUREMENTS_M2_TXT" "$MEASUREMENTS_M2"

colprof -D "$INFO M2 $PAPER" -C "$COPYRIGHT" \
        -Z $ATTRIBUTES -q $QUALITY -a l \
        -i D50 -o 1931_2 -v \
        $SOURCE_GAMUT -cmt -dpp \
        "$MEASUREMENTS_M2"
