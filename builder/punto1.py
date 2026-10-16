# -*- coding: utf-8 -*-

def get_punto1():
    return r"""
%================================================
\section{Taller. Solución parcial 1 y 4 casos especiales: Gráfico y Simplex, cada uno}
%================================================

\subsection{Fundamentación histórica y teórica de la Programación Lineal}

La \textbf{Programación Lineal (PL)} constituye uno de los avances matemáticos y operativos más trascendentales del siglo XX. Sus orígenes modernos se remontan a 1939, cuando el matemático soviético \textbf{Leonid Kantorovich} publicó su monografía pionera titulada \textit{``Métodos matemáticos para la organización y la producción''}, motivado por la optimización del corte de materiales de contrachapado y la programación del transporte ferroviario en la Unión Soviética. Por sus contribuciones seminales a la teoría de asignación óptima de recursos, Kantorovich fue galardonado con el Premio Nobel de Ciencias Económicas en 1975.

De manera paralela e independiente, en 1947, el matemático estadounidense \textbf{George Bernard Dantzig}, trabajando para el proyecto militar \textit{SCOOP} (\textit{Scientific Computation of Optimum Programs}) de la Fuerza Aérea de los Estados Unidos, formuló formalmente el modelo general de programación lineal e inventó el célebre \textbf{Método Simplex}. Ese mismo año, Dantzig visitó al ilustre matemático \textbf{John von Neumann} en el Instituto de Estudios Avanzados de Princeton; von Neumann reconoció inmediatamente la conexión estructural profunda entre la programación lineal y la teoría de juegos matriciales, sentando las bases analíticas del \textbf{Teorema de la Dualidad Lineal}.

\subsubsection{Formulación canónica y Teorema Fundamental}
Un problema de programación lineal en su forma estándar se define como:
\begin{equation}
\min \quad Z = c^T x \quad \text{sujeto a} \quad A x = b, \quad x \geq 0
\end{equation}
donde $A \in \mathbb{R}^{m \times n}$ con $\text{rango}(A) = m < n$, $b \in \mathbb{R}^m$, $c \in \mathbb{R}^n$ y $x \in \mathbb{R}^n$. El espacio de soluciones factibles $\mathcal{F} = \{x \in \mathbb{R}^n : Ax = b, x \geq 0\}$ define geométricamente un \textbf{poliedro convexo cerrado}. 

El \textbf{Teorema Fundamental de la Programación Lineal} postula que si el conjunto factible $\mathcal{F}$ no es vacío y posee al menos un punto extremo, y si el valor óptimo de $Z$ es finito, entonces existe al menos un \textbf{punto extremo (vértice)} de $\mathcal{F}$ que es una solución óptima. A nivel algebraico, cada vértice corresponde de manera unívoca a una \textbf{Solución Básica Factible (SBF)}, obtenida particionando la matriz $A = [B \mid N]$ en una base invertible $B \in \mathbb{R}^{m \times m}$ y un bloque no básico $N$, tal que $x_B = B^{-1}b \geq 0$ y $x_N = 0$.

No obstante la elegancia del método Simplex estándar, existen cuatro configuraciones polihédricas atípicas conocidas como los \textbf{Cuatro Casos Especiales de la Programación Lineal}. A continuación se analiza cada uno en profundidad desde la perspectiva geométrica y algebraico-tabular.

%------------------------------------------------
\subsection{Caso Especial 1: Degeneración (Degeneracy)}

\subsubsection{Fundamento geométrico en $\mathbb{R}^2$ y $\mathbb{R}^n$}
En un espacio bidimensional $\mathbb{R}^2$, un vértice estándar está determinado por la intersección de exactamente dos hiperplanos (rectas) de restricción activas. La \textbf{degeneración geométrica} ocurre cuando \textbf{tres o más restricciones concurrentes} intersectan exactamente en el mismo punto de coordenadas $(x_1^*, x_2^*)$. 

En el espacio general $\mathbb{R}^n$, un vértice factible se define por la intersección de $n$ hiperplanos linealmente independientes. Si en dicho vértice concurren $n + k$ hiperplanos (con $k \geq 1$), el vértice está geométricamente \textit{sobredeterminado}, existiendo múltiples combinaciones de variables que pueden ser seleccionadas para formar una base algebraica del mismo punto físico.

\begin{figure}[H]
\centering
\begin{tikzpicture}[scale=0.95]
    % Ejes coordenados
    \draw[-{Latex[length=3mm]}, thick] (-0.5,0) -- (6,0) node[right] {$x_1$};
    \draw[-{Latex[length=3mm]}, thick] (0,-0.5) -- (0,5.5) node[above] {$x_2$};
    
    % Restricciones concurrentes en (2,2)
    % R1: x1 + x2 <= 4 -> pasa por (0,4) y (4,0)
    \draw[blue, thick] (-0.2, 4.2) -- (4.5, -0.5) node[pos=0.15, above right] {$R_1: x_1 + x_2 \leq 4$};
    % R2: x1 <= 2 -> vertical
    \draw[red, thick] (2, -0.5) -- (2, 5) node[pos=0.9, right] {$R_2: x_1 \leq 2$};
    % R3: x2 <= 2 -> horizontal
    \draw[teal, thick] (-0.5, 2) -- (5, 2) node[pos=0.85, above] {$R_3: x_2 \leq 2$};
    
    % Region factible
    \fill[gray!25, opacity=0.7] (0,0) -- (2,0) -- (2,2) -- (0,2) -- cycle;
    \draw[thick] (0,0) -- (2,0) -- (2,2) -- (0,2) -- cycle;
    
    % Vertice degenerado
    \filldraw[purple] (2,2) circle (3pt) node[above right] {\textbf{Vértice Degenerado} $(2,2)$};
    \node at (1,1) {\textbf{Región Factible}};
\end{tikzpicture}
\caption{Representación gráfica de un punto extremo degenerado en $(2,2)$ por concurrencia de $R_1, R_2$ y $R_3$.}
\label{fig:deg_geometrica}
\end{figure}

\subsubsection{Manifestación tabular en el Método Simplex}
En el Simplex tabular, la degeneración se revela algebraicamente cuando se produce un \textbf{empate en la prueba de la razón mínima} para escoger la variable saliente:
\begin{equation}
\theta = \min_{i : y_{ik} > 0} \left\{ \frac{\bar{b}_i}{y_{ik}} \right\}
\end{equation}
Al presentarse un empate entre la fila $r$ y la fila $s$, ambas variables básicas alcanzan simultáneamente el valor cero cuando la variable entrante $x_k$ toma el valor $\theta$. Dado que sólo una de ellas puede abandonar la base (por ejemplo, $x_{Br}$), la otra variable empatada ($x_{Bs}$) permanece obligatoriamente en la base en la siguiente iteración pero con un valor idénticamente nulo:
\begin{equation}
\bar{b}_s^{(nuevo)} = 0
\end{equation}
Una solución básica factible donde al menos una variable básica es igual a cero se clasifica rigurosamente como una \textbf{Solución Básica Factible Degenerada}.

\subsubsection{El fenómeno de Ciclaje (Cycling) y reglas de Bland}
Cuando una base es degenerada ($\bar{b}_s = 0$), en una iteración posterior la prueba de la razón mínima puede arrojar $\theta = 0$. Como la función objetivo se actualiza según:
\begin{equation}
Z^{(nuevo)} = Z^{(actual)} - \theta \cdot \Delta_k
\end{equation}
si $\theta = 0$, se tiene $\Delta Z = 0$. El algoritmo ejecuta un pivoteo algebraico cambiando la columna de la base, pero el punto geométrico $(x_1, x_2)$ y el valor de $Z$ permanecen estrictamente estáticos. Si se presenta una secuencia consecutiva de pivotes con $\theta = 0$, el Simplex puede visitar cíclicamente un conjunto idéntico de bases repetidas, entrando en un \textbf{bucle infinito} denominado \textit{ciclaje}. Los primeros contraejemplos analíticos de ciclaje fueron construidos por Alan Hoffman (1953) y E. M. L. Beale (1955).

Para anular teóricamente el ciclaje se aplican mecanismos de prevención:
\begin{enumerate}
    \item \textbf{Regla del menor subíndice de Bland (Robert Bland, 1977):} Ante empates en la variable entrante (costo reducido más negativo), se selecciona aquella con el menor índice de variable $j$. De igual forma, ante empates en la razón mínima saliente, se expulsa la variable básica con el menor subíndice $i$. Bland demostró inductivamente que esta regla garantiza convergencia finita y excluye la repetición de bases.
    \item \textbf{Método de Perturbación de Abraham Charnes (1952) / Simplex Lexicográfico (Dantzig, Orden y Wolfe, 1954):} Consiste en sustituir el vector $b$ por un vector perturbado $b(\epsilon) = b + \sum_{j=1}^m \epsilon^j e_j$ para $\epsilon > 0$ infinitesimal, transformando todos los valores del lado derecho en polinomios independientes y eliminando empates con probabilidad 1.
\end{enumerate}

\begin{table}[H]
\centering
\caption{Tabla Simplex ilustrativa con presencia de base degenerada ($x_{B1} = 0$)}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{c|cccccc|c|c}
\toprule
\textbf{Base} & $x_1$ & $x_2$ & $s_1$ & $s_2$ & $s_3$ & $Z$ & \textbf{RHS} & \textbf{Razón Mínima} \\
\midrule
$s_1$ & 0 & 1 & 1 & -1 & 0 & 0 & \textbf{0} & $0 / 1 = 0$ (Saliente) \\
$x_1$ & 1 & 0 & 0 & 1 & 0 & 0 & 2 & -- \\
$s_3$ & 0 & 2 & 0 & 0 & 1 & 0 & 4 & $4 / 2 = 2$ \\
\midrule
$Z$   & 0 & -3 & 0 & 1 & 0 & 1 & 12 & $\Delta_2 = -3 < 0$ (Entrante) \\
\bottomrule
\end{tabular}
\end{table}

%------------------------------------------------
\subsection{Caso Especial 2: Soluciones Óptimas Múltiples (Infinitas Soluciones)}

\subsubsection{Fundamento geométrico en $\mathbb{R}^2$}
Se produce cuando el vector gradiente de la función objetivo $\nabla Z = c$ es paralelo al vector normal de una restricción activa que define una cara o arista del poliedro factible:
\begin{equation}
c = \lambda a_i \quad \text{para algún } \lambda > 0
\end{equation}
En consecuencia, la recta o hiperplano de nivel de la función objetivo ($c^T x = k$) se vuelve colineal y se superpone a todo el segmento de recta delimitado entre dos puntos extremos adyacentes $x^{(1)}$ y $x^{(2)}$.

\begin{figure}[H]
\centering
\begin{tikzpicture}[scale=0.95]
    % Ejes
    \draw[-{Latex[length=3mm]}, thick] (-0.5,0) -- (6,0) node[right] {$x_1$};
    \draw[-{Latex[length=3mm]}, thick] (0,-0.5) -- (0,5.5) node[above] {$x_2$};
    
    % Restriccion activa: x1 + x2 <= 4
    \draw[blue, thick] (-0.5, 4.5) -- (4.5, -0.5) node[pos=0.1, above right] {$x_1 + x_2 \leq 4$};
    % Restriccion x2 <= 3
    \draw[teal, thick] (-0.5, 3) -- (5, 3) node[pos=0.85, above] {$x_2 \leq 3$};
    % Restriccion x1 <= 3
    \draw[teal, thick] (3, -0.5) -- (3, 5) node[pos=0.85, right] {$x_1 \leq 3$};
    
    % Poligono factible
    \fill[gray!25, opacity=0.7] (0,0) -- (3,0) -- (3,1) -- (1,3) -- (0,3) -- cycle;
    \draw[thick] (0,0) -- (3,0) -- (3,1) -- (1,3) -- (0,3) -- cycle;
    
    % Segmento optimo resaltado
    \draw[red, line width=2.5pt] (3,1) -- (1,3);
    \filldraw[red] (3,1) circle (3pt) node[right] {$x^{(1)} = (3,1)$};
    \filldraw[red] (1,3) circle (3pt) node[left] {$x^{(2)} = (1,3)$};
    
    % Linea de nivel de la funcion objetivo Max Z = 2x1 + 2x2 = 8
    \draw[dashed, purple, thick] (0.2, 3.8) -- (3.8, 0.2) node[pos=0.9, above right] {$Z = 2x_1 + 2x_2 = 8$};
    \node[red] at (2.2,2.3) {\textbf{Infinitos Óptimos}};
\end{tikzpicture}
\caption{Soluciones óptimas múltiples a lo largo del segmento que une los vértices $(3,1)$ y $(1,3)$.}
\label{fig:optimos_multiples}
\end{figure}

\subsubsection{Manifestación tabular en el Método Simplex}
En la tabla simplex óptima (donde todos los costos reducidos satisfacen $\Delta_j \geq 0$ para minimización o $\Delta_j \leq 0$ para maximización), se verifica que al menos una \textbf{variable no básica} $x_k \notin \mathcal{B}$ posee un \textbf{costo reducido idénticamente nulo}:
\begin{equation}
\Delta_k = c_k - z_k = c_k - c_B^T B^{-1} A_k = 0
\end{equation}
Al seleccionar $x_k$ como variable entrante y aplicar el algoritmo de pivoteo estándar, la variable entra a la base con un valor estrictamente positivo $\theta > 0$. Sin embargo, el valor de la función objetivo experimenta un cambio nulo:
\begin{equation}
\Delta Z = \theta \cdot \Delta_k = \theta \cdot 0 = 0
\end{equation}
Esto produce una \textbf{segunda Solución Básica Factible Óptima} $x^{(2)}$ distinta de $x^{(1)}$, pero con el mismo valor óptimo $Z^*$.

\subsubsection{Teorema de la combinación convexa infinita}
Sea $\mathcal{S}^*$ el conjunto de puntos óptimos. Dado que el modelo es lineal, si $x^{(1)} \in \mathcal{S}^*$ y $x^{(2)} \in \mathcal{S}^*$, cualquier combinación convexa:
\begin{equation}
x(\alpha) = \alpha x^{(1)} + (1 - \alpha) x^{(2)}, \quad \forall \alpha \in [0, 1]
\end{equation}
cumple:
\begin{align}
A x(\alpha) &= A (\alpha x^{(1)} + (1 - \alpha) x^{(2)}) = \alpha A x^{(1)} + (1 - \alpha) A x^{(2)} = \alpha b + (1 - \alpha) b = b \\
c^T x(\alpha) &= \alpha c^T x^{(1)} + (1 - \alpha) c^T x^{(2)} = \alpha Z^* + (1 - \alpha) Z^* = Z^*
\end{align}
Por ende, existen infinitos puntos factibles que maximizan o minimizan exactamente el valor de $Z$.

\begin{table}[H]
\centering
\caption{Tabla Simplex Óptima 1 con variable no básica $x_2$ con costo reducido $\Delta_2 = 0$}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{c|ccccc|c|c}
\toprule
\textbf{Base} & $x_1$ & $x_2$ & $s_1$ & $s_2$ & $Z$ & \textbf{RHS} & \textbf{Razón Mínima} \\
\midrule
$x_1$ & 1 & 1 & 1 & 0 & 0 & 4 & $4 / 1 = 4$ \\
$s_2$ & 0 & 1 & -1 & 1 & 0 & 2 & $2 / 1 = \mathbf{2}$ (Saliente) \\
\midrule
$Z$   & 0 & \textbf{0} & 2 & 0 & 1 & 8 & $\Delta_2 = 0$ (Entrante Alternativa) \\
\bottomrule
\end{tabular}
\end{table}

%------------------------------------------------
\subsection{Caso Especial 3: Solución No Acotada (Unboundedness)}

\subsubsection{Fundamento geométrico y cono de recesión}
Un problema de programación lineal es no acotado cuando el poliedro factible $\mathcal{F}$ contiene una semirrecta o rayo que se extiende indefinidamente hacia el infinito en una dirección a lo largo de la cual la función objetivo mejora continuamente. Formalmente, existe una dirección de recesión $d \in \mathbb{R}^n$ ($d \neq 0, d \geq 0$) perteneciente al cono de recesión:
\begin{equation}
\text{rec}(\mathcal{F}) = \{ d \in \mathbb{R}^n : A d \leq 0, d \geq 0 \}
\end{equation}
tal que el producto interno con el gradiente de optimización satisface:
\begin{equation}
c^T d < 0 \quad (\text{en Minimización}) \qquad \text{o} \qquad c^T d > 0 \quad (\text{en Maximización})
\end{equation}
Bajo estas condiciones, para cualquier punto factible $x_0 \in \mathcal{F}$, el rayo $\{x_0 + \lambda d : \lambda \geq 0\} \subset \mathcal{F}$, y cuando $\lambda \to \infty$, $Z \to \pm \infty$.

\begin{figure}[H]
\centering
\begin{tikzpicture}[scale=0.95]
    % Ejes
    \draw[-{Latex[length=3mm]}, thick] (-0.5,0) -- (6,0) node[right] {$x_1$};
    \draw[-{Latex[length=3mm]}, thick] (0,-0.5) -- (0,5.5) node[above] {$x_2$};
    
    % Restriccion: x1 - x2 <= 1 -> x2 >= x1 - 1
    \draw[blue, thick] (-0.5, -1.5) -- (5.5, 4.5) node[pos=0.8, above left] {$x_1 - x_2 \leq 1$};
    % Restriccion: x2 >= 1
    \draw[teal, thick] (-0.5, 1) -- (5.5, 1) node[pos=0.2, above] {$x_2 \geq 1$};
    
    % Region no acotada
    \fill[gray!25, opacity=0.7] (0,1) -- (2,1) -- (5.5,4.5) -- (0,4.5) -- cycle;
    \draw[thick] (0,1) -- (2,1) -- (5.5,4.5);
    
    % Gradiente de crecimiento
    \draw[-{Latex[length=4mm]}, line width=1.5pt, red] (2,2) -- (4,4.5) node[right] {$\nabla Z \to \infty$};
    \node at (1.5,3.2) {\textbf{Región Abierta}};
    \node at (1.5,2.6) {\textbf{No Acotada}};
\end{tikzpicture}
\caption{Región factible no acotada en el sentido de optimización de la función objetivo.}
\label{fig:no_acotada}
\end{figure}

\subsubsection{Manifestación tabular en el Método Simplex}
En una tabla simplex intermedia, se elige una variable entrante $x_k$ con costo reducido favorable ($\Delta_k = c_k - z_k < 0$ para minimización o $> 0$ para maximización). Sin embargo, al evaluar los elementos de la columna de intercambio $y_k = B^{-1} A_k$, se constata que:
\begin{equation}
y_{ik} \leq 0, \quad \forall i = 1, \dots, m
\end{equation}
Al no existir ningún denominador $y_{ik} > 0$, la prueba de la razón mínima $\min \{ \bar{b}_i / y_{ik} : y_{ik} > 0 \}$ tiene un conjunto admisible \textbf{vacío}. Esto indica que la variable no básica $x_k$ puede incrementarse arbitrariamente sin que ninguna de las variables básicas actuales disminuya su valor hasta anularse; de hecho, al ser $y_{ik} \le 0$, las variables básicas crecen o permanecen constantes conforme $x_k \to \infty$. El algoritmo concluye formalmente que el problema es \textbf{no acotado}.

\begin{table}[H]
\centering
\caption{Tabla Simplex con detección de solución no acotada (columna $x_1 \leq 0$)}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{c|ccccc|c|c}
\toprule
\textbf{Base} & $x_1$ & $x_2$ & $s_1$ & $s_2$ & $Z$ & \textbf{RHS} & \textbf{Razón Mínima} \\
\midrule
$s_1$ & \textbf{-1} & 1 & 1 & 0 & 0 & 3 & Ninguna ($y_{11} < 0$) \\
$s_2$ & \textbf{0}  & 2 & 0 & 1 & 0 & 6 & Ninguna ($y_{21} = 0$) \\
\midrule
$Z$   & \textbf{-5} & 2 & 0 & 0 & 1 & 15 & $\Delta_1 = -5 < 0$ (No acotado) \\
\bottomrule
\end{tabular}
\end{table}

%------------------------------------------------
\subsection{Caso Especial 4: Región Factible Vacía (Infactibilidad)}

\subsubsection{Fundamento geométrico y Teorema de Farkas}
Ocurre cuando el sistema de desigualdades lineales y no negatividades que definen el modelo contiene contradicciones intrínsecas, de modo que la intersección de todos los semiespacios cerrados es el conjunto vacío:
\begin{equation}
\mathcal{F} = \{ x \in \mathbb{R}^n : A x \leq b, x \geq 0 \} = \emptyset
\end{equation}
Desde la perspectiva de la teoría de dualidad, el célebre \textbf{Lema de Farkas} (Gyula Farkas, 1902) establece que exactamente uno de los dos sistemas siguientes admite solución:
\begin{enumerate}
    \item Existe $x \in \mathbb{R}^n$ tal que $A x \leq b, x \geq 0$.
    \item Existe $y \in \mathbb{R}^m$ tal que $y^T A \geq 0, y \geq 0$ y $y^T b < 0$.
\end{enumerate}
Por ende, la infactibilidad primal se demuestra constructivamente encontrando un vector multiplicador dual $y \geq 0$ que produce una combinación lineal absurda de las restricciones (por ejemplo, $0 \leq -2$).

\begin{figure}[H]
\centering
\begin{tikzpicture}[scale=0.95]
    % Ejes
    \draw[-{Latex[length=3mm]}, thick] (-0.5,0) -- (6,0) node[right] {$x_1$};
    \draw[-{Latex[length=3mm]}, thick] (0,-0.5) -- (0,5.5) node[above] {$x_2$};
    
    % Restriccion 1: x1 + x2 <= 2
    \draw[blue, thick] (-0.5, 2.5) -- (2.5, -0.5) node[pos=0.2, above right] {$x_1 + x_2 \leq 2$};
    \fill[blue!15, opacity=0.5] (0,0) -- (2,0) -- (0,2) -- cycle;
    
    % Restriccion 2: x1 + x2 >= 4
    \draw[red, thick] (1, 4.5) -- (5, 0.5) node[pos=0.1, above right] {$x_1 + x_2 \geq 4$};
    \fill[red!15, opacity=0.5] (1,4.5) -- (5,0.5) -- (5.5,5.5) -- (0,5.5) -- cycle;
    
    \node[blue] at (0.8,0.7) {Semieje $\le 2$};
    \node[red] at (3.5,3.8) {Semieje $\ge 4$};
    \node at (2.8,2.2) {\textbf{INTERSECCIÓN VACÍA: } $\mathcal{F} = \emptyset$};
\end{tikzpicture}
\caption{Infactibilidad provocada por semiespacios mutuamente disjuntos.}
\label{fig:infactibilidad}
\end{figure}

\subsubsection{Manifestación tabular en Dos Fases y Gran M}
Dado que el origen $(0,0)$ viola las restricciones de tipo $\geq$ o $=$, se introducen variables artificiales $R_i \geq 0$:
\begin{itemize}
    \item \textbf{Método de las Dos Fases:} En la Fase 1 se minimiza la suma de las variables artificiales:
    \begin{equation}
    \min \quad W = \sum_{i=1}^m R_i
    \end{equation}
    Si al alcanzar la tabla óptima de la Fase 1 el valor final es $W^* > 0$, se concluye taxativamente que no existe ningún punto factible que satisfaga el sistema original simultáneamente.
    \item \textbf{Método de la Gran M:} Se penalizan las variables artificiales con un coeficiente $M \to \infty$ en la función objetivo. Si en la tabla final simplex se cumplen las condiciones de optimalidad pero al menos una variable artificial $R_i$ permanece en la base con valor estrictamente positivo ($R_i > 0$), el problema original es infactible.
\end{itemize}

\begin{table}[H]
\centering
\caption{Tabla final de Fase 1 confirmando infactibilidad con $W^* = 2 > 0$}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{c|cccccc|c}
\toprule
\textbf{Base} & $x_1$ & $x_2$ & $s_1$ & $e_2$ & $R_2$ & $W$ & \textbf{RHS} \\
\midrule
$s_1$ & 1 & 1 & 1 & 0 & 0 & 0 & 2 \\
$R_2$ & 0 & 0 & -1 & -1 & 1 & 0 & \textbf{2} \\
\midrule
$W$   & 0 & 0 & 1 & 1 & 0 & 1 & \textbf{2} (Óptimo de Fase 1: $W^* > 0$) \\
\bottomrule
\end{tabular}
\end{table}

%------------------------------------------------
\subsection{Espacio formal para la solución del Parcial 1}

De acuerdo con las instrucciones de la asignatura, se preserva el siguiente espacio estructurado para consignar formalmente el enunciado, formulación matemática, desarrollo analítico, gráfico bidimensional y tablas simplex correspondientes a la evaluación del Parcial 1:

\begin{figure}[H]
\centering
\fbox{
\begin{minipage}{0.92\textwidth}
\vspace{0.4cm}
\begin{center}
    \textbf{\large CUADERNO DE REGISTRO -- SOLUCIÓN PARCIAL 1}\\[0.2cm]
    \textit{Asignatura: Sistemas y Modelos -- Universidad Tecnológica de Bolívar}
\end{center}
\vspace{0.3cm}
\textbf{1. Enunciado oficial del problema asignado:}\\
\rule{\textwidth}{0.4pt}
\vspace{1.0cm}

\textbf{2. Modelo matemático canónico:}\\
\[
\text{Optimizar } Z = c_1 x_1 + c_2 x_2 \quad \text{sujeto a} \quad A x \le b, \quad x_1, x_2 \ge 0.
\]
\vspace{0.5cm}

\textbf{3. Resolución por el Método Gráfico y determinación de vértices:}\\
\rule{\textwidth}{0.4pt}
\vspace{1.5cm}

\textbf{4. Tablas del Algoritmo Simplex Tabular (Paso a Paso):}\\
\rule{\textwidth}{0.4pt}
\vspace{1.5cm}

\textbf{5. Solución óptima e interpretación ingenieril:}\\
\rule{\textwidth}{0.4pt}
\vspace{1.0cm}
\end{minipage}
}
\caption{Plantilla estandarizada para la incorporación de los desarrollos del Parcial 1.}
\label{fig:plantilla_parcial1}
\end{figure}
"""

