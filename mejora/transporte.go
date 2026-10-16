package main

import (
	"math"
	"runtime"
	"sync"
)

// ProblemaTransporte define los datos de un problema de transporte
type ProblemaTransporte struct {
	M, N    int
	Costos  [][]float64
	Oferta  []float64
	Demanda []float64
}

// SolucionVogel genera la solucion inicial basica factible
func (p *ProblemaTransporte) SolucionVogel() ([][]float64, [][]bool) {
	m, n := p.M, p.N
	alloc := make([][]float64, m)
	basic := make([][]bool, m)
	for i := range alloc {
		alloc[i] = make([]float64, n)
		basic[i] = make([]bool, n)
	}

	s := make([]float64, m)
	copy(s, p.Oferta)
	d := make([]float64, n)
	copy(d, p.Demanda)

	rowActive := make([]bool, m)
	colActive := make([]bool, n)
	for i := range rowActive {
		rowActive[i] = true
	}
	for j := range colActive {
		colActive[j] = true
	}

	rowPen := make([]float64, m)
	colPen := make([]float64, n)
	numW := runtime.NumCPU()

	for countTrue(rowActive) > 0 && countTrue(colActive) > 0 {
		if countTrue(rowActive) == 1 {
			i := firstTrue(rowActive)
			for j := 0; j < n; j++ {
				if colActive[j] {
					qty := minFloat(s[i], d[j])
					alloc[i][j] = qty
					basic[i][j] = true
					s[i] -= qty
					d[j] -= qty
					if d[j] == 0 {
						colActive[j] = false
					}
				}
			}
			rowActive[i] = false
			break
		}

		if countTrue(colActive) == 1 {
			j := firstTrue(colActive)
			for i := 0; i < m; i++ {
				if rowActive[i] {
					qty := minFloat(s[i], d[j])
					alloc[i][j] = qty
					basic[i][j] = true
					s[i] -= qty
					d[j] -= qty
					if s[i] == 0 {
						rowActive[i] = false
					}
				}
			}
			colActive[j] = false
			break
		}

		// Penalizaciones de filas y columnas (paralelizadas concurrentemente si m >= 64 o n >= 64)
		if m >= 64 || n >= 64 {
			var wg sync.WaitGroup
			chunkR := (m + numW - 1) / numW
			for w := 0; w < numW; w++ {
				rs := w * chunkR
				re := rs + chunkR
				if re > m {
					re = m
				}
				if rs >= m {
					break
				}
				wg.Add(1)
				go func(start, end int) {
					defer wg.Done()
					for i := start; i < end; i++ {
						if !rowActive[i] {
							rowPen[i] = -1
						} else {
							min1, min2 := 1e18, 1e18
							count := 0
							for j := 0; j < n; j++ {
								if colActive[j] {
									c := p.Costos[i][j]
									count++
									if c < min1 {
										min2 = min1
										min1 = c
									} else if c < min2 {
										min2 = c
									}
								}
							}
							if count >= 2 {
								rowPen[i] = min2 - min1
							} else if count == 1 {
								rowPen[i] = min1
							}
						}
					}
				}(rs, re)
			}

			chunkC := (n + numW - 1) / numW
			for w := 0; w < numW; w++ {
				cs := w * chunkC
				ce := cs + chunkC
				if ce > n {
					ce = n
				}
				if cs >= n {
					break
				}
				wg.Add(1)
				go func(start, end int) {
					defer wg.Done()
					for j := start; j < end; j++ {
						if !colActive[j] {
							colPen[j] = -1
						} else {
							min1, min2 := 1e18, 1e18
							count := 0
							for i := 0; i < m; i++ {
								if rowActive[i] {
									c := p.Costos[i][j]
									count++
									if c < min1 {
										min2 = min1
										min1 = c
									} else if c < min2 {
										min2 = c
									}
								}
							}
							if count >= 2 {
								colPen[j] = min2 - min1
							} else if count == 1 {
								colPen[j] = min1
							}
						}
					}
				}(cs, ce)
			}
			wg.Wait()
		} else {
			for i := 0; i < m; i++ {
				if !rowActive[i] {
					rowPen[i] = -1
				} else {
					min1, min2 := 1e18, 1e18
					count := 0
					for j := 0; j < n; j++ {
						if colActive[j] {
							c := p.Costos[i][j]
							count++
							if c < min1 {
								min2 = min1
								min1 = c
							} else if c < min2 {
								min2 = c
							}
						}
					}
					if count >= 2 {
						rowPen[i] = min2 - min1
					} else if count == 1 {
						rowPen[i] = min1
					}
				}
			}

			for j := 0; j < n; j++ {
				if !colActive[j] {
					colPen[j] = -1
				} else {
					min1, min2 := 1e18, 1e18
					count := 0
					for i := 0; i < m; i++ {
						if rowActive[i] {
							c := p.Costos[i][j]
							count++
							if c < min1 {
								min2 = min1
								min1 = c
							} else if c < min2 {
								min2 = c
							}
						}
					}
					if count >= 2 {
						colPen[j] = min2 - min1
					} else if count == 1 {
						colPen[j] = min1
					}
				}
			}
		}

		maxR := maxSlice(rowPen)
		maxC := maxSlice(colPen)

		var bestI, bestJ int
		if maxR >= maxC {
			bestI = indexOf(rowPen, maxR)
			minC := 1e18
			for j := 0; j < n; j++ {
				if colActive[j] && p.Costos[bestI][j] < minC {
					minC = p.Costos[bestI][j]
					bestJ = j
				}
			}
		} else {
			bestJ = indexOf(colPen, maxC)
			minC := 1e18
			for i := 0; i < m; i++ {
				if rowActive[i] && p.Costos[i][bestJ] < minC {
					minC = p.Costos[i][bestJ]
					bestI = i
				}
			}
		}

		qty := minFloat(s[bestI], d[bestJ])
		alloc[bestI][bestJ] = qty
		basic[bestI][bestJ] = true
		s[bestI] -= qty
		d[bestJ] -= qty

		if s[bestI] == 0 && d[bestJ] == 0 {
			if countTrue(rowActive) > countTrue(colActive) {
				rowActive[bestI] = false
			} else {
				colActive[bestJ] = false
			}
		} else if s[bestI] == 0 {
			rowActive[bestI] = false
		} else {
			colActive[bestJ] = false
		}
	}

	return alloc, basic
}

type Point struct {
	R, C int
}

// ConstruirArbolBasico crea la lista de adyacencia del árbol abarcador bipartito formado por las celdas básicas.
func (p *ProblemaTransporte) ConstruirArbolBasico(basic [][]bool) [][]int {
	m, n := p.M, p.N
	adj := make([][]int, m+n)
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			if basic[i][j] {
				adj[i] = append(adj[i], m+j)
				adj[m+j] = append(adj[m+j], i)
			}
		}
	}
	return adj
}

// BFSScratch mantiene estructuras preasignadas para la búsqueda BFS de circuitos cerrados.
// Evita crear y destruir millones de slices en cada iteración (cero presión en el GC).
type BFSScratch struct {
	Parent  []int
	Visited []int
	Queue   []int
	Token   int
}

// NuevoBFSScratch crea un buffer reutilizable de BFS para un grafo bipartito de numV vértices.
func NuevoBFSScratch(numV int) *BFSScratch {
	p := make([]int, numV)
	for i := range p {
		p[i] = -1
	}
	return &BFSScratch{
		Parent:  p,
		Visited: make([]int, numV),
		Queue:   make([]int, numV),
		Token:   1,
	}
}

// BuscarCircuitoEnArbolScratch realiza la búsqueda en anchura sin alocaciones dinámicas de memoria.
func BuscarCircuitoEnArbolScratch(startI, startJ, m, n int, adj [][]int, sc *BFSScratch) []Point {
	startV := m + startJ
	targetV := startI

	sc.Token++
	token := sc.Token

	sc.Visited[startV] = token
	sc.Parent[startV] = -1
	qHead, qTail := 0, 0
	sc.Queue[qTail] = startV
	qTail++

	found := false
	for qHead < qTail {
		curr := sc.Queue[qHead]
		qHead++

		if curr == targetV {
			found = true
			break
		}

		for _, nxt := range adj[curr] {
			if sc.Visited[nxt] != token {
				sc.Visited[nxt] = token
				sc.Parent[nxt] = curr
				sc.Queue[qTail] = nxt
				qTail++
			}
		}
	}

	if !found {
		return nil
	}

	curr := targetV
	length := 0
	for curr != -1 {
		length++
		curr = sc.Parent[curr]
	}

	path := make([]int, length)
	curr = targetV
	for idx := length - 1; idx >= 0; idx-- {
		path[idx] = curr
		curr = sc.Parent[curr]
	}

	circuito := make([]Point, 0, length+1)
	circuito = append(circuito, Point{startI, startJ})

	for k := 0; k < length-1; k++ {
		u := path[k]
		v := path[k+1]
		var pt Point
		if u >= m {
			pt = Point{R: v, C: u - m}
		} else {
			pt = Point{R: u, C: v - m}
		}
		circuito = append(circuito, pt)
	}

	return circuito
}

// BuscarCircuitoEnArbol mantiene compatibilidad general usando un scratch efímero
func BuscarCircuitoEnArbol(startI, startJ int, m, n int, adj [][]int) []Point {
	sc := NuevoBFSScratch(m + n)
	return BuscarCircuitoEnArbolScratch(startI, startJ, m, n, adj, sc)
}

// BuscarCircuitoCerrado es la función de interfaz para compatibilidad
func (p *ProblemaTransporte) BuscarCircuitoCerrado(startI, startJ int, basic [][]bool) []Point {
	adj := p.ConstruirArbolBasico(basic)
	return BuscarCircuitoEnArbol(startI, startJ, p.M, p.N, adj)
}

// SteppingStoneSecuencial ejecuta el método tradicional evaluando celdas una por una
func (p *ProblemaTransporte) SteppingStoneSecuencial() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	sc := NuevoBFSScratch(m + n)

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)
		minDelta := 0.0
		var celdaEntrante Point
		var circuitoEntrante []Point

		for i := 0; i < m; i++ {
			for j := 0; j < n; j++ {
				if !basic[i][j] {
					circuito := BuscarCircuitoEnArbolScratch(i, j, m, n, adj, sc)
					if len(circuito) > 0 {
						delta := 0.0
						for k, pt := range circuito {
							if k%2 == 0 {
								delta += p.Costos[pt.R][pt.C]
							} else {
								delta -= p.Costos[pt.R][pt.C]
							}
						}
						if delta < minDelta {
							minDelta = delta
							celdaEntrante = Point{i, j}
							circuitoEntrante = circuito
						}
					}
				}
			}
		}

		if minDelta >= 0 || len(circuitoEntrante) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuitoEntrante {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// ResultadoEvaluacionCelda para el paralelismo de Stepping Stone
type ResultadoEvaluacionCelda struct {
	P        Point
	Circuito []Point
	Delta    float64
}

// CalcularGridBloques calcula las dimensiones (gr, gc) de la grilla 2D para dividir la matriz en bloques
func CalcularGridBloques(workers, m, n int) (int, int) {
	bestGR, bestGC := 1, workers
	minDiff := 1e9
	for gr := 1; gr <= workers; gr++ {
		if workers%gr == 0 {
			gc := workers / gr
			diff := math.Abs(float64(gr)/float64(gc) - float64(m)/float64(n))
			if diff < minDiff {
				minDiff = diff
				bestGR, bestGC = gr, gc
			}
		}
	}
	return bestGR, bestGC
}

// SteppingStoneParaleloFilas particiona la matriz dividiendo las filas entre los núcleos de CPU.
func (p *ProblemaTransporte) SteppingStoneParaleloFilas() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	numWorkers := runtime.NumCPU()

	scs := make([]*BFSScratch, numWorkers)
	for w := 0; w < numWorkers; w++ {
		scs[w] = NuevoBFSScratch(m + n)
	}

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		localBests := make([]ResultadoEvaluacionCelda, numWorkers)
		var wg sync.WaitGroup
		rowsPerWorker := (m + numWorkers - 1) / numWorkers

		for w := 0; w < numWorkers; w++ {
			rStart := w * rowsPerWorker
			rEnd := rStart + rowsPerWorker
			if rEnd > m {
				rEnd = m
			}
			if rStart >= m {
				break
			}

			wg.Add(1)
			go func(workerIdx, rs, re int) {
				defer wg.Done()
				bestDelta := 0.0
				var bestPt Point
				var bestCirc []Point
				sc := scs[workerIdx]

				for i := rs; i < re; i++ {
					for j := 0; j < n; j++ {
						if !basic[i][j] {
							circuito := BuscarCircuitoEnArbolScratch(i, j, m, n, adj, sc)
							if len(circuito) > 0 {
								delta := 0.0
								for k, cPt := range circuito {
									if k%2 == 0 {
										delta += p.Costos[cPt.R][cPt.C]
									} else {
										delta -= p.Costos[cPt.R][cPt.C]
									}
								}
								if delta < bestDelta {
									bestDelta = delta
									bestPt = Point{i, j}
									bestCirc = circuito
								}
							}
						}
					}
				}
				localBests[workerIdx] = ResultadoEvaluacionCelda{P: bestPt, Circuito: bestCirc, Delta: bestDelta}
			}(w, rStart, rEnd)
		}

		wg.Wait()

		minDelta := 0.0
		var celdaEntrante Point
		var circuitoEntrante []Point

		for _, res := range localBests {
			if res.Delta < minDelta {
				minDelta = res.Delta
				celdaEntrante = res.P
				circuitoEntrante = res.Circuito
			}
		}

		if minDelta >= 0 || len(circuitoEntrante) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuitoEntrante {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// SteppingStoneParaleloCeldas distribuye las celdas de forma continua lineal entre todos los núcleos de CPU.
// Varias CPUs pueden compartir la misma fila si hay más núcleos que filas (sin desperdiciar ningún core).
func (p *ProblemaTransporte) SteppingStoneParaleloCeldas() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	numWorkers := runtime.NumCPU()
	totalCeldas := m * n

	scs := make([]*BFSScratch, numWorkers)
	for w := 0; w < numWorkers; w++ {
		scs[w] = NuevoBFSScratch(m + n)
	}

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		localBests := make([]ResultadoEvaluacionCelda, numWorkers)
		var wg sync.WaitGroup

		for w := 0; w < numWorkers; w++ {
			cStart := w * totalCeldas / numWorkers
			cEnd := (w + 1) * totalCeldas / numWorkers
			if cStart >= totalCeldas {
				break
			}

			wg.Add(1)
			go func(workerIdx, startIdx, endIdx int) {
				defer wg.Done()
				bestDelta := 0.0
				var bestPt Point
				var bestCirc []Point
				sc := scs[workerIdx]

				for idx := startIdx; idx < endIdx; idx++ {
					i := idx / n
					j := idx % n
					if !basic[i][j] {
						circuito := BuscarCircuitoEnArbolScratch(i, j, m, n, adj, sc)
						if len(circuito) > 0 {
							delta := 0.0
							for k, cPt := range circuito {
								if k%2 == 0 {
									delta += p.Costos[cPt.R][cPt.C]
								} else {
									delta -= p.Costos[cPt.R][cPt.C]
								}
							}
							if delta < bestDelta {
								bestDelta = delta
								bestPt = Point{i, j}
								bestCirc = circuito
							}
						}
					}
				}
				localBests[workerIdx] = ResultadoEvaluacionCelda{P: bestPt, Circuito: bestCirc, Delta: bestDelta}
			}(w, cStart, cEnd)
		}

		wg.Wait()

		minDelta := 0.0
		var celdaEntrante Point
		var circuitoEntrante []Point

		for _, res := range localBests {
			if res.Delta < minDelta {
				minDelta = res.Delta
				celdaEntrante = res.P
				circuitoEntrante = res.Circuito
			}
		}

		if minDelta >= 0 || len(circuitoEntrante) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuitoEntrante {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// SteppingStoneParaleloBloques particiona la matriz en sub-bloques 2D (tiling) asignando un bloque a cada núcleo.
func (p *ProblemaTransporte) SteppingStoneParaleloBloques() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	numWorkers := runtime.NumCPU()
	gr, gc := CalcularGridBloques(numWorkers, m, n)
	totalBlocks := gr * gc

	scs := make([]*BFSScratch, totalBlocks)
	for b := 0; b < totalBlocks; b++ {
		scs[b] = NuevoBFSScratch(m + n)
	}

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		localBests := make([]ResultadoEvaluacionCelda, totalBlocks)
		var wg sync.WaitGroup

		blockIdx := 0
		for br := 0; br < gr; br++ {
			rStart := br * m / gr
			rEnd := (br + 1) * m / gr
			for bc := 0; bc < gc; bc++ {
				cStart := bc * n / gc
				cEnd := (bc + 1) * n / gc

				wg.Add(1)
				go func(idx, rs, re, cs, ce int) {
					defer wg.Done()
					bestDelta := 0.0
					var bestPt Point
					var bestCirc []Point
					sc := scs[idx]

					for i := rs; i < re; i++ {
						for j := cs; j < ce; j++ {
							if !basic[i][j] {
								circuito := BuscarCircuitoEnArbolScratch(i, j, m, n, adj, sc)
								if len(circuito) > 0 {
									delta := 0.0
									for k, cPt := range circuito {
										if k%2 == 0 {
											delta += p.Costos[cPt.R][cPt.C]
										} else {
											delta -= p.Costos[cPt.R][cPt.C]
										}
									}
									if delta < bestDelta {
										bestDelta = delta
										bestPt = Point{i, j}
										bestCirc = circuito
									}
								}
							}
						}
					}
					localBests[idx] = ResultadoEvaluacionCelda{P: bestPt, Circuito: bestCirc, Delta: bestDelta}
				}(blockIdx, rStart, rEnd, cStart, cEnd)
				blockIdx++
			}
		}

		wg.Wait()

		minDelta := 0.0
		var celdaEntrante Point
		var circuitoEntrante []Point

		for _, res := range localBests {
			if res.Delta < minDelta {
				minDelta = res.Delta
				celdaEntrante = res.P
				circuitoEntrante = res.Circuito
			}
		}

		if minDelta >= 0 || len(circuitoEntrante) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuitoEntrante {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuitoEntrante); k += 2 {
			pt := circuitoEntrante[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// SteppingStoneParalelo mantiene compatibilidad apuntando a la particion por celdas
func (p *ProblemaTransporte) SteppingStoneParalelo() (float64, int) {
	return p.SteppingStoneParaleloCeldas()
}

// MetodoMODI resuelve el problema de transporte usando variables duales u y v
func (p *ProblemaTransporte) MetodoMODI() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		// Calcular potenciales duales u y v mediante recorrido del árbol en O(m+n)
		u := make([]*float64, m)
		v := make([]*float64, n)
		valZero := 0.0
		u[0] = &valZero

		for startRow := 0; startRow < m; startRow++ {
			if u[startRow] != nil {
				queue := []int{startRow}
				for len(queue) > 0 {
					curr := queue[0]
					queue = queue[1:]

					if curr < m {
						// curr es fila i
						for _, nxt := range adj[curr] {
							col := nxt - m
							if v[col] == nil {
								val := p.Costos[curr][col] - *u[curr]
								v[col] = &val
								queue = append(queue, nxt)
							}
						}
					} else {
						// curr es columna j
						col := curr - m
						for _, nxt := range adj[curr] {
							row := nxt
							if u[row] == nil {
								val := p.Costos[row][col] - *v[col]
								u[row] = &val
								queue = append(queue, nxt)
							}
						}
					}
				}
			}
		}

		// Si alguna componente quedó sin conectar (degeneración), asignar 0.0
		for i := 0; i < m; i++ {
			if u[i] == nil {
				z := 0.0
				u[i] = &z
			}
		}
		for j := 0; j < n; j++ {
			if v[j] == nil {
				z := 0.0
				v[j] = &z
			}
		}

		minDelta := 0.0
		var celdaEntrante Point
		for i := 0; i < m; i++ {
			uVal := *u[i]
			for j := 0; j < n; j++ {
				if !basic[i][j] {
					delta := p.Costos[i][j] - (uVal + *v[j])
					if delta < minDelta {
						minDelta = delta
						celdaEntrante = Point{i, j}
					}
				}
			}
		}

		if minDelta >= 0 {
			break
		}

		circuito := BuscarCircuitoEnArbol(celdaEntrante.R, celdaEntrante.C, m, n, adj)
		if len(circuito) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuito {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// MetodoMODIParaleloFilas fragmenta la evaluacion de deltas dividiendo la matriz por filas entre los núcleos de CPU.
func (p *ProblemaTransporte) MetodoMODIParaleloFilas() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	numWorkers := runtime.NumCPU()

	type DeltaCandidate struct {
		P     Point
		Delta float64
	}

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		u := make([]float64, m)
		v := make([]float64, n)
		uKnown := make([]bool, m)
		vKnown := make([]bool, n)
		uKnown[0] = true

		for startRow := 0; startRow < m; startRow++ {
			if uKnown[startRow] {
				queue := []int{startRow}
				for len(queue) > 0 {
					curr := queue[0]
					queue = queue[1:]

					if curr < m {
						for _, nxt := range adj[curr] {
							col := nxt - m
							if !vKnown[col] {
								v[col] = p.Costos[curr][col] - u[curr]
								vKnown[col] = true
								queue = append(queue, nxt)
							}
						}
					} else {
						col := curr - m
						for _, nxt := range adj[curr] {
							row := nxt
							if !uKnown[row] {
								u[row] = p.Costos[row][col] - v[col]
								uKnown[row] = true
								queue = append(queue, nxt)
							}
						}
					}
				}
			}
		}

		candidates := make([]DeltaCandidate, numWorkers)
		var wg sync.WaitGroup
		rowsPerWorker := (m + numWorkers - 1) / numWorkers

		for w := 0; w < numWorkers; w++ {
			rStart := w * rowsPerWorker
			rEnd := rStart + rowsPerWorker
			if rEnd > m {
				rEnd = m
			}
			if rStart >= m {
				break
			}

			wg.Add(1)
			go func(workerID, rs, re int) {
				defer wg.Done()
				bestDelta := 0.0
				var bestPt Point

				for i := rs; i < re; i++ {
					ui := u[i]
					for j := 0; j < n; j++ {
						if !basic[i][j] {
							delta := p.Costos[i][j] - (ui + v[j])
							if delta < bestDelta {
								bestDelta = delta
								bestPt = Point{i, j}
							}
						}
					}
				}
				candidates[workerID] = DeltaCandidate{P: bestPt, Delta: bestDelta}
			}(w, rStart, rEnd)
		}

		wg.Wait()

		minDelta := 0.0
		var celdaEntrante Point
		for _, cand := range candidates {
			if cand.Delta < minDelta {
				minDelta = cand.Delta
				celdaEntrante = cand.P
			}
		}

		if minDelta >= 0 {
			break
		}

		circuito := BuscarCircuitoEnArbol(celdaEntrante.R, celdaEntrante.C, m, n, adj)
		if len(circuito) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuito {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// MetodoMODIParaleloCeldas resuelve el problema de transporte usando variables duales u y v,
// fragmentando la matriz de costos reducidos (deltas) de forma continua entre todos los núcleos de CPU.
func (p *ProblemaTransporte) MetodoMODIParaleloCeldas() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	numWorkers := runtime.NumCPU()
	totalCeldas := m * n

	type DeltaCandidate struct {
		P     Point
		Delta float64
	}

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		// Calcular potenciales duales u y v
		u := make([]float64, m)
		v := make([]float64, n)
		uKnown := make([]bool, m)
		vKnown := make([]bool, n)
		uKnown[0] = true

		for startRow := 0; startRow < m; startRow++ {
			if uKnown[startRow] {
				queue := []int{startRow}
				for len(queue) > 0 {
					curr := queue[0]
					queue = queue[1:]

					if curr < m {
						for _, nxt := range adj[curr] {
							col := nxt - m
							if !vKnown[col] {
								v[col] = p.Costos[curr][col] - u[curr]
								vKnown[col] = true
								queue = append(queue, nxt)
							}
						}
					} else {
						col := curr - m
						for _, nxt := range adj[curr] {
							row := nxt
							if !uKnown[row] {
								u[row] = p.Costos[row][col] - v[col]
								uKnown[row] = true
								queue = append(queue, nxt)
							}
						}
					}
				}
			}
		}

		candidates := make([]DeltaCandidate, numWorkers)
		var wg sync.WaitGroup

		for w := 0; w < numWorkers; w++ {
			cStart := w * totalCeldas / numWorkers
			cEnd := (w + 1) * totalCeldas / numWorkers
			if cStart >= totalCeldas {
				break
			}

			wg.Add(1)
			go func(workerID, startIdx, endIdx int) {
				defer wg.Done()
				bestDelta := 0.0
				var bestPt Point

				for idx := startIdx; idx < endIdx; idx++ {
					i := idx / n
					j := idx % n
					if !basic[i][j] {
						delta := p.Costos[i][j] - (u[i] + v[j])
						if delta < bestDelta {
							bestDelta = delta
							bestPt = Point{i, j}
						}
					}
				}
				candidates[workerID] = DeltaCandidate{P: bestPt, Delta: bestDelta}
			}(w, cStart, cEnd)
		}

		wg.Wait()

		minDelta := 0.0
		var celdaEntrante Point
		for _, cand := range candidates {
			if cand.Delta < minDelta {
				minDelta = cand.Delta
				celdaEntrante = cand.P
			}
		}

		if minDelta >= 0 {
			break
		}

		circuito := BuscarCircuitoEnArbol(celdaEntrante.R, celdaEntrante.C, m, n, adj)
		if len(circuito) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuito {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// MetodoMODIParaleloBloques resuelve el problema de transporte dividiendo la matriz de deltas en bloques 2D
func (p *ProblemaTransporte) MetodoMODIParaleloBloques() (float64, int) {
	m, n := p.M, p.N
	alloc, basic := p.SolucionVogel()
	iteraciones := 0
	numWorkers := runtime.NumCPU()
	gr, gc := CalcularGridBloques(numWorkers, m, n)
	totalBlocks := gr * gc

	type DeltaCandidate struct {
		P     Point
		Delta float64
	}

	for {
		iteraciones++
		adj := p.ConstruirArbolBasico(basic)

		// Calcular potenciales duales u y v
		u := make([]float64, m)
		v := make([]float64, n)
		uKnown := make([]bool, m)
		vKnown := make([]bool, n)
		uKnown[0] = true

		for startRow := 0; startRow < m; startRow++ {
			if uKnown[startRow] {
				queue := []int{startRow}
				for len(queue) > 0 {
					curr := queue[0]
					queue = queue[1:]

					if curr < m {
						for _, nxt := range adj[curr] {
							col := nxt - m
							if !vKnown[col] {
								v[col] = p.Costos[curr][col] - u[curr]
								vKnown[col] = true
								queue = append(queue, nxt)
							}
						}
					} else {
						col := curr - m
						for _, nxt := range adj[curr] {
							row := nxt
							if !uKnown[row] {
								u[row] = p.Costos[row][col] - v[col]
								uKnown[row] = true
								queue = append(queue, nxt)
							}
						}
					}
				}
			}
		}

		candidates := make([]DeltaCandidate, totalBlocks)
		var wg sync.WaitGroup

		blockIdx := 0
		for br := 0; br < gr; br++ {
			rStart := br * m / gr
			rEnd := (br + 1) * m / gr
			for bc := 0; bc < gc; bc++ {
				cStart := bc * n / gc
				cEnd := (bc + 1) * n / gc

				wg.Add(1)
				go func(idx, rs, re, cs, ce int) {
					defer wg.Done()
					bestDelta := 0.0
					var bestPt Point

					for i := rs; i < re; i++ {
						ui := u[i]
						for j := cs; j < ce; j++ {
							if !basic[i][j] {
								delta := p.Costos[i][j] - (ui + v[j])
								if delta < bestDelta {
									bestDelta = delta
									bestPt = Point{i, j}
								}
							}
						}
					}
					candidates[idx] = DeltaCandidate{P: bestPt, Delta: bestDelta}
				}(blockIdx, rStart, rEnd, cStart, cEnd)
				blockIdx++
			}
		}

		wg.Wait()

		minDelta := 0.0
		var celdaEntrante Point
		for _, cand := range candidates {
			if cand.Delta < minDelta {
				minDelta = cand.Delta
				celdaEntrante = cand.P
			}
		}

		if minDelta >= 0 {
			break
		}

		circuito := BuscarCircuitoEnArbol(celdaEntrante.R, celdaEntrante.C, m, n, adj)
		if len(circuito) == 0 {
			break
		}

		theta := 1e18
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] < theta {
				theta = alloc[pt.R][pt.C]
			}
		}

		for k, pt := range circuito {
			if k%2 == 0 {
				alloc[pt.R][pt.C] += theta
			} else {
				alloc[pt.R][pt.C] -= theta
			}
		}

		basic[celdaEntrante.R][celdaEntrante.C] = true
		for k := 1; k < len(circuito); k += 2 {
			pt := circuito[k]
			if alloc[pt.R][pt.C] == 0 {
				basic[pt.R][pt.C] = false
				break
			}
		}
	}

	costoTotal := 0.0
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			costoTotal += alloc[i][j] * p.Costos[i][j]
		}
	}
	return costoTotal, iteraciones
}

// MetodoMODIParalelo mantiene compatibilidad apuntando a la particion por celdas
func (p *ProblemaTransporte) MetodoMODIParalelo() (float64, int) {
	return p.MetodoMODIParaleloCeldas()
}


// Funciones utilitarias
func countTrue(b []bool) int {
	c := 0
	for _, v := range b {
		if v {
			c++
		}
	}
	return c
}

func firstTrue(b []bool) int {
	for i, v := range b {
		if v {
			return i
		}
	}
	return -1
}

func minFloat(a, b float64) float64 {
	if a < b {
		return a
	}
	return b
}

func maxSlice(s []float64) float64 {
	m := -1e18
	for _, v := range s {
		if v > m {
			m = v
		}
	}
	return m
}

func indexOf(s []float64, val float64) int {
	for i, v := range s {
		if v == val {
			return i
		}
	}
	return -1
}

func containsPoint(slice []Point, p Point) bool {
	for _, pt := range slice {
		if pt.R == p.R && pt.C == p.C {
			return true
		}
	}
	return false
}
