package main

import (
	"runtime"
	"sync"
	"sync/atomic"
)

// ProblemaAsignacion define una matriz de asignacion NxN
type ProblemaAsignacion struct {
	N      int
	Costos [][]float64
}

// FuerzaBrutaSecuencial evalua todas las N! permutaciones de manera secuencial
func (p *ProblemaAsignacion) FuerzaBrutaSecuencial() (float64, int64) {
	n := p.N
	minCosto := 1e18
	var evalCount int64
	var used [32]bool

	var search func(row int, currentCost float64)
	search = func(row int, currentCost float64) {
		if row == n {
			evalCount++
			if currentCost < minCosto {
				minCosto = currentCost
			}
			return
		}
		for col := 0; col < n; col++ {
			if !used[col] {
				used[col] = true
				search(row+1, currentCost+p.Costos[row][col])
				used[col] = false
			}
		}
	}

	search(0, 0)
	return minCosto, evalCount
}

// FuerzaBrutaParalela distribuye el arbol de busqueda entre todos los cores de la CPU
func (p *ProblemaAsignacion) FuerzaBrutaParalela() (float64, int64) {
	n := p.N
	var globalMin atomic.Uint64
	// Codificamos como entero escalado para CompareAndSwap atomico
	const scale = 1000.0
	globalMin.Store(^uint64(0)) // Infinito

	var totalEvals atomic.Int64
	var wg sync.WaitGroup

	numWorkers := runtime.NumCPU()

	// Tareas de nivel 1 (primera columna elegida para la fila 0)
	// Si N es grande, podemos distribuir nivel 1 o nivel 2
	type Task struct {
		c0, c1 int
	}
	tasks := make(chan Task, n*n)

	// Llenar canal con bifurcaciones de nivel 2 (n * (n-1) tareas)
	for c0 := 0; c0 < n; c0++ {
		for c1 := 0; c1 < n; c1++ {
			if c1 != c0 {
				tasks <- Task{c0, c1}
			}
		}
	}
	close(tasks)

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			var used [32]bool
			var localEvals int64
			localMin := 1e18

			var search func(row int, currentCost float64)
			search = func(row int, currentCost float64) {
				if row == n {
					localEvals++
					if currentCost < localMin {
						localMin = currentCost
						intCost := uint64(currentCost * scale)
						for {
							cur := globalMin.Load()
							if intCost >= cur {
								break
							}
							if globalMin.CompareAndSwap(cur, intCost) {
								break
							}
						}
					}
					return
				}
				for col := 0; col < n; col++ {
					if !used[col] {
						used[col] = true
						search(row+1, currentCost+p.Costos[row][col])
						used[col] = false
					}
				}
			}

			for task := range tasks {
				used[task.c0] = true
				used[task.c1] = true
				cost0 := p.Costos[0][task.c0] + p.Costos[1][task.c1]
				search(2, cost0)
				used[task.c0] = false
				used[task.c1] = false
			}
			totalEvals.Add(localEvals)
		}()
	}

	wg.Wait()
	return float64(globalMin.Load()) / scale, totalEvals.Load()
}

// MetodoHungaro implementa el algoritmo hungaro clasico O(n^3) en Go
func (p *ProblemaAsignacion) MetodoHungaro() (float64, []int) {
	n := p.N
	mat := make([][]float64, n)
	for i := range mat {
		mat[i] = make([]float64, n)
		copy(mat[i], p.Costos[i])
	}

	// Paso 1: Reduccion por filas
	for i := 0; i < n; i++ {
		minFila := mat[i][0]
		for j := 1; j < n; j++ {
			if mat[i][j] < minFila {
				minFila = mat[i][j]
			}
		}
		for j := 0; j < n; j++ {
			mat[i][j] -= minFila
		}
	}

	// Paso 2: Reduccion por columnas
	for j := 0; j < n; j++ {
		minCol := mat[0][j]
		for i := 1; i < n; i++ {
			if mat[i][j] < minCol {
				minCol = mat[i][j]
			}
		}
		for i := 0; i < n; i++ {
			mat[i][j] -= minCol
		}
	}

	// Lineas minimas usando emparejamiento maximo de bipartito
	for {
		matchR := make([]int, n)
		matchC := make([]int, n)
		for i := range matchR {
			matchR[i] = -1
			matchC[i] = -1
		}

		var dfs func(u int, visited []bool) bool
		dfs = func(u int, visited []bool) bool {
			for v := 0; v < n; v++ {
				if mat[u][v] == 0 && !visited[v] {
					visited[v] = true
					if matchC[v] < 0 || dfs(matchC[v], visited) {
						matchR[u] = v
						matchC[v] = u
						return true
					}
				}
			}
			return false
		}

		for r := 0; r < n; r++ {
			visited := make([]bool, n)
			dfs(r, visited)
		}

		// Encontrar lineas minimas con el Teorema de Konig
		visitedR := make([]bool, n)
		visitedC := make([]bool, n)
		var queue []int
		for r := 0; r < n; r++ {
			if matchR[r] < 0 {
				visitedR[r] = true
				queue = append(queue, r)
			}
		}

		for len(queue) > 0 {
			currR := queue[0]
			queue = queue[1:]
			for c := 0; c < n; c++ {
				if mat[currR][c] == 0 && !visitedC[c] {
					visitedC[c] = true
					if matchC[c] >= 0 && !visitedR[matchC[c]] {
						visitedR[matchC[c]] = true
						queue = append(queue, matchC[c])
					}
				}
			}
		}

		var markedR, markedC []int
		for r := 0; r < n; r++ {
			if !visitedR[r] {
				markedR = append(markedR, r)
			}
		}
		for c := 0; c < n; c++ {
			if visitedC[c] {
				markedC = append(markedC, c)
			}
		}

		numLineas := len(markedR) + len(markedC)
		if numLineas >= n {
			// Asignacion optima encontrada
			costoTotal := 0.0
			for i := 0; i < n; i++ {
				if matchR[i] >= 0 {
					costoTotal += p.Costos[i][matchR[i]]
				}
			}
			return costoTotal, matchR
		}

		// Ajuste de matriz: encontrar k minimo no cubierto
		k := 1e18
		for r := 0; r < n; r++ {
			if !sliceContains(markedR, r) {
				for c := 0; c < n; c++ {
					if !sliceContains(markedC, c) && mat[r][c] < k {
						k = mat[r][c]
					}
				}
			}
		}

		for r := 0; r < n; r++ {
			rCubierta := sliceContains(markedR, r)
			for c := 0; c < n; c++ {
				cCubierta := sliceContains(markedC, c)
				if !rCubierta && !cCubierta {
					mat[r][c] -= k
				} else if rCubierta && cCubierta {
					mat[r][c] += k
				}
			}
		}
	}
}

func sliceContains(slice []int, val int) bool {
	for _, v := range slice {
		if v == val {
			return true
		}
	}
	return false
}

