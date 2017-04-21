#!/user/bin/env python3
# -*- coding: utf8 -*-

#===================================================#
#                    cleanup.py                     #
#                  Joshua Westgard                  # 
#                    2015-07-16                     #
#                                                   #
#  Data preprocessing script for md-newspapers DB   #
#   Usage: python3 cleanup.py [in.csv] [out.csv]    #
#===================================================#

import sys, csv, datetime

infields = ['state', 'city', 'county', 'title', 'year_pub_start', 'year_pub_end', 
'lccn', 'oclc', 'issn', 'owner_producer', 'url', 'subscription_req', 'image_type', 
'full_text_search', 'date_avail_start', 'date_avail_end', 'issues', 'comments']

outfields = ['id'] + infields + ['range_avail','range_pub','year_facets_list']

with open(sys.argv[1], 'r') as infile, open(sys.argv[2], 'w') as outfile:
    
    # skip header row in order to use own fieldnames
    next(infile)
    
    # instantiate the reader and writer objects
    dr = csv.DictReader(infile, fieldnames=infields)
    dw = csv.DictWriter(outfile, fieldnames=outfields)
    dw.writeheader()
    
    # loop over the input file, writing results to output file
    for n, row in enumerate(dr):
    
        # create id column
        row['id'] = n + 1
        
        # strip out commas from issue data (should be integer data)
        row['issues'] = row['issues'].replace(',', '')
        
        # split format column on commas and save as space-delimited field
        types = row['image_type'].split(',')
        row['image_type'] = " ".join([t.strip(' ') for t in types])
    
        # get the years from the end of the available date strings
        avail_start = row['date_avail_start'].split('/')[-1]
        avail_end = row['date_avail_end'].split('/')[-1]
    
        # handle the end date of "current"
        if avail_end == "current":
            avail_end = "2015"
    
        # create display ranges for dates available and dates published
        row['range_avail'] = '{0}-{1}'.format(avail_start, avail_end)
        row['range_pub'] = '{0}-{1}'.format(row['year_pub_start'], row['year_pub_end'])
    
        # generate a field holding the range of years between the begin and end years
        yrs = range(int(avail_start), int(avail_end) + 1)
        row['year_facets_list'] = " ".join([str(x) for x in yrs])
        
        dw.writerow(row)
            

    
    
    
