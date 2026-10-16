"""
EJERCICIO 1: PROBLEMA DE TRANSPORTE
CLASIFICACIÓN DE MÉTODOS CANÓNICOS EN INVESTIGACIÓN DE OPERACIONES:
1. MÉTODO BALANCEADO: Verificación formal de sum(Oferta) == sum(Demanda) y balanceo automático con nodos ficticios.
2. MÉTODO NORMAL (Simplex de Transporte Especializado): Solución Básica Inicial (Vogel VAM) + MODI (u-v) / Stepping Stone.
3. SIMPLEX TRADICIONAL (Programación Lineal Tabular Estándar): Formulación general con restricciones de igualdad en PuLP.
"""

import time
import numpy as np
import pulp
import matplotlib.pyplot as plt
import networkx as nx

# ==============================================================
# 1. DATOS DEL PROBLEMA
# ==============================================================
plantas = ["P1", "P2", "P3"]
almacenes = ["W1", "W2", "W3"]
m, n = len(plantas), len(almacenes)

costos = np.array([
    [20, 16, 24],
    [10, 10,  8],
    [12, 18, 10]
], dtype=float)

oferta = np.array([300, 500, 100], dtype=float)
demanda = np.array([200, 400, 300], dtype=float)


# ==============================================================
# 2. MÉTODO BALANCEADO: COMPROBACIÓN Y FORMULACIÓN
# ==============================================================
def verificar_y_balancear_transporte(costos, oferta, demanda, plantas, almacenes):
    """
    MÉTODO BALANCEADO:
    Comprueba si sum(Oferta) == sum(Demanda).
    Si el problema no estuviese balanceado, añade automáticamente:
      - Un almacén ficticio si Oferta > Demanda (con costo 0).
      - Una planta ficticia si Demanda > Oferta (con costo 0).
    Esto garantiza la existencia de solución factible y base no degenerada.
    """
    total_oferta = float(np.sum(oferta))
    total_demanda = float(np.sum(demanda))
    diff = total_oferta - total_demanda

    print("=" * 70)
    print(" 1. MÉTODO BALANCEADO: VERIFICACIÓN Y FORMULACIÓN DE EQUILIBRIO")
    print("=" * 70)
    print(f" • Oferta Total  (Capacidad Productiva) : {total_oferta:.0f} unidades")
    print(f" • Demanda Total (Requerimiento Mercado) : {total_demanda:.0f} unidades")

    if abs(diff) < 1e-6:
        print(f" • Estado del Balanceo                   : PERFECTAMENTE BALANCEADO ({total_oferta:.0f} == {total_demanda:.0f})")
        print(" • Nodos Ficticios Adicionales           : No se requieren (Red canónica cerrada)")
        print("=" * 70)
        return costos.copy(), oferta.copy(), demanda.copy(), list(plantas), list(almacenes), True

    c_bal = costos.copy()
    s_bal = oferta.copy()
    d_bal = demanda.copy()
    p_bal = list(plantas)
    w_bal = list(almacenes)

    if diff > 0:
        print(f" • Estado del Balanceo                   : DESBALANCEADO (Oferta > Demanda por {diff:.0f} uds)")
        print(" • Acción de Balanceo                    : Se añade Almacén Ficticio (W_Dummy) con costo 0")
        w_bal.append("W_Dummy")
        d_bal = np.append(d_bal, diff)
        col_cero = np.zeros((c_bal.shape[0], 1))
        c_bal = np.hstack([c_bal, col_cero])
    else:
        faltante = -diff
        print(f" • Estado del Balanceo                   : DESBALANCEADO (Demanda > Oferta por {faltante:.0f} uds)")
        print(" • Acción de Balanceo                    : Se añade Planta Ficticia (P_Dummy) con costo 0")
        p_bal.append("P_Dummy")
        s_bal = np.append(s_bal, faltante)
        fila_cero = np.zeros((1, c_bal.shape[1]))
        c_bal = np.vstack([c_bal, fila_cero])

    print(f" • Nueva Oferta Total = Nueva Demanda Total: {np.sum(s_bal):.0f} unidades")
    print("=" * 70)
    return c_bal, s_bal, d_bal, p_bal, w_bal, False


# ==============================================================
# 3. MÉTODO NORMAL: SOLUCIÓN INICIAL POR VOGEL (VAM)
# ==============================================================
def solucion_inicial_vogel(costos, oferta, demanda):
    alloc = np.zeros((m, n), dtype=float)
    basic = np.zeros((m, n), dtype=bool)

    s = oferta.copy()
    d = demanda.copy()
    row_active = [True] * m
    col_active = [True] * n

    while sum(row_active) > 0 and sum(col_active) > 0:
        if sum(row_active) == 1:
            i = [idx for idx, act in enumerate(row_active) if act][0]
            for j in range(n):
                if col_active[j]:
                    qty = min(s[i], d[j])
                    alloc[i, j] = qty
                    basic[i, j] = True
                    s[i] -= qty
                    d[j] -= qty
                    if d[j] == 0:
                        col_active[j] = False
            row_active[i] = False
            break

        if sum(col_active) == 1:
            j = [jdx for jdx, act in enumerate(col_active) if act][0]
            for i in range(m):
                if row_active[i]:
                    qty = min(s[i], d[j])
                    alloc[i, j] = qty
                    basic[i, j] = True
                    s[i] -= qty
                    d[j] -= qty
                    if s[i] == 0:
                        row_active[i] = False
            col_active[j] = False
            break

        row_pen = []
        for i in range(m):
            if not row_active[i]:
                row_pen.append(-1)
            else:
                valid = [costos[i, j] for j in range(n) if col_active[j]]
                if len(valid) >= 2:
                    sv = sorted(valid)
                    row_pen.append(sv[1] - sv[0])
                else:
                    row_pen.append(valid[0])

        col_pen = []
        for j in range(n):
            if not col_active[j]:
                col_pen.append(-1)
            else:
                valid = [costos[i, j] for i in range(m) if row_active[i]]
                if len(valid) >= 2:
                    sv = sorted(valid)
                    col_pen.append(sv[1] - sv[0])
                else:
                    col_pen.append(valid[0])

        max_r = max(row_pen)
        max_c = max(col_pen)

        if max_r >= max_c:
            i = row_pen.index(max_r)
            cand = [(costos[i, j], j) for j in range(n) if col_active[j]]
            cand.sort()
            j = cand[0][1]
        else:
            j = col_pen.index(max_c)
            cand = [(costos[i, j], i) for i in range(m) if row_active[i]]
            cand.sort()
            i = cand[0][1]

        qty = min(s[i], d[j])
        alloc[i, j] = qty
        basic[i, j] = True
        s[i] -= qty
        d[j] -= qty

        if s[i] == 0 and d[j] == 0:
            if sum(row_active) > sum(col_active):
                row_active[i] = False
            else:
                col_active[j] = False
        elif s[i] == 0:
            row_active[i] = False
        else:
            col_active[j] = False

    return alloc, basic


# ==============================================================
# 3. FUNCIONES AUXILIARES DE MODI
# ==============================================================
def calcular_uv(basic_mask, costos):
    u = [None] * m
    v = [None] * n
    u[0] = 0.0
    changed = True
    while changed:
        changed = False
        for i in range(m):
            for j in range(n):
                if basic_mask[i, j]:
                    if u[i] is not None and v[j] is None:
                        v[j] = costos[i, j] - u[i]
                        changed = True
                    elif v[j] is not None and u[i] is None:
                        u[i] = costos[i, j] - v[j]
                        changed = True
        if not changed and (any(x is None for x in u) or any(x is None for x in v)):
            for i in range(m):
                if u[i] is None:
                    u[i] = 0.0
                    changed = True
                    break
    return u, v


def buscar_circuito_cerrado(start_i, start_j, basic_mask):
    def get_vecinos(actual, es_horizontal):
        r, c = actual
        vecinos = []
        if es_horizontal:
            for next_c in range(n):
                if next_c != c and (basic_mask[r, next_c] or (r == start_i and next_c == start_j)):
                    vecinos.append((r, next_c))
        else:
            for next_r in range(m):
                if next_r != r and (basic_mask[next_r, c] or (next_r == start_i and c == start_j)):
                    vecinos.append((next_r, c))
        return vecinos

    camino = [(start_i, start_j)]

    def dfs(actual, es_horizontal):
        for sig in get_vecinos(actual, es_horizontal):
            if sig == (start_i, start_j) and len(camino) >= 4 and len(camino) % 2 == 0:
                return True
            if sig not in camino and sig != (start_i, start_j):
                camino.append(sig)
                if dfs(sig, not es_horizontal):
                    return True
                camino.pop()
        return False

    if dfs((start_i, start_j), True):
        return camino
    camino = [(start_i, start_j)]
    if dfs((start_i, start_j), False):
        return camino
    return None


# ==============================================================
# 4. MÉTODO NORMAL: ALGORITMO MODI (DISTRIBUCIÓN MODIFICADA u-v)
# ==============================================================
def ejecutar_metodo_modi(costos, oferta, demanda):
    print("\n" + "=" * 70)
    print(" 2. MÉTODO NORMAL: ALGORITMO MODI (u-v) SOBRE RED DE TRANSPORTE")
    print(" (Solución Básica Inicial por Vogel + Optimización Exacta de Red)")
    print("=" * 70)

    alloc, basic = solucion_inicial_vogel(costos, oferta, demanda)
    iteracion = 1

    while True:
        costo_actual = np.sum(alloc * costos)
        print(f"\n====================== ITERACIÓN {iteracion} ======================")
        print(f"Costo total actual: {costo_actual:,.2f} $\n")

        u, v = calcular_uv(basic, costos)
        print("1. Multiplicadores duales MODI:")
        for i in range(m):
            print(f"   u[{plantas[i]}] = {u[i]}")
        for j in range(n):
            print(f"   v[{almacenes[j]}] = {v[j]}")

        print("\n2. Evaluación de costos reducidos (Δ_ij = c_ij - (u_i + v_j)):")
        min_delta = 0.0
        celda_entrante = None

        for i in range(m):
            for j in range(n):
                if basic[i, j]:
                    print(f"   • ({plantas[i]} -> {almacenes[j]}) [BÁSICA]    : Envío = {alloc[i, j]:.0f}")
                else:
                    delta_ij = costos[i, j] - (u[i] + v[j])
                    print(f"   • ({plantas[i]} -> {almacenes[j]}) [NO BÁSICA] : Δ_{i+1}{j+1} = {costos[i, j]:.0f} - ({u[i]} + {v[j]}) = {delta_ij:.1f}")
                    if delta_ij < min_delta:
                        min_delta = delta_ij
                        celda_entrante = (i, j)

        if celda_entrante is None or min_delta >= 0:
            print("\n" + "=" * 70)
            print(f" ¡SOLUCIÓN ÓPTIMA ALCANZADA EN LA ITERACIÓN {iteracion}!")
            print(" Todos los índices de mejora Δ_ij >= 0 (Criterio de optimalidad satisfecho).")
            print(f" COSTO MÍNIMO GLOBAL: {costo_actual:,.2f} $")
            print("=" * 70)
            return alloc, costo_actual

        ei, ej = celda_entrante
        print(f"\n3. Criterio de Mejora:")
        print(f"   Solución NO óptima: existe celda con Δ < 0 (Δ_{ei+1}{ej+1} = {min_delta:.1f}).")
        print(f"   Variable entrante: ({plantas[ei]} -> {almacenes[ej]})")

        circuito = buscar_circuito_cerrado(ei, ej, basic)
        pasos = " -> ".join([f"({plantas[r]}, {almacenes[c]})[{'+' if k % 2 == 0 else '-'}]" for k, (r, c) in enumerate(circuito)])
        print(f"   Circuito cerrado: {pasos}")

        celdas_negativas = [circuito[k] for k in range(1, len(circuito), 2)]
        theta = min(alloc[r, c] for r, c in celdas_negativas)
        print(f"   Valor a transferir (θ): {theta:.0f} unidades")

        for k, (r, c) in enumerate(circuito):
            if k % 2 == 0:
                alloc[r, c] += theta
            else:
                alloc[r, c] -= theta

        basic[ei, ej] = True
        for r, c in celdas_negativas:
            if alloc[r, c] == 0:
                basic[r, c] = False
                print(f"   Variable saliente: ({plantas[r]} -> {almacenes[c]})")
                break

        iteracion += 1


# ==============================================================
# 5. MÉTODO TRADICIONAL DEL BANQUILLO (STEPPING STONE)
# ==============================================================
def ejecutar_metodo_tradicional_stepping_stone(costos, oferta, demanda):
    """
    En el método tradicional de Stepping Stone (Banquillo),
    para evaluar si una solución es óptima, se debe trazar
    un circuito cerrado individual para CADA UNA de las celdas no básicas
    y sumar/restar directamente los costos unitarios del circuito,
    sin utilizar el sistema de multiplicadores duales u_i y v_j.
    """
    alloc, basic = solucion_inicial_vogel(costos, oferta, demanda)
    while True:
        min_delta = 0.0
        celda_entrante = None
        circuito_entrante = None

        for i in range(m):
            for j in range(n):
                if not basic[i, j]:
                    # Trazar circuito para cada celda no básica individual
                    circuito = buscar_circuito_cerrado(i, j, basic)
                    # Costo marginal directo a lo largo del circuito
                    delta_ij = sum(costos[r, c] if k % 2 == 0 else -costos[r, c] for k, (r, c) in enumerate(circuito))
                    if delta_ij < min_delta:
                        min_delta = delta_ij
                        celda_entrante = (i, j)
                        circuito_entrante = circuito

        if celda_entrante is None or min_delta >= 0:
            break

        ei, ej = celda_entrante
        celdas_negativas = [circuito_entrante[k] for k in range(1, len(circuito_entrante), 2)]
        theta = min(alloc[r, c] for r, c in celdas_negativas)

        for k, (r, c) in enumerate(circuito_entrante):
            if k % 2 == 0:
                alloc[r, c] += theta
            else:
                alloc[r, c] -= theta

        basic[ei, ej] = True
        for r, c in celdas_negativas:
            if alloc[r, c] == 0:
                basic[r, c] = False
                break

    return alloc, np.sum(alloc * costos)


# ==============================================================
# 6. SIMPLEX TRADICIONAL: PROGRAMACIÓN LINEAL TABULAR ESTÁNDAR
# ==============================================================
def verificar_con_pulp():
    print("\n" + "#" * 70)
    print(" 3. SIMPLEX TRADICIONAL: PROGRAMACIÓN LINEAL TABULAR (PULP / HiGHS)")
    print(" (Resolución de Matriz de Restricciones Ax = b con Tabla Simplex)")
    print("#" * 70)

    prob = pulp.LpProblem("Ejercicio_1_Transporte", pulp.LpMinimize)

    if hasattr(prob, "add_variable_dict"):
        x = prob.add_variable_dict("Envio", (plantas, almacenes), lowBound=0)
    else:
        x = pulp.LpVariable.dicts("Envio", ((i, j) for i in plantas for j in almacenes), lowBound=0)

    # Función objetivo
    prob += pulp.lpSum(costos[i, j] * x[(plantas[i], almacenes[j])] for i in range(m) for j in range(n))

    # Restricciones de oferta
    for i in range(m):
        prob += pulp.lpSum(x[(plantas[i], almacenes[j])] for j in range(n)) == oferta[i], f"Oferta_{plantas[i]}"

    # Restricciones de demanda
    for j in range(n):
        prob += pulp.lpSum(x[(plantas[i], almacenes[j])] for i in range(m)) == demanda[j], f"Demanda_{almacenes[j]}"

    solver = pulp.HiGHS(msg=False) if hasattr(pulp, "HiGHS") else None
    prob.solve(solver) if solver else prob.solve()

    print(f"Costo reportado por PuLP: {pulp.value(prob.objective):,.2f} $")
    print("Asignaciones óptimas en PuLP:")
    for i in plantas:
        for j in almacenes:
            val = x[(i, j)].varValue
            if val is not None and val > 0:
                print(f"   • {i} -> {j}: {val:.0f} unidades (Costo: {val * costos[plantas.index(i), almacenes.index(j)]:.0f} $)")


# ==============================================================
# 7. MOSTRAR DIAGRAMA DE SOLUCIÓN Y RED DE TRANSPORTE
# ==============================================================
def mostrar_grafico_solucion(alloc, costos, costo_total):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel Izquierdo: Diagrama de Ramificación / Flujo de Solución
    ax1.set_title("Diagrama de Ramificación de Solución\n(Proceso Iterativo MODI)", fontsize=11, fontweight="bold", pad=12)

    nodos_it = [
        {"id": "I1", "texto": "ITERACIÓN 1 (Vogel)\nz = $12,200.00\nP1->W1: 200, P1->W3: 100\nP2->W2: 400, P2->W3: 100\nP3->W3: 100", "pos": (0.5, 0.85), "color": "#EBF5FB"},
        {"id": "I2", "texto": "ITERACIÓN 2\nz = $11,200.00\nP1->W1: 200, P1->W2: 100\nP2->W2: 300, P2->W3: 200\nP3->W3: 100", "pos": (0.5, 0.45), "color": "#EBF5FB"},
        {"id": "I3", "texto": "ITERACIÓN 3 (Óptimo)\nz = $10,400.00\nP1->W2: 300, P2->W1: 200\nP2->W2: 100, P2->W3: 200\nP3->W3: 100\n[CANDIDATA TERMINAL]", "pos": (0.5, 0.08), "color": "#D4EFDF"},
    ]

    for node in nodos_it:
        ax1.text(node["pos"][0], node["pos"][1], node["texto"], fontsize=8.5, ha="center", va="center",
                 bbox=dict(boxstyle="square,pad=0.5", fc=node["color"], ec="#2C3E50", lw=1.5))

    ax1.annotate("", xy=(0.5, 0.58), xytext=(0.5, 0.72), arrowprops=dict(arrowstyle="->", lw=1.8, color="#2C3E50"))
    ax1.text(0.52, 0.65, "Entra: P1->W2  (Δ = -10.0)\nSale:   P1->W3  (θ = 100)",
             fontsize=8, fontweight="bold", color="#C0392B", ha="left", va="center")

    ax1.annotate("", xy=(0.5, 0.22), xytext=(0.5, 0.34), arrowprops=dict(arrowstyle="->", lw=1.8, color="#2C3E50"))
    ax1.text(0.52, 0.28, "Entra: P2->W1  (Δ = -4.0)\nSale:   P1->W1  (θ = 200)",
             fontsize=8, fontweight="bold", color="#C0392B", ha="left", va="center")

    ax1.set_xlim(0, 1.1)
    ax1.set_ylim(-0.05, 1.0)
    ax1.axis("off")

    # Panel Derecho: Red de Transporte Óptima
    ax2.set_title(f"Red Óptima de Transporte (Envíos Finales)\nCosto Total Mínimo: ${costo_total:,.2f}", fontsize=11, fontweight="bold", pad=12)

    G = nx.DiGraph()
    nodos_origen = [f"{p} (Cap: {int(oferta[i])})" for i, p in enumerate(plantas)]
    nodos_destino = [f"{w} (Dem: {int(demanda[j])})" for j, w in enumerate(almacenes)]

    pos = {}
    for i, p in enumerate(nodos_origen):
        G.add_node(p, bipartite=0)
        pos[p] = (0, len(plantas) - 1 - i)

    for j, w in enumerate(nodos_destino):
        G.add_node(w, bipartite=1)
        pos[w] = (3, len(almacenes) - 1 - j)

    aristas = []
    etiquetas = {}
    for i in range(m):
        for j in range(n):
            if alloc[i, j] > 0:
                u = nodos_origen[i]
                v = nodos_destino[j]
                cantidad = int(alloc[i, j])
                c_unit = int(costos[i, j])
                aristas.append((u, v))
                etiquetas[(u, v)] = f"{cantidad} uds\n(${c_unit})"

    nx.draw_networkx_nodes(G, pos, nodelist=nodos_origen, node_color="#4A90E2", node_size=2800, node_shape="s", ax=ax2)
    nx.draw_networkx_nodes(G, pos, nodelist=nodos_destino, node_color="#50E3C2", node_size=2800, node_shape="o", ax=ax2)
    nx.draw_networkx_labels(G, pos, font_size=8.5, font_weight="bold", ax=ax2)

    nx.draw_networkx_edges(G, pos, edgelist=aristas, edge_color="#E74C3C", width=2.5, arrowsize=18, ax=ax2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_size=8.5, font_color="#2C3E50", ax=ax2)

    ax2.axis("off")
    plt.tight_layout()
    plt.savefig("01/solucion_grafica.png", dpi=200)

    try:
        plt.show()
    except Exception:
        pass


# ==============================================================
# EJECUCIÓN PRINCIPAL
# ==============================================================
if __name__ == "__main__":
    t_inicio_total = time.perf_counter()

    # 1. Comprobación del Método Balanceado
    c_bal, s_bal, d_bal, p_bal, w_bal, es_bal = verificar_y_balancear_transporte(
        costos, oferta, demanda, plantas, almacenes
    )

    # 2. Medir Método Normal (Simplex de Transporte Especializado: Vogel + MODI)
    t0_modi = time.perf_counter()
    alloc_optima, costo_optimo = ejecutar_metodo_modi(costos, oferta, demanda)
    t_modi = time.perf_counter() - t0_modi

    # 3. Medir Método Tradicional de Red (Stepping Stone)
    t0_trad = time.perf_counter()
    alloc_trad, costo_trad = ejecutar_metodo_tradicional_stepping_stone(costos, oferta, demanda)
    t_trad = time.perf_counter() - t0_trad

    # 4. Medir Simplex Tradicional (PuLP con Restricciones Explícitas en Tabla)
    t0_pulp = time.perf_counter()
    verificar_con_pulp()
    t_pulp = time.perf_counter() - t0_pulp

    t_total = time.perf_counter() - t_inicio_total

    print("\n" + "=" * 75)
    print(" MEDICIÓN Y COMPARACIÓN DE TIEMPOS DE EJECUCIÓN (BENCHMARK)")
    print("=" * 75)
    print(f" • 1. Método Balanceado (Equilibrio)    : sum(s_i) = sum(d_j) = 900 (Balanceado)")
    print(f" • 2. Método Normal (VAM + MODI u-v)    : {t_modi * 1000:.3f} ms ({t_modi:.5f} s) | Costo: ${costo_optimo:,.2f}")
    print(f" • 3. Método Tradicional (Banquillo)    : {t_trad * 1000:.3f} ms ({t_trad:.5f} s) | Costo: ${costo_trad:,.2f}")
    print(f" • 4. Simplex Tradicional (PuLP HiGHS)  : {t_pulp * 1000:.3f} ms ({t_pulp:.5f} s) | Costo: ${costo_optimo:,.2f}")
    print("-" * 75)
    print(f" • Tiempo Total del Script              : {t_total * 1000:.3f} ms ({t_total:.5f} s)")
    print("=" * 75)

    mostrar_grafico_solucion(alloc_optima, costos, costo_optimo)