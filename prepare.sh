#!/bin/bash 
grep -v '^#' ms_data_dirty.csv |
sed '/^$/d' |
sed 's/,,*/,/g' |
cut -d',' -f1,2,4,5,6 |
tee ms_data.csv > /dev/null
echo "Total rows not including excluding header:"
tail -n +2 ms_data.csv | wc -l

echo "First couple of rows:"
head ms_data.csv
