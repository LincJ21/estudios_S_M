"""
EJERCICIO 2: PROBLEMA DE ASIGNACIÓN
CLASIFICACIÓN DE MÉTODOS CANÓNICOS EN INVESTIGACIÓN DE OPERACIONES:
1. MÉTODO BALANCEADO: Verificación formal de matriz cuadrada n x n (Empresas == Centrales) y balanceo automático con entidades ficticias.
2. MÉTODO NORMAL (Algoritmo Especializado Canónico): Método Húngaro (Kuhn-Munkres O(n^3)) con dualidad Kőnig-Egerváry.
3. SIMPLEX TRADICIONAL (Programación Lineal Entera Binaria): Formulación estándar en PuLP con Unimodularidad Total.
4. MÉTODO COMBINATORIO TRADICIONAL: Enumeración Exhaustiva (Fuerza Bruta n!).

Mantenimiento preventivo de tres centrales eléctricas por tres empresas auxiliares.
Costos (en miles de euros):
             Central 1   Central 2   Central 3
  Empresa A     10           9           5
  Empresa B      9           8           3
  Empresa C      6           4           7
"""

import time
import math
import itertools
import numpy as np
import pulp
import matplotlib.pyplot as plt
import networkx as nx

# ==============================================================
# 1. DATOS DEL PROBLEMA
# ==============================================================
empresas = ["Empresa A", "Empresa B", "Empresa C"]
centrales = ["Central 1", "Central 2", "Central 3"]
n = len(empresas)

costos_originales = np.array([
    [10, 9, 5],
    [ 9, 8, 3],
    [ 6, 4, 7]
], dtype=float)


# ==============================================================
# 2. MÉTODO BALANCEADO: COMPROBACIÓN Y FORMULACIÓN CUADRADA (n x n)
# ==============================================================
def verificar_y_balancear_asignacion(costos, empresas, centrales):
    """
    MÉTODO BALANCEADO:
    Para aplicar el Método Húngaro y la formulación canónica de asignación,
    el número de agentes (filas) debe ser exactamente igual al número de tareas (columnas).
    Si m != n:
      - Si filas < columnas: Se añaden empresas/agentes ficticios con costo 0.
      - Si columnas < filas: Se añaden centrales/tareas ficticias con costo 0.
    """
    n_filas, n_cols = costos.shape
    print("=" * 70)
    print(" 1. MÉTODO BALANCEADO: VERIFICACIÓN Y FORMULACIÓN CUADRADA")
    print("=" * 70)
    print(f" • Cantidad de Agentes (Empresas) : {n_filas}")
    print(f" • Cantidad de Tareas (Centrales) : {n_cols}")

    if n_filas == n_cols:
        print(f" • Estado del Balanceo            : PERFECTAMENTE BALANCEADO ({n_filas}x{n_cols} Cuadrada)")
        print(" • Entidades Ficticias            : No se requieren (Asignación biyectiva directa)")
        print("=" * 70)
        return costos.copy(), list(empresas), list(centrales), True

    c_bal = costos.copy()
    e_bal = list(empresas)
    cnt_bal = list(centrales)

    if n_filas < n_cols:
        diff = n_cols - n_filas
        print(f" • Estado del Balanceo            : DESBALANCEADO (Faltan {diff} agentes)")
        for k in range(diff):
            e_bal.append(f"Empresa_Dummy_{k+1}")
        c_bal = np.vstack([c_bal, np.zeros((diff, n_cols))])
    else:
        diff = n_filas - n_cols
        print(f" • Estado del Balanceo            : DESBALANCEADO (Faltan {diff} tareas)")
        for k in range(diff):
            cnt_bal.append(f"Central_Dummy_{k+1}")
        c_bal = np.hstack([c_bal, np.zeros((n_filas, diff))])

    print(f" • Nueva Dimensión Balanceada      : {c_bal.shape[0]}x{c_bal.shape[1]}")
    print("=" * 70)
    return c_bal, e_bal, cnt_bal, False


# ==============================================================
# 3. MÉTODO COMBINATORIO TRADICIONAL: ENUMERACIÓN EXHAUSTIVA (FUERZA BRUTA n!)
# ==============================================================
def ejecutar_metodo_tradicional_enumeracion(costos):
    """
    El método tradicional directo para problemas de asignación consiste
    en la Enumeración Exhaustiva de todas las n! permutaciones posibles
    de asignación biyectiva entre empresas y centrales, evaluando
    el coste total de cada combinación y eligiendo la de menor costo.
    """
    print("\n" + "=" * 70)
    print(" 1. MÉTODO TRADICIONAL: ENUMERACIÓN EXHAUSTIVA (FUERZA BRUTA)")
    print(f" Evaluación de todas las n! permutaciones ({n}! = {math.factorial(n)} combinaciones)")
    print("=" * 70)

    mejor_costo = float("inf")
    mejor_permutacion = None
    indice = 1

    for perm in itertools.permutations(range(n)):
        costo_comb = sum(costos[i, perm[i]] for i in range(n))
        detalle = " + ".join([f"{costos[i, perm[i]]:.0f} ({empresas[i]}->{centrales[perm[i]]})" for i in range(n)])
        print(f" Combinación {indice}: {detalle} = {costo_comb:.0f}k €")

        if costo_comb < mejor_costo:
            mejor_costo = costo_comb
            mejor_permutacion = perm
        indice += 1

    print("-" * 70)
    print(" Asignación Óptima Tradicional:")
    for i in range(n):
        j = mejor_permutacion[i]
        print(f"  • {empresas[i]} ---> {centrales[j]} (Coste: {costos[i, j]:.0f}k €)")
    print(f" COSTE MÍNIMO TRADICIONAL: {mejor_costo:.0f} mil euros ({int(mejor_costo)*1000:,} €)")
    print("=" * 70)

    return mejor_permutacion, mejor_costo


# ==============================================================
# 4. MÉTODO NORMAL: ALGORITMO HÚNGARO (KUHN-MUNKRES O(n^3))
# ==============================================================
def ejecutar_metodo_hungaro(costos):
    print("\n" + "=" * 70)
    print(" 2. MÉTODO NORMAL: ALGORITMO HÚNGARO (KUHN-MUNKRES POLINOMIAL O(n^3))")
    print(" (Algoritmo Especializado Canónico de Asignación Biyectiva)")
    print("=" * 70)

    matriz = costos.copy()

    print("\n--- MATRIZ ORIGINAL DE COSTOS (miles de €) ---")
    print(f"{'':12}" + "".join([f"{c:>12}" for c in centrales]))
    for i, emp in enumerate(empresas):
        valores = "".join([f"{int(matriz[i, j]):>12}" for j in range(n)])
        print(f"{emp:12}{valores}")

    # PASO 1: Reducción por Filas
    print("\n" + "-" * 70)
    print("PASO 1: Reducción por Filas (Restar el menor valor de cada fila)")
    print("-" * 70)
    minimos_filas = np.min(matriz, axis=1)
    for i, emp in enumerate(empresas):
        print(f" • Mínimo de {emp}: {int(minimos_filas[i])}")
        matriz[i, :] -= minimos_filas[i]

    print("\nMatriz después del Paso 1:")
    print(f"{'':12}" + "".join([f"{c:>12}" for c in centrales]))
    for i, emp in enumerate(empresas):
        valores = "".join([f"{int(matriz[i, j]):>12}" for j in range(n)])
        print(f"{emp:12}{valores}")

    # PASO 2: Reducción por Columnas
    print("\n" + "-" * 70)
    print("PASO 2: Reducción por Columnas (Restar el menor valor de cada columna)")
    print("-" * 70)
    minimos_columnas = np.min(matriz, axis=0)
    for j, cent in enumerate(centrales):
        print(f" • Mínimo de {cent}: {int(minimos_columnas[j])}")
        matriz[:, j] -= minimos_columnas[j]

    print("\nMatriz después del Paso 2:")
    print(f"{'':12}" + "".join([f"{c:>12}" for c in centrales]))
    for i, emp in enumerate(empresas):
        valores = "".join([f"{int(matriz[i, j]):>12}" for j in range(n)])
        print(f"{emp:12}{valores}")

    # PASO 3 & 4: Trazado de líneas mínimas
    def encontrar_lineas_minimas(m_ceros):
        grafo = {i: [j for j in range(n) if m_ceros[i, j] == 0] for i in range(n)}
        match_r, match_c = {}, {}

        for r in range(n):
            visitados = set()
            def dfs(u):
                for v in grafo[u]:
                    if v not in visitados:
                        visitados.add(v)
                        if v not in match_c or dfs(match_c[v]):
                            match_r[u] = v
                            match_c[v] = u
                            return True
                return False
            dfs(r)

        filas_no_cubiertas = [r for r in range(n) if r not in match_r]
        filas_visitadas = set(filas_no_cubiertas)
        cols_visitadas = set()

        cola = list(filas_no_cubiertas)
        while cola:
            curr_r = cola.pop(0)
            for c in grafo[curr_r]:
                if c not in cols_visitadas:
                    cols_visitadas.add(c)
                    if c in match_c and match_c[c] not in filas_visitadas:
                        filas_visitadas.add(match_c[c])
                        cola.append(match_c[c])

        filas_con_linea = [r for r in range(n) if r not in filas_visitadas]
        cols_con_linea = list(cols_visitadas)
        num_lineas = len(filas_con_linea) + len(cols_con_linea)

        return num_lineas, filas_con_linea, cols_con_linea, match_r

    iteracion = 1
    while True:
        num_lineas, filas_linea, cols_linea, asignacion_indices = encontrar_lineas_minimas(matriz)
        print("\n" + "-" * 70)
        print(f"PASO 3 (Iteración {iteracion}): Cubrimiento de ceros con líneas mínimas")
        print("-" * 70)
        print(f" • Número de líneas necesarias: {num_lineas} (Tamaño requerido N = {n})")

        lineas_desc = []
        if filas_linea:
            lineas_desc.append("Filas: " + ", ".join([empresas[r] for r in filas_linea]))
        if cols_linea:
            lineas_desc.append("Columnas: " + ", ".join([centrales[c] for c in cols_linea]))
        print(f" • Líneas trazadas: {'; '.join(lineas_desc)}")

        if num_lineas >= n:
            print(" >>> Condición satisfecha: Número de líneas = N. ¡Asignación óptima alcanzada! <<<")
            break

        # PASO 4: Modificación por el menor no cubierto
        no_cubiertos = [matriz[r, c] for r in range(n) for c in range(n) if r not in filas_linea and c not in cols_linea]
        k = min(no_cubiertos)
        print(f"\nPASO 4: Ajuste de la matriz (Líneas {num_lineas} < {n})")
        print(f" • Elemento no cubierto mínimo (k): {int(k)}")
        print(f" • Restar {int(k)} a los elementos no cubiertos y sumarlo a las intersecciones.")

        for r in range(n):
            for c in range(n):
                if r not in filas_linea and c not in cols_linea:
                    matriz[r, c] -= k
                elif r in filas_linea and c in cols_linea:
                    matriz[r, c] += k

        print("\nMatriz después del ajuste:")
        print(f"{'':12}" + "".join([f"{c:>12}" for c in centrales]))
        for i, emp in enumerate(empresas):
            valores = "".join([f"{int(matriz[i, j]):>12}" for j in range(n)])
            print(f"{emp:12}{valores}")

        iteracion += 1

    # PASO 5: Asignación Final Óptima
    print("\n" + "=" * 70)
    print(" RESULTADO FINAL: ASIGNACIÓN ÓPTIMA (MÉTODO HÚNGARO)")
    print("=" * 70)

    asignaciones = []
    costo_total = 0.0

    for i in range(n):
        j = asignacion_indices[i]
        c = costos[i, j]
        costo_total += c
        asignaciones.append((empresas[i], centrales[j], c))
        print(f" • {empresas[i]} ---> {centrales[j]} | Coste: {int(c)} mil euros ({int(c)*1000:,} €)")

    print(f"\n COSTE TOTAL MÍNIMO: {int(costo_total)} mil euros ({int(costo_total)*1000:,} €)")
    print("=" * 70)

    return asignaciones, costo_total


# ==============================================================
# 5. SIMPLEX TRADICIONAL: PROGRAMACIÓN LINEAL BINARIA (PULP)
# ==============================================================
def verificar_con_pulp(costos):
    print("\n" + "#" * 70)
    print(" 3. SIMPLEX TRADICIONAL: PROGRAMACIÓN LINEAL BINARIA (PULP / HiGHS)")
    print(" (Solución Continua de Vértices Enteros vía Unimodularidad Total)")
    print("#" * 70)

    prob = pulp.LpProblem("Problema_Asignacion_Electrica", pulp.LpMinimize)

    if hasattr(prob, "add_variable_dict"):
        x = prob.add_variable_dict("Asig", (empresas, centrales), cat="Binary")
    else:
        x = pulp.LpVariable.dicts("Asig", ((i, j) for i in empresas for j in centrales), cat="Binary")

    prob += pulp.lpSum(costos[i, j] * x[(empresas[i], centrales[j])] for i in range(n) for j in range(n))

    for i in range(n):
        prob += pulp.lpSum(x[(empresas[i], centrales[j])] for j in range(n)) == 1, f"Empresa_{empresas[i]}"

    for j in range(n):
        prob += pulp.lpSum(x[(empresas[i], centrales[j])] for i in range(n)) == 1, f"Central_{centrales[j]}"

    solver = pulp.HiGHS(msg=False) if hasattr(pulp, "HiGHS") else None
    prob.solve(solver) if solver else prob.solve()

    costo_pulp = pulp.value(prob.objective)
    print(f"Costo reportado por PuLP: {int(costo_pulp)} mil euros ({int(costo_pulp)*1000:,} €)")
    print("Asignaciones óptimas en PuLP:")
    for i in range(n):
        for j in range(n):
            if x[(empresas[i], centrales[j])].varValue == 1:
                c = int(costos[i, j])
                print(f"   • {empresas[i]} -> {centrales[j]}: {c} mil euros")

    return costo_pulp


# ==============================================================
# 6. VISUALIZACIÓN GRÁFICA DE LA ASIGNACIÓN
# ==============================================================
def mostrar_grafico_asignacion(asignaciones, costo_total, ruta_guardado="02/asignacion_hungaro.png"):
    plt.figure(figsize=(9, 6))
    G = nx.DiGraph()

    pos = {}
    for i, emp in enumerate(empresas):
        G.add_node(emp, bipartite=0)
        pos[emp] = (0, 2 - i)

    for j, cent in enumerate(centrales):
        G.add_node(cent, bipartite=1)
        pos[cent] = (3, 2 - j)

    aristas = []
    etiquetas = {}
    for emp, cent, c in asignaciones:
        aristas.append((emp, cent))
        etiquetas[(emp, cent)] = f"Coste: {int(c)}k €"

    nx.draw_networkx_nodes(G, pos, nodelist=empresas, node_color="#3498DB", node_size=3200, node_shape="s")
    nx.draw_networkx_nodes(G, pos, nodelist=centrales, node_color="#2ECC71", node_size=3200, node_shape="o")
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

    nx.draw_networkx_edges(G, pos, edgelist=aristas, edge_color="#E74C3C", width=3, arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_size=10, font_color="#2C3E50")

    plt.title(f"Asignación Óptima - Método Húngaro\nCoste Total Mínimo: {int(costo_total)} mil euros ({int(costo_total)*1000:,} €)",
              fontsize=12, fontweight="bold", pad=15)
    plt.axis("off")
    plt.tight_layout()

    import os
    os.makedirs("02", exist_ok=True)
    plt.savefig(ruta_guardado, dpi=200)

    try:
        plt.show()
    except Exception:
        pass


# ==============================================================
# EJECUCIÓN PRINCIPAL CON BENCHMARK DE TIEMPOS
# ==============================================================
if __name__ == "__main__":
    t_inicio_total = time.perf_counter()

    # 1. Comprobación del Método Balanceado
    c_bal, e_bal, cnt_bal, es_bal = verificar_y_balancear_asignacion(
        costos_originales, empresas, centrales
    )

    # 2. Medir Método Tradicional Combinatorio (Enumeración Exhaustiva n!)
    t0_trad = time.perf_counter()
    perm_trad, costo_trad = ejecutar_metodo_tradicional_enumeracion(costos_originales)
    t_trad = time.perf_counter() - t0_trad

    # 3. Medir Método Normal (Algoritmo Húngaro O(n^3))
    t0_hungaro = time.perf_counter()
    asignaciones_optimas, costo_hungaro = ejecutar_metodo_hungaro(costos_originales)
    t_hungaro = time.perf_counter() - t0_hungaro

    # 4. Medir Simplex Tradicional (PuLP Programación Entera Binaria)
    t0_pulp = time.perf_counter()
    costo_pulp = verificar_con_pulp(costos_originales)
    t_pulp = time.perf_counter() - t0_pulp

    t_total = time.perf_counter() - t_inicio_total

    # Benchmark Comparativo
    print("\n" + "=" * 75)
    print(" MEDICIÓN Y COMPARACIÓN DE TIEMPOS DE EJECUCIÓN (BENCHMARK)")
    print("=" * 75)
    print(f" • 1. Método Balanceado (Equilibrio)    : Matriz 3x3 (Perfectamente Balanceado)")
    print(f" • 2. Método Normal (Húngaro O(n^3))    : {t_hungaro * 1000:.3f} ms ({t_hungaro:.5f} s) | Coste: {costo_hungaro:.0f}k €")
    print(f" • 3. Simplex Tradicional (PuLP HiGHS)  : {t_pulp * 1000:.3f} ms ({t_pulp:.5f} s) | Coste: {costo_pulp:.0f}k €")
    print(f" • 4. Método Exhaustivo (Fuerza Bruta)  : {t_trad * 1000:.3f} ms ({t_trad:.5f} s) | Coste: {costo_trad:.0f}k €")
    print("-" * 75)
    print(f" • Tiempo Total del Script              : {t_total * 1000:.3f} ms ({t_total:.5f} s)")
    print("=" * 75)

    mostrar_grafico_asignacion(asignaciones_optimas, costo_hungaro)
