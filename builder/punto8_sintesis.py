# -*- coding: utf-8 -*-

def get_punto8():
    return r"""
%================================================
\newpage
\section{Síntesis Global, Conclusiones y Referencias Bibliográficas}
%================================================

\subsection{Tabla maestra comparativa de los 7 puntos del Cuaderno de Apuntes}

A continuación se presenta el cuadro sinóptico integral que consolida las dimensiones conceptuales, metodológicas y computacionales desarrolladas en los siete puntos de la actividad:

\begin{table}[H]
\centering
\caption{Matriz consolidada del Cuaderno de Apuntes Digital (Sistemas y Modelos)}
\renewcommand{\arraystretch}{1.3}
\resizebox{\textwidth}{!}{
\begin{tabular}{clllll}
\toprule
\textbf{Punto} & \textbf{Eje Temático} & \textbf{Herramienta} & \textbf{Método Algorítmico} & \textbf{Solución Óptima} & \textbf{Métrica Clave / Desempeño} \\
\midrule
\textbf{1} & Parcial 1 y 4 Casos Especiales & Teórico / Gráfico & Gráfico y Simplex Tabular & Plantilla estructurada & 4 Casos: Degen, Mult, No Acot, Infact \\
\textbf{2} & PL Entera (Producción) & phpSimplex & Branch and Bound (Árbol) & $x_1^*=3, x_2^*=1, Z^*=\$19.000$ & 5 nodos evaluados (12 capturas) \\
\textbf{3} & PL Entera (Mismo Problema P2) & Python (PuLP) & Branch and Cut (Solver CBC) & $x_1^*=3, x_2^*=1, Z^*=\$19.000$ & Tiempo: 1.8 ms (100\% concordancia) \\
\textbf{4} & Transporte Balanceado y No Bal. & Python (PuLP) & Simplex Tradicional Tabular & $Z^* = \$10,400.00$ & Tiempo: 12.831 ms (Base 1.0x) \\
\textbf{5} & Transporte (Mismo Problema P4) & Python (01.py) & Simplex Mejorado (Vogel + MODI) & $Z^* = \$10,400.00$ & \textbf{Tiempo: 0.165 ms (Speedup 77.8x)} \\
\textbf{6} & Asignación Biyectiva (Energía) & Python (PuLP) & Simplex Tradicional (TUM) & 17.000 \euro{} (17k \euro) & Tiempo: 11.230 ms (Base 1.0x) \\
\textbf{7} & Asignación (Mismo Problema P6) & Python (02.py) & Simplex Mejorado (Algoritmo Húngaro) & 17.000 \euro{} (17k \euro) & \textbf{Tiempo: 0.045 ms (Speedup 249.5x)} \\
\bottomrule
\end{tabular}
}
\end{table}

\subsection{Conclusiones metodológicas transversales}

El desarrollo integral de este cuaderno de apuntes digital permite extraer conclusiones fundamentales para la ingeniería y la ciencia de la optimización:

\begin{enumerate}
    \item \textbf{Superioridad de los algoritmos de red especializados:}
    La comparación directa realizada entre los Puntos 4 y 5, y entre los Puntos 6 y 7, demuestra empíricamente que cuando un problema de programación lineal posee una estructura topológica de red (grafo bipartito conexo), los algoritmos especializados (\textbf{MODI $u-v$} y \textbf{Algoritmo Húngaro}) superan abrumadoramente al Método Simplex Tradicional en velocidad de ejecución:
    \begin{itemize}
        \item En transporte, MODI alcanzó una aceleración de \textbf{77.8x} respecto a PuLP.
        \item En asignación, el Algoritmo Húngaro alcanzó una aceleración de \textbf{249.5x} respecto a PuLP.
    \end{itemize}
    Esta diferencia radica en la sustitución de la costosa inversión matricial densa $\mathcal{O}(N^3)$ por recorridos en árboles abarcadores y búsquedas de caminos aumentantes en tiempo lineal o cuadrático.

    \item \textbf{La Unimodularidad Total como puente entre lo continuo y lo discreto:}
    Tanto en el modelo de transporte como en el de asignación, la propiedad matemática de \textbf{Unimodularidad Total (TUM)} de las matrices de incidencia garantiza que todos los vértices del poliedro continuo sean enteros. Esto elimina la necesidad de costosos árboles de Branch and Bound, permitiendo que la relajación lineal continua entregue directamente soluciones físicamente aplicables.

    \item \textbf{El impacto de las aproximaciones inteligentes iniciales:}
    El análisis iterativo de transporte evidenció la importancia crítica del \textbf{Método de Aproximación de Vogel (VAM)}. Al considerar el costo de arrepentimiento, VAM situó al sistema a tan solo dos pivoteos del óptimo global, minimizando drásticamente las iteraciones necesarias frente a inicializaciones arbitrarias.

    \item \textbf{Complementariedad entre herramientas visuales y código autónomo:}
    El uso de herramientas pedagógicas como \textbf{phpSimplex} permite desmitificar el árbol de bifurcación de Branch and Bound, mientras que el desarrollo de scripts nativos en \textbf{Python (PuLP, NumPy y NetworkX)} dota al futuro ingeniero de capacidades de automatización industrial escalables a problemas de millones de variables.
\end{enumerate}

\subsection{Verificación formal de las observaciones de la actividad}

\begin{itemize}
    \item \textbf{Enunciado, modelo matemático, solución óptima e interpretación:} Presentes exhaustivamente en cada uno de los problemas abordados (Puntos 2 a 7).
    \item \textbf{Explicación de código fuente:} Se detalló minuciosamente el procedimiento, las variables y las sentencias utilizadas en los scripts de Python (Puntos 3, 4, 5, 6 y 7).
    \item \textbf{Medición y tablas comparativas de tiempos:}
    \begin{itemize}
        \item Puntos 4 y 5: Documentado en la Sección~5 con tabla formal y explicación del Speedup de 77.8x.
        \item Puntos 6 y 7: Documentado en la Sección~7 con tabla formal y explicación del Speedup de 249.5x.
    \end{itemize}
    \item \textbf{Incorporación y explicación de gráficas:} Se integraron y analizaron en detalle las 12 capturas de phpSimplex (Punto 2), las figuras de transporte balanceado y no balanceado (Punto 4), el panel integrado, la red de transporte y el árbol de MODI (Punto 5), y el grafo bipartito de asignación unívoca (Punto 7).
    \item \textbf{Presentación institucional:} Estructurado para el cumplimiento de las normas de entrega de la Universidad Tecnológica de Bolívar bajo la cátedra del profesor Isaac Zúñiga Silgado.
\end{itemize}

%================================================
\subsection{Referencias Bibliográficas Académicas}
%================================================

\begin{enumerate}
    \item \textbf{Birkhoff, G.} (1946). \textit{Tres observaciones sobre el álgebra lineal}. Universidad Nacional de Tucumán, Revista Serie A, 5, 147--151.
    \item \textbf{Bland, R. G.} (1977). \textit{New finite pivoting rules for the simplex method}. Mathematics of Operations Research, 2(2), 103--107.
    \item \textbf{Charnes, A.} (1952). \textit{Optimality and degeneracy in linear programming}. Econometrica, 20(2), 160--170.
    \item \textbf{Dakin, R. J.} (1965). \textit{A tree-search algorithm for mixed integer programming problems}. The Computer Journal, 8(3), 250--255.
    \item \textbf{Dantzig, G. B.} (1947). \textit{Maximization of a linear function of variables subject to linear inequalities}. En T. C. Koopmans (Ed.), \textit{Activity Analysis of Production and Allocation} (pp. 339--347). John Wiley \& Sons.
    \item \textbf{Dantzig, G. B.} (1951). \textit{Application of the simplex method to a transportation problem}. En T. C. Koopmans (Ed.), \textit{Activity Analysis of Production and Allocation} (pp. 359--373). John Wiley \& Sons.
    \item \textbf{Dantzig, G. B.} (1963). \textit{Linear Programming and Extensions}. Princeton University Press.
    \item \textbf{Egerváry, J.} (1931). \textit{Matrixok kombinatorikus tulajdonságairól (Sobre propiedades combinatorias de matrices)}. Matematikai és Fizikai Lapok, 38, 16--28.
    \item \textbf{Gomory, R. E.} (1958). \textit{Outline of an algorithm for integer solutions to linear programs}. Bulletin of the American Mathematical Society, 64(5), 275--278.
    \item \textbf{Hitchcock, F. L.} (1941). \textit{The distribution of a product from several sources to numerous localities}. Journal of Mathematics and Physics, 20(1-4), 224--230.
    \item \textbf{Hoffman, A. J.} (1953). \textit{Cycling in the simplex algorithm}. National Bureau of Standards Report, 2974.
    \item \textbf{Hoffman, A. J., \& Kruskal, J. B.} (1956). \textit{Integral boundary points of convex polyhedra}. Linear Inequalities and Related Systems, Annals of Mathematics Studies, 38, 223--246.
    \item \textbf{Kantorovich, L. V.} (1939). \textit{Mathematical methods of organizing and planning production}. Management Science, 6(4), 366--422 (Traducción al inglés, 1960).
    \item \textbf{Koopmans, T. C.} (1947). \textit{Optimum utilization of the transportation system}. Proceedings of the International Statistical Conferences, Washington D.C., 5, 136--145.
    \item \textbf{Kőnig, D.} (1931). \textit{Gráfok és mátrixok (Grafos y matrices)}. Matematikai és Fizikai Lapok, 38, 116--119.
    \item \textbf{Kuhn, H. W.} (1955). \textit{The Hungarian method for the assignment problem}. Naval Research Logistics Quarterly, 2(1-2), 83--97.
    \item \textbf{Land, A. H., \& Doig, A. G.} (1960). \textit{An automatic method of solving discrete programming problems}. Econometrica, 28(3), 497--520.
    \item \textbf{Munkres, J.} (1957). \textit{Algorithms for the assignment and transportation problems}. Journal of the Society for Industrial and Applied Mathematics, 5(1), 32--38.
    \item \textbf{von Neumann, J.} (1953). \textit{A certain zero-sum two-person game equivalent to the optimal assignment problem}. Contributions to the Theory of Games, 2, 5--12.
\end{enumerate}

\end{document}
"""

