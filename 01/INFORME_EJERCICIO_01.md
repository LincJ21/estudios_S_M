# INFORME TÉCNICO: EJERCICIO 1 - PROBLEMA DE TRANSPORTE
## Optimización de Red Logística mediante Vogel (VAM), MODI (u-v), Stepping Stone y PuLP

---

### 1. DESCRIPCIÓN DEL PROBLEMA

Una corporación manufacturera dispone de tres plantas de producción ($P_1, P_2, P_3$) y debe abastecer la demanda de tres almacenes regionales de distribución ($W_1, W_2, W_3$). El objetivo es determinar el plan de envíos óptimo que minimice el costo total de transporte, garantizando que no se exceda la capacidad de las plantas y se satisfaga exactamente la demanda requerida.

#### Parámetros del Sistema:
*   **Capacidades de Producción (Oferta)**:
    *   Planta 1 ($P_1$): $300$ unidades.
    *   Planta 2 ($P_2$): $500$ unidades.
    *   Planta 3 ($P_3$): $100$ unidades.
    *   *Oferta Total*: $\sum_{i=1}^3 s_i = 300 + 500 + 100 = 900$ unidades.
*   **Requerimientos Regionales (Demanda)**:
    *   Almacén 1 ($W_1$): $200$ unidades.
    *   Almacén 2 ($W_2$): $400$ unidades.
    *   Almacén 3 ($W_3$): $300$ unidades.
    *   *Demanda Total*: $\sum_{j=1}^3 d_j = 200 + 400 + 300 = 900$ unidades.
*   **Condición de Balanceo**:
    $$\sum_{i=1}^3 s_i = \sum_{j=1}^3 d_j = 900 \quad \text{(Problema de Transporte Equilibrado)}$$

#### Matriz de Costos Unitarios de Transporte ($c_{ij}$ en $/unidad):

| Origen / Destino | Almacén 1 ($W_1$) | Almacén 2 ($W_2$) | Almacén 3 ($W_3$) | Oferta ($s_i$) |
| :--- | :---: | :---: | :---: | :---: |
| **Planta 1 ($P_1$)** | $20 | $16 | $24 | **300** |
| **Planta 2 ($P_2$)** | $10 | $10 | $8 | **500** |
| **Planta 3 ($P_3$)** | $12 | $18 | $10 | **100** |
| **Demanda ($d_j$)** | **200** | **400** | **300** | **900** |

---

### 2. FORMULACIÓN MATEMÁTICA FORMAL

Sea $x_{ij} \ge 0$ la cantidad de unidades enviadas desde la planta $i$ hacia el almacén $j$.

#### Función Objetivo:
$$\min Z = 20 x_{11} + 16 x_{12} + 24 x_{13} + 10 x_{21} + 10 x_{22} + 8 x_{23} + 12 x_{31} + 18 x_{32} + 10 x_{33}$$

#### Sujeto a:
*   **Restricciones de Oferta (Plantas)**:
    $$x_{11} + x_{12} + x_{13} = 300 \quad (P_1)$$
    $$x_{21} + x_{22} + x_{23} = 500 \quad (P_2)$$
    $$x_{31} + x_{32} + x_{33} = 100 \quad (P_3)$$
*   **Restricciones de Demanda (Almacenes)**:
    $$x_{11} + x_{21} + x_{31} = 200 \quad (W_1)$$
    $$x_{12} + x_{22} + x_{32} = 400 \quad (W_2)$$
    $$x_{13} + x_{23} + x_{33} = 300 \quad (W_3)$$
*   **No Negatividad e Integridad**:
    $$x_{ij} \ge 0 \quad \forall i \in \{1, 2, 3\}, j \in \{1, 2, 3\}$$

*Propiedad de la Base*: Toda Solución Básica Factible no degenerada está conformada por exactamente $m + n - 1 = 3 + 3 - 1 = 5$ variables básicas acíclicas.

---

### 2.1. CLASIFICACIÓN CONCEPTUAL DE LOS MÉTODOS CANÓNICOS

En la teoría clásica de Investigación de Operaciones y Optimización Lineal, la resolución de este modelo se articula a través de tres pilares metodológicos:

#### 1. El Método Balanceado (Condición de Equilibrio de Flujos)
*   **Fundamento Matemático**: Un problema de transporte se clasifica como balanceado si la suma total de las capacidades de oferta de los orígenes es idéntica a la suma total de los requerimientos de demanda de los destinos:
    $$\sum_{i=1}^m s_i = \sum_{j=1}^n d_j$$
*   **Garantía Estructural**: El balanceo garantiza la existencia de al menos una Solución Básica Factible y asegura que el poliedro de restricciones sea acotado (compacto).
*   **Tratamiento de Desbalanceos**: Si $\sum s_i \neq \sum d_j$, el problema se balancea artificialmente introduciendo:
    *   Un **Almacén/Destino Ficticio** ($W_{\text{dummy}}$) con demanda faltante $d_{\text{dummy}} = \sum s_i - \sum d_j$ y costos unitarios $c_{i, \text{dummy}} = 0$ (si $\sum s_i > \sum d_j$).
    *   Una **Planta/Origen Ficticio** ($P_{\text{dummy}}$) con oferta faltante $s_{\text{dummy}} = \sum d_j - \sum s_i$ y costos unitarios $c_{\text{dummy}, j} = 0$ (si $\sum d_j > \sum s_i$).
*   **Aplicación al Ejercicio 1**: En este caso, $\sum s_i = 300 + 500 + 100 = 900$ y $\sum d_j = 200 + 400 + 300 = 900$. La red es estrictamente balanceada, por lo que no requiere nodos ficticios.

#### 2. El Simplex Tradicional (Programación Lineal Tabular Estándar)
*   **Fundamento**: Es el algoritmo general desarrollado por George Dantzig (1947). Concibe el problema como un sistema algebraico general $\min \mathbf{c}^T \mathbf{x}$ sujeto a $\mathbf{A}\mathbf{x} = \mathbf{b}, \mathbf{x} \ge \mathbf{0}$.
*   **Estructura Matricial**: La matriz de restricciones $\mathbf{A}$ tiene dimensiones $(m + n) \times (m \cdot n)$ ($6 \times 9 = 54$ elementos). Dado que una restricción es redundante ($\sum s_i = \sum d_j$), el rango es $m + n - 1 = 5$.
*   **Mecánica de Cálculo**: El Simplex tradicional mantiene una base explícita $\mathbf{B}$ de dimensión $5 \times 5$, calcula su inversa $\mathbf{B}^{-1}$ y actualiza toda la tabla simplex mediante operaciones elementales de fila de Gauss-Jordan en cada iteración ($O((m+n)^2)$ por pivoteo). En este proyecto está implementado y resuelto mediante PuLP (motor HiGHS/CBC).

#### 3. El Método Normal (Simplex de Transporte Especializado de Redes)
*   **Fundamento**: Aprovecha la estructura topológica de grafo bipartito y la propiedad de que toda base invertible corresponde a un **árbol abarcador (Spanning Tree)** sin ciclos en la red.
*   **Fase 1 (Solución Inicial)**: Emplea heurísticas basadas en penalización por arrepentimiento como el **Método de Aproximación de Vogel (VAM)**, que evalúa la diferencia entre los dos costos mínimos de cada fila y columna, generando una solución inicial de altísima calidad ($Z = \$12,200.00$).
*   **Fase 2 (Prueba de Optimalidad y Reasignación)**:
    *   **Método MODI (u-v)**: Determina los potenciales duales resolviendo $u_i + v_j = c_{ij}$ para las $m+n-1$ celdas básicas en tiempo lineal $O(m+n)$. Calcula los costos reducidos $\Delta_{ij} = c_{ij} - (u_i + v_j)$ para las celdas no básicas. Si $\min \Delta_{ij} < 0$, encuentra el ciclo cerrado alternante en el árbol y redistribuye un flujo $\theta$.
    *   **Método Tradicional (Stepping Stone / Banquillo)**: Traza manualmente el circuito cerrado individual para cada celda no básica evaluando directamente el cambio marginal sin calcular potenciales duales.

---

### 3. DESARROLLO PASO A PASO MEDIANTE ALGORITMOS EXACTOS

#### 3.1. Fase 1: Solución Inicial por Aproximación de Vogel (VAM)
El método de Vogel evalúa en cada paso la penalización por arrepentimiento (diferencia entre los dos menores costos):

1.  **Paso 1**:
    *   Penalizaciones de Fila:
        *   Fila 1: $|20 - 16| = 4$
        *   Fila 2: $|10 - 8| = 2$
        *   Fila 3: $|12 - 10| = 2$
    *   Penalizaciones de Columna:
        *   Columna 1: $|12 - 10| = 2$
        *   Columna 2: $|16 - 10| = 6$ (Máxima penalización global)
        *   Columna 3: $|10 - 8| = 2$
    *   Se selecciona Columna 2 ($W_2$). El costo mínimo es $c_{22} = 10$ ($P_2$).
    *   Se asigna $x_{22} = \min(s_2, d_2) = \min(500, 400) = 400$.
    *   Columna 2 queda satisfecha ($d_2 = 0$). Oferta restante en $P_2 = 100$.
2.  **Paso 2**:
    *   Penalizaciones restantes: Fila 1 = $|24 - 20| = 4$, Fila 2 = $|10 - 8| = 2$, Fila 3 = $|12 - 10| = 2$.
    *   Columna 1 = $|12 - 10| = 2$, Columna 3 = $|10 - 8| = 2$.
    *   Mayor penalización: Fila 1 ($P_1$). Costo mínimo entre $W_1$ y $W_3$ es $c_{11} = 20$.
    *   Se asigna $x_{11} = \min(300, 200) = 200$.
    *   Columna 1 queda satisfecha ($d_1 = 0$). Oferta restante en $P_1 = 100$.
3.  **Paso 3**:
    *   Solo queda activa la Columna 3 ($W_3$, demanda requerida = 300).
    *   Se asigna a $P_1$: $x_{13} = 100$ ($P_1$ agotada).
    *   Se asigna a $P_2$: $x_{23} = 100$ ($P_2$ agotada).
    *   Se asigna a $P_3$: $x_{33} = 100$ ($P_3$ agotada).

**Resultado SBF Inicial (Vogel)**:
*   Variables básicas: $x_{11} = 200$, $x_{13} = 100$, $x_{22} = 400$, $x_{23} = 100$, $x_{33} = 100$ (Exactamente 5 básicas).
*   **Costo Inicial $Z_1$**:
    $$Z_1 = (200 \times 20) + (100 \times 24) + (400 \times 10) + (100 \times 8) + (100 \times 10) = 4000 + 2400 + 4000 + 800 + 1000 = \$12,200.00$$

---

#### 3.2. Fase 2: Proceso Iterativo de Optimización MODI (u-v)

##### Iteración 1:
1.  **Cálculo de Multiplicadores Duales ($u_i + v_j = c_{ij}$ para celdas básicas)**:
    *   Sea $u_1 = 0$:
    *   Celda $(1, 1)$: $u_1 + v_1 = 20 \implies 0 + v_1 = 20 \implies v_1 = 20$
    *   Celda $(1, 3)$: $u_1 + v_3 = 24 \implies 0 + v_3 = 24 \implies v_3 = 24$
    *   Celda $(2, 3)$: $u_2 + v_3 = 8 \implies u_2 + 24 = 8 \implies u_2 = -16$
    *   Celda $(2, 2)$: $u_2 + v_2 = 10 \implies -16 + v_2 = 10 \implies v_2 = 26$
    *   Celda $(3, 3)$: $u_3 + v_3 = 10 \implies u_3 + 24 = 10 \implies u_3 = -14$
2.  **Evaluación de Costos Reducidos ($\Delta_{ij} = c_{ij} - (u_i + v_j)$ para no básicas)**:
    *   $\Delta_{12} = c_{12} - (u_1 + v_2) = 16 - (0 + 26) = \mathbf{-10.0}$
    *   $\Delta_{21} = c_{21} - (u_2 + v_1) = 10 - (-16 + 20) = 10 - 4 = +6.0$
    *   $\Delta_{31} = c_{31} - (u_3 + v_1) = 12 - (-14 + 20) = 12 - 6 = +6.0$
    *   $\Delta_{32} = c_{32} - (u_3 + v_2) = 18 - (-14 + 26) = 18 - 12 = +6.0$
3.  **Pivote**:
    *   Variable entrante: $x_{12}$ con $\Delta_{12} = -10.0$.
    *   Circuito cerrado: $(1, 2) \to (2, 2) \to (2, 3) \to (1, 3) \to (1, 2)$.
    *   Celdas con signo negativo: $(2, 2)$ con $400$, y $(1, 3)$ con $100$.
    *   $\theta = \min(400, 100) = 100$.
    *   Variable saliente: $x_{13}$ (llega a 0).
    *   **Nuevo Costo**: $Z_2 = 12200 + (100 \times (-10)) = \$11,200.00$.

##### Iteración 2:
1.  **Celdas básicas**: $x_{11}=200$, $x_{12}=100$, $x_{22}=300$, $x_{23}=200$, $x_{33}=100$.
2.  **Duales**: $u_1=0 \implies v_1=20, v_2=16 \implies u_2=-6 \implies v_3=14 \implies u_3=-4$.
3.  **Costos reducidos no básicos**:
    *   $\Delta_{13} = 24 - (0 + 14) = +10.0$
    *   $\Delta_{21} = 10 - (-6 + 20) = \mathbf{-4.0}$
    *   $\Delta_{31} = 12 - (-4 + 20) = -4.0$
    *   $\Delta_{32} = 18 - (-4 + 16) = +6.0$
4.  **Pivote**:
    *   Variable entrante: $x_{21}$ ($\Delta = -4.0$).
    *   Circuito cerrado: $(2, 1) \to (1, 1) \to (1, 2) \to (2, 2) \to (2, 1)$.
    *   Celdas negativas: $(1, 1)$ con $200$, y $(2, 2)$ con $300$.
    *   $\theta = \min(200, 300) = 200$.
    *   Variable saliente: $x_{11}$.
    *   **Nuevo Costo**: $Z_3 = 11200 + (200 \times (-4)) = \$10,400.00$.

##### Iteración 3 (Condición de Optimalidad Alcanzada):
1.  **Celdas básicas**: $x_{12}=300$, $x_{21}=200$, $x_{22}=100$, $x_{23}=200$, $x_{33}=100$.
2.  **Duales**: $u_1=0 \implies v_2=16 \implies u_2=-6 \implies v_1=16, v_3=14 \implies u_3=-4$.
3.  **Costos reducidos**:
    *   $\Delta_{11} = 20 - (0 + 16) = +4.0 \ge 0$
    *   $\Delta_{13} = 24 - (0 + 14) = +10.0 \ge 0$
    *   $\Delta_{31} = 12 - (-4 + 16) = 0.0 \ge 0$ (Solución óptima alternativa posible)
    *   $\Delta_{32} = 18 - (-4 + 16) = +6.0 \ge 0$
4.  Como todos los $\Delta_{ij} \ge 0$, **la solución es matemáticamente óptima**.

---

### 4. SOLUCIÓN ÓPTIMA FINAL

#### Matriz de Asignación Óptima de Envíos:

| Planta / Almacén | $W_1$ | $W_2$ | $W_3$ | Total Oferta Enviada |
| :--- | :---: | :---: | :---: | :---: |
| **Planta 1 ($P_1$)** | 0 | **300** | 0 | 300 / 300 |
| **Planta 2 ($P_2$)** | **200** | **100** | **200** | 500 / 500 |
| **Planta 3 ($P_3$)** | 0 | 0 | **100** | 100 / 100 |
| **Total Demanda Recibida** | 200 / 200 | 400 / 400 | 300 / 300 | **900 / 900** |

#### Desglose del Costo Mínimo Total:
*   $P_1 \to W_2$: $300 \text{ uds} \times \$16 = \$4,800.00$
*   $P_2 \to W_1$: $200 \text{ uds} \times \$10 = \$2,000.00$
*   $P_2 \to W_2$: $100 \text{ uds} \times \$10 = \$1,000.00$
*   $P_2 \to W_3$: $200 \text{ uds} \times \$8 = \$1,600.00$
*   $P_3 \to W_3$: $100 \text{ uds} \times \$10 = \$1,000.00$
*   **COSTO TOTAL MÍNIMO**: **\$10,400.00**

---

### 5. VERIFICACIÓN CRUZADA Y BENCHMARK

El script [`01.py`](file:///home/lincj/Documentos/S_&_M/01/01.py) ejecutó la validación rigurosa contrastando los métodos canónicos, confirmando convergencia al idéntico costo óptimo global:

| Categoría Metodológica | Método / Algoritmo | Costo Obtenido | Estado de Factibilidad | Tiempo CPU |
| :--- | :--- | :---: | :---: | :---: |
| **1. Método Balanceado** | Verificación de Red Equilibrada ($\sum s_i = \sum d_j$) | \$10,400.00 | Factible Balanceado | 0.015 ms |
| **2. Método Normal** | Solución Vogel + Optimización MODI ($u_i + v_j = c_{ij}$) | \$10,400.00 | Óptimo Global | 0.165 ms |
| **3. Método Tradicional de Red** | Stepping Stone (Circuitos Cerrados Directos) | \$10,400.00 | Óptimo Global | 0.442 ms |
| **4. Simplex Tradicional** | Programación Lineal Tabular Estándar (PuLP / HiGHS) | \$10,400.00 | Óptimo Global | 12.831 ms |

#### Gráficos y Entregables del Ejercicio:
1.  **Red de Transporte Óptima**: [`01/solucion_grafica.png`](file:///home/lincj/Documentos/S_&_M/01/solucion_grafica.png) (Panel derecho) y [`01/red_transporte.png`](file:///home/lincj/Documentos/S_&_M/01/red_transporte.png) ilustrando el grafo dirigido bipartito con las 5 rutas activas y los flujos óptimos.
2.  **Árbol de Ramificación de Solución**: [`01/solucion_grafica.png`](file:///home/lincj/Documentos/S_&_M/01/solucion_grafica.png) (Panel izquierdo) y [`01/arbol_ramificacion.png`](file:///home/lincj/Documentos/S_&_M/01/arbol_ramificacion.png) detallando la transición paso a paso desde Vogel (\$12,200) $\to$ Iteración 2 (\$11,200) $\to$ Iteración 3 (\$10,400).


