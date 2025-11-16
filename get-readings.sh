#!/bin/sh

#
# Copyright Scott Balneaves <sbalneav@beaconia.ca>
#

# NOTE: you must be signed into the meater app on your phone

FILENAME="cook.log"

read-meater.py -h > $FILENAME

while /bin/true; do
    read-meater.py >> $FILENAME
    sleep(600)
done
