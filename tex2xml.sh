#!/bin/sh
 
# $1: .tex file name, without extension
# $2: .bib file name, without extension
 
# clean some stuff in the tex file before pandoc
cp $1.tex $1_copy.tex
sed -i 's/figure\*/figure/g' $1_copy.tex
# # sed -i 's/seistable\*/tabular/g' $1.tex
sed -i 's/\makeseistitle{/\makeseistitle\n{%/g' $1_copy.tex

# convert tex file to jats xml file
pandoc $1_copy.tex -f latex -t jats+element_citations --citeproc --bibliography=$2.bib --mathjax --metadata link-citations=true --natbib --csl apa.csl -s -o $1.xml

rm -rf $1_copy.tex

# extract tex metadata to jats metadata
python3 metatex2jats.py $1

# clean math formulas, several cases depending on the presence of labels
perl -i -00pe 's/(<disp-formula>)[\S\n\t\v ]*?<alternatives>[\S\d\n\t ]*?(<tex-math>)[\S\n\t\v ]*?<!\[CDATA\[([\S\n\t\v ]*?)(\\label\{([\S\n\t\v ]*?)\})\]\]>[\S\n\t\v ]*?<\/tex-math>[\S\n\t\v ]*?<\/disp-formula>/<disp-formula id="$5"><label>$5<\/label>$2<![CDATA[$3]]><\/tex-math><\/disp-formula>/gmi' $1.xml
perl -i -00pe 's/(<disp-formula>)[\S\n\t\v ]*?<alternatives>[\S\d\n\t ]*?(<tex-math>)[\S\n\t\v ]*?<!\[CDATA\[(\\label\{([\S\n\t\v ]*?)\})([\S\n\t\v ]*?)\]\]>[\S\n\t\v ]*?<\/tex-math>[\S\n\t\v ]*?<\/disp-formula>/<disp-formula id="$4"><label>$4<\/label>$2<![CDATA[$5]]><\/tex-math><\/disp-formula>/gmi' $1.xml
perl -i -00pe 's/(<disp-formula>)[\S\n\t\v ]*?<alternatives>[\S\d\n\t ]*?(<tex-math>)[\S\n\t\v ]*?<!\[CDATA\[([\S\n\t\v ]*?)\]\]>[\S\n\t\v ]*?<\/tex-math>[\S\n\t\v ]*?<\/disp-formula>/<disp-formula id="">$2<![CDATA[$3]]><\/tex-math><\/disp-formula>/gmi' $1.xml
# 
perl -i -00pe 's/(<inline-formula>)[\S\n\t\v ]*?<alternatives>[\S\n\t\v ].*?(<tex-math)>([\S\n\t\v ]*?)((<\/tex-math>)([\S\n\t\v ]*?)[\S\n\t\v ]*?<\/alternatives>)/$1$2>$3$5/gmi' $1.xml

# clean ids
python3 cleanidjats.py $1

# replace jats xml file metadata
sed -e '/<front>/,/<\/front>/!b' -e "/<\/front>/!d;r $1_metadata.jats" -e 'd' $1.xml > $1_galley.xml

# clean multiple abstracts in final 1_galley
perl -i -00pe 's/<boxed-text>\n\s*<boxed-text>/<boxed-text>/g' $1_galley.xml
perl -i -00pe 's/<\/boxed-text>\n\s*<\/boxed-text>/<\/boxed-text>/g' $1_galley.xml

# clean xref
# cleans first xref after a figure is referenced to
perl -i -00pe 's/(fig[\S\d\n\t ]{0,9}<xref )/$1ref-type=\"fig\" /ig' $1_galley.xml
# cleans first xref after a table is referenced to
perl -i -00pe 's/(tab[\S\d\n\t ]{0,9}<xref )/$1ref-type="table" /ig' $1_galley.xml

# cleans other xrefs after 1st one, iterating to find xref without ref-type
python3 cleanxrefjats.py $1_galley

# clean/add figures extensions if not already there
perl -i -00pe 's/mime-subtype=\"\" xlink:href=\"(.*?)\.pdf\"/mime-subtype=\"pdf\" xlink:href=\"$1\.pdf\"/ig' $1_galley.xml
perl -i -00pe 's/mime-subtype=\"\" xlink:href=\"(.*?)\.png\"/mime-subtype=\"png\" xlink:href=\"$1\.png\"/ig' $1_galley.xml
perl -i -00pe 's/mime-subtype=\"\" xlink:href=\"(.*?)\.jpg\"/mime-subtype=\"jpg\" xlink:href=\"$1\.jpg\"/ig' $1_galley.xml
perl -i -00pe 's/mime-subtype=\"(.*?)\" xlink:href=\"(.*?)(\.pdf|\.png|\.jpg){0,1}\"/mime-subtype=\"$1\" xlink:href=\"$2\.$1\"/ig' $1_galley.xml

# cleans table ids
table_max=20
for VAR in `seq 1 $table_max`
do
    perl -i -00pe "s/\[tbl$VAR\]/$VAR/ig" $1_galley.xml
done

# clean credits file
sed -i 's/\\&/&amp;/g' $1_credits.jats

# add credits as section in the galley file
sed -n -i -e "/<\/body>/r $1_credits.jats" -e 1x -e '2,${x;p}' -e '${x;p}' $1_galley.xml


#eof

