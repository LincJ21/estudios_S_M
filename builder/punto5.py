# -*- coding: utf-8 -*-

def get_punto5(code_01):
    return r"""
%================================================
\newpage
\section{Taller. Soluciones de problemas de PL con herramientas computacionales - PARTE 2 (Librería de Python asignada). Solución Problema de Transporte, balanceado y no balanceado. Solución con el método simplex tradicional mejorado. Solucionar el mismo problema del punto 4}
%================================================

\subsection{Fundamentación matemática profunda del Simplex Tradicional Mejorado}

El \textbf{Método Simplex Tradicional Mejorado} para problemas de transporte (conocido en la literatura como el \textbf{Simplex de Transporte} o \textbf{Método MODI / Distribución Modificada}) es una especialización exacta del Simplex general que aprovecha las propiedades algebraicas y combinatorias intrínsecas de las redes de flujo:

\subsubsection{Unimodularidad Total y naturaleza entera de las bases}
En 1956, los matemáticos \textbf{Alan J. Hoffman} y \textbf{Joseph B. Kruskal} demostraron que la matriz de incidencia nodo-arco $A$ de cualquier grafo bipartito conexo es \textbf{Totalmente Unimodular (TUM)}. Esto implica que el determinante de cualquier submatriz cuadrada no singular de $A$ es igual a $+1$ o $-1$:
\begin{equation}
\det(B) \in \{-1, +1\}
\end{equation}
Por la regla de Cramer, la solución básica $x_B = B^{-1}b$ involucra únicamente divisiones por $\det(B) = \pm 1$. Por lo tanto, si las ofertas $s_i$ y las demandas $d_j$ son números enteros, \textbf{todas las soluciones básicas factibles son automáticamente enteras}, sin necesidad de invocar métodos de bifurcación ni algoritmos de corte.

\subsubsection{Correspondencia entre Bases y Árboles Abarcadores (Spanning Trees)}
En un problema con $m$ fuentes y $n$ destinos:
\begin{itemize}
    \item Cada base matemática no degenerada corresponde biunívocamente a un \textbf{árbol abarcador generador (Spanning Tree)} en el grafo bipartito $K_{m,n}$.
    \item El árbol conecta los $m+n$ nodos utilizando exactamente:
    \begin{equation}
    |\mathcal{B}| = m + n - 1 \text{ arcos básicos}
    \end{equation}
    \item La propiedad topológica de \textbf{aciclismo} del árbol es el análogo gráfico directo de la \textbf{independencia lineal} de las columnas en el álgebra matricial.
\end{itemize}

\subsubsection{El Sistema de Potenciales Duales (MODI $u-v$)}
A partir de las condiciones de holgura complementaria de Karush-Kuhn-Tucker (KKT), para toda celda perteneciente a la base actual $(i, j) \in \mathcal{B}$ se satisface rigurosamente:
\begin{equation}
u_i + v_j = c_{ij}
\end{equation}
donde $u_i$ representa el potencial dual del nodo origen $i$, y $v_j$ representa el potencial dual del nodo destino $j$. Este sistema posee $m+n-1$ ecuaciones lineales y $m+n$ incógnitas. Al fijar un nodo de referencia arbitrario (por ejemplo, $u_1 = 0$), el sistema se transforma en una estructura \textbf{estrictamente triangular}, la cual se resuelve mediante sustitución hacia adelante en tiempo lineal $\mathcal{O}(m+n)$, eliminando por completo la inversión de matrices densas de costo $\mathcal{O}((m+n)^3)$.

Los \textbf{costos reducidos} para todas las rutas no básicas $(i, j) \notin \mathcal{B}$ se calculan directamente como:
\begin{equation}
\Delta_{ij} = c_{ij} - (u_i + v_j)
\end{equation}
\begin{itemize}
    \item Si $\Delta_{ij} \geq 0$ para todo $(i, j) \notin \mathcal{B}$, la solución actual es el \textbf{Óptimo Global}.
    \item Si existe al menos un $\Delta_{ij} < 0$, la solución puede mejorarse. Se escoge como variable básica entrante la ruta con el costo marginal más negativo:
    \begin{equation}
    (p, q) = \arg\min_{(i,j) \notin \mathcal{B}} \Delta_{ij}
    \end{equation}
\end{itemize}

\subsubsection{Circuito cerrado fundamental y pivoteo de Stepping Stone (Banquillo)}
Al añadir la arista no básica $(p, q)$ al árbol abarcador, se induce un \textbf{único ciclo cerrado simple ortogonal} compuesto exclusivamente por aristas básicas y la arista entrante. Se asignan signos alternados $+ / -$ a las celdas del ciclo, iniciando con $+$ en $(p, q)$. La máxima cantidad de flujo transferible sin violar la no negatividad es:
\begin{equation}
\theta = \min \{ x_{ij} : (i, j) \in \text{aristas con signo } - \}
\end{equation}
Se reasigna el flujo: $x_{ij} \leftarrow x_{ij} + \theta$ (en celdas $+$) y $x_{ij} \leftarrow x_{ij} - \theta$ (en celdas $-$). La celda donante que alcanza el valor cero abandona la base.

\subsection{Fase 1: Método de Aproximación de Vogel (VAM) - Solución Inicial}

El \textbf{Método de Aproximación de Vogel (VAM)} calcula para cada fila y columna una \textbf{penalización por arrepentimiento}, definida como la diferencia absoluta entre sus dos costos unitarios más bajos. Esta penalización mide el sobrecosto unitario en el que incurriría el sistema si se le impidiera utilizar su mejor ruta disponible.

\subsubsection{Cálculo analítico paso a paso para la Red 3x3 (900 uds)}
\begin{enumerate}
    \item \textbf{Penalizaciones iniciales:}
    \begin{itemize}
        \item Fila $P_1$: Dos menores costos son 16 y 20 $\implies \text{Penalización } = 20 - 16 = \mathbf{4}$.
        \item Fila $P_2$: Dos menores costos son 8 y 10 $\implies \text{Penalización } = 10 - 8 = \mathbf{2}$.
        \item Fila $P_3$: Dos menores costos son 10 y 12 $\implies \text{Penalización } = 12 - 10 = \mathbf{2}$.
        \item Columna $W_1$: Dos menores costos son 10 y 12 $\implies \text{Penalización } = 12 - 10 = \mathbf{2}$.
        \item Columna $W_2$: Dos menores costos son 10 y 16 $\implies \text{Penalización } = 16 - 10 = \mathbf{6}$ \textbf{(Máxima Penalización)}.
        \item Columna $W_3$: Dos menores costos son 8 y 10 $\implies \text{Penalización } = 10 - 8 = \mathbf{2}$.
    \end{itemize}
    \item \textbf{Asignación 1:} La máxima penalización corresponde a la Columna $W_2$ (valor 6). El costo mínimo en $W_2$ es $c_{22} = \$10$ (Planta 2). Asignamos $\min(s_2, d_2) = \min(500, 400) = \mathbf{400}$ unidades a $(P_2, W_2)$. La demanda de $W_2$ queda totalmente satisfecha y la columna $W_2$ sale del análisis. La oferta remanente de $P_2$ es $500 - 400 = 100$.
    \item \textbf{Asignación 2:} En las columnas activas ($W_1, W_3$), la fila $P_2$ dispone de 100 unidades y su costo mínimo es $c_{23} = \$8$. Asignamos $\min(100, 300) = \mathbf{100}$ unidades a $(P_2, W_3)$. La oferta de $P_2$ se agota totalmente. Demanda remanente de $W_3 = 300 - 100 = 200$.
    \item \textbf{Asignación 3:} La Planta $P_3$ dispone de 100 unidades y tiene en $W_3$ un costo de $c_{33} = \$10$ frente a $\$12$ en $W_1$. Asignamos $\min(100, 200) = \mathbf{100}$ unidades a $(P_3, W_3)$. La oferta de $P_3$ se agota totalmente. Demanda remanente de $W_3 = 200 - 100 = 100$.
    \item \textbf{Asignación 4 y 5:} La Planta $P_1$ dispone de 300 unidades y debe satisfacer las demandas residuales exactas: 200 unidades a $W_1$ ($c_{11} = \$20$) y 100 unidades a $W_3$ ($c_{13} = \$24$). Se asignan $x_{11} = 200$ y $x_{13} = 100$.
\end{enumerate}

\begin{table}[H]
\centering
\caption{Solución Básica Factible Inicial obtenida mediante el Método de Vogel (VAM)}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lccc|c}
\toprule
\textbf{Planta / Almacén} & \textbf{Almacén 1 ($W_1$)} & \textbf{Almacén 2 ($W_2$)} & \textbf{Almacén 3 ($W_3$)} & \textbf{Oferta} \\
\midrule
\textbf{Planta 1 ($P_1$)} & \textbf{200} ($c=20$) & -- & \textbf{100} ($c=24$) & 300 \\
\textbf{Planta 2 ($P_2$)} & -- & \textbf{400} ($c=10$) & \textbf{100} ($c=8$)  & 500 \\
\textbf{Planta 3 ($P_3$)} & -- & -- & \textbf{100} ($c=10$) & 100 \\
\midrule
\textbf{Demanda} & 200 & 400 & 300 & \textbf{900} \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Costo de la solución inicial de Vogel:}
\begin{equation}
Z_1 = 200(20) + 100(24) + 400(10) + 100(8) + 100(10) = 4000 + 2400 + 4000 + 800 + 1000 = \$12,200.00
\end{equation}

\subsection{Fase 2: Optimización Iterativa MODI ($u-v$) y Stepping Stone}

\subsubsection{Iteración 1: Evaluación y Primer Salto de Mejora}
Celdas básicas: $\mathcal{B}_1 = \{(1,1), (1,3), (2,2), (2,3), (3,3)\}$.
Fijamos $u_1 = 0$:
\begin{align}
(1, 1) \in \mathcal{B} &\implies u_1 + v_1 = c_{11} \implies 0 + v_1 = 20 \implies v_1 = 20 \\
(1, 3) \in \mathcal{B} &\implies u_1 + v_3 = c_{13} \implies 0 + v_3 = 24 \implies v_3 = 24 \\
(2, 3) \in \mathcal{B} &\implies u_2 + v_3 = c_{23} \implies u_2 + 24 = 8 \implies u_2 = -16 \\
(2, 2) \in \mathcal{B} &\implies u_2 + v_2 = c_{22} \implies -16 + v_2 = 10 \implies v_2 = 26 \\
(3, 3) \in \mathcal{B} &\implies u_3 + v_3 = c_{33} \implies u_3 + 24 = 10 \implies u_3 = -14
\end{align}

Cálculo de costos reducidos $\Delta_{ij} = c_{ij} - (u_i + v_j)$ para las 4 celdas no básicas:
\begin{align}
\Delta_{12} &= c_{12} - (u_1 + v_2) = 16 - (0 + 26) = \mathbf{-10.0} \quad \text{\textbf{(Candidata Entrante)}} \\
\Delta_{21} &= c_{21} - (u_2 + v_1) = 10 - (-16 + 20) = +6.0 \\
\Delta_{31} &= c_{31} - (u_3 + v_1) = 12 - (-14 + 20) = +6.0 \\
\Delta_{32} &= c_{32} - (u_3 + v_2) = 18 - (-14 + 26) = +6.0
\end{align}

\textbf{Circuito cerrado ortogonal de Stepping Stone para $(1, 2)$:}
\begin{equation}
(1, 2)^+ \longrightarrow (1, 3)^- \longrightarrow (2, 3)^+ \longrightarrow (2, 2)^- \longrightarrow (1, 2)
\end{equation}
Determinación del cuello de botella $\theta$:
\begin{equation}
\theta = \min \{x_{13}, x_{22}\} = \min(100, 400) = 100 \text{ unidades}
\end{equation}
Reasignación de flujos:
\begin{align}
x_{12} &= 0 + 100 = 100 \qquad (\text{Entra a la Base}) \\
x_{13} &= 100 - 100 = 0 \qquad (\text{\textbf{Sale de la Base}}) \\
x_{23} &= 100 + 100 = 200 \\
x_{22} &= 400 - 100 = 300
\end{align}
Nuevo costo: $Z_2 = 12200 + 100 \times (-10.0) = \mathbf{\$11,200.00}$.

\subsubsection{Iteración 2: Evaluación y Segundo Salto de Mejora}
Celdas básicas: $\mathcal{B}_2 = \{(1,1), (1,2), (2,2), (2,3), (3,3)\}$.
Fijamos $u_1 = 0$:
\begin{align}
v_1 = 20, \qquad v_2 = 16, \qquad u_2 = -6, \qquad v_3 = 14, \qquad u_3 = -4
\end{align}
Costos reducidos $\Delta_{ij}$:
\begin{align}
\Delta_{13} &= 24 - (0 + 14) = +10.0 \\
\Delta_{21} &= 10 - (-6 + 20) = \mathbf{-4.0} \quad \text{\textbf{(Candidata Entrante)}} \\
\Delta_{31} &= 12 - (-4 + 20) = -4.0 \quad (\text{Empate, regla de Bland selecciona } (2,1)) \\
\Delta_{32} &= 18 - (-4 + 16) = +6.0
\end{align}

\textbf{Circuito cerrado de Stepping Stone para $(2, 1)$:}
\begin{equation}
(2, 1)^+ \longrightarrow (1, 1)^- \longrightarrow (1, 2)^+ \longrightarrow (2, 2)^- \longrightarrow (2, 1)
\end{equation}
Determinación de $\theta$:
\begin{equation}
\theta = \min \{x_{11}, x_{22}\} = \min(200, 300) = 200 \text{ unidades}
\end{equation}
Reasignación de flujos:
\begin{align}
x_{21} &= 0 + 200 = 200 \qquad (\text{Entra a la Base}) \\
x_{11} &= 200 - 200 = 0 \qquad (\text{\textbf{Sale de la Base}}) \\
x_{12} &= 100 + 200 = 300 \\
x_{22} &= 300 - 200 = 100
\end{align}
Nuevo costo: $Z_3 = 11200 + 200 \times (-4.0) = \mathbf{\$10,400.00}$.

\subsubsection{Iteración 3: Comprobación de Optimalidad Global}
Celdas básicas: $\mathcal{B}_3 = \{(1,2), (2,1), (2,2), (2,3), (3,3)\}$.
Fijamos $u_2 = 0$:
\begin{align}
v_1 = 10, \qquad v_2 = 10, \qquad v_3 = 8, \qquad u_1 = 6, \qquad u_3 = 2
\end{align}
Costos reducidos $\Delta_{ij}$:
\begin{align}
\Delta_{11} &= 20 - (6 + 10) = \mathbf{+4.0} \geq 0 \\
\Delta_{13} &= 24 - (6 + 8) = \mathbf{+10.0} \geq 0 \\
\Delta_{31} &= 12 - (2 + 10) = \mathbf{0.0} \geq 0 \\
\Delta_{32} &= 18 - (2 + 10) = \mathbf{+6.0} \geq 0
\end{align}
Dado que \textbf{todos los costos reducidos son mayores o iguales a cero ($\Delta_{ij} \geq 0$)}, el algoritmo ha alcanzado el \textbf{Óptimo Global}. Costo mínimo definitivo: $\mathbf{Z^* = \$10,400.00}$.

\subsection{Código fuente íntegro en Python del Método Simplex Mejorado (01.py)}

A continuación se transcribe en su totalidad el código del archivo \texttt{01/01.py}, el cual implementa de manera nativa y autónoma las rutinas de Vogel, MODI $u-v$, Stepping Stone, comparación de rendimiento y generación gráfica:

\begin{lstlisting}[language=Python, caption={Código fuente completo de 01/01.py para el Simplex Tradicional Mejorado}]
""" + code_01 + r"""
\end{lstlisting}

\subsection{Explicación exhaustiva del código fuente}

\begin{enumerate}
    \item \textbf{Procedimiento general y modularidad:}
    \begin{itemize}
        \item \texttt{verificar\_y\_balancear\_transporte}: Compara $\sum s_i$ frente a $\sum d_j$ con tolerancia flotante. Si detecta asimetría, concatena un nodo ficticio (\texttt{W\_Dummy} o \texttt{P\_Dummy}) con vector de costos cero.
        \item \texttt{solucion\_inicial\_vogel}: Implementa el algoritmo VAM evaluando iterativamente las dos menores entradas por fila y columna sobre las submatrices activas y asigna el flujo saturante $\min(s_i, d_j)$.
        \item \texttt{calcular\_uv}: Resuelve el sistema lineal triangular $u_i + v_j = c_{ij}$ para las $m+n-1$ celdas básicas mediante un bucle de propagación en tiempo lineal.
        \item \texttt{buscar\_circuito\_cerrado}: Implementa una búsqueda recursiva en profundidad (DFS) para rastrear el único ciclo ortogonal cerrado alternando movimientos horizontales y verticales sobre las aristas del árbol abarcador.
        \item \texttt{ejecutar\_metodo\_modi}: Orquesta el bucle de optimización calculando $\Delta_{ij}$, detectando la celda entrante más negativa y reasignando el flujo $\theta$.
        \item \texttt{ejecutar\_metodo\_tradicional\_stepping\_stone}: Proporciona la evaluación alternativa basada en la traza completa de polígonos ortogonales para validar los gradientes de costo.
        \item \texttt{verificar\_con\_pulp}: Valida la solución óptima frente al solver Simplex continuo HiGHS de PuLP.
        \item \texttt{mostrar\_grafico\_solucion}: Compila y guarda las figuras gráficas de la red y del árbol de iteraciones.
    \end{itemize}

    \item \textbf{Variables utilizadas:}
    \begin{itemize}
        \item \texttt{costos}, \texttt{oferta}, \texttt{demanda}: Arreglos bidimensionales y unidimensionales de tipo \texttt{np.ndarray}.
        \item \texttt{alloc}: Matriz float de tamaño $m \times n$ que almacena las cantidades físicas de producto transportado.
        \item \texttt{basic}: Matriz booleana ($m \times n$) que actúa como máscara lógica indicando qué celdas integran la base actual.
        \item \texttt{u}, \texttt{v}: Listas que almacenan los potenciales duales de filas y columnas.
        \item \texttt{theta}: Escalar que representa el volumen límite transferible a lo largo del circuito cerrado.
    \end{itemize}

    \item \textbf{Sentencias utilizadas:}
    \begin{itemize}
        \item Indexación booleana avanzada de NumPy (\texttt{costos[np.ix\_(filas, cols)]}).
        \item Control de flujo iterativo mediante bucles \texttt{while True} gobernados por condiciones de optimalidad $\Delta_{ij} \geq -\epsilon$.
        \item Rutinas de visualización mediante \texttt{networkx.bipartite} y \texttt{matplotlib.pyplot}.
    \end{itemize}
\end{enumerate}

\subsection{Explicación detallada de las gráficas generadas}

El script \texttt{01.py} compila y genera automáticamente tres archivos visuales de diagnóstico de alta resolución:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{01/solucion_grafica.png}
    \caption{Panel Integrado de Diagnóstico (\texttt{01/solucion\_grafica.png}): Árbol de transición iterativa de MODI (izquierda) y red bipartita óptima de transporte (derecha).}
    \label{fig:p5_panel_integrado}
\end{figure}

\begin{enumerate}
    \item \textbf{Panel Integrado (\texttt{solucion\_grafica.png}):}
    Combina en una única lámina técnica los dos componentes del análisis: la convergencia iterativa paso a paso del método MODI y la topología física del despacho de carga. Permite visualizar simultáneamente cómo el costo total decrece monótonamente (\$12.200 $\to$ \$11.200 $\to$ \$10.400) mientras la estructura de asignación de la red se reconfigura.

    \item \textbf{Árbol de Transición Iterativa (\texttt{01/arbol\_ramificacion.png}):}
    Detalla la trayectoria algorítmica:
    \begin{itemize}
        \item \textbf{Nodo 1 (Solución Inicial VAM):} Muestra el costo de arranque de \textbf{\$12,200.00} y la presencia de la celda más desfavorable $(P_1, W_2)$ con $\Delta = -10.0$.
        \item \textbf{Nodo 2 (Iteración 1 MODI):} Muestra el costo reducido a \textbf{\$11,200.00} tras ingresar $P_1 \to W_2$ y expulsar $P_1 \to W_3$ con un flujo $\theta = 100$.
        \item \textbf{Nodo 3 (Iteración 2 MODI - Óptimo):} Muestra el costo terminal de \textbf{\$10,400.00} tras el ingreso de $P_2 \to W_1$ con $\theta = 200$. El nodo se marca con contorno reforzado certificando que todos los $\Delta_{ij} \geq 0$.
    \end{itemize}

    \begin{figure}[H]
        \centering
        \includegraphics[width=0.45\textwidth]{01/arbol_ramificacion.png}
        \caption{Árbol de transición iterativa de costos y pivotes MODI (\texttt{01/arbol\_ramificacion.png}).}
        \label{fig:p5_arbol_individual}
    \end{figure}

    \item \textbf{Grafo Bipartito de la Red Óptima (\texttt{red\_transporte.png}):}
    \begin{figure}[H]
        \centering
        \includegraphics[width=0.62\textwidth]{01/red_transporte.png}
        \caption{Grafo bipartito de la red logística óptima (\texttt{01/red\_transporte.png}).}
        \label{fig:p5_red_individual}
    \end{figure}
    \begin{itemize}
        \item \textbf{Partición de Origen (Izquierda):} Cuadrados azules que identifican las plantas $P_1$, $P_2$ y $P_3$, indicando en su etiqueta interior su capacidad total de oferta ($s_1=300, s_2=500, s_3=100$).
        \item \textbf{Partición de Destino (Derecha):} Círculos verdes que identifican los almacenes $W_1$, $W_2$ y $W_3$, indicando en su etiqueta la demanda atendida ($d_1=200, d_2=400, d_3=300$).
        \item \textbf{Arcos Dirigidos de Flujo (Flechas Rojas):} Representan las 5 rutas básicas activas ($m+n-1 = 5$), rotuladas con el volumen despachado y el costo unitario de transporte:
        \begin{itemize}
            \item $P_1 \to W_2$: 300 unidades a \$16/u.
            \item $P_2 \to W_1$: 200 unidades a \$10/u.
            \item $P_2 \to W_2$: 100 unidades a \$10/u.
            \item $P_2 \to W_3$: 200 unidades a \$8/u.
            \item $P_3 \to W_3$: 100 unidades a \$10/u.
        \end{itemize}
    \end{itemize}
\end{enumerate}

\subsection{Medición de tiempos y tabla comparativa de ejecución (Puntos 4 vs 5)}

Para cumplir con la observación obligatoria de la actividad, se ejecutó un protocolo riguroso de benchmarking midiendo el tiempo de CPU en milisegundos con el temporizador de alta resolución \texttt{time.perf\_counter()}:

\begin{table}[H]
\centering
\caption{Tabla comparativa de tiempos de ejecución y eficiencia computacional: Punto 4 vs Punto 5}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lcccc}
\toprule
\textbf{Enfoque Metodológico} & \textbf{Algoritmo Específico} & \textbf{Costo Óptimo} & \textbf{Tiempo CPU} & \textbf{Speedup} \\
\midrule
\textbf{Punto 4 (Simplex Tradicional)} & PuLP HiGHS (Formulación Tabular) & \$10,400.00 & 12.831 ms & 1.0x (Referencia) \\
\textbf{Punto 5 (Simplex Mejorado)}    & Stepping Stone (Traza de Ciclos) & \$10,400.00 & 0.442 ms  & 29.0x \\
\textbf{Punto 5 (Simplex Mejorado)}    & \textbf{MODI $u-v$ (Vogel + Dual)} & \textbf{\$10,400.00} & \textbf{0.165 ms} & \textbf{77.8x} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Explicación de los resultados de la tabla}

Los datos de la tabla comparativa evidencian que el **Método Simplex Tradicional Mejorado (MODI $u-v$) es 77.8 veces más rápido** que el Simplex Tradicional implementado en PuLP:
\begin{enumerate}
    \item \textbf{Eliminación de la inversión matricial densa:} El Simplex Tradicional de PuLP trata el transporte como un programa lineal general $Ax = b$, obligando al motor C++ a mantener y factorizar una matriz de base de dimensión $5 \times 5$ mediante álgebra matricial densa o dispersa de costo $\mathcal{O}((m+n)^2)$. En agudo contraste, el Simplex Mejorado (MODI) calcula los potenciales duales mediante sustitución hacia adelante a través del árbol abarcador en tiempo estrictamente lineal $\mathcal{O}(m+n)$.
    \item \textbf{Aceleración por aproximación inteligente (VAM):} El Simplex Tradicional comienza desde una base arbitraria con variables artificiales. Por el contrario, el Simplex Mejorado arranca con el método de Vogel, situándose a solo 2 iteraciones del óptimo global (\$12.200 $\to$ \$10.400).
    \item \textbf{Eficiencia en memoria y jerarquía de caché:} El código de \texttt{01.py} opera directamente sobre matrices continuas de NumPy en memoria contigua, aprovechando al máximo la caché L1/L2 del procesador y evitando la sobrecarga de instanciación de objetos de variables y compilación de archivos intermedios de PuLP.
\end{enumerate}
"""
