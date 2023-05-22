#!/bin/sh
 
# $1: .tex file name, without extension
# $2: .bib file name, without extension
 
# clean some stuff in the tex file before pandoc
cp $1.tex $1_copy.tex
sed -i 's/figure\*/figure/g' $1_copy.tex
sed -i 's/\\makeseistitle{/\\makeseistitle\n{%/g' $1_copy.tex
sed -i 's/seistable/tabular/g' $1_copy.tex
sed -i 's/\\begin{acknowledgements}/\\begin{acknowledgements}Acknowledgements/g' $1_copy.tex

# clean inline code
perl -i -00pe 's/\\code\{(.*?)\}/\{$1\}/ig' $1_copy.tex

# convert tex file to jats xml file
pandoc $1_copy.tex -f latex -t jats+element_citations --citeproc --bibliography=$2.bib --mathjax --metadata link-citations=true --natbib --csl apa.csl -s -o $1.xml
rm -rf $1_copy.tex

# clean stuff
python3 cleanjats.py $1

# replace bib in the xml file
sed -i -n '/<back>/,/<\/back>/p' bib.xml
sed -i -e '/<back>/,/<\/back>/!b' -e "/<\/back>/!d;r bib.xml" -e 'd' $1.xml

# clean metadata and replace in the xml file
sed -i 's/\\&/&amp;/g' $1_metadata.xml
sed -e '/<front>/,/<\/front>/!b' -e "/<\/front>/!d;r $1_metadata.xml" -e 'd' $1.xml > $1_galley.xml

# clean credits file and add as section in the xml file
sed -i 's/\\&/&amp;/g' $1_credits.xml
sed -n -i -e "/<\/body>/r $1_credits.xml" -e 1x -e '2,${x;p}' -e '${x;p}' $1_galley.xml

# clean and format multiple abstracts in final galley
perl -i -00pe 's/<boxed-text>\n\s*<boxed-text>/<boxed-text>/g' $1_galley.xml
perl -i -00pe 's/<\/boxed-text>\n\s*<\/boxed-text>/<\/boxed-text>/g' $1_galley.xml
# make first word of abstract bold
perl -i -00pe 's/<boxed-text>[\n\t ]*?<p>(Non-technical summary|\S{5,25}) ([\S\d\n\t ]*?)<\/p>[\n\t ]*?<\/boxed-text>/<boxed-text><p>\n <bold>$1.<\/bold> $2\n<\/p><\/boxed-text>/gmi' $1_galley.xml

# clean all working files
rm -rf $1_metadata.xml
rm -rf $1_credits.xml
rm -rf $1.xml
rm -rf bib.xml

#eof

