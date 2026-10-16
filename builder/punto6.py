# -*- coding: utf-8 -*-

def get_punto6():
    return r"""
%================================================
\newpage
\section{Taller. Soluciones de problemas de PL con herramientas computacionales - PARTE 2 (Librería de Python asignada). Solución Problema de Asignación. Solución con el método simplex tradicional}
%================================================

\subsection{Historia y fundamentos teóricos del Problema de Asignación}

El \textbf{Problema de Asignación} es uno de los modelos combinatorios clásicos más estudiados en la investigación de operaciones y la microeconomía. Matemáticamente, representa un caso límite altamente degenerado del problema de transporte, caracterizado por una correspondencia biunívoca ($1$-a-$1$) donde el número de agentes u orígenes es exactamente igual al número de tareas o destinos ($m = n$), con capacidades de oferta unitarias ($s_i = 1$) y demandas unitarias ($d_j = 1$).

\subsubsection{El Teorema de Birkhoff-von Neumann y Unimodularidad Total}
El tratamiento del problema de asignación mediante programación lineal descansa sobre un resultado monumental de la geometría convexa: el \textbf{Teorema de Birkhoff-von Neumann} (Garrett Birkhoff, 1946; John von Neumann, 1953). Este teorema demuestra que el poliedro continuo de las matrices doblemente estocásticas:
\begin{equation}
\mathcal{D}_n = \left\{ X \in \mathbb{R}^{n \times n} : \sum_{j=1}^n x_{ij} = 1, \quad \sum_{i=1}^n x_{ij} = 1, \quad x_{ij} \geq 0 \right\}
\end{equation}
es exactamente la \textbf{envoltura convexa} del conjunto de las matrices de permutación $\mathcal{P}_n$. 

Dado que la matriz de restricciones del problema de asignación es \textbf{Totalmente Unimodular (TUM)} (Hoffman y Kruskal, 1956), todos los puntos extremos (vértices) del poliedro relajado continuo $\mathcal{D}_n$ son vectores estrictamente binarios con componentes $x_{ij} \in \{0, 1\}$. 

\textbf{Implicación fundamental para el Simplex Tradicional:}
Esta propiedad garantiza que al resolver el problema de asignación mediante el \textbf{Método Simplex Tradicional} (relajando $x_{ij} \in \{0, 1\}$ a $0 \leq x_{ij} \leq 1$), el algoritmo siempre convergerá en un vértice óptimo puramente entero sin requerir branch and bound ni ramificaciones combinatorias.

\subsection{Enunciado del problema de asignación de mantenimiento energético}

Una corporación del sector eléctrico debe programar el mantenimiento preventivo anual de tres centrales generadoras críticas:
\begin{itemize}
    \item \textbf{Central 1:} Central Hidroeléctrica de embalse.
    \item \textbf{Central 2:} Central Termoeléctrica de ciclo combinado.
    \item \textbf{Central 3:} Central Nuclear de potencia base.
\end{itemize}
Para realizar los trabajos técnicos especializados se contrata a tres empresas auxiliares de ingeniería de alta precisión: \textbf{Empresa A}, \textbf{Empresa B} y \textbf{Empresa C}. Debido a directrices contractuales y de disponibilidad de cuadrillas técnicas, rigen las siguientes restricciones:
\begin{enumerate}
    \item Cada empresa contratista sólo puede ser adjudicataria de exactamente una central eléctrica.
    \item Cada central eléctrica debe recibir el servicio de exactamente una empresa contratista.
\end{enumerate}
Las cotizaciones recibidas (costos de intervención $c_{ij}$ expresados en miles de euros, k\euro) se presentan en la siguiente matriz cuadrada de orden $3 \times 3$:

\begin{table}[H]
\centering
\caption{Matriz de costos unitarios de mantenimiento ($c_{ij}$ en miles de €)}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{lccc}
\toprule
\textbf{Empresa Auxiliar / Central} & \textbf{Central 1 (Hidro)} & \textbf{Central 2 (Termo)} & \textbf{Central 3 (Nuclear)} \\
\midrule
\textbf{Empresa A} & 10 & 9 & 5 \\
\textbf{Empresa B} & 9  & 8 & 3 \\
\textbf{Empresa C} & 6  & 4 & 7 \\
\bottomrule
\end{tabular}
\end{table}

Se requiere determinar la adjudicación de contratos que minimice el costo operativo total anual de la corporación utilizando el Método Simplex Tradicional a través de la biblioteca \textbf{PuLP} en Python.

\subsection{Modelo matemático formal (Simplex Tradicional Binario)}

\textbf{Variables de decisión binarias:}
\begin{equation}
x_{ij} = \begin{cases} 
1 & \text{si la Empresa } i \text{ realiza el mantenimiento de la Central } j \\ 
0 & \text{en caso contrario} 
\end{cases}
\end{equation}
para todo $i \in \{A, B, C\}$ y $j \in \{1, 2, 3\}$.

\textbf{Función objetivo:} Minimizar el costo financiero global de mantenimiento (en miles de €):
\begin{equation}
\min \quad Z = \sum_{i \in \{A, B, C\}} \sum_{j=1}^3 c_{ij} x_{ij}
\end{equation}

\textbf{Sujeto a las restricciones de asignación unívoca:}
\begin{align}
\sum_{j=1}^3 x_{ij} &= 1 \quad \forall i \in \{A, B, C\} \qquad \text{(Cada empresa atiende exactamente 1 central)} \\
\sum_{i \in \{A, B, C\}} x_{ij} &= 1 \quad \forall j \in \{1, 2, 3\} \qquad \text{(Cada central es atendida por 1 empresa)} \\
x_{ij} &\in \{0, 1\} \quad \forall i, j.
\end{align}

\subsection{Código fuente completo en Python con PuLP (Simplex Tradicional)}

A continuación se presenta el código completo en Python que modela y resuelve el problema de asignación mediante el Simplex Tradicional en PuLP:

\begin{lstlisting}[language=Python, caption={Código completo en Python con PuLP para Simplex Tradicional en Asignación}]
import time
import pulp

def resolver_asignacion_simplex_tradicional():
    # Resuelve el problema de asignacion de mantenimiento energetico
    # mediante el Metodo Simplex Tradicional implementado en PuLP (CBC/HiGHS).
    inicio_cpu = time.perf_counter()

    empresas = ["Empresa A", "Empresa B", "Empresa C"]
    centrales = ["Central 1", "Central 2", "Central 3"]
    costos = [
        [10, 9, 5],
        [ 9, 8, 3],
        [ 6, 4, 7]
    ]

    # 1. Definicion del modelo en sentido de minimizacion
    prob = pulp.LpProblem("Asignacion_Simplex_Tradicional_P6", pulp.LpMinimize)

    # 2. Declaracion de la cuadricula de variables binarias x_ij
    pares = [(i, j) for i in range(3) for j in range(3)]
    x = pulp.LpVariable.dicts("Asig", pares, cat="Binary")

    # 3. Funcion objetivo de costo total
    prob += pulp.lpSum(costos[i][j] * x[(i, j)] for i in range(3) for j in range(3)), "Costo_Total_kEUR"

    # 4. Restricciones de fila: Una central por cada empresa
    for i in range(3):
        prob += pulp.lpSum(x[(i, j)] for j in range(3)) == 1, f"Asignacion_Empresa_{empresas[i]}"

    # 5. Restricciones de columna: Una empresa por cada central
    for j in range(3):
        prob += pulp.lpSum(x[(i, j)] for i in range(3)) == 1, f"Cobertura_Central_{centrales[j]}"

    # 6. Resolucion computacional mediante solver Simplex
    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    fin_cpu = time.perf_counter()
    tiempo_ms = (fin_cpu - inicio_cpu) * 1000
    costo_optimo = pulp.value(prob.objective)

    print("=" * 70)
    print(" RESULTADOS SIMPLEX TRADICIONAL (PuLP) - PROBLEMA DE ASIGNACION (P6)")
    print("=" * 70)
    print(f" • Estatus de la Solucion        : {pulp.LpStatus[prob.status]}")
    print(f" • Costo Minimo Total Adjudicado : {costo_optimo:.0f} mil euros (17.000 €)")
    print(f" • Tiempo de Ejecucion CPU       : {tiempo_ms:.3f} ms")
    print(" • Plan de Adjudicacion Optimo:")
    for i in range(3):
        for j in range(3):
            if x[(i, j)].varValue == 1:
                print(f"    - {empresas[i]} -> {centrales[j]} : {costos[i][j]}k €")
    print("=" * 70)

    return costo_optimo, tiempo_ms

if __name__ == "__main__":
    resolver_asignacion_simplex_tradicional()
\end{lstlisting}

\subsection{Explicación exhaustiva del código fuente}

\begin{enumerate}
    \item \textbf{Procedimiento general:}
    \begin{itemize}
        \item Se parametriza la matriz de costos como una lista de listas indexada por enteros $0, 1, 2$.
        \item Se inicializa el modelo de optimización mediante la clase \texttt{LpProblem} con el flag de minimización.
        \item Se crea un diccionario de 9 variables binarias a través de la función utilitaria \texttt{pulp.LpVariable.dicts()} pasando la bandera declarativa \texttt{cat="Binary"}.
        \item Se formulan las $2n = 6$ ecuaciones de enlace unitarias utilizando bucles \texttt{for} combinados con el sumador lineal \texttt{pulp.lpSum()}.
        \item Se ejecuta el solver CBC y se filtran las rutas adjudicadas condicionando a \texttt{x[(i, j)].varValue == 1}.
    \end{itemize}

    \item \textbf{Variables utilizadas:}
    \begin{itemize}
        \item \texttt{empresas}, \texttt{centrales}: Listas de cadenas de texto con los identificadores cualitativos de los agentes y recursos.
        \item \texttt{costos}: Estructura matricial de datos con los coeficientes $c_{ij}$.
        \item \texttt{pares}: Lista de tuplas con las 9 combinaciones posibles de asignación.
        \item \texttt{x}: Diccionario de variables binarias indexado por tuplas \texttt{(i, j)}.
        \item \texttt{costo\_optimo}: Escalar numérico que almacena el valor mínimo de la función objetivo.
    \end{itemize}

    \item \textbf{Sentencias utilizadas:}
    \begin{itemize}
        \item \texttt{pulp.LpVariable.dicts(..., cat="Binary")}: Generador masivo de variables dicotómicas.
        \item Sobrecarga del operador relacional de igualdad \texttt{== 1}: Establece las restricciones de partición exacta.
        \item \texttt{prob.solve()}: Despacha el modelo hacia el solver Simplex subyacente.
    \end{itemize}
\end{enumerate}

\subsection{Solución óptima e interpretación gerencial}

La resolución mediante el Simplex Tradicional arroja un costo óptimo total de:
\begin{equation}
Z^* = 17 \text{ mil euros} \quad (17.000 \text{ \euro})
\end{equation}

\textbf{Distribución de adjudicación de contratos:}
\begin{itemize}
    \item \textbf{Empresa A $\to$ Central 1 (Hidroeléctrica):} Costo contractual de \textbf{10k \euro}.
    \item \textbf{Empresa B $\to$ Central 3 (Nuclear):} Costo contractual de \textbf{3k \euro}.
    \item \textbf{Empresa C $\to$ Central 2 (Termoeléctrica):} Costo contractual de \textbf{4k \euro}.
\end{itemize}

\textbf{Análisis de costo de oportunidad global:}
A primera vista, una toma de decisiones codiciosa (\textit{greedy}) podría verse tentada a asignar la Empresa A a la Central 3, dado que ofrece una tarifa baja de 5k \euro. Sin embargo, el análisis integral del Simplex Tradicional demuestra que la Empresa B tiene una ventaja comparativa aún mayor en la Central 3 (tarifa de 3k \euro). Al reservar a la Empresa B para la Central 3 y a la Empresa C para la Central 2 (4k \euro), la Empresa A debe asumir obligatoriamente la Central 1 (10k \euro). Cualquier otra combinación alternativa eleva la factura total (por ejemplo, asignar $A \to 3$, $B \to 2$, $C \to 1$ cuesta $5 + 8 + 6 = 19\text{k \euro}$, un sobrecosto del $11.7\%$).
"""
