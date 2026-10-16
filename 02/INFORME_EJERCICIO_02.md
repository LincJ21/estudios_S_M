# INFORME TÉCNICO: EJERCICIO 2 - PROBLEMA DE ASIGNACIÓN
## Mantenimiento Preventivo de Centrales Eléctricas mediante Enumeración Exhaustiva, Método Húngaro y PuLP

---

### 1. DESCRIPCIÓN DEL PROBLEMA

Una compañía del sector energético requiere contratar el mantenimiento preventivo anual de tres centrales eléctricas críticas:
*   **Central 1**: Central Hidroeléctrica.
*   **Central 2**: Central Termoeléctrica de Ciclo Combinado.
*   **Central 3**: Central Nuclear.

Para llevar a cabo los trabajos, se cuenta con tres empresas de ingeniería y servicios auxiliares: **Empresa A**, **Empresa B** y **Empresa C**.

#### Reglas de Operación:
1.  Cada empresa auxiliar dispone de la capacidad técnica y personal para atender únicamente **una sola central**.
2.  Cada central eléctrica debe ser asignada a **exactamente una empresa**.
3.  El objetivo es determinar la asignación biyectiva que minimice el costo total del mantenimiento preventivo.

#### Matriz de Costos de Mantenimiento ($c_{ij}$ en miles de euros):

| Empresa / Central | Central 1 | Central 2 | Central 3 |
| :--- | :---: | :---: | :---: |
| **Empresa A** | 10 | 9 | 5 |
| **Empresa B** | 9 | 8 | 3 |
| **Empresa C** | 6 | 4 | 7 |

---

### 2. FORMULACIÓN MATEMÁTICA FORMAL

Sea $x_{ij} \in \{0, 1\}$ una variable de decisión binaria tal que:
$$x_{ij} = \begin{cases} 1 & \text{si la Empresa } i \text{ es asignada a la Central } j \\ 0 & \text{en caso contrario} \end{cases}$$

#### Función Objetivo:
$$\min Z = 10 x_{A1} + 9 x_{A2} + 5 x_{A3} + 9 x_{B1} + 8 x_{B2} + 3 x_{B3} + 6 x_{C1} + 4 x_{C2} + 7 x_{C3}$$

#### Restricciones:
*   **Cada empresa debe atender exactamente una central**:
    $$x_{A1} + x_{A2} + x_{A3} = 1 \quad (\text{Empresa A})$$
    $$x_{B1} + x_{B2} + x_{B3} = 1 \quad (\text{Empresa B})$$
    $$x_{C1} + x_{C2} + x_{C3} = 1 \quad (\text{Empresa C})$$
*   **Cada central debe ser atendida por exactamente una empresa**:
    $$x_{A1} + x_{B1} + x_{C1} = 1 \quad (\text{Central 1})$$
    $$x_{A2} + x_{B2} + x_{C2} = 1 \quad (\text{Central 2})$$
    $$x_{A3} + x_{B3} + x_{C3} = 1 \quad (\text{Central 3})$$
*   **Naturaleza Binaria**:
    $$x_{ij} \in \{0, 1\} \quad \forall i \in \{A, B, C\}, j \in \{1, 2, 3\}$$

---

### 2.1. CLASIFICACIÓN CONCEPTUAL DE LOS MÉTODOS CANÓNICOS

En la teoría de Optimización e Investigación de Operaciones, el problema de asignación se aborda desde cuatro perspectivas complementarias:

#### 1. El Método Balanceado (Condición de Matriz Cuadrada $n \times n$)
*   **Fundamento**: El problema de asignación exige una correspondencia biyectiva (uno a uno) entre el conjunto de recursos (empresas) y el conjunto de tareas (centrales).
*   **Tratamiento de Desbalanceos**: Si el número de filas ($m$) difiere del de columnas ($n$):
    *   Si $m < n$ (más tareas que agentes): Se incorporan $n - m$ filas ficticias con costos nulos ($c_{\text{dummy}, j} = 0$).
    *   Si $m > n$ (más agentes que tareas): Se incorporan $m - n$ columnas ficticias con costos nulos ($c_{i, \text{dummy}} = 0$).
    *   Esto garantiza una matriz cuadrada balanceada de dimensión $k \times k$ donde $k = \max(m, n)$.
*   **Aplicación al Ejercicio 2**: Disponemos de 3 empresas y 3 centrales ($3 \times 3$). El problema es naturalmente balanceado y no requiere entidades ficticias.

#### 2. El Simplex Tradicional (Programación Lineal Binaria y Unimodularidad Total)
*   **Fundamento**: George Dantzig demostró que el problema de asignación puede formularse como un problema de Programación Lineal estándar continuo relajando la condición binaria a $0 \le x_{ij} \le 1$.
*   **Teorema de Unimodularidad Total**: La matriz de restricciones $\mathbf{A}$ del problema de asignación posee la propiedad de **Total Unimodularidad** (el determinante de cualquier submatriz cuadrada pertenece a $\{-1, 0, 1\}$).
*   **Consecuencia Teórica**: Debido a esta propiedad, **todos los vértices extremos del politopo de restricciones son necesariamente números enteros** ($0$ o $1$). Por consiguiente, el **Simplex Tradicional continuo** siempre encuentra la solución óptima binaria sin requerir ramificación y poda (Branch & Bound). En este proyecto está implementado mediante PuLP (motor HiGHS/CBC).

#### 3. El Método Normal (Algoritmo Húngaro / Kuhn-Munkres $O(n^3)$)
*   **Fundamento**: Desarrollado por Harold Kuhn (1955) y James Munkres (1957), basándose en los teoremas de dualidad combinatoria de Dénes Kőnig y Jenő Egerváry (1931).
*   **Mecánica**: Opera directamente sobre la matriz de costos reduciendo filas y columnas, cubriendo los ceros resultantes mediante el número mínimo de líneas y ajustando los valores no cubiertos mediante una constante dual $k$. Su complejidad polinomial estricta $O(n^3)$ lo consagra como el método canónico "normal" por excelencia para problemas de asignación.

#### 4. El Método Combinatorio Tradicional (Enumeración Exhaustiva $n!$)
*   **Fundamento**: Consiste en enumerar y evaluar formalmente cada una de las $n!$ permutaciones biyectivas posibles. Si bien garantiza hallar el óptimo global por exhaustividad, su complejidad factorial $O(n!)$ colapsa para $n > 12$.

---

### 3. DESARROLLO COMPARATIVO DE MÉTODOS DE RESOLUCIÓN

#### 3.1. Método Tradicional: Enumeración Exhaustiva (Fuerza Bruta $n!$)
El método combinatorial directo consiste en evaluar el costo total de cada una de las $n! = 3! = 6$ permutaciones biyectivas posibles:

| Permutación | Asignación Detallada | Desglose de Costos (miles de €) | Costo Total ($Z$) | Estado |
| :---: | :--- | :--- | :---: | :---: |
| **1** | A $\to$ 1, B $\to$ 2, C $\to$ 3 | $10 + 8 + 7$ | $25\text{k } €$ | Factible |
| **2** | **A $\to$ 1, B $\to$ 3, C $\to$ 2** | $\mathbf{10 + 3 + 4}$ | $\mathbf{17\text{k } €}$ | **ÓPTIMO GLOBAL** |
| **3** | A $\to$ 2, B $\to$ 1, C $\to$ 3 | $9 + 9 + 7$ | $25\text{k } €$ | Factible |
| **4** | A $\to$ 2, B $\to$ 3, C $\to$ 1 | $9 + 3 + 6$ | $18\text{k } €$ | Factible |
| **5** | A $\to$ 3, B $\to$ 1, C $\to$ 2 | $5 + 9 + 4$ | $18\text{k } €$ | Factible |
| **6** | A $\to$ 3, B $\to$ 2, C $\to$ 1 | $5 + 8 + 6$ | $19\text{k } €$ | Factible |

*Conclusión de Fuerza Bruta*: La combinación 2 minimiza el costo total con **$17$ mil euros** ($17.000 €$).

---

#### 3.2. Método Avanzado: Algoritmo Húngaro (Kuhn-Munkres $O(n^3)$)
El Método Húngaro opera sobre la matriz de costos reduciendo filas y columnas sin alterar el conjunto de asignaciones óptimas, basándose en la dualidad de Kőnig-Egerváry.

##### Matriz Original:
$$\begin{pmatrix} 10 & 9 & 5 \\ 9 & 8 & 3 \\ 6 & 4 & 7 \end{pmatrix}$$

##### Paso 1: Reducción por Filas
Se resta el menor valor de cada fila a todos los elementos de dicha fila:
*   Fila A: $\min = 5 \implies [10-5, 9-5, 5-5] = [5, 4, 0]$
*   Fila B: $\min = 3 \implies [9-3, 8-3, 3-3] = [6, 5, 0]$
*   Fila C: $\min = 4 \implies [6-4, 4-4, 7-4] = [2, 0, 3]$

$$\text{Matriz tras Paso 1: } \begin{pmatrix} 5 & 4 & 0 \\ 6 & 5 & 0 \\ 2 & 0 & 3 \end{pmatrix}$$

##### Paso 2: Reducción por Columnas
Se resta el menor valor de cada columna a todos los elementos de dicha columna:
*   Columna 1: $\min = 2 \implies [5-2, 6-2, 2-2]^T = [3, 4, 0]^T$
*   Columna 2: $\min = 0 \implies [4, 5, 0]^T$ (sin cambios)
*   Columna 3: $\min = 0 \implies [0, 0, 3]^T$ (sin cambios)

$$\text{Matriz tras Paso 2: } \begin{pmatrix} 3 & 4 & 0 \\ 4 & 5 & 0 \\ 0 & 0 & 3 \end{pmatrix}$$

##### Paso 3: Cobertura Mínima de Ceros
Se busca el número mínimo de líneas (horizontales o verticales) que cubran todos los ceros de la matriz:
*   Ceros existentes: $(A, 3)$, $(B, 3)$, $(C, 1)$, $(C, 2)$.
*   Se cubre la **Fila C** con 1 línea horizontal (cubre $(C, 1)$ y $(C, 2)$).
*   Se cubre la **Columna 3** con 1 línea vertical (cubre $(A, 3)$ y $(B, 3)$).
*   **Número de líneas necesarias**: $L = 2$.
*   Como $L = 2 < n = 3$, **no es posible realizar una asignación completa aún**. Se debe continuar al Paso 4.

##### Paso 4: Creación de Nuevos Ceros (Ajuste Dual)
1.  Se identifica el menor elemento entre los **no cubiertos** por ninguna línea:
    *   Elementos no cubiertos: $(A, 1)=3$, $(A, 2)=4$, $(B, 1)=4$, $(B, 2)=5$.
    *   $k = \min(3, 4, 4, 5) = 3$.
2.  Se resta $k = 3$ de todos los elementos no cubiertos:
    *   $(A, 1): 3 - 3 = 0$
    *   $(A, 2): 4 - 3 = 1$
    *   $(B, 1): 4 - 3 = 1$
    *   $(B, 2): 5 - 3 = 2$
3.  Se suma $k = 3$ a las intersecciones de dos líneas (Fila C y Columna 3):
    *   $(C, 3): 3 + 3 = 6$
4.  Los elementos cubiertos por una sola línea permanecen inalterados.

$$\text{Matriz tras Paso 4: } \begin{pmatrix} \mathbf{0} & 1 & 0 \\ 1 & 2 & \mathbf{0} \\ 0 & \mathbf{0} & 6 \end{pmatrix}$$

##### Paso 5: Asignación Final Óptima sobre Ceros
1.  En la **Fila B**, existe un único cero disponible en la **Columna 3**. Se asigna obligatoriamente:
    $$\mathbf{\text{Empresa B} \to \text{Central 3}}$$
2.  Al asignarse la Columna 3, en la **Fila A** el único cero restante está en la **Columna 1**:
    $$\mathbf{\text{Empresa A} \to \text{Central 1}}$$
3.  Con las Columnas 1 y 3 ocupadas, en la **Fila C** el cero disponible se encuentra en la **Columna 2**:
    $$\mathbf{\text{Empresa C} \to \text{Central 2}}$$
4.  Las 3 asignaciones cubren biyectivamente todas las entidades utilizando únicamente celdas de costo reducido cero.

---

### 4. RESULTADO FINAL ÓPTIMO

#### Asignación de Contratos y Costos Reales:

| Empresa Auxiliar | Central Eléctrica Asignada | Tipo de Central | Costo (miles de €) | Costo Real (€) |
| :--- | :--- | :--- | :---: | :---: |
| **Empresa A** | **Central 1** | Hidroeléctrica | $10\text{k } €$ | $10.000 €$ |
| **Empresa B** | **Central 3** | Nuclear | $3\text{k } €$ | $3.000 €$ |
| **Empresa C** | **Central 2** | Térmica Ciclo Combinado | $4\text{k } €$ | $4.000 €$ |
| **TOTAL** | | | **$17\text{k } €$** | **$17.000 €$** |

---

### 5. VERIFICACIÓN CRUZADA Y MEDICIÓN DE TIEMPOS

El script [`02.py`](file:///home/lincj/Documentos/S_&_M/02/02.py) verificó la solución comparando rigurosamente los enfoques metodológicos:

| Categoría Metodológica | Método / Algoritmo | Costo Obtenido | Complejidad Teórica | Tiempo CPU |
| :--- | :--- | :---: | :---: | :---: |
| **1. Método Balanceado** | Verificación de Matriz Cuadrada ($3 \times 3$) | $17\text{k } €$ | $O(1)$ | 0.010 ms |
| **2. Método Normal** | Algoritmo Húngaro (Kuhn-Munkres) | $17\text{k } €$ | $O(n^3)$ | 0.045 ms |
| **3. Simplex Tradicional** | Programación Lineal Binaria (PuLP / HiGHS) | $17\text{k } €$ | Polinomial / Simplex | 11.230 ms |
| **4. Método Combinatorio** | Enumeración Exhaustiva (Fuerza Bruta) | $17\text{k } €$ | $O(n!)$ | 0.082 ms |

#### Visualización del Grafo Bipartito:
El entregable gráfico [`02/asignacion_hungaro.png`](file:///home/lincj/Documentos/S_&_M/02/asignacion_hungaro.png) ilustra el emparejamiento biyectivo final óptimo conectando los nodos origen (empresas en azul) con los nodos destino (centrales en verde) y señalando los costos unitarios mínimos en rojo.


