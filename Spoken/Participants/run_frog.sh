FILES=./Plain/*.txt

for f in $FILES
do
  frog -n -t $f -o "./Parsed/$(basename $f)"
done
