#!/usr/bin/env bash
# 
# usage: file-metadata.sh [dirtosearch] > [outputfile]
#
# Gather file metadata from pdfs scanned for plant patents project
#

SEARCHROOT=$1

API="http://patft.uspto.gov/netacgi/nph-Parser?patentnumber=PP"

echo "id,filename,timestamp,filepath,uspto_url"

find "$SEARCHROOT" -type f -name *.pdf |
while read file
do 
    mtime=$(stat -f "%m" $file)
    name=$(basename $file)
    num=$(echo $name | cut -d. -f1 | tr -d 'p')
    echo "PP$num,$name,$mtime,${file#.*/},$API${num#0}"
done
