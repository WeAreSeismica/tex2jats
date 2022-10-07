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
- check that the dates format is correct (Month dd, YYYY)


## Workflow
1) Copy tex2xml.sh, apa.csl, cleanidjats.py and metatex2jats.py to your current working directory (CWD, where the TeX galley is):  
`cd /cwd/`  
`cp /path/to/tex2jats/tex2xml.sh ./`  
`cp /path/to/tex2jats/*.py ./`  
`cp  /path/to/tex2jats/apa.csl ./`  

2) In your CWD, use tex2xml.sh to convert the TeX to JATS XML:  
`./tex2xml.sh proof biblio`  
with:  
    - `proof`, the name of the TeX galley without the extension (which should be .tex)
    - `biblio`, the name of the corrected list of references, without the extension (which should be .bib)

3) This will output:
- `proof.xml`  
- `proof_metadata.jats`  
- `proof_credits.jats`
- `proof_galley.xml`
- `proof_tab1.tex` if you have one table (see point (5)), and one similar file per table
- `proof_tab1.xml`  
You will then work with the XML galley only (`proof_galley.xml`). Other files are only here for correction if needed.

4) How to view the XML galley? To my knowledge, there is no open-source and easy-to-use tool, so the best way is to open it with a text editor. You will be able to view the galley before publishing on OJS. If you open it with a web browser, it will show something ugly (JATS XML differs from web XML).

5) If there are **TABLES** in your TeX galley, tex2xml.sh will export two files for each table: tabxx.tex and tabxx.xml, xx ranging from 1 to the total number of arrays present in the article.  
For each table:  
    1)  Correct any unwanted symbol in `tabxx.tex`
    2)  Translate the `tabxx.tex` to HTML with https://tableconvert.com/latex-to-html
    3)  Copy the HTML code  in the XML table file `tabxx.xml`, where indicated
    4)  Replace the wrong table code in the XML galley `proof_galley.xml` with the updated `tabxx.xml`. In the XML galley, tables are under a `boxed-text` environnement.

6) Proofread XML galley and add metadata if necessary. Some things to check by visual inspection of the XML galley:
- Metadata, author names, credits, affiliations are here
- Abstracts are here
- Reference list is here
- Every figure is here 

7) Upload the galley PDF and XML files to the OJS website. 
- For the XML galley, images need to be uploaded separately (no need to fill in the caption etc.)
- Don't forget the uploading order:
    1) PDF galley
    2) XML galley
    3) Supplementary Materials (any)
    4) Review reports

## TO DO
- Don't use regex, because it is unstable with XML? Oops...