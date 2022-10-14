#!/bin/bash
 
# $1: .tex file name, without extension
# $2: .bib file name, without extension
 
# clean some stuff in the tex file before pandoc
cp $1.tex $1_copy.tex
sed -i 's/figure\*/figure/g' $1_copy.tex
# sed -i 's/seistable\*/tabular/g' $1.tex
sed -i 's/\makeseistitle{/\makeseistitle\n{%/g' $1_copy.tex

# convert tex file to jats xml file
pandoc $1_copy.tex -f latex -t jats+element_citations --citeproc --bibliography=$2.bib --mathjax --metadata link-citations=true --natbib --csl apa.csl -s -o $1.xml

rm -rf $1_copy.tex

# extract tex metadata to jats metadata
python3 metatex2jats.py $1

# clean math formulas
perl -i -00pe 's/(<disp-formula>)[\S\n\t\v ]*?<alternatives>[\S\n\t\v ].*?(<tex-math)\>([\S\n\t\v ]*?)(\\label\{([\S\n\t\v ]*?)\}[\S\n\t\v ]*?<\/alternatives>)/$1$2 id="$5"\\>$3\]\]><\/tex-math>/rgmi' $1.xml

perl -i -00pe 's/(<inline-formula>)[\S\n\t\v ]*?<alternatives>[\S\n\t\v ].*?(<tex-math)\>([\S\n\t\v ]*?)((<\/tex-math>)([\S\n\t\v ]*?)[\S\n\t\v ]*?<\/alternatives>)/$1$2\>$3$5/gmi' $1.xml

# clean ids
python3 cleanidjats.py $1

# replace jats xml file metadata
sed -e '/<front>/,/<\/front>/!b' -e "/<\/front>/!d;r $1_metadata.jats" -e 'd' $1.xml > $1_galley.xml

# clean multiple abstracts in final 1_galley
perl -i -00pe 's/<boxed-text>\n\s*<boxed-text>/<boxed-text>/g' $1_galley.xml
perl -i -00pe 's/<\/boxed-text>\n\s*<\/boxed-text>/<\/boxed-text>/g' $1_galley.xml

# clean figures xref
perl -i -00pe 's/(fig(?:.{0,1}|[a-z]{0,1}).{0,3}<xref )/$1ref-type="fig" /ig' $1_galley.xml
for VAR in {1..20}
do
    perl -i -00pe "s/(fig(?:.{0,1}|[a-z]{0,1}.{0,3})(?:<xref .{10,50}<\/xref>(?s:.){1,10}){$VAR}<xref )/\1ref-type=\"fig\" /ig" $1_galley.xml
done

# clean/add figures extensions if not already there
perl -i -00pe "s/mime-subtype=\"pdf\"/mime-subtype=\"png\"/ig" $1_galley.xml
perl -i -00pe 's/xlink:href=\"([\S\n\t\v ]*?).pdf\"/xlink:href=\"$1.png\"/ig' $1_galley.xml

# clean tables xref
perl -i -00pe 's/(tab(?:.{0,1}|[a-z]{0,1}).{0,3}<xref )/$1ref-type="table" /ig' $1_galley.xml
for VAR in {1..20}
do
    perl -i -00pe "s/(tab(?:.{0,1}|[a-z]{0,1}.{0,3})(?:<xref .{10,50}<\/xref>(?s:.){1,10}){$VAR}<xref )/\1ref-type=\"table\" /ig" $1_galley.xml
    perl -i -00pe "s/\[tbl{$VAR}\]/{$VAR}/ig" $1_galley.xml
done

# clean credits file
sed -i 's/\\&/&amp;/g' $1_credits.jats

# add credits as section in the galley file
sed -n -i -e "/<\/body>/r $1_credits.jats" -e 1x -e '2,${x;p}' -e '${x;p}' $1_galley.xml


#eof

