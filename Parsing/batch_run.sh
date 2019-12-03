#!/usr/bin/env bash

# Set the directory where the BibTeX files are
INPUT_PATH=/Users/bipashabanerjee/Documents/CS/sem3/publish/bibData/journal

# Set the directory to store the generated strings
ANNOTATED_PATH=/Users/bipashabanerjee/Documents/CS/sem3/publish/styleData/journals


# Set the directory when the binary is
CODE_PATH=$(pwd)/utils
echo $CODE_PATH
BATCH_SIZE=50

# STYLES=(modern-language-association)
STYLES=(modern-language-association apa chicago-annotated-bibliography american-medical-association american-chemical-society ieee turabian-fullnote-bibliography 
national-library-of-medicine-grant-proposals vancouver)
# This file is needed to generate specific styles
for s in ${STYLES[*]};
do
  if [[ ! -d $ANNOTATED_PATH/$s ]]; then
    mkdir $ANNOTATED_PATH/$s
  fi

  echo $s && java -XX:ReservedCodeCacheSize=512m -cp "/usr/local/opt/scala@2.12/libexec/lib/scala-library.jar:$CODE_PATH/ref2bib-assembly-0.1.1.jar" sg.edu.nus.comp.wing.etd.Reference2Bibliography \
    -i $INPUT_PATH -p "*.bib" -B $BATCH_SIZE -s $s -o $ANNOTATED_PATH/$s/output.txt
 
done

#The path to where the generated strings are
#The output is rows without invalid texts
for f in styleData/journals/*/output.txt; do
  echo $f && grep '^<[a-z\-]*>.*\W$' $f | sed 's/\\t/\/t/g' | grep -E '<([^<]+)>.*</\1>' > ${f%output.txt}/output.no_invalid_rows.txt;
done