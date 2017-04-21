#!/usr/bin/env bash
# 
# usage: ./pdf-pgcount.sh [dirtosearch] [extension or filename glob]
# 
# scans pdf files with ghostscript and returns filename and number of pages

find $1 -type f -name $2 | 
while read filename
do 
    gs_cmd="($filename) (r) file runpdfbegin pdfpagecount = quit"
    num_pages=$(gs -q -dNODISPLAY -c "$gs_cmd")
    echo $filename","$num_pages
done
