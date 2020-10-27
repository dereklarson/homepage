%% Intro Options
\ProvidesClass{resume}[2020/10/21 resume]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{
  \PassOptionsToClass{\CurrentOption}{article}%
}
\ProcessOptions\relax
\LoadClass{article}

%% Package Imports
\usepackage[hmargin=1.25cm, vmargin=0.7cm]{geometry}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{titlesec}
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{babel}
\usepackage[UKenglish]{isodate}
\usepackage{fontspec,xltxtra,xunicode}
\usepackage{enumitem}                         % More itemize options
\usepackage{fontspec}
% From https://tex.stackexchange.com/questions/132888/fontawesome-font-not-found
% Make sure to change the year if needed
\defaultfontfeatures{Path = /usr/local/texlive/2020/texmf-dist/fonts/opentype/public/fontawesome/}
\usepackage{fontawesome}                      % Adds many icons
\usepackage[hidelinks]{hyperref}
\usepackage{amssymb}
\usepackage{stackengine}
\usepackage{scalerel}
\usepackage{xcolor}
\usepackage{graphicx}

%% Cite publications
\usepackage{cite}
\renewcommand\refname{\vskip -1.5cm}

%% Color definitions for the themes
% Dark
\definecolor{dark_page}{HTML}{020c1b}              % Dark backgound
\definecolor{dark_date}{HTML}{a8b2d1}              % light-slate
\definecolor{dark_primary}{HTML}{ccd6f6}           % lightest slate
\definecolor{dark_heading}{HTML}{2196f3}           % Primary color is based on theme (blue)
\definecolor{dark_subheading}{HTML}{e6f1ff}        % white
% Light
\definecolor{light_page}{HTML}{ffffff}             % White backgound
\definecolor{light_date}{HTML}{666666}             % 
\definecolor{light_primary}{HTML}{2b2b2b}          % 
\definecolor{light_heading}{HTML}{6a6a6a}          % 
\definecolor{light_subheading}{HTML}{333333}       % 

{% for color in ['page', 'date', 'primary', 'heading', 'subheading'] %}
\colorlet{{"{"}}{{ color }}{{"}"}}{{"{"}}{{ theme }}_{{ color }}{{"}"}}
{% endfor %}
\pagecolor{page}

{% raw %}
%% Set main fonts
\defaultfontfeatures{Mapping=tex-text}
\setmainfont[Color=primary]{Helvetica Light}
\setsansfont[Scale=MatchLowercase,Mapping=tex-text]{Helvetica Neue UltraLight}

%% Add link icon to hyperlinks
\let\orighref\href
\renewcommand{\href}[2]{\orighref{#1}{#2\,\faExternalLink}}

%% Header details: last updated printable (light themed) version of resume link
% Args are left position and text to display
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\textblockorigin{0mm}{5mm}
\newcommand{\headerdetail}[2]{\begin{textblock}{60}(#1,0)
\color{date}\fontspec{Helvetica Neue Light}\fontsize{8pt}{10pt}\selectfont 
#2
\end{textblock}}

%% Name command
\newcommand{\namesection}[2]{
	\centering{
		\sffamily
		\fontspec{Helvetica Neue Light}\fontsize{40pt}{10cm}\selectfont #1 
	} \\
	\vspace{5pt}
	\centering{ \color{heading}\fontspec{Heiti TC Medium}\fontsize{11pt}{14pt}\selectfont #2}
	\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}
	\vspace{-15pt}
}
\titlespacing{\section}{0pt}{0pt}{0pt}

%% Headings command
\titleformat{\section}{
	\color{heading}\scshape\fontspec{Helvetica Light}
	\fontsize{16pt}{24pt}\selectfont \raggedright\uppercase}{}{0em}{}

%% Subheadings command
\titleformat{\subsection}{
	\color{subheading}
	\fontspec{Helvetica}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase}{}{0em}{}
\titlespacing{\subsection}{0pt}{\parskip}{-\parskip}
\titlespacing{\subsubsection}{0pt}{\parskip}{-\parskip}
\newcommand{\runsubsection}[1]{
	\color{subheading}\fontspec{Helvetica}
	\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase {#1} \normalfont}

%% Descriptors command
\newcommand{\descript}[1]{\color{subheading}\raggedright\scshape\fontspec{Heiti SC Medium}\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

%% Location command
\newcommand{\location}[1]{\color{heading}\raggedright\scshape\fontspec{Heiti TC Medium}\fontsize{10pt}{12pt}\selectfont {#1\\} \normalfont}

%% Section seperators command
\newcommand{\sectionsep}[0]{\vspace{8pt}}

%% Bullet Lists with fewer gaps command
\newenvironment{tightemize}[1]{
 	\begin{itemize}[leftmargin=#1, topsep=2pt, parsep=0pt, itemsep=0pt, partopsep=0pt]
	}{\end{itemize}}

{% endraw %}
