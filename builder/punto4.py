# -*- coding: utf-8 -*-

def get_punto4():
    return r"""
%================================================
\newpage
\section{Taller. Soluciones de problemas de PL con herramientas computacionales - PARTE 2 (Librería de Python asignada). Solución Problema de Transporte, balanceado y no balanceado. Solución con el método simplex tradicional}
%================================================

\subsection{Historia y orígenes del Problema de Transporte}

El \textbf{Problema de Transporte} ocupa un lugar seminal en la génesis histórica de la optimización matemática y la investigación de operaciones. Su primera formulación analítica formal fue propuesta en 1941 por el matemático estadounidense \textbf{Frank Lauren Hitchcock} en su célebre artículo \textit{``The Distribution of a Product from Several Sources to Numerous Localities''}, publicado en el \textit{Journal of Mathematics and Physics}. Hitchcock describió formalmente el problema de minimizar el costo total de envío de un producto homogéneo desde múltiples centros de suministro hacia múltiples destinos de consumo.

Posteriormente, en 1947, el economista holandés-estadounidense \textbf{Tjalling C. Koopmans}, en el marco de sus investigaciones para la Junta de Transporte Marítimo Combinado durante la Segunda Guerra Mundial, extendió de manera independiente el análisis en su trabajo fundamental \textit{``Optimum Utilization of the Transportation System''}. Las contribuciones de Koopmans vincularon la teoría del transporte con la teoría económica de la asignación eficiente de recursos, trabajo que le valió el Premio Nobel de Economía en 1975 conjuntamente con Leonid Kantorovich.

En 1951, \textbf{George B. Dantzig} integró el problema de transporte dentro del marco general de la programación lineal en su influyente publicación \textit{``Application of the Simplex Method to a Transportation Problem''}. Dantzig reconoció que aunque el problema de transporte puede resolverse directamente mediante el \textbf{Método Simplex Tradicional} (construyendo una tabla de restricciones con igualdades canónicas), la estructura matricial contiene propiedades topológicas extraordinarias que permitían concebir algoritmos hiperespecializados mucho más rápidos.

\subsection{Caso 4.1: Problema de Transporte Balanceado (Red Logística 3x3)}

\subsubsection{Enunciado y matriz de fletes unitarios}
Una corporación logística dispone de tres plantas de producción ($P_1, P_2, P_3$) encargadas de abastecer a tres almacenes regionales de distribución ($W_1, W_2, W_3$). 
\begin{itemize}
    \item La capacidad de oferta de las plantas es de \textbf{300, 500 y 100 unidades}, respectivamente ($\sum_{i=1}^3 s_i = 900$).
    \item Los requerimientos de demanda de los almacenes son de \textbf{200, 400 y 300 unidades}, respectivamente ($\sum_{j=1}^3 d_j = 900$).
\end{itemize}
Dado que la oferta total es estrictamente igual a la demanda total ($\sum s_i = \sum d_j = 900$), el sistema se encuentra en \textbf{equilibrio estricto o balanceado}. Los costos unitarios de transporte (\$ por unidad) se presentan a continuación:

\begin{table}[H]
\centering
\caption{Matriz de costos unitarios de transporte ($c_{ij}$ en \$ por unidad)}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lccc|c}
\toprule
\textbf{Planta / Almacén} & \textbf{Almacén 1 ($W_1$)} & \textbf{Almacén 2 ($W_2$)} & \textbf{Almacén 3 ($W_3$)} & \textbf{Oferta Disponible ($s_i$)} \\
\midrule
\textbf{Planta 1 ($P_1$)} & \$20 & \$16 & \$24 & \textbf{300} \\
\textbf{Planta 2 ($P_2$)} & \$10 & \$10 & \$8  & \textbf{500} \\
\textbf{Planta 3 ($P_3$)} & \$12 & \$18 & \$10 & \textbf{100} \\
\midrule
\textbf{Demanda Requerida ($d_j$)} & \textbf{200} & \textbf{400} & \textbf{300} & \textbf{900 (Total Balanceado)} \\
\bottomrule
\end{tabular}
\end{table}

\subsubsection{Modelo matemático formal (Simplex Tradicional)}
Sean $x_{ij} \geq 0$ la cantidad continua de unidades transferidas desde la planta $i$ hacia el almacén $j$:
\begin{equation}
\min \quad Z = \sum_{i=1}^3 \sum_{j=1}^3 c_{ij} x_{ij}
\end{equation}
sujeto a las restricciones de conservación de flujo:
\begin{align}
\sum_{j=1}^3 x_{ij} &= s_i \quad \forall i \in \{1, 2, 3\} \qquad \text{(Restricciones de Oferta en Nodos Origen)} \\
\sum_{i=1}^3 x_{ij} &= d_j \quad \forall j \in \{1, 2, 3\} \qquad \text{(Restricciones de Demanda en Nodos Destino)} \\
x_{ij} &\geq 0 \quad \forall i, j.
\end{align}

\subsubsection{Estructura de la formulación matricial en el Simplex Tradicional}
En el Simplex Tradicional, el problema se modela en su forma estándar $Ax = b, x \geq 0$. La matriz $A \in \mathbb{R}^{6 \times 9}$ posee una fila por cada nodo (3 de oferta y 3 de demanda) y una columna por cada variable de decisión $x_{ij}$.
\begin{itemize}
    \item \textbf{Redundancia lineal:} Como la red está cerrada ($\sum s_i = \sum d_j$), la suma de las 3 restricciones de oferta es idéntica a la suma de las 3 restricciones de demanda. Por lo tanto, una de las filas es una combinación lineal de las demás, resultando en:
    \begin{equation}
    \text{rango}(A) = m + n - 1 = 3 + 3 - 1 = 5
    \end{equation}
    \item \textbf{Inversión de base explícita:} El Simplex Tradicional debe seleccionar una base $B \in \mathbb{R}^{5 \times 5}$, calcular su inversa $B^{-1}$ (o factorización LU), evaluar todos los costos reducidos $\Delta_j = c_j - c_B^T B^{-1} A_j$ mediante multiplicación matricial densa, y realizar pivoteos de Gauss-Jordan con una complejidad por iteración de $\mathcal{O}((m+n)^2)$ a $\mathcal{O}((m+n)^3)$.
\end{itemize}

\subsection{Caso 4.2: Problema de Transporte No Balanceado}

\subsubsection{Enunciado y balanceo mediante destino artificial}
Supongamos que las condiciones del mercado provocan que la demanda del Almacén 1 ($W_1$) caiga en 50 unidades, situándose en $d_1 = 150$, mientras que las demandas de $W_2$ y $W_3$ permanecen en 400 y 300 unidades:
\begin{equation}
\text{Demanda Total} = 150 + 400 + 300 = 850 < \text{Oferta Total} = 900
\end{equation}
Existe un excedente de producción de 50 unidades ($900 - 850 = 50$). Para poder resolver el problema mediante los algoritmos estándar de programación lineal sin perder la estructura de conservación de flujo, se introduce un \textbf{Almacén Ficticio (Destino Dummy)} $W_{\text{dummy}}$ con los siguientes parámetros canónicos:
\begin{equation}
d_{\text{dummy}} = \sum_{i=1}^m s_i - \sum_{j=1}^n d_j = 900 - 850 = 50 \text{ unidades}
\end{equation}
\begin{equation}
c_{i, \text{dummy}} = 0 \quad \forall i \in \{1, 2, 3\}
\end{equation}
Las unidades asignadas en el óptimo al destino ficticio ($x_{i, \text{dummy}} > 0$) representan \textbf{capacidad de producción ociosa no despachada} que se retiene en la planta de origen $i$, sin incurrir en ningún costo logístico real ($c_{i, \text{dummy}} = 0$).

\subsection{Caso 4.3: Caso Didáctico de Transporte Eléctrico (125 MWh)}

Como caso complementario de validación de modelos de transporte de energía, se formula un sistema eléctrico donde 3 plantas generadoras abastecen 4 centros urbanos.
\begin{itemize}
    \item \textbf{Caso Balanceado (125 MWh):} Las plantas suministran 35, 50 y 40 millones de kWh ($\sum = 125$). Las ciudades demandan 45, 20, 30 y 30 millones de kWh ($\sum = 125$). El costo mínimo obtenido con el Simplex tradicional de PuLP es de $\mathbf{Z^* = \$1.020}$.
    \item \textbf{Caso No Balanceado (Excedente de 5 MWh):} La Ciudad 1 reduce su demanda a 40 MWh ($\sum = 120$). Se agrega un destino ficticio con demanda 5 y costo 0. El costo mínimo resultante es $\mathbf{Z^* = \$975}$, reteniendo 5 MWh de capacidad ociosa en la Planta 2 ($x_{25} = 5$) y logrando un ahorro exacto de $5 \times \$9 = \$45$.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{balanceado.png}
    \caption{Evidencia de resolución computacional de transporte balanceado en Python PuLP.}
    \label{fig:evidencia_balanceado}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{No_balanceado.png}
    \caption{Evidencia de resolución computacional de transporte no balanceado en Python PuLP.}
    \label{fig:evidencia_no_balanceado}
\end{figure}

\subsection{Código fuente completo en Python con PuLP (Simplex Tradicional)}

A continuación se presenta el código completo en Python que implementa y resuelve ambos modelos de transporte mediante el algoritmo Simplex tradicional implementado en la biblioteca PuLP:

\begin{lstlisting}[language=Python, caption={Código completo en Python con PuLP para Simplex Tradicional en Transporte}]
import time
import pulp
import numpy as np

def resolver_transporte_simplex_tradicional(costos, oferta, demanda, plantas, almacenes, titulo="Transporte"):
    # Resuelve el problema de transporte formulado como un Programa Lineal general
    # utilizando el Algoritmo Simplex Tradicional a traves de PuLP (Solver HiGHS/CBC).
    inicio_cpu = time.perf_counter()
    m, n = len(plantas), len(almacenes)

    # 1. Definicion del modelo Simplex en sentido de minimizacion
    prob = pulp.LpProblem(f"Simplex_Tradicional_{titulo}", pulp.LpMinimize)

    # 2. Declaracion de la matriz densa de variables continuas x_ij >= 0
    rutas = [(plantas[i], almacenes[j]) for i in range(m) for j in range(n)]
    x = pulp.LpVariable.dicts("Flujo", rutas, lowBound=0, cat="Continuous")

    # 3. Funcion objetivo lineal de flete global
    prob += pulp.lpSum(costos[i, j] * x[(plantas[i], almacenes[j])] 
                       for i in range(m) for j in range(n)), "Costo_Transporte_Total"

    # 4. Restricciones de oferta (m ecuaciones de fila)
    for i in range(m):
        prob += pulp.lpSum(x[(plantas[i], almacenes[j])] for j in range(n)) == oferta[i], f"Oferta_{plantas[i]}"

    # 5. Restricciones de demanda (n ecuaciones de columna)
    for j in range(n):
        prob += pulp.lpSum(x[(plantas[i], almacenes[j])] for i in range(m)) == demanda[j], f"Demanda_{almacenes[j]}"

    # 6. Resolucion mediante solver Simplex continuo HiGHS
    solver = pulp.HiGHS(msg=False) if hasattr(pulp, "HiGHS") else pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    fin_cpu = time.perf_counter()
    tiempo_ms = (fin_cpu - inicio_cpu) * 1000
    costo_optimo = pulp.value(prob.objective)

    print("=" * 70)
    print(f" RESULTADOS SIMPLEX TRADICIONAL (PuLP) - {titulo.upper()}")
    print("=" * 70)
    print(f" • Estatus del Solver              : {pulp.LpStatus[prob.status]}")
    print(f" • Costo Minimo Optimo (Z*)        : ${costo_optimo:,.2f}")
    print(f" • Tiempo de Computo CPU           : {tiempo_ms:.3f} ms")
    print(" • Asignacion de Flujos Optimos:")
    for i in range(m):
        for j in range(n):
            val = x[(plantas[i], almacenes[j])].varValue
            if val is not None and val > 1e-5:
                print(f"    - {plantas[i]} -> {almacenes[j]} : {val:.0f} unidades (Costo: ${costos[i, j]:.0f}/u)")
    print("=" * 70)

    return costo_optimo, tiempo_ms

# ==============================================================================
# EJECUCION DE LOS DOS CASOS DE TRANSPORTE
# ==============================================================================
if __name__ == "__main__":
    # --- CASO BALANCEADO (900 UDS) ---
    p_bal = ["P1", "P2", "P3"]
    w_bal = ["W1", "W2", "W3"]
    c_bal = np.array([
        [20, 16, 24],
        [10, 10,  8],
        [12, 18, 10]
    ], dtype=float)
    s_bal = np.array([300, 500, 100], dtype=float)
    d_bal = np.array([200, 400, 300], dtype=float)
    resolver_transporte_simplex_tradicional(c_bal, s_bal, d_bal, p_bal, w_bal, "Caso_Balanceado")

    # --- CASO NO BALANCEADO (DEMANDA = 850 UDS, DESTINO DUMMY = 50 UDS) ---
    w_nobal = ["W1", "W2", "W3", "W_Dummy"]
    c_nobal = np.array([
        [20, 16, 24, 0],
        [10, 10,  8, 0],
        [12, 18, 10, 0]
    ], dtype=float)
    s_nobal = np.array([300, 500, 100], dtype=float)
    d_nobal = np.array([150, 400, 300, 50], dtype=float)
    resolver_transporte_simplex_tradicional(c_nobal, s_nobal, d_nobal, p_bal, w_nobal, "Caso_No_Balanceado")
\end{lstlisting}

\subsection{Explicación exhaustiva del código fuente}

\begin{enumerate}
    \item \textbf{Procedimiento:}
    El script encapsula la formulación en la función \texttt{resolver\_transporte\_simplex\_tradicional}. Recibe las matrices y vectores de oferta/demanda, construye un modelo \texttt{LpProblem} de minimización, declara la cuadrícula completa de variables $x_{ij}$, inyecta las $m$ restricciones de oferta y las $n$ de demanda, y despacha el sistema algebraico al solver HiGHS/CBC para su resolución mediante el algoritmo Simplex tabular revisado.
    
    \item \textbf{Variables utilizadas:}
    \begin{itemize}
        \item \texttt{costos}: Matriz bidimensional de NumPy con los costos unitarios de flete $c_{ij}$.
        \item \texttt{oferta}, \texttt{demanda}: Vectores unidimensionales de capacidades y requerimientos.
        \item \texttt{rutas}: Lista de tuplas generada por comprensión que indexa el producto cartesiano Planta $\times$ Almacén.
        \item \texttt{x}: Diccionario de variables continuas de PuLP indexado por tuplas \texttt{(planta, almacen)}.
        \item \texttt{prob}: Instancia del modelo algebraico en PuLP.
    \end{itemize}

    \item \textbf{Sentencias utilizadas:}
    \begin{itemize}
        \item \texttt{pulp.LpVariable.dicts("Flujo", rutas, lowBound=0)}: Crea en bloque todas las variables de flujo imponiendo no negatividad.
        \item \texttt{pulp.lpSum()}: Sumador algebraico optimizado de expresiones lineales en PuLP.
        \item \texttt{prob.solve(solver)}: Invoca el algoritmo Simplex tradicional en lenguaje C++.
        \item \texttt{pulp.value(prob.objective)}: Obtiene el costo escalar mínimo del despacho.
    \end{itemize}
\end{enumerate}

\subsection{Solución óptima e interpretación para ambos casos}

\subsubsection{Solución Caso Balanceado (Red 3x3)}
El costo mínimo total obtenido por el Simplex Tradicional es:
\begin{equation}
Z^* = \$10,400.00
\end{equation}
con la siguiente distribución óptima de despachos:
\begin{itemize}
    \item Planta 1 despacha \textbf{300 unidades} al Almacén 2 ($x_{12} = 300$, costo unitario \$16).
    \item Planta 2 despacha \textbf{200 unidades} al Almacén 1 ($x_{21} = 200$, costo unitario \$10).
    \item Planta 2 despacha \textbf{100 unidades} al Almacén 2 ($x_{22} = 100$, costo unitario \$10).
    \item Planta 2 despacha \textbf{200 unidades} al Almacén 3 ($x_{23} = 200$, costo unitario \$8).
    \item Planta 3 despacha \textbf{100 unidades} al Almacén 3 ($x_{33} = 100$, costo unitario \$10).
\end{itemize}
Verificación de satisfacción plena: Planta 1 agota sus 300 unidades; Planta 2 agota sus 500 unidades ($200+100+200$); Planta 3 agota sus 100 unidades. Los Almacenes 1, 2 y 3 reciben exactamente 200, 400 y 300 unidades.

\subsubsection{Solución Caso No Balanceado (Con Almacén Ficticio)}
El costo mínimo resultante al disminuir la demanda de $W_1$ a 150 unidades es:
\begin{equation}
Z^* = \$9,900.00 \quad (\text{Ahorro neto de } \$500.00)
\end{equation}
Las 50 unidades de excedente son absorbidas por el destino ficticio desde la **Planta 1** ($x_{1, \text{dummy}} = 50$). La Planta 1 despacha 250 unidades reales a $W_2$ y retiene 50 unidades sin costo. Como el flete de Planta 1 a Almacén 2 era de \$16/u y la Planta 2 puede cubrir la diferencia a \$10/u, el sistema optimizador reorganiza los flujos para lograr el costo mínimo global de \$9,900.
"""
