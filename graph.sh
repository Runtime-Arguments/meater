#!/bin/sh

#
# Copyright Scott Balneaves <sbalneav@beaconia.ca>
#

# usage: graph.sh cook.log

SMOOTH=0

OPTIND=1
while getopts "s" opt; do
  case "$opt" in
    s)  SMOOTH=1
        ;;
  esac
done

shift $((OPTIND-1))

if [ $SMOOTH -eq 1 ]; then
    TYPE="smooth bezier"
else
    TYPE="with lines"
fi

echo "Temp,1,2,3,4" > ambient.csv
awk '{ if (substr($1,1,1) ~ /^[0-9]/ )
       printf("%s,%s,%s,%s,%s\n", $1, $3, $5, $7, $9)}' $1 >> ambient.csv

echo "Temp,1,2,3,4" > internal.csv
awk '{ if (substr($1,1,1) ~ /^[0-9]/ )
       printf("%s,%s,%s,%s,%s\n", $1, $2, $4, $6, $8)}' $1 >> internal.csv

gnuplot << EOF
set xdata time
set timefmt "%H:%M:%S"
set xlabel "Time"
set ylabel "Temperature (F)"
set format x "%H:%M" # Display only hours and minutes
set datafile separator ","
set terminal png
set output "ambient.png"
set title "Ambient"
set key outside
plot for [col=2:5] "ambient.csv" using 1:col $TYPE title columnheader
EOF

gnuplot << EOF
set xdata time
set timefmt "%H:%M:%S"
set xlabel "Time"
set ylabel "Temperature (F)"
set format x "%H:%M" # Display only hours and minutes
set datafile separator ","
set terminal png
set output "internal.png"
set title "Internal"
set key outside
plot for [col=2:5] "internal.csv" using 1:col $TYPE title columnheader
EOF

rm ambient.csv internal.csv
