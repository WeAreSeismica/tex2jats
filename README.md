# TeX 2 JATS XML for Seismica


## Dependencies
These ones are shared dependencies with the [docx/odt parsing for Seismica module](https://github.com/WeAreSeismica/seismica-sce):
- python 3.n (preferably 3.8+)
- numpy
- pandoc

Other dependencies:
- python3 datetime (often already installed)
- GNU sed, v4.8
- perl, v>5 (below not tested)


## SCE requirements
Before running the TeX2JATS converter, you need to have produced:
- final .tex galleys (proof accepted by authors)
- corrected list of references
- have the final metadata on hand (you can replace it in the JATS galley)


## Workflow
1) Copy tex2xml.sh, apa.csl, cleanidjats.py and metatex2jats.py to your current working directory (CWD, where the TeX galley is):
`cd /cwd/`  
`cp /path/to/tex2jats/tex2xml.sh ./`  
`cp /path/to/tex2jats/\*.py ./`  
`cp  /path/to/tex2jats/apa.csl ./`  

2) In your CWD, use tex2xml.sh to convert the TeX to JATS XML:
`./tex2xml.sh proof biblio`
with:
- `proof`, the name of the TeX galley without the extension (which should be .tex)
- `biblio`, the name of the corrected list of references, without the extension (which should be .bib)

3) If there are **TABLES** in your TeX galley, tex2xml.sh will export two files for each table: tabxx.tex and tabxx.xml.
For each table:
- replace the wrong table code in the galley XML by tabxx.xml
- translate the tabxx.tex to HTML with https://tableconvert.com/latex-to-html
- copy the HTML code in the XML galley

4) Proofread XML galley and add metadata if necessary

5) Upload the galley PDF and XML files to the OJS website. 
- For the XML galley, images need to be uploaded separately (no need to fill in the caption etc.)
- Don't forget the uploading order:
    1) PDF galley
    2) XML galley
    3) Supplementary Materials (any)
    4) Review reports

