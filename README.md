# TeX 2 JATS XML for Seismica

## Introduction
There are two options to run the scripts. There's a docker-based setup that only requires installation of Docker and automatically manages all other dependencies. The other option is to install the dependencies and run the shell script that calls the python files to perform the conversions.

Follow the steps in the following order - 
1. [Base Requirements for installation](#base-requirements)
2. [Pre-conversion Requirements](#pre--conversion-requirements)
3. Workflow [Docker Option](#workflow-option-1---using-docker) or [Dependencies Option](#workflow-option-2---installing-dependencies)
4. [Post-conversion checks](#post--conversion-checks)

## Base Requirements
1. Clone the github repo to your local machine. `cd` into the desired directory and clone using - 
    ```
    git clone https://github.com/WeAreSeismica/tex2jats.git
    ```

## Pre-conversion requirements
Before running the TeX2JATS converter, you need to:
1. Have produced final `.tex` galleys with updated metadata (proof accepted by authors)
2. Remove tilde (~) from authors name in `.tex` file, check that date format is correct (Month dd, YYYY)
3. Convert every figure to PNG format if not already done. You can use the following bash command (converts every PDF file which starts with fig to a PNG format, requires imagemagick, you can adjust density if needed):  
`mogrify -verbose -quality 00 -density 250  -format png ./fig*.pdf`


## Workflow Option 1 - Using Docker
1. Install [Docker](https://www.docker.com/) if you don't have it already.

1. Start up Docker. Usually you will have an application called "Docker" on your computer with a rudimentary graphical user interface (GUI). You can also run this command in the command-line interface (CLI):
    ```
    open -a Docker
    ```

1. Move the directory containing latex files to be converted into the git repo `tex2jats`.

1. Open the file `env.set`, and edit the parameters in the file as mentioned there. Spaces in names are accepted.

1. Open a shell and navigate to the wherever the git repo is cloned, which now includes the latex files directory.
    ```
    cd path/to/git/repo/tex2jats
    ```
    You can always run `pwd` to check whether you're in the right place.

1. Run docker-compose by entering the below commands in your favorite shell.
    ```
    docker-compose up -d
    ```

1. This should convert and create all the necessary files. Conversion may take up to a minute. You can check the status of the conversion by using - 
    ```
    docker-compose logs
    ```
    Verify that there are `xml` files in the latex files directory. 

1. Shut down docker-compose by entering - 
    ```
    docker-compose down
    ```

## Workflow Option 2 - Installing Dependencies

### Dependencies
These ones are shared dependencies with the [docx/odt parsing for Seismica module](https://github.com/WeAreSeismica/seismica-sce):
- python 3.n (preferably 3.8+)
- numpy
- pandoc

Other dependencies:
- python3 datetime (often already installed)
- GNU sed, v4.8
- perl, v>5 (below not tested)

### Option 2 Instructions
1. Copy tex2xml.sh, apa.csl, cleanidjats.py and metatex2jats.py to your current working directory (CWD, where the TeX galley is):  
`cd /cwd/`  
`cp /path/to/tex2jats/tex2xml.sh ./`  
`cp /path/to/tex2jats/*.py ./`  
`cp  /path/to/tex2jats/apa.csl ./`  

1. In your CWD, use tex2xml.sh to convert the TeX to JATS XML:  
`./tex2xml.sh proof biblio`  
with:  
    - `proof`, the name of the TeX galley without the extension (which should be .tex)
    - `biblio`, the name of the corrected list of references, without the extension (which should be .bib)

## Post conversion checks

1. Either of the workflows above will output the following files within the latex directory:
    - `proof.xml`  
    - `proof_metadata.jats`  
    - `proof_credits.jats`
    - `proof_galley.xml`
    - `proof_tab1.tex` if you have one table (see point (5)), and one similar file per table
    - `proof_tab1.xml`   
You will then work with the XML galley only (`proof_galley.xml`). Other files are only here for correction if needed.

### Initial checks (with a text editor)

1. Open the galley with a web browser, it **should not show any error**. You can use the web browser to debug (will show the line of every error).

3. Correct metadata if needed: Authors' names, affiliations, DOI, title, and other metadata.

4. Cross references for figures (xref) look OK. They should be printed with a format similar to:  
    `<xref ref-type="fig" alt="1" rid="fig1"&gt;1&lt;/xref>`

4. If there are **TABLES** in your TeX galley, tex2xml.sh will export two files for each table: tabxx.tex and tabxx.xml, xx ranging from 1 to the total number of arrays present in the article.  

**If the table is simple and has been converted properly by pandoc:**  
    1.  Copy the HTML header code in the XML table file `tabxx.xml`, where indicated
    1.  Replace the wrong table header in the XML galley `proof_galley.xml` with the header from `tabxx.xml`. In the XML galley, tables are under a `boxed-text` environnement, that you can remove.
    2.  
**If the table is too complex and has not been properly converted:**  
    1.  Correct any unwanted symbol in `tabxx.tex`
    2.  Translate the `tabxx.tex` to HTML with https://tableconvert.com/latex-to-html
    3.  Copy the HTML code  in the XML table file `tabxx.xml`, where indicated
    4.  Replace the wrong table code in the XML galley `proof_galley.xml` with the updated `tabxx.xml`. In the XML galley, tables are under a `boxed-text` environnement.

1. Check the acknowledgements and references

### Final checks (with the OJS preview tool)

1. Upload the XML galley to the OJS website. 
    - You can rename the XML galley 
    - Images need to be uploaded separately (no need to fill in the caption etc.)
    - Use the preview tool to open the XML Lens Viewer
2. Check that title, authors, and all metadata are printed correctly (in the main text page but also the `info` tab)
3. Cross references to figures and tables and references are OK
4. Tables are printed correctly
5. Acknowledgements are printed correctly
6. References (in the `References` tab) are printed correctly. *Note: there is a known issue with misc references that are not printed, we are working on that.*

### Known issues:
- Maths formula in captions or tables are often not converted properly
- Often in metadata, credits or acknowledgements: symbols are not properly converted, or are still escaped when they shouldn't: look for \\&, \\%,

## TO DO
- Don't use regex, because it is unstable with XML? Oops…
- Correctly parse math expressions within tables
