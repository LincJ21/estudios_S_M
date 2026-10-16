# -*- coding: utf-8 -*-

def get_punto2():
    return r"""
%================================================
\newpage
\section{Taller. Soluciones de problemas de PL con herramientas computacionales - PARTE 1 (PHP Simplex u otro)}
%================================================

\subsection{Fundamentación histórica de la Programación Lineal Entera y Branch and Bound}

El tratamiento de modelos donde las variables de decisión están restringidas a valores discretos o enteros constituye la disciplina de la \textbf{Programación Lineal Entera (PLE)}. Históricamente, resolver la relajación continua mediante el método Simplex y redondear las variables fraccionarias al entero más cercano demostró ser fatalmente erróneo: con frecuencia produce soluciones infactibles o subóptimas alejadas del verdadero óptimo global.

Para solventar esta limitación, en 1958 el matemático \textbf{Ralph E. Gomory} introdujo los \textbf{Planos Cortantes (Cutting Planes)}, agregando desigualdades lineales auxiliares que recortan el poliedro continuo sin eliminar ningún vértice entero factible. Poco después, en 1960, las investigadoras británicas \textbf{Ailsa H. Land} y \textbf{Alison G. Doig}, de la London School of Economics, publicaron en \textit{Econometrica} el trascendental algoritmo de \textbf{Ramificación y Acotación (Branch and Bound)}. En 1965, \textbf{R. J. Dakin} simplificó la técnica mediante una formulación de árbol binario directo basada en restricciones disyuntivas elementales:
\begin{equation}
x_j \leq \lfloor \bar{x}_j \rfloor \qquad \text{y} \qquad x_j \geq \lceil \bar{x}_j \rceil
\end{equation}
El algoritmo se fundamenta en tres principios rectores:
\begin{enumerate}
    \item \textbf{Ramificación (Branching):} Partición del espacio factible fraccionario en subproblemas disyuntos mutuamente excluyentes.
    \item \textbf{Acotación (Bounding):} Cálculo de cotas superiores (en maximización) e inferiores (en minimización) resolviendo la relajación lineal continua mediante el Simplex estándar en cada nodo del árbol.
    \item \textbf{Poda de Nodos (Fathoming):} Un nodo se poda y se suspende su exploración cuando se presenta una de tres condiciones:
    \begin{itemize}
        \item \textbf{Poda por infactibilidad:} La relajación continua del subproblema no tiene solución factible ($\mathcal{F}_k = \emptyset$).
        \item \textbf{Poda por cota:} El valor óptimo continuo del nodo es menor o igual (en maximización) a la mejor solución entera conocida hasta el momento (\textit{cota incumbente} $Z_I$).
        \item \textbf{Poda por integridad:} La solución continua resulta ser totalmente entera, actualizando la cota incumbente $Z_I \leftarrow \max(Z_I, Z_{nodo})$.
    \end{itemize}
\end{enumerate}

\subsection{Enunciado del problema de producción industrial}

Una planta manufacturera fabrica dos tipos de productos terminados, identificados como Producto 1 ($x_1$) y Producto 2 ($x_2$). Cada unidad del Producto 1 comercializada en el mercado genera un beneficio neto de \textbf{\$5.000}, mientras que cada unidad del Producto 2 produce un beneficio neto de \textbf{\$4.000}.

El proceso fabril depende estrictamente de dos recursos industriales escasos y no renovables durante el ciclo de planeación: \textbf{Recurso A} y \textbf{Recurso B}. Los requerimientos técnicos unitarios y la disponibilidad máxima se desglosan a continuación:
\begin{itemize}
    \item Cada unidad del Producto 1 requiere el consumo de 2 unidades del Recurso A y 1 unidad del Recurso B.
    \item Cada unidad del Producto 2 requiere el consumo de 1 unidad del Recurso A y 2 unidades del Recurso B.
    \item La empresa dispone de un inventario límite de exactamente \textbf{7 unidades del Recurso A} y \textbf{7 unidades del Recurso B}.
\end{itemize}

Por razones físico-operativas de entrega a clientes, las unidades producidas no pueden ser fraccionadas, exigiéndose que tanto $x_1$ como $x_2$ sean variables enteras no negativas. Se solicita modelar formalmente el problema y determinar la programación de producción óptima mediante el algoritmo de Branch and Bound asistido por la herramienta computacional \textbf{phpSimplex}.

\subsection{Modelo matemático formal}

\textbf{Definición de variables de decisión:}
\begin{itemize}
    \item $x_1 \in \mathbb{Z}_{\geq 0}$: Cantidad de unidades enteras a fabricar del Producto 1.
    \item $x_2 \in \mathbb{Z}_{\geq 0}$: Cantidad de unidades enteras a fabricar del Producto 2.
\end{itemize}

\textbf{Función objetivo:} Maximizar la ganancia total esperada (expresada en miles de \$):
\begin{equation}
\max \quad Z = 5 x_1 + 4 x_2
\end{equation}

\textbf{Sujeto a las restricciones tecnológicas de capacidad:}
\begin{align}
2 x_1 + 1 x_2 &\leq 7 \quad \text{(Disponibilidad máxima de Recurso A)} \\
1 x_1 + 2 x_2 &\leq 7 \quad \text{(Disponibilidad máxima de Recurso B)}
\end{align}

\textbf{Condiciones de no negatividad e integralidad:}
\begin{equation}
x_1, x_2 \geq 0, \qquad x_1, x_2 \in \mathbb{Z}.
\end{equation}

\subsection{Desarrollo analítico iterativo paso a paso en phpSimplex}

A continuación se documenta el árbol completo de ramificación y acotación ejecutado en la plataforma computacional \textbf{phpSimplex}, detallando cada subproblema con su soporte visual correspondiente:

\subsubsection{Paso 1: Solución de la Relajación Continua Inicial ($P_R$)}
Se formula el problema en phpSimplex prescindiendo inicialmente de la restricción de integralidad para encontrar la cota superior global inicial:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen1.png}
    \caption{Configuración del problema en phpSimplex (2 variables de decisión y 2 restricciones).}
    \label{fig:p2_img1}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen2.png}
    \caption{Definición de coeficientes de la función objetivo y matriz de recursos en phpSimplex.}
    \label{fig:p2_img2}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen3.png}
    \caption{Solución de la relajación continua ($P_R$): $Z = 21$, con $x_1 = 7/3 \approx 2.33, x_2 = 7/3 \approx 2.33$.}
    \label{fig:p2_img3}
\end{figure}

La solución continua del nodo raíz $P_R$ es:
\begin{equation}
x_1 = \frac{7}{3} \approx 2.333, \qquad x_2 = \frac{7}{3} \approx 2.333, \qquad Z = 21.00
\end{equation}
Al no ser valores enteros, se selecciona la variable $x_1$ para iniciar la ramificación dicotómica creando los subproblemas:
\begin{equation}
x_1 \leq \lfloor 2.333 \rfloor = 2 \quad (\text{Nodo } P_2) \qquad \text{y} \qquad x_1 \geq \lceil 2.333 \rceil = 3 \quad (\text{Nodo } P_3)
\end{equation}

\subsubsection{Paso 2: Primera ramificación sobre la variable $x_1$}

\textbf{Subproblema $P_2$ ($x_1 \leq 2$):}
Se añade la restricción $x_1 \leq 2$ al modelo original en phpSimplex:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen4.png}
    \caption{Formulación en phpSimplex del subproblema $P_2$ incorporando $x_1 \leq 2$.}
    \label{fig:p2_img4}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.48\textwidth]{Imagen5.png}
    \caption{Solución continua del subproblema $P_2$: $Z = 20$, con $x_1 = 2, x_2 = 2.5$ (fraccionario).}
    \label{fig:p2_img5}
\end{figure}

En $P_2$, se obtiene $x_1 = 2.0$, $x_2 = 2.5$ y $Z = 20.00$. Como $x_2$ sigue siendo no entero y su cota superior $Z = 20$ es prometedora, este nodo permanece como \textbf{candidato activo} para una posterior ramificación.

\textbf{Subproblema $P_3$ ($x_1 \geq 3$):}
Se añade la restricción $x_1 \geq 3$ en phpSimplex:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen6.png}
    \caption{Formulación en phpSimplex del subproblema $P_3$ incorporando $x_1 \geq 3$.}
    \label{fig:p2_img6}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen7.png}
    \caption{Solución continua del subproblema $P_3$: $Z = 19$, con $x_1 = 3, x_2 = 1$ (entera factible).}
    \label{fig:p2_img7}
\end{figure}

En $P_3$, la solución continua es $x_1 = 3.0$, $x_2 = 1.0$ y $Z = 19.00$. Dado que todas las variables son enteras, se ha descubierto la \textbf{primera solución entera factible}. Se establece la cota incumbente:
\begin{equation}
Z_I = 19.00 \quad (\text{con } x_1 = 3, x_2 = 1)
\end{equation}
El nodo $P_3$ queda formalmente \textbf{podado por integridad} (no requiere ramificaciones descendientes).

\subsubsection{Paso 3: Segunda ramificación sobre la variable $x_2$ desde el nodo $P_2$}
Retomando el nodo activo $P_2$ cuya cota es $Z = 20 > Z_I = 19$, se ramifica sobre la variable fraccionaria $x_2 = 2.5$:
\begin{equation}
x_2 \leq \lfloor 2.5 \rfloor = 2 \quad (\text{Nodo } P_4) \qquad \text{y} \qquad x_2 \geq \lceil 2.5 \rceil = 3 \quad (\text{Nodo } P_5)
\end{equation}

\textbf{Subproblema $P_4$ ($x_1 \leq 2, x_2 \leq 2$):}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen8.png}
    \caption{Formulación en phpSimplex del subproblema $P_4$ con $x_1 \leq 2$ y $x_2 \leq 2$.}
    \label{fig:p2_img8}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen9.png}
    \caption{Solución del subproblema $P_4$: $Z = 18$, con $x_1 = 2, x_2 = 2$ (entera pero inferior a la cota).}
    \label{fig:p2_img9}
\end{figure}

El nodo $P_4$ arroja una solución entera $x_1 = 2, x_2 = 2$ con $Z = 18.00$. Como $Z = 18 < Z_I = 19$, esta solución no mejora a la incumbente, por lo que $P_4$ queda \textbf{podado por cota}.

\textbf{Subproblema $P_5$ ($x_1 \leq 2, x_2 \geq 3$):}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen10.png}
    \caption{Formulación en phpSimplex del subproblema $P_5$ con $x_1 \leq 2$ y $x_2 \geq 3$.}
    \label{fig:p2_img10}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{Imagen11.png}
    \caption{Solución del subproblema $P_5$: $Z = 17$, con $x_1 = 1, x_2 = 3$ (entera pero inferior a la cota).}
    \label{fig:p2_img11}
\end{figure}

El nodo $P_5$ arroja una solución entera $x_1 = 1, x_2 = 3$ con $Z = 17.00$. Como $Z = 17 < Z_I = 19$, este nodo queda \textbf{podado por cota}.

\subsubsection{Paso 4: Árbol completo de Ramificación y Acotación}
Al no quedar ningún nodo activo en el árbol sin explorar, el algoritmo finaliza demostrando optimalidad global.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.42\textwidth]{imagen12.jpeg}
    \caption{Árbol completo de Branch and Bound confirmando la optimalidad global en el nodo $P_3$.}
    \label{fig:p2_arbol_completo}
\end{figure}

\subsection{Tabla sinóptica de los nodos del árbol}

\begin{table}[H]
\centering
\caption{Consolidado exhaustivo de subproblemas evaluados mediante Branch and Bound}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{ccccccc}
\toprule
\textbf{Nodo} & \textbf{Restricciones Adicionales} & $x_1$ & $x_2$ & \textbf{Valor $Z$} & \textbf{Naturaleza} & \textbf{Decisión de Poda} \\
\midrule
$P_R$ (Raíz) & Ninguna & $2.333$ & $2.333$ & 21.00 & Fraccionaria & Ramificar en $x_1$ \\
$P_2$ & $x_1 \leq 2$ & $2.000$ & $2.500$ & 20.00 & Fraccionaria & Ramificar en $x_2$ \\
\textbf{$P_3$} & $x_1 \geq 3$ & \textbf{3.000} & \textbf{1.000} & \textbf{19.00} & \textbf{Entera pura} & \textbf{Incumbente Óptimo} \\
$P_4$ & $x_1 \leq 2, x_2 \leq 2$ & $2.000$ & $2.000$ & 18.00 & Entera pura & Podado por cota ($18 < 19$) \\
$P_5$ & $x_1 \leq 2, x_2 \geq 3$ & $1.000$ & $3.000$ & 17.00 & Entera pura & Podado por cota ($17 < 19$) \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Solución óptima e interpretación empresarial}

La solución óptima entera global del modelo se ubica de forma unívoca en el \textbf{Nodo $P_3$}:
\begin{equation}
x_1^* = 3 \text{ unidades}, \qquad x_2^* = 1 \text{ unidad}, \qquad Z^* = \$19.000
\end{equation}

\textbf{Interpretación ingenieril y directiva:}
\begin{enumerate}
    \item \textbf{Plan de Producción Maestro:} La dirección de operaciones debe programar la manufactura de exactamente \textbf{3 unidades del Producto 1} y \textbf{1 unidad del Producto 2}, logrando la ganancia máxima factible de \textbf{\$19.000}.
    \item \textbf{Agotamiento del Recurso A (Cuello de Botella):} El consumo real de Recurso A es $2(3) + 1(1) = 7$ unidades. El inventario se agota en su totalidad ($100\%$ de utilización). Representa la restricción activa crítica que limita la expansión de las ganancias.
    \item \textbf{Holgura del Recurso B:} El consumo real de Recurso B es $1(3) + 2(1) = 5$ unidades. Se registra una holgura ocia de $7 - 5 = 2$ unidades no utilizadas, las cuales pueden ser destinadas a mantenimiento preventivo o reasignadas a otras líneas productivas.
\end{enumerate}
"""

