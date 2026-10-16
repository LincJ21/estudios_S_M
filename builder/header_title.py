# -*- coding: utf-8 -*-

def get_header_and_title():
    return r"""\documentclass[11pt,a4paper]{article}

%================================================
% PAQUETES
%================================================
\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{float}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc,patterns}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{eurosym}
\usepackage{hyperref}

\geometry{margin=2.2cm}
\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}

%================================================
% CONFIGURACIÓN DE LISTINGS (CÓDIGO FUENTE PYTHON)
%================================================
\definecolor{codegreen}{rgb}{0,0.55,0}
\definecolor{codegray}{rgb}{0.45,0.45,0.45}
\definecolor{codepurple}{rgb}{0.55,0,0.8}
\definecolor{backcolour}{rgb}{0.97,0.97,0.98}
\definecolor{codeblue}{rgb}{0.1,0.2,0.7}
\definecolor{utbblue}{rgb}{0.0,0.25,0.5}

\lstset{
    backgroundcolor=\color{backcolour},
    basicstyle=\ttfamily\scriptsize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    commentstyle=\color{codegreen},
    keywordstyle=\color{codeblue}\bfseries,
    stringstyle=\color{codepurple},
    numbers=left,
    numbersep=7pt,
    numberstyle=\tiny\color{codegray},
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    stepnumber=1,
    tabsize=4,
    frame=single,
    rulecolor=\color{gray!30},
    keepspaces=true,
    inputencoding=utf8,
    extendedchars=true,
    literate=
        {á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
        {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
        {ñ}{{\~n}}1 {Ñ}{{\~N}}1 {¡}{{!`}}1 {ő}{{\H{o}}}1
        {Δ}{{$\Delta$}}1 {θ}{{$\theta$}}1 {λ}{{$\lambda$}}1
        {•}{{$\bullet$}}1 {→}{{$\to$}}1 {≥}{{$\ge$}}1 {≤}{{$\le$}}1
        {€}{{\euro}}1
}

%================================================
% CONFIGURACIÓN DE ENCABEZADOS Y PIES DE PÁGINA
%================================================
\pagestyle{fancy}
\fancyhf{}
\lhead{\footnotesize \textbf{Universidad Tecnológica de Bolívar} -- Facultad de Ingeniería}
\rhead{\footnotesize \textbf{Sistemas y Modelos} -- Cuaderno de Apuntes Digital}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}

\hypersetup{
    colorlinks=true,
    linkcolor=utbblue,
    citecolor=utbblue,
    urlcolor=utbblue
}

\begin{document}

%================================================
% PORTADA INSTITUCIONAL
%================================================
\begin{titlepage}
    \thispagestyle{empty}
    
    \begin{tikzpicture}[remember picture, overlay]
        \node[anchor=north west, opacity=0.4] at ([xshift=2.2cm, yshift=-1.2cm]current page.north west) {
            \includegraphics[width=3.5cm]{logo_utb.png}
        };
        \node[anchor=north east, opacity=0.4] at ([xshift=-2.2cm, yshift=-1.2cm]current page.north east) {
            \includegraphics[width=4cm]{trans_digital.png}
        };
    \end{tikzpicture}

    \vspace*{2.0cm}

    \begin{center}
        {\Large \textbf{UNIVERSIDAD TECNOLÓGICA DE BOLÍVAR}}\\[1.0cm]

        {\large FACULTAD DE INGENIERÍA}\\[0.2cm]
        {\large \textbf{SISTEMAS Y MODELOS}}\\[0.8cm]
        {\Large \textbf{CUADERNO DE APUNTES DIGITAL}}\\[0.4cm]
        {\large \textbf{ACTIVIDAD PRÁCTICA INTEGRAL DE OPTIMIZACIÓN LINEAL Y REDES}}\\[1.2cm]
        
        \textbf{ESTRUCTURA TEMÁTICA DEL CUADERNO:}\\[0.2cm]
        {\footnotesize 1. Parcial 1 y Casos Especiales de Programación Lineal (Gráfico y Simplex Tabular)}\\
        {\footnotesize 2. Solución de Problemas de PL con phpSimplex (Branch and Bound)}\\
        {\footnotesize 3. Solución de Problemas de PL con Python PuLP (Branch and Cut)}\\
        {\footnotesize 4. Problema de Transporte Balanceado y No Balanceado (Simplex Tradicional)}\\
        {\footnotesize 5. Problema de Transporte (Simplex Tradicional Mejorado: Vogel, MODI y Stepping Stone)}\\
        {\footnotesize 6. Problema de Asignación Biyectiva (Simplex Tradicional Binario)}\\
        {\footnotesize 7. Problema de Asignación Biyectiva (Simplex Mejorado: Algoritmo Húngaro)}\\[1.2cm]
        
        \textbf{INTEGRANTES DEL GRUPO:}\\[0.3cm]
        Fredy Jarava Chavez -- T00064995\\
        Josué Torres Torres -- T000\\
        Héctor Cabarcas Cuadrado -- T00067602\\
        Juan Romero -- T000\\[1.2cm]

        \textbf{PROFESOR:}\\[0.3cm]
        Isaac Zúñiga Silgado\\[1.0cm]

        \textbf{Cartagena de Indias, Colombia}\\
        2026
    \end{center}
\end{titlepage}

\newpage
\tableofcontents
\newpage
\setcounter{page}{1}
"""

