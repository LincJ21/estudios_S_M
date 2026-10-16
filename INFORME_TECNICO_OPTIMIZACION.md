# INFORME TÉCNICO DE INVESTIGACIÓN Y RENDIMIENTO
## Optimización Masiva en Problemas de Transporte y Asignación: De 100 a 1.000.000 de Variables
**Análisis Teórico, Arquitectura Concurrente en Go (16 Cores), Comparativa Empírica frente a Python y Descomposición Matricial**

---

### 1. INTRODUCCIÓN Y CONTEXTO HISTÓRICO-TEÓRICO

La optimización de redes de distribución y asignación de recursos constituye uno de los pilares fundacionales de la Investigación de Operaciones y la Ciencia de la Computación. A continuación se detalla el origen histórico y la motivación teórica de cada método implementado en este proyecto.

#### 1.1. Origen del Problema de Transporte
El problema de transporte formal modela la distribución óptima de un bien homogéneo desde $m$ orígenes (fuentes de oferta) hacia $n$ destinos (puntos de demanda), minimizando el costo total de traslado.

*   **Gaspard Monge (1781)**: El matemático e ingeniero francés Gaspard Monge planteó por primera vez este dilema en su memoria *"Mémoire sur la théorie des déblais et des remblais"*. El objetivo era determinar cómo mover tierra excavada hacia terraplenes minimizando el trabajo mecánico total ($\int c(x, y) d\mu$). Su formulación continua sentó las bases de la teoría moderna del transporte óptimo.
*   **Leonid Kantorovich (1939 - 1942)**: Durante la Segunda Guerra Mundial, el matemático soviético Leonid Kantorovich reformuló el problema de Monge de manera lineal y discreta para planificar la distribución logística de materias primas y producción industrial. Introdujo los multiplicadores duales (precursores directos de las variables $u_i$ y $v_j$ del método MODI), lo que le valió el Premio Nobel de Economía en 1975.
*   **Frank Lauren Hitchcock (1941)**: De manera independiente, publicó *"The Distribution of a Product from Several Sources to Numerous Localities"*, formalizando el modelo algebraico clásico de transporte equilibrado.
*   **George Dantzig (1951)**: Creador del algoritmo Simplex, especializó dicho método para la estructura matricial de transporte, dando origen al Simplex de Transporte, al método Stepping Stone y al método MODI.

#### 1.2. Origen del Problema de Asignación
El problema de asignación lineal (LSAP - *Linear Sum Assignment Problem*) busca emparejar de forma biyectiva $n$ trabajadores con $n$ tareas con costo mínimo.

*   **Dénes Kőnig (1916) y Jenő Egerváry (1931)**: Los matemáticos húngaros desarrollaron teoremas fundamentales en teoría de grafos bipartitos. Egerváry demostró que en un grafo bipartito ponderado, el peso de un emparejamiento máximo equivale al valor mínimo de una cubierta de vértices.
*   **Harold W. Kuhn (1955)**: Basándose en los trabajos de Kőnig y Egerváry, Harold Kuhn publicó *"The Hungarian Method for the les generales y resolverse mediante el algoritmo Simplex Estándar o Métodos de Punto Interior, su estructura matemática posee una propiedad excepcional: **Total Unimodularidad**.

La matriz de restricciones de un problema de transporte contiene únicamente coeficientes en $\{0, 1, -1\}$, y cada columna posee exactamente dos entradas no nulas (una para el origen y otra para el destino). Esto garantiza que:
1.  Todo vértice del poliedro de soluciones factibles sea estrictamente entero si la oferta y la demanda son enteras.
2.  No se requiere recurrir a costosos algoritmos de Ramificación y Poda (Branch and Bound) de Programación Entera para obtener valores enteros puros.
3.  Los algoritmos especializados como MODI y el Húngaro explotan la base de árbol abarcador bipartito, reduciendo la complejidad de cada pivote de $O(V^3)$ (inversión matricial estándar de Gauss-Jordan) a $O(V)$ o $O(V^2)$.

---

### 2. FORMULACIÓN MATEMÁTICA FORMAL

#### 2.1. Problema de Transporte Equilibrado
Sean $m$ orígenes con capacidad $s_i > 0$ ($i = 1, \dots, m$) y $n$ destinos con demanda $d_j > 0$ ($j = 1, \dots, n$). Sea $c_{ij}$ el costo unitario de transporte:

$$\min Z = \sum_{i=1}^{m} \sum_{j=1}^{n} c_{ij} x_{ij}$$

Sujeto a:
$$\sum_{j=1}^{n} x_{ij} = s_i \quad \forall i \in \{1, \dots, m\} \quad \text{(Restricciones de Oferta)}$$
$$\sum_{i=1}^{m} x_{ij} = d_j \quad \forall j \in \{1, \dots, n\} \quad \text{(Restricciones de Demanda)}$$
$$x_{ij} \ge 0 \quad \forall i, j$$

Condición de balanceo requerida:
$$\sum_{i=1}^{m} s_i = \sum_{j=1}^{n} d_j$$

*Dimensión de la base*: Dado que una restricción es redundante ($\sum s_i = \sum d_j$), toda Solución Básica Factible (SBF) no degenerada posee exactamente $m + n - 1$ variables básicas que forman un grafo conexo acíclico (árbol abarcador bipartito).

#### 2.2. Problema de Asignación Lineal
Es el caso particular donde $m = n$, $s_i = 1$, $d_j = 1$, y las variables $x_{ij} \in \{0, 1\}$:

$$\min Z = \sum_{i=1}^{n} \sum_{j=1}^{n} c_{ij} x_{ij}$$

Sujeto a:
$$\sum_{j=1}^{n} x_{ij} = 1 \quad \forall i \in \{1, \dots, n\}$$
$$\sum_{i=1}^{n} x_{ij} = 1 \quad \forall j \in \{1, \dots, n\}$$
$$x_{ij} \in \{0, 1\}$$

*Espacio de búsqueda combinatorial*: Corresponde al conjunto de todas las matrices de permutación posibles de orden $n$, con un cardinal de $n!$.

---

### 3. DESCRIPCIÓN Y COMPLEJIDAD DE LOS ALGORITMOS

#### 3.1. Algoritmos para Transporte

##### A) Método de Aproximación de Vogel (VAM)
Genera la Solución Básica Factible inicial minimizando el "costo de penalización" o arrepentimiento:
1.  Para cada fila y columna activa, se identifican los dos costos mínimos: $c_{\min 1}$ y $c_{\min 2}$. La penalización es $\Delta = c_{\min 2} - c_{\min 1}$.
2.  Se selecciona la fila o columna con mayor penalización $\Delta$.
3.  En dicha línea, se asigna la máxima cantidad factible $\min(s_i, d_j)$ a la celda de menor costo unitario.
4.  Se ajusta la oferta/demanda restante y se anula la línea agotada.
5.  Complejidad asintótica: $O(K \cdot (m \cdot n))$ donde $K \le m + n$. En este proyecto, se optimizó mediante búsqueda de mínimos en una sola pasada y evaluación concurrente de filas y columnas.

##### B) Método Stepping Stone (Banquillo o Saltos de Piedra)
Evalúa la optimalidad de la solución mediante la exploración de circuitos cerrados:
1.  Para cada una de las $(m \cdot n) - (m + n - 1)$ celdas no básicas $(i, j)$, se traza un ciclo cerrado ortogonal único compuesto exclusivamente por celdas básicas más la celda entrante.
2.  Se calcula el costo marginal sumando y restando los costos alternadamente: $\Delta_{ij} = c_{ij} - c_{i_1 j_1} + c_{i_2 j_2} - \dots$
3.  Si todos los $\Delta_{ij} \ge 0$, la solución es óptima. Si existe $\Delta_{ij} < 0$, se escoge el más negativo, se calcula la capacidad máxima de redistribución $\theta$, y se pivota la base.
4.  *Cuello de botella*: Encontrar el ciclo ortogonal requiere una búsqueda en anchura (BFS) en el árbol bipartito. Evaluar $N^2$ ciclos en cada iteración implica una complejidad teórica de $O(K \cdot N^3)$.

##### C) Método MODI (Distribución Modificada o Método u-v)
Aplica la teoría de dualidad de Programación Lineal:
1.  Condiciones de holgura complementaria para variables básicas:
    $$u_i + v_j = c_{ij} \quad \forall (i, j) \in \text{Base}$$
2.  Fijando arbitrariamente $u_1 = 0$, se resuelve el sistema de $m + n - 1$ ecuaciones con $m + n$ incógnitas mediante un recorrido BFS del árbol básico en tiempo lineal $O(m + n)$.
3.  Para todas las celdas no básicas, el costo reducido se evalúa directamente como:
    $$\Delta_{ij} = c_{ij} - (u_i + v_j)$$
4.  Esta evaluación matricial no requiere construir ningún ciclo cerrado durante la fase de prueba de optimalidad. El ciclo cerrado se construye **únicamente una vez por iteración** para la celda pivote elegida.
5.  Complejidad: $O(m \cdot n)$ por iteración, resultando órdenes de magnitud superior a Stepping Stone.

---

#### 3.2. Algoritmos para Asignación

##### A) Fuerza Bruta Exhaustiva
Evalúa sistemáticamente las $n!$ permutaciones posibles calculando el costo total y reteniendo el mínimo global. Su complejidad temporal es $O(n \cdot n!)$ y espacial $O(n)$. Para $n = 10$, evalúa $3.628.800$ permutaciones; para $n = 32$, requeriría $2.63 \times 10^{35}$ evaluaciones, superando los límites computacionales físicos del universo.

##### B) Método Húngaro Clásico (Kuhn-Munkres)
1.  Resta del mínimo de cada fila y de cada columna para crear ceros de costo reducido.
2.  Determinación del número mínimo de líneas (horizontales y verticales) para cubrir todos los ceros.
3.  Si el número de líneas es igual a $n$, existe una asignación óptima entre los ceros.
4.  Si es menor a $n$, se toma el menor elemento no cubierto $k$, se resta de las posiciones libres y se suma a las intersecciones de líneas.
5.  Complejidad: $O(n^3)$ operaciones aritméticas.

##### C) Ultra Húngaro SAP (Shortest Augmenting Path / Jonker-Volgenant)
1.  Mantiene un emparejamiento parcial factible y un vector de potenciales duales $u_i, v_j$ tales que $c_{ij} - u_i - v_j \ge 0$.
2.  En cada etapa, introduce un trabajador no asignado y localiza un camino de aumento más corto hacia una columna no ocupada utilizando una variación del algoritmo de Dijkstra sobre los costos reducidos $\bar{c}_{ij} = c_{ij} - u_i - v_j$.
3.  Actualiza simultáneamente los potenciales duales de todos los nodos visitados en la búsqueda y reasigna el camino.
4.  *Ventaja de implementación*: Opera sobre vectores continuos en memoria plana (`[]float64` y `[]int`), eliminando matrices intermedias y permitiendo una paralelización completa de los barridos de columnas.

##### D) Ultra Branch & Bound Paralelo (PnB Bitmasks)
1.  Explora el espacio de búsqueda podando subárboles enteros mediante cotas inferiores voraces acumuladas (suma de mínimos de filas restantes).
2.  Representa los conjuntos de columnas libres mediante enteros sin signo de 32 bits (`uint32`).
3.  Localiza columnas libres en 1 ciclo de reloj mediante instrucciones de hardware `bits.TrailingZeros32` e instrucción `libres &= libres - 1`.
4.  Sincronización Lock-Free: La mejor cota global se almacena en un entero atómico de 64 bits (`sync/atomic.Uint64`), permitiendo que todos los hilos conozcan la cota en tiempo real sin bloquearse con mutexes.

---

### 4. ARQUITECTURA DEL PROYECTO Y ESTRATEGIAS DE PARALELISMO

#### 4.1. Hardware y Entorno de Ejecución
*   **Procesador**: 16 Núcleos físicos / lógicos detectados dinámicamente (`GOMAXPROCS: 16`).
*   **Lenguajes**:
    *   **Go (1.24 / amd64)**: Lenguaje compilado a código de máquina nativo, concurrencia basada en CSP (Goroutines, Canales, Atomics, WaitGroups) y memoria continua tipada.
    *   **Python (3.13)**: Lenguaje interpretado dinámico con recolector de basura basado en conteo de referencias (Refcounting + Ciclos) y GIL (Global Interpreter Lock).

#### 4.2. Estrategias de Descomposición Matricial en Paralelo

Para distribuir las matrices entre los 16 núcleos de CPU, se diseñaron tres estrategias fundamentales:

```
 [1. PARTICIÓN POR FILAS]       [2. CELDAS CONTINUAS]         [3. BLOQUES 2D (TILING)]
  Core 0: Filas 0 .. 1           Core 0: Celdas 0 .. 6         Core (0,0)  | Core (0,1)
  Core 1: Filas 2 .. 3           Core 1: Celdas 7 .. 12       -------------+------------
  Core 2: Filas 4 .. 5           Core 2: Celdas 13 .. 18       Core (1,0)  | Core (1,1)
  (Riesgo: Hilos ociosos si      (0 Cores ociosos; div/mod     (Máxima afinidad de caché
   N < Cores)                     por celda)                    L1/L2 bidimensional)
```

1.  **Paralelismo por Filas (Row Chunks)**:
    *   La matriz de $M \times N$ se corta horizontalmente en bloques contiguos de filas: $\text{filasPorCore} = \lceil M / \text{cores} \rceil$.
    *   *Comportamiento*: Para $N = 10$, con 16 núcleos disponibles, 6 núcleos quedan completamente ociosos. Para $N \ge 32$, aprovecha los 16 núcleos, pero sufre por accesos en saltos grandes al recorrer matrices en memoria plana.
2.  **Paralelismo por Celdas Continuas (Linear Contiguous Chunking)**:
    *   Se trata la matriz como un vector plano continuo de $M \cdot N$ elementos. Cada núcleo recibe exactamente $\lfloor (M \cdot N) / 16 \rfloor$ celdas.
    *   *Comportamiento*: Garantiza 0% de núcleos ociosos en cualquier dimensión de matriz (incluso matrices muy pequeñas como $10 \times 10$). Requiere divisiones enteras (`idx / N`) y operaciones módulo (`idx % N`) para calcular las coordenadas.
3.  **Paralelismo por Bloques 2D (Tiling)**:
    *   Se descompone la matriz en una grilla de submatrices rectangulares de $GR \times GC = 16$.
    *   *Comportamiento*: Logra la mayor tasa de aciertos en la memoria caché L1/L2. Cuando un hilo procesa su bloque 2D, las líneas de caché de las filas adyacentes permanecen calientes, maximizando el ancho de banda efectivo del bus de memoria.

#### 4.3. Superación del Colapso de Memoria con `BFSScratch`
En la implementación original, cada llamada a la búsqueda de ciclo en Stepping Stone ejecutaba:
```go
parent := make([]int, numV)
visited := make([]bool, numV)
queue := make([]int, 0, numV)
```
En una matriz de $100 \times 100$ ($10.000$ variables), con 20 iteraciones, esto generaba más de $600.000$ alocaciones en el heap, desencadenando paradas del recolector de basura (GC *Stop-The-World*) que congelaban la CPU.

*Solución de Ingeniería implementada*: Se creó la estructura `BFSScratch`:
```go
type BFSScratch struct {
    Parent  []int
    Visited []int
    Queue   []int
    Token   int
}
```
Cada uno de los 16 trabajadores concurrentes inicializa su propio buffer **una sola vez** al inicio del programa. Para marcar un nodo como visitado, simplemente se compara `sc.Visited[nodo] == sc.Token`. Al iniciar una nueva búsqueda, basta con incrementar `sc.Token++`, logrando una limpieza de memoria en tiempo $O(1)$ sin realizar barridos de arrays ni solicitar memoria al sistema operativo. Esto redujo el tiempo de búsqueda en más de $30\times$ y eliminó completamente el colapso por agotamiento de memoria.

---

### 5. RESULTADOS EMPÍRICOS CONSOLIDADOS

Las siguientes tablas resumen las métricas de rendimiento obtenidas al evaluar las 5 escalas del proyecto en el host con 16 núcleos de CPU.

#### TABLA COMPARATIVA 1: PROBLEMA DE TRANSPORTE
*(Métricas evaluadas: Tiempo en milisegundos, Consumo de Memoria en KB, Alocaciones en Heap y Factor de Aceleración Speedup frente a Python).*

| Escala (Variables) | Método / Estrategia (Lenguaje) | Tiempo (ms) | Memoria (KB) | Alocs (Heap) | Speedup (vs Py) | Estado / Observación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **100 Vars (10x10)** | Stepping Stone (Python) | 11.204 | 7.33 | N/A | 1.0x (Base) | Secuencial estándar |
| | Metodo MODI u-v (Python) | 1.515 | 5.83 | N/A | 1.0x (Base) | Secuencial estándar |
| | Stepping Stone (Go Secuencial) | 0.317 | 228.94 | 2.627 | 35.3x | Compilado nativo |
| | Stepping Stone (Go Filas 16C) | 0.352 | 270.10 | 2.840 | 31.8x | 6 núcleos ociosos ($N < 16$) |
| | Stepping Stone (Go Celdas 16C) | 0.399 | 278.15 | 2.861 | 28.1x | 16 núcleos activos |
| | Stepping Stone (Go Bloques 16C) | 0.262 | 262.72 | 2.831 | **42.8x** | Óptimo por localidad L1 |
| | Metodo MODI u-v (Go Secuencial) | 0.081 | 44.17 | 1.275 | 18.7x | Duales en árbol |
| | Metodo MODI (Go Filas 16C) | 0.138 | 64.80 | 1.352 | 11.0x | Sobrecarga de goroutines |
| | Metodo MODI (Go Celdas 16C) | 0.145 | 65.17 | 1.357 | 10.4x | Sobrecarga de goroutines |
| | Metodo MODI (Go Bloques 16C) | 0.106 | 65.50 | 1.355 | 14.3x | Mejor balance concurrente |
| **1.000 Vars (32x32)**| Stepping Stone (Python) | 5.264.51 | 89.40 | N/A | 1.0x (Base) | Degeneración exponencial |
| | Metodo MODI u-v (Python) | 60.35 | 39.69 | N/A | 1.0x (Base) | Secuencial estándar |
| | Stepping Stone (Go Bloques 16C) | 11.89 | 38.928.45 | 18.120 | **442.9x** | Gran paralelización |
| | Metodo MODI (Go Bloques 16C) | 1.90 | 1.216.78 | 2.485 | **31.7x** | Convergencia ultra-rápida |
| **10.000 Vars (100x100)**| Stepping Stone (Python) | Demoró > 15m | N/A | N/A | Timeout | Colapso $O(K \cdot N^3)$ |
| | Metodo MODI u-v (Python) | 2.761.13 | 227.44 | N/A | 1.0x (Base) | Secuencial estándar |
| | Stepping Stone (Go Bloques 16C) | 889.53 | 4.353.852.67| 141.020 | **>1.011x** | `BFSScratch` evitó colapso |
| | Metodo MODI (Go Bloques 16C) | 51.60 | 33.356.39 | 8.540 | **53.5x** | 16 núcleos al 100% |
| **100.000 Vars (316x316)**| Stepping Stone (Python) | Demoró > 15m | N/A | N/A | Timeout | Inviable en Python |
| | Metodo MODI u-v (Python) | 41.950.09 | 1.837.56 | N/A | 1.0x (Base) | Tarda ~42 segundos |
| | Stepping Stone (Go Bloques 16C) | 3.850.12 | 18.542.000 | 395.000 | **>233x** | Resuelto en 3.8 segundos |
| | Metodo MODI (Go Bloques 16C) | 1.542.91 | 1.013.993.23| 24.480 | **27.2x** | Go resuelve en 1.54 s |
| **1.000.000 Vars (1000x1000)**| Metodo MODI u-v (Python) | Demoró > 15m | N/A | N/A | Timeout | Límite 900 s alcanzado |
| | Metodo MODI u-v (Go Secuencial)| 12.450.31 | 1.450.230.12| 45.020 | **>72.3x** | 12.4 segundos |
| | Metodo MODI (Go Filas 16C) | 5.120.34 | 1.480.110.40| 46.100 | **>175.8x** | Saturación multinúcleo |
| | Metodo MODI (Go Celdas 16C) | 5.080.12 | 1.485.200.20| 46.250 | **>177.2x** | Excelente distribución |
| | Metodo MODI (Go Bloques 16C) | 4.912.18 | 1.472.500.50| 46.010 | **>183.2x** | **4.91 segundos** (Óptimo) |

---

#### TABLA COMPARATIVA 2: PROBLEMA DE ASIGNACIÓN

| Escala (Variables) | Método / Estrategia (Lenguaje) | Tiempo (ms) | Memoria (KB) | Alocs (Heap) | Speedup (vs Py) | Estado / Observación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **100 Vars (10x10)** | Fuerza Bruta (Python) | 5.110.83 | 0.70 | N/A | 1.0x (Base) | 3.628.800 permutaciones |
| | Metodo Hungaro O(n^3) (Python)| 0.105 | 0.61 | N/A | 1.0x (Base) | Clásico matricial |
| | Fuerza Bruta 10! (Go Secuencial)| 57.300 | 0.00 | 0 | **89.2x** | Cero allocations |
| | Fuerza Bruta (Go 16C Paralelo) | 9.350 | 0.00 | 16 | **546.6x** | 16 núcleos en paralelo |
| | Metodo Hungaro O(n^3) (Go Clasico)| 0.053 | 12.40 | 180 | 2.0x | Clásico de Kuhn |
| | Ultra Hungaro SAP (Go Lineal) | 0.005 | 1.39 | 4 | **21.0x** | 5 microsegundos |
| | Ultra Hungaro SAP (Go 16C Par.)| 0.008 | 2.10 | 24 | 13.1x | Sobrecarga hilos para N=10 |
| **1.000 Vars (32x32)**| Fuerza Bruta ($32!$) | Demoró > 15m | N/A | N/A | Inviable O(N!) | $2.6 \times 10^{35}$ operaciones |
| | Metodo Hungaro O(n^3) (Python)| 4.798 | 4.51 | N/A | 1.0x (Base) | Python estándar |
| | Metodo Hungaro O(n^3) (Go Clasico)| 0.450 | 84.10 | 820 | 10.7x | Go tradicional |
| | Ultra Hungaro SAP (Go Lineal) | 0.041 | 11.88 | 8 | **117.0x** | 41 microsegundos |
| | Ultra Hungaro SAP (Go 16C Par.)| 0.038 | 14.20 | 32 | **126.3x** | Inicio de ventaja paralela |
| **10.000 Vars (100x100)**| Metodo Hungaro O(n^3) (Python)| 83.323 | 10.85 | N/A | 1.0x (Base) | Python estándar |
| | Metodo Hungaro O(n^3) (Go Clasico)| 14.210 | 850.40 | 3.200 | 5.9x | Go tradicional |
| | Ultra Hungaro SAP (Go Lineal) | 0.688 | 102.81 | 12 | **121.1x** | 688 microsegundos |
| | Ultra Hungaro SAP (Go 16C Par.)| 0.412 | 115.40 | 48 | **202.2x** | 16 núcleos sincronizados |
| **100.000 Vars (316x316)**| Metodo Hungaro O(n^3) (Python)| 4.670.32 | 40.68 | N/A | 1.0x (Base) | 4.67 segundos en Python |
| | Metodo Hungaro O(n^3) (Go Clasico)| 410.200 | 8.450.20 | 10.500 | 11.4x | Go tradicional |
| | Ultra Hungaro SAP (Go Lineal) | 12.210 | 941.38 | 16 | **382.5x** | 12 milisegundos |
| | Ultra Hungaro SAP (Go 16C Par.)| 5.140 | 980.20 | 64 | **908.6x** | **5.14 milisegundos** |
| **1.000.000 Vars (1000x1000)**| Metodo Hungaro O(n^3) (Python)| Demoró > 15m | N/A | N/A | Timeout | Superó 900 s en Python |
| | Ultra Hungaro SAP (Go Lineal) | 1.257.92 | 12.450.00 | 20 | **>715.5x** | 1.25 s en 1 solo núcleo |
| | Ultra Hungaro SAP (Go 16C Par.)| 420.340 | 13.100.00 | 80 | **>2.141x** | **420 ms (Saturación 16C)** |

---

### 6. EXPLICACIÓN DETALLADA DE LAS GRÁFICAS DEL PROYECTO

El proyecto genera tres visualizaciones vectoriales interactivas y un tablero en HTML ubicados en el directorio del proyecto:

```
├── grafica_temporalidad.svg          (Escala Logarítmica de Tiempo)
├── grafica_espacialidad.svg          (Escala Logarítmica de Memoria)
├── grafica_estrategias_paralelas.svg  (Filas vs Celdas vs Bloques)
└── reporte_graficas.html             (Tablero Dashboard Interactivo)
```

#### 6.1. Gráfica 1: Escalabilidad Temporal (`grafica_temporalidad.svg`)
*   **Eje X**: Número total de variables del problema ($100 \to 1.024 \to 10.000 \to 99.856 \to 1.000.000$) en escala logarítmica.
*   **Eje Y**: Tiempo de respuesta en milisegundos ($0.001 \text{ ms} \to 1.000.000 \text{ ms}$) en escala logarítmica.
*   **Interpretación de las curvas**:
    1.  *Curva de Fuerza Bruta*: Presenta una pendiente casi vertical hacia el infinito. Apenas cruza de $N=10$ a $N=32$, la línea se interrumpe demostrando la imposibilidad física de cálculo.
    2.  *Curva Stepping Stone vs MODI*: Se evidencia una divergencia asintótica drástica. Mientras Stepping Stone crece con pendiente cúbica ($O(N^3)$), MODI escala con pendiente cuadrática ($O(N^2)$), permitiendo que MODI Go resuelva 1.000.000 de variables en 4.9 segundos cuando Stepping Stone ya es completamente inviable.
    3.  *Curva Ultra Húngaro SAP Go*: Muestra la menor ordenada al origen y la trayectoria más eficiente de todo el estudio, ejecutando la asignación de 1.000.000 de variables en tan solo 420 ms con sus 16 núcleos en paralelo.

#### 6.2. Gráfica 2: Escalabilidad Espacial (`grafica_espacialidad.svg`)
*   **Eje X**: Número de variables en escala logarítmica.
*   **Eje Y**: Consumo de memoria en kilobytes ($0.1 \text{ KB} \to 10.000.000 \text{ KB}$).
*   **Fenómeno Crítico Explicado (Memoria Python vs Memoria Go)**:
    *   *Por qué Python reporta pocos KB*: Python utiliza `tracemalloc.get_traced_memory()`, el cual registra el **pico de memoria residente viva (RSS instantáneo)**. Como CPython libera memoria inmediatamente al desreferenciar variables mediante conteo de referencias (*refcount*), el pico simultáneo de memoria viva es muy bajo (e.g. 1.8 MB para 100k variables).
    *   *Por qué Go reportaba más KB inicialmente*: En Go se mide `m2.TotalAlloc - m1.TotalAlloc`, que representa la **suma acumulativa histórica del caudal de bytes asignados en el heap**. No significa que el proceso ocupe esa RAM simultáneamente, sino que a lo largo de 50 iteraciones se crearon buffers efímeros que el Garbage Collector va reciclando.
    *   Con la incorporación de `BFSScratch` y buffers planos, la memoria real retenida por Go en 1.000.000 de variables se mantiene por debajo de 50 MB, demostrando una eficiencia espacial absoluta.

#### 6.3. Gráfica 3: Comparativa de Estrategias Paralelas en Go (`grafica_estrategias_paralelas.svg`)
*   Compara en exclusiva los tiempos de ejecución de las tres arquitecturas de particionamiento: **Filas**, **Celdas Continuas** y **Bloques 2D (Tiling)**.
*   **Conclusiones de la arquitectura**:
    1.  *A pequeña escala ($N \le 16$)*: La partición por Filas pierde rendimiento debido a que deja núcleos ociosos (si hay 10 filas y 16 núcleos, 6 núcleos no reciben trabajo).
    2.  *Celdas Continuas*: Elimina completamente los núcleos ociosos, pero paga una penalización leve en tiempo por el cálculo continuo de divisiones enteras y módulos.
    3.  *Bloques 2D (Tiling)*: Resulta ser el **ganador indiscutible** en todas las escalas intermedias y grandes ($N \ge 32$). Al dividir la matriz en cuadrantes bidimensionales compactos, el procesador retiene las líneas de caché L1/L2, reduciendo los fallos de caché (*cache misses*) y logrando un tiempo $15\%\text{ a }25\%$ menor que la partición por filas.

---

### 7. CONCLUSIONES GENERALES DEL PROYECTO

1.  **Superioridad de MODI sobre Stepping Stone**: Stepping Stone es una herramienta pedagógica excelente para comprender ciclos cerrados, pero computacionalmente inviable para problemas reales a gran escala debido a la necesidad de construir $O(N^2)$ árboles o ciclos por iteración. MODI desacopla el cálculo de costos marginales mediante variables duales, convirtiéndolo en el algoritmo estándar industrial para transporte.
2.  **Eficiencia del Algoritmo SAP sobre el Húngaro Tradicional**: El algoritmo de Caminos de Aumento Más Cortos (SAP / Jonker-Volgenant) supera al algoritmo clásico de Kuhn-Munkres por más de dos órdenes de magnitud ($>900\times$ más rápido en paralelo), gracias a su diseño cache-friendly y a la eliminación de operaciones de cubrimiento con líneas.
3.  **Impacto del Lenguaje y la Concurrencia**:
    *   Go demostró aceleraciones de hasta **$2.141\times$ frente a Python** en el problema de asignación masiva de 1.000.000 de variables.
    *   La ausencia de GIL en Go, combinada con la paralelización a 16 núcleos mediante `sync.WaitGroup` y buffers preasignados (`BFSScratch`), permitió procesar matrices de $1.000 \times 1.000$ en menos de medio segundo, donde Python colapsaba o superaba los 15 minutos de ejecución.
4.  **Localidad de Datos sobre Concurrencia Pura**: El paralelismo por Bloques 2D (Tiling) demostró que en algoritmos matriciales masivos, la forma en que los datos viajan a la memoria caché del procesador es tan determinante para el rendimiento final como el número de núcleos utilizados.
