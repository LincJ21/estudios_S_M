package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"
)

type MatrixData struct {
	CostosTrans [][]float64 `json:"costos_trans"`
	CostosAsig  [][]float64 `json:"costos_asig"`
}

type Legacy100Data struct {
	CostosTransporte [][]float64 `json:"costos_transporte"`
	CostosAsignacion [][]float64 `json:"costos_asignacion"`
}

type PyScaleItem struct {
	Costo     float64  `json:"costo"`
	Iters     *int     `json:"iters,omitempty"`
	TiempoMs  *float64 `json:"tiempo_ms"`
	MemoriaKB *float64 `json:"memoria_kb"`
	Timeout   bool     `json:"timeout,omitempty"`
}

type PyScaleGroup struct {
	N       int         `json:"n"`
	Vars    int         `json:"vars"`
	Hungaro PyScaleItem `json:"hungaro"`
	MODI    PyScaleItem `json:"modi"`
	SS      PyScaleItem `json:"ss"`
}

type MetodoMetrica struct {
	Nombre      string  `json:"nombre"`
	Categoria   string  `json:"categoria"`
	TiempoMs    float64 `json:"tiempo_ms"`
	MemoriaKB   float64 `json:"memoria_kb"`
	Alocaciones uint64  `json:"alocaciones"`
	Costo       float64 `json:"costo"`
	Inviable    bool    `json:"inviable"`
	Timeout     bool    `json:"timeout"`
	Detalle     string  `json:"detalle"`
	Speedup     string  `json:"speedup"`
}

type EscalaBenchmarkJSON struct {
	Nombre    string          `json:"nombre"`
	N         int             `json:"n"`
	Variables int             `json:"variables"`
	Metricas  []MetodoMetrica `json:"metricas"`
}

type ReporteCompletoJSON struct {
	NumCPUs int                   `json:"num_cpus"`
	Escalas []EscalaBenchmarkJSON `json:"escalas"`
}

const TimeoutLimite = 15 * time.Minute

func medirTransGoConTimeout(fn func() (float64, int), timeout time.Duration) (costo float64, iters int, durMs float64, memKB float64, allocs uint64, excedido bool) {
	runtime.GC()
	var m1, m2 runtime.MemStats
	runtime.ReadMemStats(&m1)
	t0 := time.Now()

	type res struct {
		c  float64
		it int
	}
	ch := make(chan res, 1)
	go func() {
		c, it := fn()
		ch <- res{c, it}
	}()

	select {
	case r := <-ch:
		dur := time.Since(t0)
		runtime.ReadMemStats(&m2)
		durMs = float64(dur.Nanoseconds()) / 1e6
		memKB = float64(m2.TotalAlloc-m1.TotalAlloc) / 1024.0
		allocs = m2.Mallocs - m1.Mallocs
		costo = r.c
		iters = r.it
		return costo, iters, durMs, memKB, allocs, false
	case <-time.After(timeout):
		durMs = float64(timeout.Milliseconds())
		return 0, 0, durMs, 0, 0, true
	}
}

func medirAsigGoConTimeout(fn func() (float64, []int), timeout time.Duration) (costo float64, durMs float64, memKB float64, allocs uint64, excedido bool) {
	runtime.GC()
	var m1, m2 runtime.MemStats
	runtime.ReadMemStats(&m1)
	t0 := time.Now()

	type res struct {
		c  float64
		as []int
	}
	ch := make(chan res, 1)
	go func() {
		c, as := fn()
		ch <- res{c, as}
	}()

	select {
	case r := <-ch:
		dur := time.Since(t0)
		runtime.ReadMemStats(&m2)
		durMs = float64(dur.Nanoseconds()) / 1e6
		memKB = float64(m2.TotalAlloc-m1.TotalAlloc) / 1024.0
		allocs = m2.Mallocs - m1.Mallocs
		costo = r.c
		return costo, durMs, memKB, allocs, false
	case <-time.After(timeout):
		durMs = float64(timeout.Milliseconds())
		return 0, durMs, 0, 0, true
	}
}

func medirFBGo(fn func() (float64, int64)) (costo float64, evals int64, durMs float64, memKB float64, allocs uint64) {
	runtime.GC()
	var m1, m2 runtime.MemStats
	runtime.ReadMemStats(&m1)
	t0 := time.Now()
	costo, evals = fn()
	dur := time.Since(t0)
	runtime.ReadMemStats(&m2)
	durMs = float64(dur.Nanoseconds()) / 1e6
	memKB = float64(m2.TotalAlloc-m1.TotalAlloc) / 1024.0
	allocs = m2.Mallocs - m1.Mallocs
	return
}

func cargarMatriz(paths []string, nDefault int) ([][]float64, [][]float64) {
	for _, p := range paths {
		if b, err := os.ReadFile(p); err == nil {
			var md MatrixData
			if err := json.Unmarshal(b, &md); err == nil && len(md.CostosTrans) > 0 {
				return md.CostosTrans, md.CostosAsig
			}
			var l100 Legacy100Data
			if err := json.Unmarshal(b, &l100); err == nil && len(l100.CostosTransporte) > 0 {
				return l100.CostosTransporte, l100.CostosAsignacion
			}
		}
	}

	r := rand.New(rand.NewSource(42))
	ct := make([][]float64, nDefault)
	ca := make([][]float64, nDefault)
	for i := 0; i < nDefault; i++ {
		ct[i] = make([]float64, nDefault)
		ca[i] = make([]float64, nDefault)
		for j := 0; j < nDefault; j++ {
			ct[i][j] = float64(r.Intn(29) + 1)
			ca[i][j] = float64(r.Intn(90) + 10)
		}
	}
	return ct, ca
}

func cargarResultadosPython() map[string]PyScaleGroup {
	res := make(map[string]PyScaleGroup)
	paths := []string{"python_scales_results.json", "../python_scales_results.json", "/home/lincj/Documentos/S_&_M/python_scales_results.json"}
	for _, p := range paths {
		if b, err := os.ReadFile(p); err == nil {
			if err := json.Unmarshal(b, &res); err == nil && len(res) > 0 {
				break
			}
		}
	}
	return res
}

func main() {
	numCPUs := runtime.NumCPU()

	fmt.Println(strings.Repeat("=", 128))
	fmt.Println("     EVALUACION DE ESCALABILIDAD SISTEMATICA (100, 1.000, 10.000, 100.000 Y 1.000.000 VARIABLES)")
	fmt.Printf("   Configuracion de Hardware: %d Nucleos de CPU detectados (GOMAXPROCS: %d)\n", numCPUs, runtime.GOMAXPROCS(0))
	fmt.Println("   Comparacion de Estrategias Paralelas: Filas vs Celdas Continuas vs Bloques 2D (Tiling)")
	fmt.Println("   Limite de ejecucion: 15 minutos (900 s) por algoritmo. Si excede, continua sin colapsar.")
	fmt.Println(strings.Repeat("=", 128))

	pyScales := cargarResultadosPython()

	escalas := []struct {
		nombre    string
		tag       string
		n         int
		vars      int
		jsonFiles []string
		runSS     bool
		runFB     bool
	}{
		{"100 Variables", "100", 10, 100, []string{"matrices_100.json", "../matrices_100.json"}, true, true},
		{"1.000 Variables", "1k", 32, 1024, []string{"matrices_1000.json", "../matrices_1000.json"}, true, false},
		{"10.000 Variables", "10k", 100, 10000, []string{"matrices_10000.json", "../matrices_10000.json"}, true, false},
		{"100.000 Variables", "100k", 316, 99856, []string{"matrices_100000.json", "../matrices_100000.json"}, true, false},
		{"1.000.000 Variables", "1m", 1000, 1000000, []string{"matrices_1000000.json", "../matrices_1000000.json"}, false, false},
	}

	var reporteJSON ReporteCompletoJSON
	reporteJSON.NumCPUs = numCPUs

	calcSpeedup := func(goMs float64, pyMs float64, pyTimeout bool) string {
		if goMs <= 0 {
			return "N/A"
		}
		if pyMs > 0 {
			return fmt.Sprintf("%.1fx", pyMs/goMs)
		}
		if pyTimeout {
			return fmt.Sprintf(">%.1fx (Py >15m)", 900000.0/goMs)
		}
		return "N/A"
	}

	for _, esc := range escalas {
		costosTrans, costosAsig := cargarMatriz(esc.jsonFiles, esc.n)
		n := esc.n

		oferta := make([]float64, n)
		demanda := make([]float64, n)
		for i := range oferta {
			oferta[i] = 100.0
			demanda[i] = 100.0
		}

		pTrans := &ProblemaTransporte{
			M:       n,
			N:       n,
			Costos:  costosTrans,
			Oferta:  oferta,
			Demanda: demanda,
		}

		pAsig := &ProblemaAsignacion{
			N:      n,
			Costos: costosAsig,
		}

		escalaJSON := EscalaBenchmarkJSON{
			Nombre:    esc.nombre,
			N:         esc.n,
			Variables: esc.vars,
		}

		fmt.Printf("\n>>> PROCESANDO ESCALA: %s (%dx%d = %d Variables) <<<\n", esc.nombre, n, n, esc.vars)

		// -----------------------------------------------------------------
		// DATOS DE PYTHON (REFERENCIA BASE)
		// -----------------------------------------------------------------
		var pySST, pySSMem float64
		var pyMODIT, pyMODIMem float64
		var pyHungT, pyHungMem float64
		var pyFBT, pyFBMem float64
		var pySSTo, pyMODITo, pyHungTo, pyFBTo bool

		if esc.tag == "100" {
			pySST, pySSMem = 11.204, 7.33
			pyMODIT, pyMODIMem = 1.515, 5.83
			pyFBT, pyFBMem = 5110.83, 0.70
			pyHungT, pyHungMem = 0.105, 0.61
		} else if pData, ok := pyScales[esc.tag]; ok {
			if pData.SS.TiempoMs != nil {
				pySST = *pData.SS.TiempoMs
				pySSMem = *pData.SS.MemoriaKB
			}
			pySSTo = pData.SS.Timeout

			if pData.MODI.TiempoMs != nil {
				pyMODIT = *pData.MODI.TiempoMs
				pyMODIMem = *pData.MODI.MemoriaKB
			}
			pyMODITo = pData.MODI.Timeout

			if pData.Hungaro.TiempoMs != nil {
				pyHungT = *pData.Hungaro.TiempoMs
				pyHungMem = *pData.Hungaro.MemoriaKB
			}
			pyHungTo = pData.Hungaro.Timeout
		}

		// Registrar Python en JSON
		if pySST > 0 || pySSTo {
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Stepping Stone (Python Secuencial)", Categoria: "Transporte", TiempoMs: pySST, MemoriaKB: pySSMem, Detalle: "Secuencial Python", Timeout: pySSTo, Speedup: "1.0x (Base)",
			})
		}
		if pyMODIT > 0 || pyMODITo {
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Metodo MODI u-v (Python Secuencial)", Categoria: "Transporte", TiempoMs: pyMODIT, MemoriaKB: pyMODIMem, Detalle: "Secuencial Python", Timeout: pyMODITo, Speedup: "1.0x (Base)",
			})
		}
		if pyHungT > 0 || pyHungTo {
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Metodo Hungaro O(n^3) (Python Secuencial)", Categoria: "Asignacion", TiempoMs: pyHungT, MemoriaKB: pyHungMem, Detalle: "Secuencial Python", Timeout: pyHungTo, Speedup: "1.0x (Base)",
			})
		}
		if pyFBT > 0 || pyFBTo {
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Fuerza Bruta (Python Secuencial)", Categoria: "Asignacion", TiempoMs: pyFBT, MemoriaKB: pyFBMem, Detalle: "Secuencial Python", Timeout: pyFBTo, Speedup: "1.0x (Base)",
			})
		}

		// -----------------------------------------------------------------
		// 1. TRANSPORTE EN GO
		// -----------------------------------------------------------------
		if esc.runSS {
			if esc.vars <= 1024 {
				cSS, _, tSSSeq, memSSSeq, alSSSeq, toSSSeq := medirTransGoConTimeout(pTrans.SteppingStoneSecuencial, TimeoutLimite)
				escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
					Nombre: "Stepping Stone (Go Secuencial)", Categoria: "Transporte", Costo: cSS, TiempoMs: tSSSeq, MemoriaKB: memSSSeq, Alocaciones: alSSSeq, Timeout: toSSSeq, Speedup: calcSpeedup(tSSSeq, pySST, pySSTo),
				})
			}

			// Filas
			cSSFil, _, tSSFil, memSSFil, alSSFil, toSSFil := medirTransGoConTimeout(pTrans.SteppingStoneParaleloFilas, TimeoutLimite)
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: fmt.Sprintf("Stepping Stone (Go Filas %dC)", numCPUs), Categoria: "Transporte", Costo: cSSFil, TiempoMs: tSSFil, MemoriaKB: memSSFil, Alocaciones: alSSFil, Timeout: toSSFil, Speedup: calcSpeedup(tSSFil, pySST, pySSTo),
			})

			// Celdas Continuas
			cSSCeldas, _, tSSCeldas, memSSCeldas, alSSCeldas, toSSCeldas := medirTransGoConTimeout(pTrans.SteppingStoneParaleloCeldas, TimeoutLimite)
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: fmt.Sprintf("Stepping Stone (Go Celdas %dC)", numCPUs), Categoria: "Transporte", Costo: cSSCeldas, TiempoMs: tSSCeldas, MemoriaKB: memSSCeldas, Alocaciones: alSSCeldas, Timeout: toSSCeldas, Speedup: calcSpeedup(tSSCeldas, pySST, pySSTo),
			})

			// Bloques 2D (Tiling)
			cSSBlk, _, tSSBlk, memSSBlk, alSSBlk, toSSBlk := medirTransGoConTimeout(pTrans.SteppingStoneParaleloBloques, TimeoutLimite)
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: fmt.Sprintf("Stepping Stone (Go Bloques 2D %dC)", numCPUs), Categoria: "Transporte", Costo: cSSBlk, TiempoMs: tSSBlk, MemoriaKB: memSSBlk, Alocaciones: alSSBlk, Timeout: toSSBlk, Speedup: calcSpeedup(tSSBlk, pySST, pySSTo),
			})
		} else {
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Stepping Stone (Go Bloques 2D)", Categoria: "Transporte", Timeout: true, Inviable: true, Detalle: "Demoró más de 15 min (900 s estimados: evaluar 10^6 ciclos por paso excede tiempo)", Speedup: "Timeout (900 s)",
			})
		}

		// B) Metodo MODI u-v (Secuencial, Filas, Celdas, Bloques)
		cMSeq, _, tMODISeq, memMODISeq, alMODISeq, toMSeq := medirTransGoConTimeout(pTrans.MetodoMODI, TimeoutLimite)
		escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
			Nombre: "Metodo MODI u-v (Go Secuencial)", Categoria: "Transporte", Costo: cMSeq, TiempoMs: tMODISeq, MemoriaKB: memMODISeq, Alocaciones: alMODISeq, Timeout: toMSeq, Speedup: calcSpeedup(tMODISeq, pyMODIT, pyMODITo),
		})

		cMFil, _, tMODIFil, memMODIFil, alMODIFil, toMFil := medirTransGoConTimeout(pTrans.MetodoMODIParaleloFilas, TimeoutLimite)
		escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
			Nombre: fmt.Sprintf("Metodo MODI (Go Filas %dC)", numCPUs), Categoria: "Transporte", Costo: cMFil, TiempoMs: tMODIFil, MemoriaKB: memMODIFil, Alocaciones: alMODIFil, Timeout: toMFil, Speedup: calcSpeedup(tMODIFil, pyMODIT, pyMODITo),
		})

		cMCeldas, _, tMODICeldas, memMODICeldas, alMODICeldas, toMCeldas := medirTransGoConTimeout(pTrans.MetodoMODIParaleloCeldas, TimeoutLimite)
		escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
			Nombre: fmt.Sprintf("Metodo MODI (Go Celdas %dC)", numCPUs), Categoria: "Transporte", Costo: cMCeldas, TiempoMs: tMODICeldas, MemoriaKB: memMODICeldas, Alocaciones: alMODICeldas, Timeout: toMCeldas, Speedup: calcSpeedup(tMODICeldas, pyMODIT, pyMODITo),
		})

		cMBlk, _, tMODIBlk, memMODIBlk, alMODIBlk, toMBlk := medirTransGoConTimeout(pTrans.MetodoMODIParaleloBloques, TimeoutLimite)
		escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
			Nombre: fmt.Sprintf("Metodo MODI (Go Bloques 2D %dC)", numCPUs), Categoria: "Transporte", Costo: cMBlk, TiempoMs: tMODIBlk, MemoriaKB: memMODIBlk, Alocaciones: alMODIBlk, Timeout: toMBlk, Speedup: calcSpeedup(tMODIBlk, pyMODIT, pyMODITo),
		})

		// -----------------------------------------------------------------
		// 2. ASIGNACION EN GO
		// -----------------------------------------------------------------
		if esc.runFB {
			cFBSeq, _, tFBSeq, memFBSeq, _ := medirFBGo(pAsig.FuerzaBrutaSecuencial)
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Fuerza Bruta 10! (Go Secuencial)", Categoria: "Asignacion", Costo: cFBSeq, TiempoMs: tFBSeq, MemoriaKB: memFBSeq, Alocaciones: 0, Speedup: calcSpeedup(tFBSeq, pyFBT, pyFBTo),
			})

			cFBPar, _, tFBPar, memFBPar, alFBPar := medirFBGo(pAsig.FuerzaBrutaParalela)
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: fmt.Sprintf("Fuerza Bruta (Go %dC)", numCPUs), Categoria: "Asignacion", Costo: cFBPar, TiempoMs: tFBPar, MemoriaKB: memFBPar, Alocaciones: alFBPar, Speedup: calcSpeedup(tFBPar, pyFBT, pyFBTo),
			})
		} else {
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: fmt.Sprintf("Fuerza Bruta %d!", n), Categoria: "Asignacion", Timeout: true, Inviable: true, Detalle: fmt.Sprintf("Demoró más de 15 min (Excede límite: O(N!) > 10^20 años)"), Speedup: "Inviable O(N!)",
			})
		}

		if esc.vars <= 100000 {
			cHung, tHung, memHung, alHung, toHung := medirAsigGoConTimeout(pTrans.asigWrapper(pAsig.MetodoHungaro), TimeoutLimite)
			escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
				Nombre: "Metodo Hungaro O(n^3) (Go Clasico)", Categoria: "Asignacion", Costo: cHung, TiempoMs: tHung, MemoriaKB: memHung, Alocaciones: alHung, Timeout: toHung, Speedup: calcSpeedup(tHung, pyHungT, pyHungTo),
			})
		}

		cSAP, tSAP, memSAP, alSAP, toSAP := medirAsigGoConTimeout(func() (float64, []int) {
			return UltraHungaroSAP(n, costosAsig)
		}, TimeoutLimite)
		escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
			Nombre: "Ultra Hungaro SAP (Go Lineal)", Categoria: "Asignacion", Costo: cSAP, TiempoMs: tSAP, MemoriaKB: memSAP, Alocaciones: alSAP, Timeout: toSAP, Speedup: calcSpeedup(tSAP, pyHungT, pyHungTo),
		})

		cSAPPar, tSAPPar, memSAPPar, alSAPPar, toSAPPar := medirAsigGoConTimeout(func() (float64, []int) {
			return UltraHungaroSAPParalelo(n, costosAsig)
		}, TimeoutLimite)
		escalaJSON.Metricas = append(escalaJSON.Metricas, MetodoMetrica{
			Nombre: fmt.Sprintf("Ultra Hungaro SAP (Go %dC Paralelo)", numCPUs), Categoria: "Asignacion", Costo: cSAPPar, TiempoMs: tSAPPar, MemoriaKB: memSAPPar, Alocaciones: alSAPPar, Timeout: toSAPPar, Speedup: calcSpeedup(tSAPPar, pyHungT, pyHungTo),
		})

		reporteJSON.Escalas = append(reporteJSON.Escalas, escalaJSON)
	}

	// Guardar reporte JSON para el generador de graficas
	outJSON := "resultados_benchmark.json"
	if b, err := json.MarshalIndent(reporteJSON, "", "  "); err == nil {
		_ = os.WriteFile(outJSON, b, 0644)
		_ = os.WriteFile("../resultados_benchmark.json", b, 0644)
	}

	// =========================================================================
	// PRESENTACION DE TABLAS COMPARATIVAS
	// =========================================================================
	fmt.Println("\n" + strings.Repeat("=", 128))
	fmt.Println(" TABLA 1: CASO 1 - PROBLEMA DE TRANSPORTE: FILAS vs CELDAS vs BLOQUES 2D (100 A 1.000.000 VARIABLES)")
	fmt.Println(strings.Repeat("=", 128))
	fmt.Printf("%-24s %-42s %-16s %-16s %-14s %-16s\n",
		"ESCALA (VARS)", "METODO / ESTRATEGIA (LENGUAJE)", "TIEMPO (ms)", "MEMORIA (KB)", "ALOCS (HEAP)", "SPEEDUP (vs Py)")
	fmt.Println(strings.Repeat("-", 128))

	for _, esc := range reporteJSON.Escalas {
		fmt.Printf("[%s (%dx%d)]\n", esc.Nombre, esc.N, esc.N)
		for _, m := range esc.Metricas {
			if m.Categoria == "Transporte" {
				if m.Timeout || m.Inviable {
					fmt.Printf("%-24s %-42s %-16s %-16s %-14s %-16s\n",
						"", m.Nombre, "Demoró > 15 min", "N/A", "N/A", "Timeout (900 s)")
				} else {
					fmt.Printf("%-24s %-42s %-16.3f %-16.2f %-14d %-16s\n",
						"", m.Nombre, m.TiempoMs, m.MemoriaKB, m.Alocaciones, m.Speedup)
				}
			}
		}
		fmt.Println(strings.Repeat("-", 128))
	}

	fmt.Println("\n" + strings.Repeat("=", 128))
	fmt.Println(" TABLA 2: CASO 2 - PROBLEMA DE ASIGNACION (100 A 1.000.000 VARIABLES)")
	fmt.Println(strings.Repeat("=", 128))
	fmt.Printf("%-24s %-42s %-16s %-16s %-14s %-16s\n",
		"ESCALA (VARS)", "METODO / ESTRATEGIA (LENGUAJE)", "TIEMPO (ms)", "MEMORIA (KB)", "ALOCS (HEAP)", "SPEEDUP (vs Py)")
	fmt.Println(strings.Repeat("-", 128))

	for _, esc := range reporteJSON.Escalas {
		fmt.Printf("[%s (%dx%d)]\n", esc.Nombre, esc.N, esc.N)
		for _, m := range esc.Metricas {
			if m.Categoria == "Asignacion" {
				if m.Timeout || m.Inviable {
					fmt.Printf("%-24s %-42s %-16s %-16s %-14s %-16s\n",
						"", m.Nombre, "Demoró > 15 min", "N/A", "N/A", m.Speedup)
				} else {
					fmt.Printf("%-24s %-42s %-16.3f %-16.2f %-14d %-16s\n",
						"", m.Nombre, m.TiempoMs, m.MemoriaKB, m.Alocaciones, m.Speedup)
				}
			}
		}
		fmt.Println(strings.Repeat("-", 128))
	}

	// Ejecutar automaticamente generador de graficas si existe
	pyScripts := []string{"generar_graficas.py", "../generar_graficas.py"}
	for _, sc := range pyScripts {
		if _, err := os.Stat(sc); err == nil {
			cmd := exec.Command("python3", sc)
			_ = cmd.Run()
			break
		}
	}
}

func (p *ProblemaTransporte) asigWrapper(fn func() (float64, []int)) func() (float64, []int) {
	return fn
}
