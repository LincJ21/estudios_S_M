import os

with open('01/01.py', 'r', encoding='utf-8') as f:
    code_01 = f.read()

with open('02/02.py', 'r', encoding='utf-8') as f:
    code_02 = f.read()

latex_content = r"""\documentclass[12pt,a4paper]{article}

%================================================
% PAQUETES
%================================================
\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{array}
\usepackage{float}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{tikz}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{hyperref}

\geometry{margin=2.5cm}
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
        {ñ}{{\~n}}1 {Ñ}{{\~N}}1
        {Δ}{{$\Delta$}}1 {θ}{{$\theta$}}1 {λ}{{$\lambda$}}1
        {•}{{$\bullet$}}1 {→}{{$\to$}}1 {≥}{{$\ge$}}1 {≤}{{$\le$}}1
}

%================================================
% CONFIGURACIÓN DE ENCABEZADOS Y PIES DE PÁGINA
%================================================
\pagestyle{fancy}
\fancyhf{}
\lhead{\footnotesize Universidad Tecnológica de Bolívar}
\rhead{\footnotesize Sistemas y Modelos - Taller de Optimización}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    citecolor=blue!70!black,
    urlcolor=blue!70!black
}

\begin{document}

%================================================
% PORTADA INSTITUCIONAL
%================================================
\begin{titlepage}
    \thispagestyle{empty}
    
    \begin{tikzpicture}[remember picture, overlay]
        \node[anchor=north west, opacity=0.4] at ([xshift=2.5cm, yshift=-1.2cm]current page.north west) {
            \includegraphics[width=3.5cm]{logo_utb.png}
        };
        \node[anchor=north east, opacity=0.4] at ([xshift=-2.5cm, yshift=-1.2cm]current page.north east) {
            \includegraphics[width=4cm]{trans_digital.png}
        };
    \end{tikzpicture}

    \vspace*{2.2cm}

    \begin{center}
        {\Large \textbf{UNIVERSIDAD TECNOLÓGICA DE BOLÍVAR}}\\[1.5cm]

        {\large FACULTAD DE INGENIERÍA}\\[0.3cm]
        {\large \textbf{SISTEMAS Y MODELOS}}\\[0.8cm]
        {\Large \textbf{TALLER PRÁCTICO INTEGRAL DE OPTIMIZACIÓN}}\\[1.5cm]
        
        {\small 1. Problemas de Transporte Balanceado y No Balanceado (Casos Didácticos)}\\[0.1cm]
        {\small 2. Caso de Estudio Avanzado de Transporte: Red Logística 3x3 (Código 01.py)}\\[0.1cm]
        {\small 3. Problema de Asignación Biyectiva: Mantenimiento Preventivo (Código 02.py)}\\[0.1cm]
        {\small 4. Programación Lineal de Enteros mediante Ramificación y Acotación (phpSimplex y PuLP)}\\[1.8cm]
        
        \textbf{INTEGRANTES:}\\[0.4cm]
        Fredy Jarava Chavez -- T00064995\\
        Josué Torres Torres -- T000\\
        Héctor Cabarcas Cuadrado -- T00067602\\
        Juan Romero -- T000\\[1.8cm]

        \textbf{PROFESOR:}\\[0.4cm]
        Isaac Zúñiga Silgado\\[1.2cm]

        \textbf{Cartagena de Indias, Colombia}\\
        2026
    \end{center}
\end{titlepage}

\newpage
\tableofcontents
\newpage
\setcounter{page}{1}

%================================================
\section{Problemas Didácticos de Transporte Eléctrico (125 MWh)}
%================================================

\subsection{Problema de transporte balanceado (125 MWh)}

\subsubsection{Enunciado y parámetros}
Una empresa energética dispone de tres plantas de generación para satisfacer la demanda de cuatro ciudades. Las plantas 1, 2 y 3 pueden suministrar 35, 50 y 40 millones de kWh, respectivamente ($\text{Oferta Total} = 125$). La demanda máxima requerida por las ciudades 1, 2, 3 y 4 es de 45, 20, 30 y 30 millones de kWh ($\text{Demanda Total} = 125$).

\begin{table}[H]
\centering
\caption{Costos unitarios de transporte (\$ por millón de kWh)}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{c|cccc|c}
\toprule
\textbf{Origen} & \textbf{Ciudad 1} & \textbf{Ciudad 2} & \textbf{Ciudad 3} & \textbf{Ciudad 4} & \textbf{Oferta ($S_i$)} \\
\midrule
Planta 1 & 8  & 6  & 10 & 9 & 35 \\
Planta 2 & 9  & 12 & 13 & 7 & 50 \\
Planta 3 & 14 & 9  & 16 & 5 & 40 \\
\midrule
\textbf{Demanda ($D_j$)} & 45 & 20 & 30 & 30 & \textbf{125} \\
\bottomrule
\end{tabular}
\end{table}

Dado que $\sum_{i=1}^3 S_i = \sum_{j=1}^4 D_j = 125$, el sistema está en equilibrio estricto.

\subsubsection{Modelo matemático y código en Python (PuLP)}
Sea $x_{ij} \geq 0$ la energía enviada desde la planta $i$ hacia la ciudad $j$. El modelo formal se expresa como:
\[
\min Z = \sum_{i=1}^3 \sum_{j=1}^4 c_{ij} x_{ij}
\]
sujeto a:
\[
\sum_{j=1}^4 x_{ij} = S_i \quad (i=1,2,3), \qquad \sum_{i=1}^3 x_{ij} = D_j \quad (j=1,2,3,4), \qquad x_{ij} \geq 0.
\]

\begin{lstlisting}[language=Python, caption={Script PuLP para Transporte Balanceado Didáctico}]
import pulp

plantas = ["Planta 1", "Planta 2", "Planta 3"]
ciudades = ["Ciudad 1", "Ciudad 2", "Ciudad 3", "Ciudad 4"]
oferta = {"Planta 1": 35, "Planta 2": 50, "Planta 3": 40}
demanda = {"Ciudad 1": 45, "Ciudad 2": 20, "Ciudad 3": 30, "Ciudad 4": 30}
costos = {
    ("Planta 1", "Ciudad 1"): 8,  ("Planta 1", "Ciudad 2"): 6,  ("Planta 1", "Ciudad 3"): 10, ("Planta 1", "Ciudad 4"): 9,
    ("Planta 2", "Ciudad 1"): 9,  ("Planta 2", "Ciudad 2"): 12, ("Planta 2", "Ciudad 3"): 13, ("Planta 2", "Ciudad 4"): 7,
    ("Planta 3", "Ciudad 1"): 14, ("Planta 3", "Ciudad 2"): 9,  ("Planta 3", "Ciudad 3"): 16, ("Planta 3", "Ciudad 4"): 5
}

modelo = pulp.LpProblem("Transporte_Balanceado", pulp.LpMinimize)
x = pulp.LpVariable.dicts("Flujo", ((i, j) for i in plantas for j in ciudades), lowBound=0)

modelo += pulp.lpSum(costos[(i, j)] * x[(i, j)] for i in plantas for j in ciudades)
for i in plantas:
    modelo += pulp.lpSum(x[(i, j)] for j in ciudades) == oferta[i]
for j in ciudades:
    modelo += pulp.lpSum(x[(i, j)] for i in plantas) == demanda[j]

modelo.solve(pulp.PULP_CBC_CMD(msg=False))
print(f"Costo Minimo: ${pulp.value(modelo.objective):,.2f}")
\end{lstlisting}

\subsubsection{Resultados óptimos}
La solución óptima entrega un costo mínimo de $\mathbf{Z^* = \$1.020}$, con el siguiente despacho:
Planta 1 $\to$ Ciudad 2: 10, Ciudad 3: 25. Planta 2 $\to$ Ciudad 1: 45, Ciudad 3: 5. Planta 3 $\to$ Ciudad 2: 10, Ciudad 4: 30.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{balanceado.png}
    \caption{Evidencia de resolución de transporte balanceado en Python PuLP.}
    \label{fig:pulp_balanceado}
\end{figure}

\subsection{Problema de transporte no balanceado (Excedente de 5 MWh)}

\subsubsection{Enunciado y balanceo mediante destino artificial}
La demanda de la Ciudad 1 disminuye a 40 millones de kWh, mientras las demás demandas se mantienen invariables ($\sum D_j = 120$). Como la oferta total es 125, se presenta un excedente de 5 millones de kWh. Para equilibrar el modelo, se agrega una **Ciudad 5 (Destino Artificial o Dummy)** con demanda $D_5 = 5$ y costos unitarios nulos ($c_{15} = c_{25} = c_{35} = 0$), representando capacidad ociosa retenida en las plantas generadoras.

\begin{table}[H]
\centering
\caption{Tabla balanceada con destino artificial (Ciudad 5)}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{c|ccccc|c}
\toprule
\textbf{Origen} & \textbf{Ciudad 1} & \textbf{Ciudad 2} & \textbf{Ciudad 3} & \textbf{Ciudad 4} & \textbf{Ciudad 5 (Dummy)} & \textbf{Oferta} \\
\midrule
Planta 1 & 8  & 6  & 10 & 9 & \textbf{0} & 35 \\
Planta 2 & 9  & 12 & 13 & 7 & \textbf{0} & 50 \\
Planta 3 & 14 & 9  & 16 & 5 & \textbf{0} & 40 \\
\midrule
\textbf{Demanda} & 40 & 20 & 30 & 30 & \textbf{5} & \textbf{125} \\
\bottomrule
\end{tabular}
\end{table}

\subsubsection{Resultados y análisis de la capacidad ociosa}
El costo mínimo resultante es $\mathbf{Z^* = \$975}$ (ahorro de $\$45$ respecto al caso balanceado). El destino ficticio absorbe 5 unidades procedentes de la **Planta 2** ($x_{25} = 5$). Esto es económicamente lógico: la Planta 2 abastecía a la Ciudad 1 a un costo de \$9/unidad. Al requerir la Ciudad 1 exactamente 5 unidades menos, el sistema optimizador retiene la generación en la Planta 2, ahorrando exactamente $5 \times \$9 = \$45$.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{No_balanceado.png}
    \caption{Evidencia de resolución de transporte no balanceado en Python PuLP.}
    \label{fig:pulp_no_balanceado}
\end{figure}

%================================================
\newpage
\section{Caso de Estudio Avanzado de Transporte: Red Logística 3x3 (Código 01.py)}
%================================================

\subsection{Enunciado del problema de transporte 3x3}

Una corporación manufacturera dispone de tres plantas de producción ($P_1, P_2, P_3$) y debe abastecer la demanda de tres almacenes regionales de distribución ($W_1, W_2, W_3$). El objetivo es determinar el plan de envíos óptimo que minimice el costo total de flete:

\begin{itemize}
    \item \textbf{Capacidades de oferta:} Planta 1: 300 unidades; Planta 2: 500 unidades; Planta 3: 100 unidades ($\text{Oferta Total} = 900$).
    \item \textbf{Requerimientos de demanda:} Almacén 1: 200 unidades; Almacén 2: 400 unidades; Almacén 3: 300 unidades ($\text{Demanda Total} = 900$).
\end{itemize}

\begin{table}[H]
\centering
\caption{Matriz de costos unitarios de transporte (\$ por unidad)}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lccc|c}
\toprule
\textbf{Planta / Almacén} & \textbf{Almacén 1 ($W_1$)} & \textbf{Almacén 2 ($W_2$)} & \textbf{Almacén 3 ($W_3$)} & \textbf{Oferta ($s_i$)} \\
\midrule
\textbf{Planta 1 ($P_1$)} & \$20 & \$16 & \$24 & \textbf{300} \\
\textbf{Planta 2 ($P_2$)} & \$10 & \$10 & \$8  & \textbf{500} \\
\textbf{Planta 3 ($P_3$)} & \$12 & \$18 & \$10 & \textbf{100} \\
\midrule
\textbf{Demanda ($d_j$)}   & \textbf{200} & \textbf{400} & \textbf{300} & \textbf{900} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Clasificación de los métodos canónicos en el código 01.py}

En el script \texttt{01.py}, el problema se aborda contrastando formalmente tres metodologías canónicas de la Investigación de Operaciones:

\begin{enumerate}
    \item \textbf{Método Balanceado:} Verifica la condición estricta de equilibrio $\sum s_i = \sum d_j = 900$. El script implementa la función \texttt{verificar\_y\_balancear\_transporte}, la cual detecta discrepancias de flujo e incorpora automáticamente filas o columnas ficticias con costos cero cuando el problema es desbalanceado, asegurando la existencia de una base acíclica factible.
    \item \textbf{Simplex Tradicional (Programación Lineal Tabular):} Modela algebraicamente el problema como $\min c^T x$ sujeto a $A x = b, x \ge 0$, donde la matriz $A$ posee dimensiones $(m+n) \times (m \cdot n)$ ($6 \times 9 = 54$ coeficientes) y rango $m+n-1 = 5$. Resuelve el sistema mediante inversión de base y operaciones elementales de Gauss-Jordan utilizando la librería PuLP con el motor HiGHS.
    \item \textbf{Método Normal (Simplex de Transporte Especializado):} Aprovecha la propiedad de que toda base no degenerada corresponde a un **árbol abarcador (Spanning Tree)** en el grafo bipartito:
    \begin{itemize}
        \item \textbf{Solución Inicial:} Método de Aproximación de Vogel (VAM), evaluando penalizaciones por arrepentimiento por fila y columna.
        \item \textbf{Optimización Exacta:} Algoritmo MODI ($u_i + v_j = c_{ij}$), evaluando costos reducidos $\Delta_{ij} = c_{ij} - (u_i + v_j)$ y redistribuyendo flujos a lo largo de ciclos cerrados ortogonales.
        \item \textbf{Método Tradicional de Red:} Stepping Stone (Banquillo), trazando ciclos elementales celda por celda.
    \end{itemize}
\end{enumerate}

\subsection{Desarrollo analítico iterativo paso a paso de MODI}

\textbf{Iteración 1 (Solución Inicial por Vogel):}
\begin{itemize}
    \item Celdas básicas: $x_{11} = 200, x_{13} = 100, x_{22} = 400, x_{23} = 100, x_{33} = 100$ (5 básicas).
    \item Costo inicial: $Z_1 = (200 \times 20) + (100 \times 24) + (400 \times 10) + (100 \times 8) + (100 \times 10) = \mathbf{\$12,200.00}$.
    \item Multiplicadores duales ($u_1 = 0$): $v_1 = 20, v_3 = 24, u_2 = -16, v_2 = 26, u_3 = -14$.
    \item Costo reducido no básico más negativo: $\Delta_{12} = c_{12} - (u_1 + v_2) = 16 - (0 + 26) = \mathbf{-10.0}$.
    \item Circuito cerrado: $(1, 2) \to (2, 2) \to (2, 3) \to (1, 3) \to (1, 2)$. Celdas con signo negativo: $(2, 2)$ con 400, $(1, 3)$ con 100. Valor de transferencia: $\theta = \min(400, 100) = 100$.
    \item Entra a la base: $(1, 2)$. Sale de la base: $(1, 3)$.
\end{itemize}

\textbf{Iteración 2:}
\begin{itemize}
    \item Celdas básicas: $x_{11} = 200, x_{12} = 100, x_{22} = 300, x_{23} = 200, x_{33} = 100$.
    \item Costo actual: $Z_2 = 12200 + 100 \times (-10.0) = \mathbf{\$11,200.00}$.
    \item Multiplicadores duales ($u_1 = 0$): $v_2 = 16, u_2 = -6, v_3 = 14, u_3 = -4, v_1 = 20$.
    \item Costo reducido no básico más negativo: $\Delta_{21} = c_{21} - (u_2 + v_1) = 10 - (-6 + 20) = \mathbf{-4.0}$.
    \item Circuito cerrado: $(2, 1) \to (1, 1) \to (1, 2) \to (2, 2) \to (2, 1)$. Celdas negativas: $(1, 1)$ con 200, $(2, 2)$ con 300. Transferencia: $\theta = \min(200, 300) = 200$.
    \item Entra a la base: $(2, 1)$. Sale de la base: $(1, 1)$.
\end{itemize}

\textbf{Iteración 3 (Condición de Optimalidad Alcanzada):}
\begin{itemize}
    \item Celdas básicas: $x_{12} = 300, x_{21} = 200, x_{22} = 100, x_{23} = 200, x_{33} = 100$.
    \item Costo actual: $Z_3 = 11200 + 200 \times (-4.0) = \mathbf{\$10,400.00}$.
    \item Multiplicadores duales ($u_1 = 0$): $v_2 = 16, u_2 = -6, v_1 = 16, v_3 = 14, u_3 = -4$.
    \item Costos reducidos no básicos:
    \[
    \Delta_{11} = 20 - (0 + 16) = +4.0 \geq 0, \qquad \Delta_{13} = 24 - (0 + 14) = +10.0 \geq 0
    \]
    \[
    \Delta_{31} = 12 - (-4 + 16) = 0.0 \geq 0, \qquad \Delta_{32} = 18 - (-4 + 16) = +6.0 \geq 0
    \]
    \item Como $\Delta_{ij} \geq 0$ para toda celda no básica, \textbf{se ha alcanzado el óptimo global globalmente inmejorable}.
\end{itemize}

\subsection{Explicación de las gráficas generadas por el código 01.py}

El script \texttt{01.py} genera automáticamente archivos de visualización gráfica en alta resolución:

\subsubsection{1. Panel Integrado: solucion\_grafica.png}
Este panel doble (Figura~\ref{fig:solucion_grafica_01}) condensa el ciclo completo de resolución:
\begin{itemize}
    \item \textbf{Panel Izquierdo (Diagrama de Ramificación / Flujo Iterativo):} Expone la trayectoria algorítmica desde el nodo inicial generado por Vogel ($Z = \$12,200.00$), ilustrando con cajas de estado y flechas anotadas la celda entrante, la celda saliente y el flujo transferido ($\theta$). Se observa la transición a la Iteración 2 ($Z = \$11,200.00$) y finalmente la convergencia hacia la Iteración 3 en verde claro, marcada como \textbf{[CANDIDATA TERMINAL - ÓPTIMO GLOBAL]} ($Z = \$10,400.00$).
    \item \textbf{Panel Derecho (Red Óptima de Transporte):} Representa el grafo bipartito final con nodos de oferta (cuadrados azules a la izquierda indicando las capacidades de 300, 500 y 100) y nodos de demanda (círculos verdes a la derecha indicando 200, 400 y 300). Las flechas dirigidas rojas señalan los 5 arcos básicos activos con el volumen exacto de unidades y el costo unitario correspondiente.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{01/solucion_grafica.png}
    \caption{Panel integrado de solución generado por \texttt{01.py}: diagrama de ramificación iterativo de MODI (izquierda) y red bipartita óptima de transporte (derecha).}
    \label{fig:solucion_grafica_01}
\end{figure}

\subsubsection{2. Red de Transporte Bipartita: red\_transporte.png}
La Figura~\ref{fig:red_transporte_01} presenta de forma aislada la red física de distribución resultante. Se evidencia con absoluta claridad que la Planta 2 actúa como el nodo central neurálgico de la logística despachando hacia los tres almacenes ($W_1: 200\text{ uds}, W_2: 100\text{ uds}, W_3: 200\text{ uds}$), mientras que la Planta 1 se enfoca exclusivamente en $W_2$ (300 uds) y la Planta 3 en $W_3$ (100 uds).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.70\textwidth]{01/red_transporte.png}
    \caption{Red óptima de transporte generada por \texttt{01.py} ilustrando las 5 rutas activas y los flujos asignados.}
    \label{fig:red_transporte_01}
\end{figure}

\subsubsection{3. Diagrama de Ramificación Iterativo: arbol\_ramificacion.png}
La Figura~\ref{fig:arbol_ramificacion_01} ilustra exclusivamente la evolución de la función objetivo y la toma de decisiones por pivoteo de MODI, sirviendo como mapa conceptual de la optimización en red.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.45\textwidth]{01/arbol_ramificacion.png}
    \caption{Árbol de ramificación y secuencia de pivoteos iterativos generado por \texttt{01.py}.}
    \label{fig:arbol_ramificacion_01}
\end{figure}

\subsection{Resultados y benchmark de rendimiento del código 01.py}

\begin{table}[H]
\centering
\caption{Matriz de asignación óptima final obtenida por \texttt{01.py}}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lccc|c}
\toprule
\textbf{Planta / Almacén} & \textbf{Almacén 1 ($W_1$)} & \textbf{Almacén 2 ($W_2$)} & \textbf{Almacén 3 ($W_3$)} & \textbf{Total Enviado} \\
\midrule
\textbf{Planta 1 ($P_1$)} & 0 & \textbf{300} & 0 & 300 / 300 \\
\textbf{Planta 2 ($P_2$)} & \textbf{200} & \textbf{100} & \textbf{200} & 500 / 500 \\
\textbf{Planta 3 ($P_3$)} & 0 & 0 & \textbf{100} & 100 / 100 \\
\midrule
\textbf{Total Recibido}   & \textbf{200 / 200} & \textbf{400 / 400} & \textbf{300 / 300} & \textbf{900 / 900} \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[H]
\centering
\caption{Benchmark comparativo de tiempos de ejecución de \texttt{01.py}}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lccc}
\toprule
\textbf{Método Evaluado} & \textbf{Costo Mínimo} & \textbf{Tiempo CPU} & \textbf{Speedup vs PuLP} \\
\midrule
1. Método Balanceado (Chequeo)           & \$10,400.00 & 0.015 ms & -- \\
2. Método Normal (Vogel VAM + MODI u-v)  & \$10,400.00 & \textbf{0.165 ms} & \textbf{77.8x más rápido} \\
3. Método Tradicional (Stepping Stone)   & \$10,400.00 & 0.442 ms & 29.0x más rápido \\
4. Simplex Tradicional (PuLP HiGHS)      & \$10,400.00 & 12.831 ms & 1.0x (Base) \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Código fuente completo y comentado (01.py)}

A continuación se transcribe en su totalidad el código fuente del script \texttt{01/01.py}:

\begin{lstlisting}[language=Python, caption={Código fuente completo de 01/01.py}]
"""
