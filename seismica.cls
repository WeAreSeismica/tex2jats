% Documentclass seismica.cls

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{seismica}[2022 LaTeX2e document class]

\newif\if@review
\@reviewfalse
\DeclareOption{review}{\@reviewtrue}

\newif\if@onecolumn
\@onecolumnfalse
\DeclareOption{onecolumn}{\@onecolumntrue}

\newif\if@fastreport
\@fastreportfalse
\DeclareOption{fastreport}{\@fastreporttrue}

\newif\if@breakmath
\@breakmathfalse
\DeclareOption{breakmath}{\@breakmathtrue}

\newif\if@luatex
\@luatexfalse
\DeclareOption{luatex}{\@luatextrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\if@review
\@onecolumntrue
\fi

\if@onecolumn
\LoadClass[10pt,twoside,a4paper,onecolumn]{article}
\else
\LoadClass[10pt,twoside,a4paper,twocolumn]{article}
\fi

\RequirePackage[headsep=0.7cm,top=2cm,bottom=1.5cm,left=1.5cm,right=1.5cm,footskip=0.7cm]{geometry}
\setlength{\columnsep}{0.8cm}
\RequirePackage[table]{xcolor}
\definecolor{seismicacolor1light}{RGB}{38,81,143}
\definecolor{seismicacolor1}{RGB}{18,52,103}
\definecolor{seismicacolor2}{RGB}{77,185,123}
\definecolor{seismicacolor3}{RGB}{222,60,75}
\RequirePackage[unicode,
				bookmarks=true,
				linkcolor=seismicacolor1light,
				citecolor=seismicacolor1light,
				hidelinks,
				hyperfootnotes=false]{hyperref}
\hypersetup{colorlinks,linkcolor=seismicacolor1light}
\hypersetup{colorlinks,citecolor=seismicacolor1light}
\hypersetup{colorlinks,urlcolor=gray}
%\RequirePackage[natbibapa,sectionbib,doi]{apacite}
%\bibliographystyle{apacite}
\RequirePackage[round]{natbib}
\bibliographystyle{plainnat}
\RequirePackage{doi}
\RequirePackage{polyglossia}
\RequirePackage{fontspec}
\setmainlanguage[]{english}
\RequirePackage{graphicx}
\RequirePackage{titlesec}
\RequirePackage{titling}
\RequirePackage{abstract}
\RequirePackage{fancyhdr}
\RequirePackage{bookmark}
\RequirePackage{caption} 
\RequirePackage{academicons}
\RequirePackage[noblocks]{authblk}
\setcounter{Maxaffil}{0}
\RequirePackage{adjustbox}
\RequirePackage[savepos]{zref}
\RequirePackage{datatool}
\RequirePackage{etoolbox}

% fonts and math
\RequirePackage{lmodern}
\RequirePackage[opentype,
				default,
				tabular,
				lining]{sourcesanspro}
\RequirePackage[opentype,
				default,
				tabular,
				lining]{sourceserifpro}
\RequirePackage{amsmath}
\if@breakmath
	\RequirePackage{breqn}
	\renewenvironment{equation}{%
		\begin{dmath}}{%
		\end{dmath}}
\else
	\RequirePackage{unicode-math} % in conflict with breqn
	\setmathfont{latinmodern-math.otf}
\fi

\RequirePackage{lineno} %% loaded here because incompatibility with breqn
\if@review
\linenumbers
\fi

\newcommand{\mathbfup}[1]{\mathord{\textnormal{\textbf{#1}}}}
\setmainfont{SourceSerifPro-Regular.otf}
\renewcommand{\sfdefault}{\sourcesanspro}
\renewcommand{\rmdefault}{\sourceserifpro}
\newcommand{\sflight}{\sourcesansprolight}
\newcommand{\rmlight}{\sourceserifprolight}

% Redefine thanks symbol for compatibility with fonts
\def\@fnsymbol#1{\ensuremath{\ifcase#1\or *\or \dagger\or \ddagger\or
		\mathsection\or \mathparagraph\or \|\or **\or \dagger\dagger
		\or \ddagger\ddagger \else\@ctrerr\fi}}
	
%-------------------------------------------------------------------------------
%                Configuration for authors
%-------------------------------------------------------------------------------

% package authblk
\renewcommand*{\Authsep}{, }
\renewcommand*{\Authand}{, }
\renewcommand*{\Authands}{, }
\renewcommand*{\Authfont}{\bfseries\sfdefault}    % make author names boldface    
\setlength{\affilsep}{0.2cm}   % set the space between author and affiliation
\renewcommand*{\Affilfont}{\normalfont\sflight\small}
\renewcommand\AB@affilsepx{, \protect\Affilfont}

% package academicons
\newcommand{\orcid}[1]{\href{https://orcid.org/#1}{\textcolor[HTML]{A6CE39}{\aiOrcid}}}

% Credit
\DTLgnewdb{credits}
\newcommand*{\credit}[2]{%
	\DTLnewrow{credits}%
	\DTLnewdbentry{credits}{credrole}{#1}%
	\DTLnewdbentry{credits}{credauthor}{#2}%
}

%-------------------------------------------------------------------------------
%                information box
%-------------------------------------------------------------------------------
\RequirePackage[absolute]{textpos}
\RequirePackage{longtable,booktabs,tabularx,colortbl}

% Article info
\def\receiveddate#1{\def\@receiveddate{#1}}
\def\accepteddate#1{\def\@accepteddate{#1}}
\def\publisheddate#1{\def\@publisheddate{#1}}
\def\thevolume#1{\def\@thevolume{#1}}
\def\thenumber#1{\def\@thenumber{#1}}
\thenumber{}
\def\theyear#1{\def\@theyear{#1}}

% Volunteers names
\def\editorname#1{\def\@editorname{#1}}
\editorname{}
\def\copyedname#1{\def\@copyedname{#1}}
\copyedname{}
\def\typesetname#1{\def\@typesetname{#1}}
\typesetname{}
\def\prodname#1{\def\@prodname{#1}}
\prodname{}

\newcommand{\@insert@metadata}{%
	\begin{textblock*}{3cm}[1,1](\dimexpr\textwidth-\oddsidemargin\relax,\dimexpr\paperheight-\zposy{loc:end_abstract}sp\relax)
		\footnotesize\raggedright%
		\setlength{\parskip}{\baselineskip}%
		\setlength{\parindent}{\z@}%
		\more@metadata\par
	\end{textblock*}
}

\newcommand{\printifnotempty}[4]{%
	\sbox0{#3}%
	\ifdim\wd0=0pt
	{}% if #3 is empty
	\else
	%	\begin{flushright}
	{\raggedleft\sflight \textcolor{gray}{#1: }{#2}\sfdefault \textcolor{gray}{#3}#4}% if #2 is not empty
	%	\end{flushright}
	\fi
}

\newcommand{\more@metadata}{%
	\printifnotempty{Edited by}{\\}{\@editorname}{\par}
	\printifnotempty{Received}{\\}{\@receiveddate}{\\}
	\printifnotempty{Accepted}{\\}{\@accepteddate}{\\}
	\printifnotempty{Published}{\\}{\@publisheddate}{\par}
	\printifnotempty{Typesetting by}{\\}{\@typesetname}{\\}
	\printifnotempty{Copy-editing by}{\\}{\@copyedname}{\\}
	\printifnotempty{Production by}{\\}{\@prodname}{\par}
}

%-------------------------------------------------------------------------------
%                Configuration for heading
%-------------------------------------------------------------------------------
% For credit
\newcommand{\printcreditifnotempty}{%
	\ifdim\DTLrowcount{credits}pt=0pt
	\else
	\vskip .5em
	\footnotesize\raggedright\sfdefault\textcolor{seismicacolor1}{Author contributions:} \DTLforeach*{credits}{\Credrole=credrole, \Credauthor=credauthor}{\textcolor{seismicacolor1}{ \sflight\textit{ \Credrole}: \Credauthor.} }
	\fi
}

\pretitle{
	\begin{flushleft}
		\fontsize{21pt}{1em}\bfseries\sfdefault
	}
	\posttitle{%
	\end{flushleft}%
	\vskip .2cm
}
\preauthor{%
	\lineskip 0.2cm%
	\begin{flushleft}
	}

\postauthor{%
	\end{flushleft}%
	\vskip -.5em
	\printcreditifnotempty
	\par
}
\predate{}
\postdate{}
\date{}

\if@fastreport
\newcommand{\banner}{banner_fast}
\else
\newcommand{\banner}{banner}
\fi

\def\doi#1{\def\@doi{#1}}
\doi{}


\renewcommand\maketitlehooka{%
	\vspace{-1.5cm}
	\includegraphics[width=\textwidth]{\banner}
	
	{\vspace*{-1.3cm} \hspace{0.2cm} 
		\href{https://doi.org/\@doi}{\sfdefault \color{white} \small doi:\@doi} }
	
	\vspace*{1.7cm}
}

\renewcommand\maketitlehookd{%
	\pagestyle{fancy}
	\thispagestyle{plain}
	\@insert@metadata
}

%-------------------------------------------------------------------------------
%                Configuration for asbtract
%-------------------------------------------------------------------------------

\newcommand*{\abstracttitlestyle}[1]{{\sfdefault \large \bfseries #1}}

\let\oldthanks\thanks
\renewcommand{\thanks}[1]{\oldthanks{\small \sflight #1}}

\newenvironment{summary}[1]
{
	%	\pdfbookmark{#1}{#1}
	\vspace{0.3cm}
	\par
	\noindent \abstracttitlestyle{#1} \hspace{0.2cm}
	\sfdefault 
}%
{
}

\if@onecolumn
\newcommand*{\makeseistitle}[1]{%
	\maketitle
	\begin{adjustbox}{minipage=0.68\paperwidth}
		#1
		\zsavepos{loc:end_abstract}
	\end{adjustbox}
	\vspace{1cm}
}
\else
\newcommand*{\makeseistitle}[1]{%
	\twocolumn[%
	\maketitle
	\begin{adjustbox}{minipage=0.68\paperwidth}
		#1
		\zsavepos{loc:end_abstract}
	\end{adjustbox}
	\vspace{1cm}
	]
	\saythanks
}
\fi

%-------------------------------------------------------------------------------
%                Configuration for sections
%-------------------------------------------------------------------------------

\titleformat{\section}{\fontsize{14pt}{1em}\bfseries\sfdefault}{\thesection}{1em}{}
%\titlespacing\section{0pt}{8pt plus 4pt minus 2pt}{6pt plus 2pt minus 2pt}
\titleformat{\subsection}{\fontsize{12pt}{0.3em}\bfseries\sfdefault}{\thesubsection}{1em}{}
%\titlespacing\subsection{0pt}{12pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}
\titleformat{\subsubsection}{\fontsize{11pt}{0.1em}\bfseries\sfdefault}{\thesubsubsection}{1em}{}
%\titlespacing\subsubsection{0pt}{8pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}

\if@fastreport
	\setcounter{secnumdepth}{0}
\else
	\setcounter{secnumdepth}{2}
\fi

%-------------------------------------------------------------------------------
%                Configuration for header and footer
%-------------------------------------------------------------------------------

\if@fastreport
\newcommand{\articletype}{\color{seismicacolor2}FAST REPORT}
\else
\newcommand{\articletype}{ARTICLE}
\fi

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\fancyfoot[L]{\sfdefault\bfseries\footnotesize \thepage}
\fancyfoot[R]{\sflight \footnotesize {\scshape \bfseries \color{seismicacolor1light} SEISMICA} | volume \@thevolume.\@thenumber  |  \@theyear}
\fancyhead[L]{\sflight \footnotesize {\scshape \bfseries \color{seismicacolor1light} SEISMICA} | {\scshape \bfseries \articletype} | \@title}
%\fancyhead[R]{\footnotesize \@author[1]}
\renewcommand{\headrule}{}

\fancypagestyle{plain}{%
	\fancyhead{}
	\renewcommand{\headrule}{}
}

%
%%-------------------------------------------------------------------------------
%%                Configuration for captions
%%-------------------------------------------------------------------------------

\captionsetup{font=sf, 
	labelfont=bf, 
	labelsep=quad, 
	justification=justified, 
	singlelinecheck=false, oneside}


% equations
\if@breakmath
\renewcommand{\eqnumcolor}{\color{gray}}
\renewcommand{\eqnumfont}{\sfdefault}
\else
\renewcommand{\eqref}[1]{\textup{\eqreftagform@{\ref{#1}}}}
\let\eqreftagform@\tagform@
\def\tagform@#1{%
	\maketag@@@{\color{gray}\sfdefault(\ignorespaces#1\unskip\@@italiccorr)}%
}
\fi

\renewcommand{\theequation}{\color{gray}\sfdefault\arabic{equation}}


%
%%-------------------------------------------------------------------------------
%%                Configuration for tables
%%-------------------------------------------------------------------------------
\def\thickhline{%
	\noalign{\ifnum0=`}\fi\color{gray}\hrule \@height \thickarrayrulewidth \futurelet
	\reserved@a\@xthickhline}
\def\@xthickhline{\ifx\reserved@a\thickhline
	\vskip\doublerulesep
	\vskip-\thickarrayrulewidth
	\fi
	\ifnum0=`{\fi}}


\newenvironment{seistable}[1][*{50}{l}]{%
	\setlength{\arrayrulewidth}{0.5pt}
	\newlength{\thickarrayrulewidth}
	\setlength{\thickarrayrulewidth}{1.5\arrayrulewidth}
	\arrayrulecolor{gray}
	\sflight\small
	\begin{center}
	\begin{tabular}{#1}\thickhline\rule{0pt}{2ex} }{%
		\thickhline\end{tabular}\end{center}\vspace*{-0.7cm}}

%%-------------------------------------------------------------------------------
%%                Configuration for footnotes
%%-------------------------------------------------------------------------------
\let\oldfootnote\footnote
\renewcommand{\footnote}[1]{\oldfootnote{\sflight #1}}
\renewcommand\footnoterule{{\color{lightgray}\rule{0.3\linewidth}{0.05pt}\vspace{0.15cm}}}

%%-------------------------------------------------------------------------------
%%                Configuration for references
%%-------------------------------------------------------------------------------

\setlength{\bibsep}{3pt} %espacement entre les references biblio
\renewcommand{\bibsection}{\section*{References}}
\def\bibfont{\small\sffamily}
\newcommand*{\doi}[1]{\href{http://doi.org/#1}{doi: #1}}

% end of seismica.cls 
