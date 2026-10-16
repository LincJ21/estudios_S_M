# Optimización de Alto Rendimiento en Go: Transporte y Asignación (100 Variables)

Este proyecto replica, optimiza y valida matemáticamente los problemas de **Transporte** y **Asignación** ($10 \times 10 = 100$ variables) en **Go (Golang)** y **Python**.

El sistema está diseñado para **adaptarse automáticamente a los recursos de hardware del computador** donde se ejecute (`runtime.NumCPU()`), fraccionando dinámicamente la matriz y los árboles combinatorios entre todos los núcleos disponibles.

---

## 🧭 ¿Qué se Paraleliza en Cada Problema?

### 1. En el Problema de Transporte (10x10 = 100 variables)
* **Stepping Stone Paralelo:** Fracciona las filas y celdas no básicas de la matriz entre todos los núcleos de CPU del host. Cada hilo evalúa concurrentemente los **circuitos cerrados ortogonales** sobre el árbol abarcador bipartito con memoria plana, eliminando contención y alocaciones de memoria.
* **MODI Paralelo:** Fracciona la matriz de costos y potenciales duales entre los núcleos para calcular en paralelo los **costos reducidos marginales** ($\Delta_{ij} = c_{ij} - (u_i + v_j)$) y encontrar la variable entrante con mayor tasa de mejora.
* **Ultra MODI Paralelo:** Motor con evaluación vectorizada de deltas y actualización de base optimizada.

### 2. En el Problema de Asignación (10x10 = 100 variables)
* **Fuerza Bruta Paralela:** Fracciona el espacio factorial de **$10! = 3,628,800$ permutaciones** repartiendo las ramas iniciales del árbol de decisión entre los 16 núcleos con balanceo dinámico de carga y sincronización *lock-free* en hardware (`atomic.CompareAndSwap`).
* **Ultra Branch & Bound Paralelo:** Paraleliza la exploración reduciendo el espacio de búsqueda en un $99.999\%$ mediante **máscaras de bits de 32 bits** (`math/bits`) y cotas inferiores voraces con podas atómicas entre hilos.
* **Ultra Húngaro SAP (*Shortest Augmenting Path*):** Implementación lineal continua con memoria prealocada (alcanza tiempos de **$3\text{ }\mu\text{s}$**).

---

## 📁 Archivos del Proyecto

| Archivo | Contenido |
| :--- | :--- |
| [`matrices_100.json`](file:///home/lincj/Documentos/S_&_M/matrices_100.json) | Matrices idénticas de 100 variables compartidas entre Python y Go para paridad matemática. |
| [`03.py`](file:///home/lincj/Documentos/S_&_M/03.py) | Benchmark y validación en Python (sin dependencias externas obligatorias). |
| [`mejora/transporte.go`](file:///home/lincj/Documentos/S_&_M/mejora/transporte.go) | Vogel, Stepping Stone Secuencial/Paralelo, MODI ($u-v$) Secuencial/Paralelo adaptativo. |
| [`mejora/asignacion.go`](file:///home/lincj/Documentos/S_&_M/mejora/asignacion.go) | Fuerza Bruta Secuencial/Paralela ($10!$) y Método Húngaro $O(n^3)$. |
| [`mejora/ultra_performance.go`](file:///home/lincj/Documentos/S_&_M/mejora/ultra_performance.go) | Motores Ultra: Branch & Bound Bitmask Paralelo, Húngaro SAP ($3\text{ }\mu\text{s}$) y Ultra MODI. |
| [`mejora/main.go`](file:///home/lincj/Documentos/S_&_M/mejora/main.go) | Orquestador de pruebas con detección dinámica de CPU, benchmarks y bloque de validación cruzada. |

---

## 🚀 Cómo Ejecutar

### En Go:
```bash
cd /home/lincj/Documentos/S_&_M/mejora
go run .
```

### En Python:
```bash
python3 /home/lincj/Documentos/S_&_M/03.py
```

---

## 📊 Resultados de Benchmark en Máquina Host (16 Cores CPU)

```text
======================================================================================
       OPTIMIZACIÓN DE ALTO RENDIMIENTO EN GO: TRANSPORTE Y ASIGNACIÓN        
   Configuración Dinámica de Hardware: 16 Núcleos de CPU detectados (GOMAXPROCS: 16)
   Todos los algoritmos paralelos se adaptan automáticamente a los recursos del host.
======================================================================================

██████████████████████████████████████████████████████████████████████████████████████
 [PROBLEMA 1] PROBLEMA DE TRANSPORTE (10x10 = 100 Variables)
 Distribución en Matriz: 10 filas fraccionadas dinámicamente entre 16 Cores de CPU
 ¿Qué se paraleliza aquí?
  • En Stepping Stone: La evaluación de ciclos cerrados ortogonales en celdas no básicas.
  • En MODI: El cálculo masivo de costos reducidos Δ_ij = c_ij - (u_i + v_j).
██████████████████████████████████████████████████████████████████████████████████████

 1. Método Tradicional (Stepping Stone Secuencial)        : Costo: 3300.00 | Iters: 5 | Tiempo: 0.250 ms (250 µs)
 2. Método Tradicional Paralelo (Stepping Stone 16 Cores) : Costo: 3300.00 | Iters: 5 | Tiempo: 0.594 ms (594 µs)
 3. Método Avanzado (MODI u-v Secuencial)                  : Costo: 3300.00 | Iters: 5 | Tiempo: 0.079 ms (79 µs)
 4. Método Avanzado Paralelo (MODI 16 Cores)               : Costo: 3300.00 | Iters: 5 | Tiempo: 0.201 ms (201 µs)
 5. Ultra Transporte MODI Paralelo (16 Cores)              : Costo: 3300.00 | Iters: 5 | Tiempo: 0.116 ms (116 µs) 🚀

--------------------------------------------------------------------------------------
 TABLA COMPARATIVA ESPECÍFICA: PROBLEMA DE TRANSPORTE (100 VARIABLES)
--------------------------------------------------------------------------------------
MÉTODO TRANSPORTE                    PYTHON             GO (HOST)        ACELERACIÓN (SPEEDUP)
--------------------------------------------------------------------------------------
Stepping Stone Secuencial            3.109 ms           0.250 ms         12.4x más rápido
Stepping Stone Paralelo (16 cores)   3.109 ms           0.594 ms         5.2x más rápido
MODI (u-v) Secuencial                0.305 ms           0.079 ms         3.9x más rápido
MODI Paralelo (16 cores)             0.305 ms           0.201 ms         1.5x más rápido
Ultra MODI Paralelo (16 cores)       0.305 ms           0.116 ms         2.6x más rápido 🚀
--------------------------------------------------------------------------------------


██████████████████████████████████████████████████████████████████████████████████████
 [PROBLEMA 2] PROBLEMA DE ASIGNACIÓN (10x10 = 100 Variables)
 Distribución Factorial: 10! (3,628,800 permutaciones) repartidas entre 16 Cores de CPU
 ¿Qué se paraleliza aquí?
  • En Fuerza Bruta: Ramas iniciales del árbol distribuidas concurrentemente en hilos.
  • En Ultra Branch & Bound: Ramas de decisión con bitmasks de 32 bits y podas atómicas.
██████████████████████████████████████████████████████████████████████████████████████

 1. Tradicional (Fuerza Bruta Secuencial 10!)            : Coste: 248 | Perms: 3628800 | Tiempo: 59.51 ms
 2. Tradicional Paralelo (Fuerza Bruta 16 Cores)         : Coste: 248 | Perms: 3628800 | Tiempo: 9.24 ms  | Multi-Core: 6.44x ⚡
 3. Avanzado (Método Húngaro O(n^3))                      : Coste: 248 | Tiempo: 0.057 ms (57 µs)
 4. Ultra Branch & Bound Paralelo (16 Cores, Bits)        : Coste: 248 | Podas: 24 evals | Tiempo: 0.129 ms (129 µs) 🚀
 5. Ultra Húngaro SAP (Memoria Lineal Continua)           : Coste: 248 | Tiempo: 0.003 ms (3 µs) 🚀

--------------------------------------------------------------------------------------
 TABLA COMPARATIVA ESPECÍFICA: PROBLEMA DE ASIGNACIÓN (100 VARIABLES)
--------------------------------------------------------------------------------------
MÉTODO ASIGNACIÓN                    PYTHON             GO (HOST)        ACELERACIÓN (SPEEDUP)
--------------------------------------------------------------------------------------
Fuerza Bruta Secuencial (10!)        2792.75 ms         59.51 ms         46.9x más rápido
Fuerza Bruta Paralela (16 cores)     2792.75 ms         9.24 ms          302.3x más rápido ⚡
Método Húngaro O(n^3)                0.066 ms           0.057 ms         1.2x más rápido
Ultra Branch&Bound Par. (16 cores)   2792.75 ms (FB)    0.129 ms         21649.2x más rápido 🚀
Ultra Húngaro SAP (Lineal)           0.066 ms           0.003 ms         22.0x más rápido 🚀
--------------------------------------------------------------------------------------

======================================================================================
             BLOQUE DE VALIDACIÓN CRUZADA DE OPTIMALIDAD (GO Y PYTHON)        
======================================================================================
 • TRANSPORTE (Costo Óptimo = 3,300.00):
   - Stepping Stone Secuencial (3300.00) == Paralelo (3300.00)       -> [VALIDACIÓN: OK - EXACTA]
   - MODI Secuencial (3300.00) == Paralelo (3300.00) == Ultra (3300.00) -> [VALIDACIÓN: OK - EXACTA]
   - Validación cruzada con Python MODI (3300.00) y SS (3300.00)     -> [COINCIDENCIA 100%]

 • ASIGNACIÓN (Coste Óptimo = 248):
   - Fuerza Bruta Secuencial (248) == Paralela (248)           -> [VALIDACIÓN: OK - EXACTA]
   - Húngaro (248) == Ultra B&B (248) == Ultra SAP (248)       -> [VALIDACIÓN: OK - EXACTA]
   - Validación cruzada con Python Húngaro (248) y FB (248)         -> [COINCIDENCIA 100%]

 >>> CONFIRMADO: TODOS LOS ALGORITMOS EN PYTHON Y GO CONVERGEN A LA SOLUCIÓN ÓPTIMA EXACTA <<<
======================================================================================
```
