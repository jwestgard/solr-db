#!/bin/bash

echo -e "\n"
echo -e "=================================="
echo -e "|  MD Newspapers Data Converter  |"
echo -e "=================================="

INPUT_FILE=$1

header="id,state,city,county,title,year_pub_start,year_pub_end,lccn,oclc,issn, \
subscription_req,owner_producer,url,image_type,full_text_search,date_avail_start, \
date_avail_end,issues,comments"

# Set up temp.csv file with column headings to receive data 
echo $header > temp.csv

# Translate all CR to LF chars (squeezing [-s] any resulting double LF chars into one), 
# and translate all VT chars to pipes, passing the cleaned data to the temp file.
echo -e "• Translating line endings and converting vertical tabs to pipe chars ..."
tr -s '\r\n' '\n' < $INPUT_FILE | tr -s '\v' '\|' >> temp.csv

# Validate the resulting cleaned-up CSV file using csvclean.
echo -en "• Validating resulting file with csvclean ... "
csvclean -n temp.csv

# Separate the instrumentation column from the others, deleting spaces.
echo -e "• Separating and cleaning the 'instrumentation' column ... "
csvcut -c instrumentation temp.csv | tr -d ' ' > instrumentation.csv

# Separate the additional info field and translate internal returns 
# (previously converted to pipes) into semi-colons, removing any leading 
# spaces, duplicate semi-colons, and extra trailing spaces.
echo -e "• Separating and cleaning the 'additional info' column ... "
csvcut -c additional_info temp.csv | 
sed -E -e 's/ *\|+ */; /g' -e 's/ "$/"/' > addinfo.csv

# Push all data except [-C] the previous two columns into a separate container.
csvcut -C instrumentation,additional_info temp.csv > others.csv

# Apply a series of transformations to the data, and pass cleaned data to new file
echo -e "• Applying sed rules to clean and remove remaining extraneous characters... "
# Replace multiple PIPEs with single PIPE
sed -E 's/\|+/\|/g' others.csv |
# Trim extra spaces between values in a multivalued field
sed -E 's/\ *\|\ */\|/g' |
# Trim extra space between fields
sed -E 's/\ *,/,/g' |
# Trim beginning space inside quotes 
sed -E -e 's/^\"\ */\"/g' -e 's/,\"\ */,\"/g' |
# Trim trailing space inside quotes 
sed -E -e 's/\ *\",/\",/g' -e 's/\ *\"$/\"/g' |
# Remove trailing PIPE in a field
sed -E -e 's/\|\"$/\"/g' -e 's/\|\",/\",/g' > others-clean.csv

echo -e "• Joining resulting data files into result.csv ... "
csvjoin others-clean.csv instrumentation.csv addinfo.csv > result.csv 

echo -e "• Cleaning up and removing temporary files ... "
rm addinfo.csv others.csv instrumentation.csv temp.csv others-clean.csv

echo -e $(wc -l < result.csv) "lines written. Conversion complete! Goodbye!\n"
