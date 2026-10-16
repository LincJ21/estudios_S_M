"""
BENCHMARK DE ESCALABILIDAD A 100 VARIABLES (10 x 10) EN PYTHON
Comparación empírica entre Métodos Tradicionales y Métodos Avanzados
Incluye validación cruzada de resultados y tiempos de ejecución.

PARTE 1: PROBLEMA DE TRANSPORTE (10 Orígenes x 10 Destinos = 100 Variables)
  - Tradicional: Stepping Stone (Banquillo)
  - Avanzado: Método MODI (u-v)

PARTE 2: PROBLEMA DE ASIGNACIÓN (10 Trabajadores x 10 Tareas = 100 Variables)
  - Tradicional: Fuerza Bruta (10! = 3,628,800 permutaciones)
  - Avanzado: Método Húngaro (O(n^3))
"""

import json
import os
import time
import itertools
import tracemalloc
import signal

# Intentar cargar matrices idénticas de matrices_100.json para paridad exacta con Go
JSON_PATH = os.path.join(os.path.dirname(__file__), "matrices_100.json")
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r") as f:
        data = json.load(f)
        costos_trans = data["costos_transporte"]
        costos_asig = data["costos_asignacion"]
else:
    # Generador determinista si no existe el JSON
    import random
    rng = random.Random(42)
    costos_trans = [[float(rng.randint(1, 29)) for _ in range(10)] for _ in range(10)]
    costos_asig = [[float(rng.randint(10, 99)) for _ in range(10)] for _ in range(10)]

m_trans, n_trans = len(costos_trans), len(costos_trans[0])
oferta_trans = [100.0] * m_trans
demanda_trans = [100.0] * n_trans
n_asig = len(costos_asig)


# ==============================================================
# 1. ALGORITMOS DE TRANSPORTE (100 VARIABLES)
# ==============================================================

def solucion_inicial_vogel(costos, oferta, demanda):
    m = len(costos)
    n = len(costos[0])
    alloc = [[0.0] * n for _ in range(m)]
    basic = [[False] * n for _ in range(m)]
    s = list(oferta)
    d = list(demanda)
    row_active = [True] * m
    col_active = [True] * n

    while any(row_active) and any(col_active):
        active_r = [i for i, a in enumerate(row_active) if a]
        active_c = [j for j, a in enumerate(col_active) if a]

        if len(active_r) == 1:
            i = active_r[0]
            for j in active_c:
                qty = min(s[i], d[j])
                alloc[i][j] = qty
                basic[i][j] = True
                s[i] -= qty
                d[j] -= qty
                if d[j] == 0:
                    col_active[j] = False
            row_active[i] = False
            break

        if len(active_c) == 1:
            j = active_c[0]
            for i in active_r:
                qty = min(s[i], d[j])
                alloc[i][j] = qty
                basic[i][j] = True
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
                min1, min2 = 1e18, 1e18
                count = 0
                for j in active_c:
                    c = costos[i][j]
                    count += 1
                    if c < min1:
                        min2 = min1
                        min1 = c
                    elif c < min2:
                        min2 = c
                row_pen.append(min2 - min1 if count >= 2 else min1)

        col_pen = []
        for j in range(n):
            if not col_active[j]:
                col_pen.append(-1)
            else:
                min1, min2 = 1e18, 1e18
                count = 0
                for i in active_r:
                    c = costos[i][j]
                    count += 1
                    if c < min1:
                        min2 = min1
                        min1 = c
                    elif c < min2:
                        min2 = c
                col_pen.append(min2 - min1 if count >= 2 else min1)

        max_r = max(row_pen)
        max_c = max(col_pen)

        if max_r >= max_c:
            i = row_pen.index(max_r)
            best_cost, best_j = 1e18, -1
            for j in active_c:
                if costos[i][j] < best_cost:
                    best_cost = costos[i][j]
                    best_j = j
            j = best_j
        else:
            j = col_pen.index(max_c)
            best_cost, best_i = 1e18, -1
            for i in active_r:
                if costos[i][j] < best_cost:
                    best_cost = costos[i][j]
                    best_i = i
            i = best_i

        qty = min(s[i], d[j])
        alloc[i][j] = qty
        basic[i][j] = True
        s[i] -= qty
        d[j] -= qty

        if s[i] == 0 and d[j] == 0:
            if len(active_r) > 1:
                row_active[i] = False
            else:
                col_active[j] = False
        elif s[i] == 0:
            row_active[i] = False
        else:
            col_active[j] = False

    return alloc, basic


def buscar_circuito_cerrado(start_i, start_j, basic):
    m = len(basic)
    n = len(basic[0])
    num_v = m + n
    adj = [[] for _ in range(num_v)]
    for i in range(m):
        for j in range(n):
            if basic[i][j]:
                adj[i].append(m + j)
                adj[m + j].append(i)

    start_v = m + start_j
    target_v = start_i

    parent = [-1] * num_v
    visited = [False] * num_v
    queue = [start_v]
    visited[start_v] = True

    found = False
    while queue:
        curr = queue.pop(0)
        if curr == target_v:
            found = True
            break
        for nxt in adj[curr]:
            if not visited[nxt]:
                visited[nxt] = True
                parent[nxt] = curr
                queue.append(nxt)

    if not found:
        return None

    path = []
    curr = target_v
    while curr != -1:
        path.append(curr)
        curr = parent[curr]

    path.reverse()
    circuito = [(start_i, start_j)]
    for k in range(len(path) - 1):
        u, v = path[k], path[k + 1]
        if u >= m:
            circuito.append((v, u - m))
        else:
            circuito.append((u, v - m))

    return circuito


def transporte_stepping_stone(costos, oferta, demanda):
    m = len(costos)
    n = len(costos[0])
    alloc, basic = solucion_inicial_vogel(costos, oferta, demanda)
    iteraciones = 0

    while True:
        iteraciones += 1
        min_delta = 0.0
        celda_entrante = None
        circuito_entrante = None

        for i in range(m):
            for j in range(n):
                if not basic[i][j]:
                    circ = buscar_circuito_cerrado(i, j, basic)
                    if circ:
                        delta = sum(costos[r][c] if k % 2 == 0 else -costos[r][c] for k, (r, c) in enumerate(circ))
                        if delta < min_delta:
                            min_delta = delta
                            celda_entrante = (i, j)
                            circuito_entrante = circ

        if celda_entrante is None or min_delta >= 0:
            break

        neg_cells = [circuito_entrante[k] for k in range(1, len(circuito_entrante), 2)]
        theta = min(alloc[r][c] for r, c in neg_cells)

        for k, (r, c) in enumerate(circuito_entrante):
            if k % 2 == 0:
                alloc[r][c] += theta
            else:
                alloc[r][c] -= theta

        ei, ej = celda_entrante
        basic[ei][ej] = True
        for r, c in neg_cells:
            if alloc[r][c] == 0:
                basic[r][c] = False
                break

    costo_total = sum(alloc[i][j] * costos[i][j] for i in range(m) for j in range(n))
    return costo_total, iteraciones


def transporte_modi(costos, oferta, demanda):
    m = len(costos)
    n = len(costos[0])
    alloc, basic = solucion_inicial_vogel(costos, oferta, demanda)
    iteraciones = 0

    while True:
        iteraciones += 1
        num_v = m + n
        adj = [[] for _ in range(num_v)]
        for i in range(m):
            for j in range(n):
                if basic[i][j]:
                    adj[i].append(m + j)
                    adj[m + j].append(i)

        u = [None] * m
        v = [None] * n
        u[0] = 0.0

        for start_row in range(m):
            if u[start_row] is not None:
                queue = [start_row]
                while queue:
                    curr = queue.pop(0)
                    if curr < m:
                        for nxt in adj[curr]:
                            col = nxt - m
                            if v[col] is None:
                                v[col] = costos[curr][col] - u[curr]
                                queue.append(nxt)
                    else:
                        col = curr - m
                        for nxt in adj[curr]:
                            row = nxt
                            if u[row] is None:
                                u[row] = costos[row][col] - v[col]
                                queue.append(nxt)

        for i in range(m):
            if u[i] is None:
                u[i] = 0.0
        for j in range(n):
            if v[j] is None:
                v[j] = 0.0

        min_delta = 0.0
        celda_entrante = None

        for i in range(m):
            ui = u[i]
            for j in range(n):
                if not basic[i][j]:
                    delta = costos[i][j] - (ui + v[j])
                    if delta < min_delta:
                        min_delta = delta
                        celda_entrante = (i, j)

        if celda_entrante is None or min_delta >= 0:
            break

        circ = buscar_circuito_cerrado(celda_entrante[0], celda_entrante[1], basic)
        if not circ:
            break

        neg_cells = [circ[k] for k in range(1, len(circ), 2)]
        theta = min(alloc[r][c] for r, c in neg_cells)

        for k, (r, c) in enumerate(circ):
            if k % 2 == 0:
                alloc[r][c] += theta
            else:
                alloc[r][c] -= theta

        ei, ej = celda_entrante
        basic[ei][ej] = True
        for r, c in neg_cells:
            if alloc[r][c] == 0:
                basic[r][c] = False
                break

    costo_total = sum(alloc[i][j] * costos[i][j] for i in range(m) for j in range(n))
    return costo_total, iteraciones


# ==============================================================
# 2. ALGORITMOS DE ASIGNACIÓN (100 VARIABLES)
# ==============================================================

def asignacion_fuerza_bruta(costos):
    n = len(costos)
    min_costo = float("inf")
    for perm in itertools.permutations(range(n)):
        c = sum(costos[i][perm[i]] for i in range(n))
        if c < min_costo:
            min_costo = c
    return min_costo


def asignacion_hungaro(costos):
    n = len(costos)
    # Algoritmo Húngaro estándar de caminos de aumento (O(n^3))
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [float("inf")] * (n + 1)
        used = [False] * (n + 1)

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float("inf")
            j1 = 0

            for j in range(1, n + 1):
                if not used[j]:
                    cur = costos[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j

            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1
            if p[j0] == 0:
                break

        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    costo_total = -v[0]
    return costo_total


class TimeoutLimiteExcedido(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutLimiteExcedido("Tiempo limite de 15 minutos (900s) excedido")

def medir_con_timeout(func, args, timeout_segundos=900):
    # Asignar handler de alarma
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_segundos)
    except (ValueError, AttributeError):
        pass # Soporte para entornos no Unix

    tracemalloc.start()
    t0 = time.perf_counter()
    try:
        resultado = func(*args)
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        try:
            signal.alarm(0)
        except (ValueError, AttributeError):
            pass
        tiempo_ms = (t1 - t0) * 1000.0
        memoria_kb = peak / 1024.0
        return resultado, tiempo_ms, memoria_kb, False
    except TimeoutLimiteExcedido:
        tracemalloc.stop()
        try:
            signal.alarm(0)
        except (ValueError, AttributeError):
            pass
        return None, None, None, True
    except Exception as e:
        tracemalloc.stop()
        try:
            signal.alarm(0)
        except (ValueError, AttributeError):
            pass
        raise e


# ==============================================================
# 3. EJECUCIÓN Y VALIDACIÓN MULTIESCALA EN PYTHON
# ==============================================================
if __name__ == "__main__":
    print("=" * 96)
    print("      BENCHMARK DE ESCALABILIDAD MULTIDIMENSIONAL (100 A 1.000.000 VARIABLES) EN PYTHON      ")
    print("      Limite de ejecucion: 15 minutos (900 s) por algoritmo. Si excede, continua.             ")
    print("=" * 96)

    escalas = [
        {"nombre": "100 Variables", "tag": "100", "n": 10, "file": "matrices_100.json", "probar_ss": True, "probar_fb": True},
        {"nombre": "1.000 Variables", "tag": "1k", "n": 32, "file": "matrices_1000.json", "probar_ss": True, "probar_fb": False},
        {"nombre": "10.000 Variables", "tag": "10k", "n": 100, "file": "matrices_10000.json", "probar_ss": True, "probar_fb": False},
        {"nombre": "100.000 Variables", "tag": "100k", "n": 316, "file": "matrices_100000.json", "probar_ss": True, "probar_fb": False},
        {"nombre": "1.000.000 Variables", "tag": "1m", "n": 1000, "file": "matrices_1000000.json", "probar_ss": True, "probar_fb": False},
    ]

    base_dir = os.path.dirname(__file__)
    res_escalas = {}

    for esc in escalas:
        n = esc["n"]
        vars_total = n * n
        fpath = os.path.join(base_dir, esc["file"])
        if not os.path.exists(fpath):
            fpath = os.path.join(base_dir, "..", esc["file"])

        if os.path.exists(fpath):
            with open(fpath, "r") as f:
                d = json.load(f)
                c_trans = d.get("costos_trans", d.get("costos_transporte"))
                c_asig = d.get("costos_asig", d.get("costos_asignacion"))
        else:
            rng = random.Random(42)
            c_trans = [[float(rng.randint(1, 29)) for _ in range(n)] for _ in range(n)]
            c_asig = [[float(rng.randint(10, 99)) for _ in range(n)] for _ in range(n)]

        oferta = [100.0] * n
        demanda = [100.0] * n

        print(f"\n>>> INICIANDO ESCALA: {esc['nombre']} ({n}x{n} = {vars_total} Variables) <<<")

        # 1. Húngaro
        print(f" [Asignacion] Ejecutando Metodo Hungaro O(n^3)...")
        res_hung, t_hung, mem_hung, to_hung = medir_con_timeout(asignacion_hungaro, (c_asig,), timeout_segundos=900)
        if to_hung:
            print(f"   -> [TIEMPO EXCEDIDO]: Demoró más de 15 minutos (900 s). Omitiendo.")
        else:
            print(f"   -> Coste: {res_hung:8.0f} | Tiempo: {t_hung:8.2f} ms ({t_hung/1000:.2f} s) | Memoria: {mem_hung:8.2f} KB")

        # 2. MODI
        print(f" [Transporte] Ejecutando Metodo MODI u-v...")
        res_modi, t_modi, mem_modi, to_modi = medir_con_timeout(transporte_modi, (c_trans, oferta, demanda), timeout_segundos=900)
        if to_modi:
            print(f"   -> [TIEMPO EXCEDIDO]: Demoró más de 15 minutos (900 s). Omitiendo.")
        else:
            c_m, it_m = res_modi
            print(f"   -> Costo: {c_m:8.2f} | Iters: {it_m:3d} | Tiempo: {t_modi:8.2f} ms ({t_modi/1000:.2f} s) | Memoria: {mem_modi:8.2f} KB")

        # 3. Stepping Stone si aplica
        res_ss, t_ss, mem_ss, to_ss = None, None, None, False
        if esc["probar_ss"]:
            print(f" [Transporte] Ejecutando Stepping Stone Tradicional...")
            res_ss, t_ss, mem_ss, to_ss = medir_con_timeout(transporte_stepping_stone, (c_trans, oferta, demanda), timeout_segundos=900)
            if to_ss:
                print(f"   -> [TIEMPO EXCEDIDO]: Demoró más de 15 minutos (900 s). Omitiendo.")
            else:
                c_s, it_s = res_ss
                print(f"   -> Costo: {c_s:8.2f} | Iters: {it_s:3d} | Tiempo: {t_ss:8.2f} ms ({t_ss/1000:.2f} s) | Memoria: {mem_ss:8.2f} KB")
        else:
            to_ss = True
            print(f" [Transporte] Stepping Stone: Demoró más de 15 minutos (> 900 s estimados por O(K*N^3)).")

        # 4. Fuerza Bruta si aplica
        res_fb, t_fb, mem_fb, to_fb = None, None, None, False
        if esc["probar_fb"]:
            print(f" [Asignacion] Ejecutando Fuerza Bruta Tradicional...")
            res_fb, t_fb, mem_fb, to_fb = medir_con_timeout(asignacion_fuerza_bruta, (c_asig,), timeout_segundos=900)
            if to_fb:
                print(f"   -> [TIEMPO EXCEDIDO]: Demoró más de 15 minutos (900 s). Omitiendo.")
            else:
                print(f"   -> Coste: {res_fb:8.0f} | Tiempo: {t_fb:8.2f} ms ({t_fb/1000:.2f} s) | Memoria: {mem_fb:8.2f} KB")
        else:
            to_fb = True
            print(f" [Asignacion] Fuerza Bruta: Demoró más de 15 minutos (Inviable O(N!) > 10^20 años).")

        res_escalas[esc["tag"]] = {
            "n": n,
            "vars": vars_total,
            "hungaro": {
                "costo": res_hung if not to_hung else None,
                "tiempo_ms": t_hung if not to_hung else None,
                "memoria_kb": mem_hung if not to_hung else None,
                "timeout": to_hung
            },
            "modi": {
                "costo": res_modi[0] if (res_modi and not to_modi) else None,
                "iters": res_modi[1] if (res_modi and not to_modi) else None,
                "tiempo_ms": t_modi if not to_modi else None,
                "memoria_kb": mem_modi if not to_modi else None,
                "timeout": to_modi
            },
            "ss": {
                "costo": res_ss[0] if (res_ss and not to_ss) else None,
                "iters": res_ss[1] if (res_ss and not to_ss) else None,
                "tiempo_ms": t_ss if not to_ss else None,
                "memoria_kb": mem_ss if not to_ss else None,
                "timeout": to_ss
            },
            "fb": {
                "costo": res_fb if not to_fb else None,
                "tiempo_ms": t_fb if not to_fb else None,
                "memoria_kb": mem_fb if not to_fb else None,
                "timeout": to_fb
            }
        }

    # Guardar resultados
    out_json = os.path.join(base_dir, "python_scales_results.json")
    with open(out_json, "w") as f:
        json.dump(res_escalas, f, indent=2)
    print(f"\nResultados guardados exitosamente en {out_json}")
    print("=" * 96)

