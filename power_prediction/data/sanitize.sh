# Delete all rows that have a date with no time
sed -i 's/.*2018,.*//' $1
sed -i 's/.*2019,.*//' $1

# Get rid of all the empty lines
sed -i '/^$/d' $1