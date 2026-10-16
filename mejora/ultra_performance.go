package main

import (
	"math/bits"
	"runtime"
	"sync"
	"sync/atomic"
)

// UltraAsignacionBitmaskPnB: Branch and Bound Paralelo ultrarrápido con Bitmasks de 32 bits
// y poda de cotas con lectura atómica sin bloqueos (Lock-Free).
func UltraAsignacionBitmaskPnB(n int, costos [][]float64) (float64, int64) {
	// Cota inferior voraz inicial para podar de inmediato
	// Precalculamos el minimo de cada fila
	minFila := make([]float64, n)
	for i := 0; i < n; i++ {
		m := costos[i][0]
		for j := 1; j < n; j++ {
			if costos[i][j] < m {
				m = costos[i][j]
			}
		}
		minFila[i] = m
	}

	// Cota inferior acumulada para el sufijo de filas [row..n-1]
	sufijoMin := make([]float64, n+1)
	for i := n - 1; i >= 0; i-- {
		sufijoMin[i] = sufijoMin[i+1] + minFila[i]
	}

	const scale = 1000.0
	var globalMin atomic.Uint64
	globalMin.Store(^uint64(0)) // Infinito

	var totalEvals atomic.Int64
	numWorkers := runtime.NumCPU()
	var wg sync.WaitGroup

	// Generamos tareas de inicio basadas en las primeras 2 decisiones
	type InicioTask struct {
		c0, c1 int
		cost   float64
		mask   uint32
	}
	tasks := make(chan InicioTask, n*n)

	for c0 := 0; c0 < n; c0++ {
		for c1 := 0; c1 < n; c1++ {
			if c1 != c0 {
				mask := uint32((1 << c0) | (1 << c1))
				cost := costos[0][c0] + costos[1][c1]
				tasks <- InicioTask{c0, c1, cost, mask}
			}
		}
	}
	close(tasks)

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			var localEvals int64

			var search func(row int, currentCost float64, mask uint32)
			search = func(row int, currentCost float64, mask uint32) {
				// PODA CRÍTICA (Branch and Bound):
				// Si el costo actual + la cota inferior teorica restante supera el minimo global, PODAR rama.
				curGlobal := float64(globalMin.Load()) / scale
				if currentCost+sufijoMin[row] >= curGlobal {
					return
				}

				if row == n {
					localEvals++
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
					return
				}

				// Operaciones de bits ultra-rápidas para encontrar columnas libres
				// mask tiene 1s en columnas ocupadas; ~mask tiene 1s en libres
				libres := (^mask) & ((1 << n) - 1)
				for libres > 0 {
					col := bits.TrailingZeros32(libres)
					libres &= libres - 1 // Limpiar el bit menos significativo
					search(row+1, currentCost+costos[row][col], mask|(1<<col))
				}
			}

			for task := range tasks {
				search(2, task.cost, task.mask)
			}
			totalEvals.Add(localEvals)
		}()
	}

	wg.Wait()
	return float64(globalMin.Load()) / scale, totalEvals.Load()
}

// UltraHungaroSAP: Algoritmo de Asignación por Caminos de Aumento Más Cortos (Shortest Augmenting Path)
// Implementación optimizada de bajo nivel con memoria lineal continua y reutilización de buffers.
func UltraHungaroSAP(n int, costos [][]float64) (float64, []int) {
	u := make([]float64, n+1)
	v := make([]float64, n+1)
	p := make([]int, n+1)
	way := make([]int, n+1)
	minv := make([]float64, n+1)
	used := make([]bool, n+1)

	for i := 1; i <= n; i++ {
		p[0] = i
		j0 := 0
		for j := 0; j <= n; j++ {
			minv[j] = 1e18
			used[j] = false
		}

		for {
			used[j0] = true
			i0 := p[j0]
			delta := 1e18
			j1 := 0

			u_i0 := u[i0]
			c_row := costos[i0-1]

			for j := 1; j <= n; j++ {
				if !used[j] {
					cur := c_row[j-1] - u_i0 - v[j]
					if cur < minv[j] {
						minv[j] = cur
						way[j] = j0
					}
					if minv[j] < delta {
						delta = minv[j]
						j1 = j
					}
				}
			}

			for j := 0; j <= n; j++ {
				if used[j] {
					u[p[j]] += delta
					v[j] -= delta
				} else {
					minv[j] -= delta
				}
			}

			j0 = j1
			if p[j0] == 0 {
				break
			}
		}

		for {
			j1 := way[j0]
			p[j0] = p[j1]
			j0 = j1
			if j0 == 0 {
				break
			}
		}
	}

	asignacion := make([]int, n)
	for j := 1; j <= n; j++ {
		if p[j] > 0 {
			asignacion[p[j]-1] = j - 1
		}
	}

	costoTotal := -v[0]
	return costoTotal, asignacion
}

// UltraHungaroSAPParalelo: Versión multihilo del algoritmo de caminos de aumento más cortos.
// Divide la búsqueda y actualización de columnas entre todos los núcleos de CPU (16 Cores),
// saturando la capacidad del procesador al 100% en matrices medianas y grandes.
func UltraHungaroSAPParalelo(n int, costos [][]float64) (float64, []int) {
	if n < 64 {
		return UltraHungaroSAP(n, costos)
	}

	numW := runtime.NumCPU()
	u := make([]float64, n+1)
	v := make([]float64, n+1)
	p := make([]int, n+1)
	way := make([]int, n+1)
	minv := make([]float64, n+1)
	used := make([]bool, n+1)

	type workerRes struct {
		minDelta float64
		bestJ    int
	}
	localRes := make([]workerRes, numW)
	chunk := (n + numW - 1) / numW

	for i := 1; i <= n; i++ {
		p[0] = i
		j0 := 0
		for j := 0; j <= n; j++ {
			minv[j] = 1e18
			used[j] = false
		}

		for {
			used[j0] = true
			i0 := p[j0]

			var wg sync.WaitGroup
			for w := 0; w < numW; w++ {
				jStart := w*chunk + 1
				jEnd := jStart + chunk
				if jEnd > n+1 {
					jEnd = n + 1
				}
				if jStart > n {
					localRes[w] = workerRes{minDelta: 1e18, bestJ: 0}
					continue
				}

				wg.Add(1)
				go func(wIdx, js, je int) {
					defer wg.Done()
					locDelta := 1e18
					locJ := 0
					u_i0 := u[i0]
					c_row := costos[i0-1]

					for j := js; j < je; j++ {
						if !used[j] {
							cur := c_row[j-1] - u_i0 - v[j]
							if cur < minv[j] {
								minv[j] = cur
								way[j] = j0
							}
							if minv[j] < locDelta {
								locDelta = minv[j]
								locJ = j
							}
						}
					}
					localRes[wIdx] = workerRes{minDelta: locDelta, bestJ: locJ}
				}(w, jStart, jEnd)
			}
			wg.Wait()

			delta := 1e18
			j1 := 0
			for w := 0; w < numW; w++ {
				if localRes[w].minDelta < delta {
					delta = localRes[w].minDelta
					j1 = localRes[w].bestJ
				}
			}

			// Actualización dual en paralelo
			var wg2 sync.WaitGroup
			chunkAll := (n + 1 + numW - 1) / numW
			for w := 0; w < numW; w++ {
				js := w * chunkAll
				je := js + chunkAll
				if je > n+1 {
					je = n + 1
				}
				if js > n {
					break
				}
				wg2.Add(1)
				go func(start, end int) {
					defer wg2.Done()
					for j := start; j < end; j++ {
						if used[j] {
							u[p[j]] += delta
							v[j] -= delta
						} else {
							minv[j] -= delta
						}
					}
				}(js, je)
			}
			wg2.Wait()

			j0 = j1
			if p[j0] == 0 {
				break
			}
		}

		for {
			j1 := way[j0]
			p[j0] = p[j1]
			j0 = j1
			if j0 == 0 {
				break
			}
		}
	}

	asignacion := make([]int, n)
	for j := 1; j <= n; j++ {
		if p[j] > 0 {
			asignacion[p[j]-1] = j - 1
		}
	}

	costoTotal := -v[0]
	return costoTotal, asignacion
}

// UltraTransporteMODIParalelo: Motor de Ultra Rendimiento para Transporte.
// Paraleliza la evaluación de los costos reducidos (deltas) en todas las celdas
// no básicas adaptándose dinámicamente al 100% de los núcleos del procesador.
func UltraTransporteMODIParalelo(m, n int, costos [][]float64, oferta, demanda []float64) (float64, int) {
	p := &ProblemaTransporte{
		M:       m,
		N:       n,
		Costos:  costos,
		Oferta:  oferta,
		Demanda: demanda,
	}
	return p.MetodoMODIParalelo()
}
