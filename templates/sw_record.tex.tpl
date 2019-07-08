{% raw %}
\documentclass[fleqn,14pt]{extarticle}
\usepackage{reportForm}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{fixltx2e}
\usepackage{graphicx}
\usepackage{longtable}
\usepackage{float}
%\usepackage{wrapfig}
\usepackage[normalem]{ulem}
\usepackage{textcomp}
\usepackage{marvosym}
\usepackage{wasysym}
\usepackage{latexsym}
\usepackage{amssymb}
\usepackage{amstext}
\usepackage{hyperref}
\usepackage{pxrubrica}

\tolerance=1000
\subtitle{({% endraw %}{{ Start }}$\sim${{ End }}{% raw %})}
\usepackage{strike}
\usepackage{setspace}
\setstretch{.95}
\setcounter{section}{0}
\author{{% endraw %}{{ Belongs }}{% raw %}\vspace{3mm}\\\ruby[Pm]{{% endraw %}{{ Familyname }}{% raw %}}{{% endraw %}{{ FamilynameRuby }}{% raw %}} \ruby[Pm]{{% endraw %}{{ Givenname }}{% raw %}}{{% endraw %}{{ GivennameRuby }}{% raw %}}}{% endraw %}
{% raw %}
\date{{% endraw %}{{ Name }}{% raw %}}
{% endraw %}
{% raw %}
\title{記録書　No.{% endraw %}{{ Number }}{% raw %}}
{% endraw %}
{% raw %}
\hypersetup{
  pdfkeywords={},
  pdfsubject={},
  pdfcreator={Emacs 24.4.1 (Org mode 8.2.10)}}
\begin{document}
\maketitle

\section{実績}
\subsection{研究関連}
{% endraw %}

{% raw %}
\subsection{研究室関連}
\begin{enumerate}
{% endraw %}
{% for event in Calendars.Labo.events.prev %}
{{ event.fmt("\\item %SUMMARY\n\\hfill\n(%START)", "%-m/%-d") }}
{% endfor %}
{% raw %}
\end{enumerate}
{% endraw %}

{% raw %}
\subsection{大学院関連}
\begin{enumerate}
{% endraw %}
{% for event in Calendars.Univ.events.prev %}
{{ event.fmt("\\item %SUMMARY\n\\hfill\n(%START)", "%-m/%-d") }}
{% endfor %}
{% raw %}
\end{enumerate}
{% endraw %}

{% raw %}
\section{詳細および反省・感想}
{% endraw %}

{% raw %}
\section{今後の予定}
\subsection{研究関連}
{% endraw %}

{% raw %}
\subsection{研究室関連}
\begin{enumerate}
{% endraw %}
{% for event in Calendars.Labo.events.next %}
{{ event.fmt("\\item %SUMMARY\n\\hfill\n(%START)", "%-m/%-d") }}
{% endfor %}
{% raw %}
\end{enumerate}
{% endraw %}

{% raw %}
\subsection{大学院関連}
\begin{enumerate}
{% endraw %}
{% for event in Calendars.Univ.events.next %}
{{ event.fmt("\\item %SUMMARY\n\\hfill\n(%START)", "%-m/%-d") }}
{% endfor %}
{% raw %}
\end{enumerate}
{% endraw %}

{% raw %}
\end{document}
{% endraw %}