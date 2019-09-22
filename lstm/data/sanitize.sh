# Delete all the lines with the word 'Pool'
sed -i 's/.*2018,.*//' $1

# Get rid of all the empty lines
sed -i '/^$/d' $1