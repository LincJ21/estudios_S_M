# INVESTIGACIÓN DE OPERACIONES Y COMPUTACIÓN DE ALTO RENDIMIENTO
## Optimización en Redes de Transporte, Asignación Biyectiva y Escalabilidad Masiva (100 a 1.000.000 de Variables)

Repositorio integral de algoritmos exactos de Investigación de Operaciones implementados y optimizados en **Python** y **Go**. El proyecto abarca desde casos de estudio didácticos clásicos (Transporte y Asignación 3x3) hasta motores concurrentes de ultra rendimiento en Go capaces de saturar 16 núcleos de CPU y resolver problemas de hasta un millón de variables en tiempo real.

---

### TABLA DE CONTENIDOS
1. [Estructura del Repositorio](#1-estructura-del-repositorio)
2. [Descripción de los Módulos](#2-descripción-de-los-módulos)
   * [Módulo 01: Problema de Transporte (3x3)](#módulo-01-problema-de-transporte-3x3)
   * [Módulo 02: Problema de Asignación (3x3)](#módulo-02-problema-de-asignación-3x3)
   * [Módulo 03 & Mejora: Escalabilidad Masiva y Computación Concurrente (100 a 1.000.000 Vars)](#módulo-03--mejora-escalabilidad-masiva-y-computación-concurrente)
3. [Estrategias de Paralelismo Matricial en Go (16 Cores)](#3-estrategias-de-paralelismo-matricial-en-go-16-cores)
4. [Técnicas de Optimización y Superación del Colapso](#4-técnicas-de-optimización-y-superación-del-colapso)
5. [Resultados Empíricos Consolidados y Speedups](#5-resultados-empíricos-consolidados-y-speedups)
6. [Visualizaciones y Tablero Interactivo](#6-visualizaciones-y-tablero-interactivo)
7. [Guía de Instalación y Ejecución](#7-guía-de-instalación-y-ejecución)
8. [Referencias Teóricas](#8-referencias-teóricas)

---

### 1. ESTRUCTURA DEL REPOSITORIO

```text
.
├── 01/                                      # Módulo 1: Caso de Estudio Transporte 3x3
│   ├── 01.py                                # Script en Python (Vogel, MODI, Stepping Stone, PuLP)
│   ├── INFORME_EJERCICIO_01.md              # Informe técnico detallado del Ejercicio 1
│   ├── P_Lineal.txt                         # Modelo algebraico del problema lineal
│   ├── red_transporte.png                   # Diagrama de red de transporte óptima
│   ├── arbol_ramificacion.png               # Diagrama de flujo iterativo de MODI
│   └── solucion_grafica.png                 # Panel combinado de resultados
│
├── 02/                                      # Módulo 2: Caso de Estudio Asignación 3x3
│   ├── 02.py                                # Script en Python (Fuerza Bruta, Húngaro, PuLP)
│   ├── INFORME_EJERCICIO_02.md              # Informe técnico detallado del Ejercicio 2
│   └── asignacion_hungaro.png               # Grafo bipartito de la asignación óptima
│
├── mejora/                                  # Módulo 3: Motor Concurrente de Alto Rendimiento en Go
│   ├── main.go                              # Orquestador del benchmark multiescala (16 Cores)
│   ├── transporte.go                        # Vogel concurrente, Stepping Stone (BFSScratch) y MODI
│   ├── asignacion.go                        # Fuerza Bruta concurrente y Húngaro clásico en Go
│   ├── ultra_performance.go                 # Ultra Húngaro SAP (Lineal y Paralelo 16C) y Branch & Bound
│   ├── go.mod                               # Definición del módulo de Go
│   └── README.md                            # Guía técnica interna del módulo Go
│
├── 03.py                                    # Benchmark multiescala en Python (100 a 1M vars con timeout)
├── generar_graficas.py                      # Generador autónomo de gráficos vectoriales SVG y HTML
├── INFORME_TECNICO_OPTIMIZACION.md          # Informe técnico general de escalabilidad y rendimiento
│
├── matrices_100.json                        # Dataset: 100 variables (10x10)
├── matrices_1000.json                       # Dataset: 1.024 variables (32x32)
├── matrices_10000.json                      # Dataset: 10.000 variables (100x100)
├── matrices_100000.json                     # Dataset: 99.856 variables (316x316)
├── matrices_1000000.json                    # Dataset: 1.000.000 variables (1.000x1.000)
│
├── grafica_temporalidad.svg                 # Gráfica SVG: Tiempo de Ejecución vs Variables (Log-Log)
├── grafica_espacialidad.svg                 # Gráfica SVG: Consumo de Memoria vs Variables (Log-Log)
├── grafica_estrategias_paralelas.svg         # Gráfica SVG: Filas vs Celdas Continuas vs Bloques 2D
├── python_scales_results.json               # Resultados empíricos serializados de Python
├── resultados_benchmark.json                # Resultados consolidados multiescala en JSON
└── reporte_graficas.html                    # Tablero visual interactivo integrado (Dashboard)
```

---

### 2. DESCRIPCIÓN DE LOS MÓDULOS

#### Módulo 01: Problema de Transporte (3x3)
*   **Problema Real**: Abastecimiento de 3 almacenes regionales ($W_1, W_2, W_3$) desde 3 plantas de producción ($P_1, P_2, P_3$) minimizando el costo de flete con oferta y demanda total de 900 unidades.
*   **Pilares Metodológicos Canónicos**:
    1.  **Método Balanceado**: Verificación formal de la condición $\sum s_i = \sum d_j = 900$. El módulo comprueba la factibilidad de la red y documenta el balanceo automático con nodos ficticios (costo 0) para casos desbalanceados.
    2.  **Método Normal (Simplex de Transporte Especializado)**: Solución Básica Inicial voraz por Aproximación de Vogel (VAM) ($Z_1 = \$12,200.00$) y optimización exacta en red mediante el método MODI ($u_i + v_j = c_{ij}$) iterativo ($Z_2 = \$11,200.00 \to Z_3 = \$10,400.00$). Incluye también el método tradicional de red de Stepping Stone (Banquillo).
    3.  **Simplex Tradicional**: Formulación general de Programación Lineal en tabla simplex con restricciones explícitas de igualdad $\mathbf{A}\mathbf{x} = \mathbf{b}$ resuelto mediante PuLP (motor HiGHS) confirmando el óptimo global en **\$10,400.00**.
*   **Documentación**: [INFORME_EJERCICIO_01.md](01/INFORME_EJERCICIO_01.md).

#### Módulo 02: Problema de Asignación (3x3)
*   **Problema Real**: Contratación del mantenimiento preventivo anual de tres centrales eléctricas (Hidroeléctrica, Ciclo Combinado y Nuclear) asignadas biyectivamente a tres empresas de ingeniería (Empresas A, B y C).
*   **Pilares Metodológicos Canónicos**:
    1.  **Método Balanceado**: Verificación formal de matriz cuadrada $n \times n$ ($3 \times 3$). Documenta e implementa la nivelación automática mediante agentes o tareas ficticias con costo nulo cuando la matriz es rectangular.
    2.  **Método Normal (Algoritmo Húngaro / Kuhn-Munkres $O(n^3)$)**: Método estándar de reducción de matrices de costos, cobertura mínima de líneas y ajuste dual Kőnig-Egerváry.
    3.  **Simplex Tradicional**: Formulación continua de Programación Lineal demostrando que, por la Total Unimodularidad de la matriz de coeficientes, el Simplex estándar converge directamente a soluciones enteras binarias puras sin necesidad de Branch & Bound. Resuelto con PuLP (HiGHS).
    4.  **Método Combinatorio Tradicional**: Enumeración exhaustiva de las $3! = 6$ permutaciones para evidenciar el costo factorial $O(n!)$.
*   **Solución Óptima**: Empresa A $\to$ Central 1, Empresa B $\to$ Central 3, Empresa C $\to$ Central 2. Costo total mínimo: **$17$ mil euros ($17.000 €$)**.
*   **Documentación**: [INFORME_EJERCICIO_02.md](02/INFORME_EJERCICIO_02.md).

#### Módulo 03 & Mejora: Escalabilidad Masiva y Computación Concurrente
Evalúa sistemáticamente el comportamiento asintótico de los algoritmos al escalar el tamaño de la matriz en 5 órdenes de magnitud:
1.  **100 Variables** ($10 \times 10$)
2.  **1.000 Variables** ($32 \times 32 = 1.024$ vars)
3.  **10.000 Variables** ($100 \times 100$)
4.  **100.000 Variables** ($316 \times 316 = 99.856$ vars)
5.  **1.000.000 Variables** ($1.000 \times 1.000$)

Implementa motores comparativos entre Python (interpretado monohilo con GIL) y Go (compilado nativo con 16 núcleos en paralelo).

---

### 3. ESTRATEGIAS DE PARALELISMO MATRICIAL EN GO (16 CORES)

Para descomponer las matrices entre los 16 núcleos del procesador host, se diseñaron y evaluaron tres patrones de concurrencia:

1.  **Paralelismo por Filas (Row Chunks)**:
    *   Divide la matriz horizontalmente en franjas continuas de filas.
    *   *Ventaja*: Simplicidad en indexación contigua de memoria en Go.
    *   *Limitación*: Ineficiente cuando $M < 16$ (deja núcleos ociosos en matrices pequeñas como $10 \times 10$).
2.  **Paralelismo por Celdas Continuas (Linear Contiguous Chunking)**:
    *   Trata la matriz como un arreglo lineal plano de $M \cdot N$ celdas repartidas exactamente entre los 16 trabajadores.
    *   *Ventaja*: Cero núcleos ociosos en cualquier dimensión de matriz.
    *   *Sobrecarga*: Costo leve por divisiones enteras y módulo para traducir índice lineal a $(i, j)$.
3.  **Paralelismo por Bloques 2D (Tiling)**:
    *   Descompone la matriz en una grilla de sub-bloques rectangulares de $GR \times GC = 16$.
    *   *Ventaja*: **Máxima tasa de aciertos en memoria caché L1/L2**. Al recorrer bloques bidimensionales compactos, las líneas de caché se reutilizan entre filas contiguas, logrando el menor tiempo de ejecución global en matrices de gran escala.

---

### 4. TÉCNICAS DE OPTIMIZACIÓN Y SUPERACIÓN DEL COLAPSO

#### 4.1. Cero Alocaciones con `BFSScratch` en Stepping Stone
En matrices medianas y grandes, Stepping Stone colapsaba debido a la creación masiva de slices dinámicos en el heap durante el recorrido BFS de ciclos cerrados ($O(N^2)$ búsquedas por iteración), lo cual provocaba pausas críticas del Garbage Collector.
*Solución*: Se diseñó `BFSScratch` con un sistema de tokens por trabajador (`sc.Token++`). Esto permite verificar nodos visitados en tiempo $O(1)$ sin reinicializar arreglos y sin realizar alocaciones en el bucle principal, aumentando la velocidad en más de $30\times$.

#### 4.2. Ultra Húngaro SAP Paralelo (16 Cores al 100%)
El algoritmo de Caminos de Aumento Más Cortos (SAP / Jonker-Volgenant) fue paralelizado en Go (`UltraHungaroSAPParalelo`) distribuyendo la búsqueda de mínimos de columnas y las actualizaciones duales entre los 16 núcleos con `sync.WaitGroup`, logrando saturar la CPU al 100% y resolviendo 1.000.000 de variables en **420 milisegundos**.

#### 4.3. Control de Límites de Ejecución (Timeouts de 15 Minutos)
*   En **Python** ([`03.py`](03.py)): Las funciones se ejecutan bajo `signal.alarm(900)`. Si un método supera los 15 minutos (900 s), se captura la excepción `TimeoutLimiteExcedido`, registrando `Demoró más de 15 min (900 s)` y continuando sin bloquear las demás pruebas.
*   En **Go** ([`mejora/main.go`](mejora/main.go)): Los algoritmos se ejecutan en goroutines concurrentes supervisadas por canales con `time.After(15 * time.Minute)`.
*   Para Fuerza Bruta en $N \ge 32$ ($32! \approx 2.6 \times 10^{35}$ operaciones), se identifica analíticamente la inviabilidad para evitar bloqueos innecesarios (`Inviable O(N!) > 10^20 años`).

---

### 5. RESULTADOS EMPÍRICOS CONSOLIDADOS Y SPEEDUPS

#### Resumen: Problema de Transporte (100 a 1.000.000 de Variables)

| Escala (Variables) | Método / Estrategia | Tiempo Python | Tiempo Go (16C) | Speedup (vs Py) | Estado |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **100 Vars (10x10)** | Stepping Stone | 11.20 ms | 0.26 ms | **42.8x** | Óptimo Bloques 2D |
| | Metodo MODI u-v | 1.51 ms | 0.10 ms | **14.3x** | Óptimo Bloques 2D |
| **1.000 Vars (32x32)**| Stepping Stone | 5.264 ms | 11.88 ms | **442.9x** | Gran aceleración Go |
| | Metodo MODI u-v | 60.35 ms | 1.90 ms | **31.7x** | Go converge en <2 ms |
| **10.000 Vars (100x100)**| Stepping Stone | > 15 min | 889.53 ms | **>1.011x** | Py supera timeout |
| | Metodo MODI u-v | 2.761 ms | 51.60 ms | **53.5x** | Go 53x más rápido |
| **100.000 Vars (316x316)**| Stepping Stone | > 15 min | 3.850 ms | **>233x** | Resuelto en 3.8 s |
| | Metodo MODI u-v | 41.950 ms | 1.542 ms | **27.2x** | Go en 1.5 s vs Py 42 s |
| **1.000.000 Vars (1000x1000)**| Metodo MODI u-v | > 15 min | 4.912 ms | **>183.2x** | **Go resuelve en 4.9 s** |

#### Resumen: Problema de Asignación (100 a 1.000.000 de Variables)

| Escala (Variables) | Método / Estrategia | Tiempo Python | Tiempo Go (16C) | Speedup (vs Py) | Estado |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **100 Vars (10x10)** | Fuerza Bruta (10!) | 5.110.83 ms | 9.35 ms | **546.6x** | Go 16C Paralelo |
| | Ultra Hungaro SAP | 0.10 ms (Húngaro) | 0.008 ms | **13.1x** | 8 microsegundos |
| **1.000 Vars (32x32)**| Fuerza Bruta (32!) | Inviable O(N!) | Inviable O(N!) | N/A | $2.6 \times 10^{35}$ ops |
| | Ultra Hungaro SAP | 4.79 ms | 0.038 ms | **126.3x** | 38 microsegundos |
| **10.000 Vars (100x100)**| Ultra Hungaro SAP | 83.32 ms | 0.412 ms | **202.2x** | 412 microsegundos |
| **100.000 Vars (316x316)**| Ultra Hungaro SAP | 4.670.32 ms | 5.14 ms | **908.6x** | **5.14 milisegundos** |
| **1.000.000 Vars (1000x1000)**| Ultra Hungaro SAP | > 15 min | 420.34 ms | **>2.141x** | **420 ms (Pico 2.141x)** |

---

### 6. VISUALIZACIONES Y TABLERO INTERACTIVO

El proyecto genera de forma autónoma tres gráficos vectoriales SVG en escala log-log y un tablero interactivo HTML:

1.  **Escalabilidad Temporal** ([`grafica_temporalidad.svg`](grafica_temporalidad.svg)):
    Muestra la divergencia en tiempo de ejecución (ms) frente al número de variables, evidenciando el colapso asintótico de Fuerza Bruta y Stepping Stone frente a la estabilidad de MODI y Ultra SAP.
2.  **Escalabilidad Espacial** ([`grafica_espacialidad.svg`](grafica_espacialidad.svg)):
    Analiza la diferencia entre el pico de memoria viva instantánea en Python (`tracemalloc`) y el caudal de asignaciones acumuladas en Go (`TotalAlloc`).
3.  **Comparativa de Estrategias Paralelas** ([`grafica_estrategias_paralelas.svg`](grafica_estrategias_paralelas.svg)):
    Compara Filas vs Celdas Continuas vs Bloques 2D (Tiling), demostrando por qué la afinidad a la memoria caché L1/L2 otorga a los Bloques 2D una ventaja de entre $15\%$ y $25\%$.
4.  **Tablero Web Interactivo** ([`reporte_graficas.html`](reporte_graficas.html)):
    Dashboard moderno con tema oscuro que integra las tres gráficas interactivas con descripciones técnicas completas.

---

### 7. GUÍA DE INSTALACIÓN Y EJECUCIÓN

#### Requisitos Previos:
*   **Go**: Versión 1.20 o superior (probado en Go 1.24).
*   **Python**: Versión 3.9 o superior (probado en Python 3.13).

#### 1. Ejecutar Casos Didácticos 3x3:
```bash
# Ejercicio 1: Transporte 3x3
python3 01/01.py

# Ejercicio 2: Asignación 3x3
python3 02/02.py
```

#### 2. Ejecutar Benchmark Masivo en Go (Aprovechando 16 Cores):
```bash
cd mejora
go run .
```
*El motor compilará en memoria, detectará automáticamente los 16 núcleos de su procesador, ejecutará las 5 escalas (hasta 1.000.000 de variables), presentará las tablas con la columna `SPEEDUP (vs Py)` y regenerará los gráficos automáticamente.*

#### 3. Ejecutar Benchmark Multiescala en Python:
```bash
python3 03.py
```
*Evaluará las escalas con un límite de 15 minutos por algoritmo, registrando los resultados en `python_scales_results.json`.*

#### 4. Visualizar Tablero Gráfico en el Navegador:
```bash
xdg-open reporte_graficas.html
```

---

### 8. REFERENCIAS TEÓRICAS

1.  **Monge, G. (1781)**. *Mémoire sur la théorie des déblais et des remblais*. Histoire de l'Académie Royale des Sciences de Paris.
2.  **Kantorovich, L. V. (1939)**. *Mathematical Methods of Organizing and Planning Production*. Management Science, 6(4), 366-422.
3.  **Hitchcock, F. L. (1941)**. *The Distribution of a Product from Several Sources to Numerous Localities*. Journal of Mathematics and Physics, 20(1-4), 224-230.
4.  **Dantzig, G. B. (1951)**. *Application of the Simplex Method to a Transportation Problem*. Activity Analysis of Production and Allocation, 359-373.
5.  **Kuhn, H. W. (1955)**. *The Hungarian Method for the Assignment Problem*. Naval Research Logistics Quarterly, 2(1-2), 83-97.
6.  **Munkres, J. (1957)**. *Algorithms for the Assignment and Transportation Problems*. Journal of the Society for Industrial and Applied Mathematics, 5(1), 32-38.
7.  **Jonker, R., & Volgenant, A. (1987)**. *A Shortest Augmenting Path Algorithm for Dense and Sparse Linear Assignment Problems*. Computing, 38(4), 325-340.

