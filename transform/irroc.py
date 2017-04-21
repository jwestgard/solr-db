#!/user/bin/env python3
# -*- coding: utf8 -*-
#
#===================================================#
#                    cleanup.py                     #
#                  Joshua Westgard                  # 
#                    2015-12-11                     #
#                                                   #
#      Data preprocessing script for IRRoC DB       #
#   Usage: python3 cleanup.py [in.csv] [out.csv]    #
#===================================================#

import sys, csv, re

infields = ['id', 'str_resource', 'str_description', 'website',
            'see_also_url', 'meta_title', 'meta_description', 'stage_list',
            'task_list', 'category']

outfields = infields + ['stage_list_facet', 'task_list_facet']

with open(sys.argv[1], 'r') as infile, open(sys.argv[2], 'w') as outfile:
    
    # skip header row in order to use own fieldnames
    next(infile)
    
    # instantiate the reader and writer objects
    dr = csv.DictReader(infile, fieldnames=infields)
    dw = csv.DictWriter(outfile, fieldnames=outfields)
    dw.writeheader()
    
    exp = re.compile(r'\d+::([^\b])')
    
    # loop over the input file, writing results to output file
    for row in dr:
        
    # remove hash marks from URL
        m = re.search('#(.+)#', row['website'])
        if m:
            row['website'] = m.group(1)
        
        # remove spaces from all multivalued fields
        row['stage_list_facet'] = row['stage_list'].replace('; ', ';')
        row['task_list_facet'] = row['task_list'].replace('; ', ';')
        row['meta_description'] = row['meta_description'].replace(', ', ',')
        
        # create stage_list_facet and task_list_facet cols and strip numbers
        row['stage_list'] = re.sub(exp, r'\1', row['stage_list_facet'])
        row['task_list'] = re.sub(exp, r'\1', row['task_list_facet'])
                
        # write row
        dw.writerow(row)
