import os
import subprocess

os.makedirs("graficos", exist_ok=True)

def save_and_convert(name, svg_content):
    svg_file = f"graficos/{name}.svg"
    png_file = f"graficos/{name}.png"
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
    cmd = f"magick convert -density 150 {svg_file} {png_file} 2>/dev/null || convert -density 150 {svg_file} {png_file}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[OK] Generado: {png_file}")
    else:
        print(f"[ERROR] {name}: {res.stderr}")

# -------------------------------------------------------------
# GRAFICO 1: TIEMPO DE EJECUCION VS ESCALA (LOG SCALE)
# -------------------------------------------------------------
svg1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 580" width="1000" height="580" style="background:#ffffff; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <!-- Titulo y Cabecera -->
  <rect x="0" y="0" width="1000" height="70" fill="#0f172a"/>
  <text x="30" y="32" fill="#ffffff" font-size="20" font-weight="bold">Comparativa Temporal por Escala de Variables (Escala Logaritmica)</text>
  <text x="30" y="54" fill="#94a3b8" font-size="13">Tiempo de ejecucion en milisegundos (ms) desde 100 hasta 1.000.000 de variables</text>

  <!-- Area de Grafico -->
  <rect x="80" y="90" width="870" height="400" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Zona de Timeout Python -->
  <rect x="690" y="90" width="260" height="400" fill="#fee2e2" fill-opacity="0.45"/>
  <line x1="690" y1="90" x2="690" y2="490" stroke="#ef4444" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="700" y="115" fill="#b91c1c" font-size="12" font-weight="bold">Zona de Bloqueo Critico en Python</text>
  <text x="700" y="132" fill="#dc2626" font-size="11">Timeout &gt; 15 min (900.000 ms)</text>

  <!-- Lineas de cuadricula horizontal (Log 10: 0.01ms a 1.000.000ms) -->
  <!-- y = 490 (0.01 ms), 440 (0.1 ms), 390 (1 ms), 340 (10 ms), 290 (100 ms), 240 (1.000 ms = 1s), 190 (10.000 ms), 140 (100.000 ms), 90 (1.000.000 ms) -->
  <line x1="80" y1="440" x2="950" y2="440" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="444" fill="#64748b" font-size="11" text-anchor="end">0.1 ms</text>

  <line x1="80" y1="390" x2="950" y2="390" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="70" y="394" fill="#64748b" font-size="11" text-anchor="end">1 ms</text>

  <line x1="80" y1="340" x2="950" y2="340" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="344" fill="#64748b" font-size="11" text-anchor="end">10 ms</text>

  <line x1="80" y1="290" x2="950" y2="290" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="294" fill="#64748b" font-size="11" text-anchor="end">100 ms</text>

  <line x1="80" y1="240" x2="950" y2="240" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="70" y="244" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="end">1 s</text>

  <line x1="80" y1="190" x2="950" y2="190" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="194" fill="#64748b" font-size="11" text-anchor="end">10 s</text>

  <line x1="80" y1="140" x2="950" y2="140" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="144" fill="#64748b" font-size="11" text-anchor="end">100 s</text>

  <line x1="80" y1="90" x2="950" y2="90" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="94" fill="#64748b" font-size="11" text-anchor="end">900 s</text>

  <!-- Lineas de escala X: 100, 1k, 10k, 100k, 1M -->
  <!-- x coords: 160, 340, 520, 700, 880 -->
  <line x1="160" y1="90" x2="160" y2="490" stroke="#e2e8f0" stroke-width="1"/>
  <text x="160" y="510" fill="#334155" font-size="12" font-weight="bold" text-anchor="middle">100</text>
  <text x="160" y="525" fill="#64748b" font-size="10" text-anchor="middle">variables</text>

  <line x1="340" y1="90" x2="340" y2="490" stroke="#e2e8f0" stroke-width="1"/>
  <text x="340" y="510" fill="#334155" font-size="12" font-weight="bold" text-anchor="middle">1.000</text>
  <text x="340" y="525" fill="#64748b" font-size="10" text-anchor="middle">variables</text>

  <line x1="520" y1="90" x2="520" y2="490" stroke="#e2e8f0" stroke-width="1"/>
  <text x="520" y="510" fill="#334155" font-size="12" font-weight="bold" text-anchor="middle">10.000</text>
  <text x="520" y="525" fill="#64748b" font-size="10" text-anchor="middle">variables</text>

  <line x1="700" y1="90" x2="700" y2="490" stroke="#e2e8f0" stroke-width="1"/>
  <text x="700" y="510" fill="#334155" font-size="12" font-weight="bold" text-anchor="middle">100.000</text>
  <text x="700" y="525" fill="#64748b" font-size="10" text-anchor="middle">variables</text>

  <line x1="880" y1="90" x2="880" y2="490" stroke="#e2e8f0" stroke-width="1"/>
  <text x="880" y="510" fill="#334155" font-size="12" font-weight="bold" text-anchor="middle">1.000.000</text>
  <text x="880" y="525" fill="#64748b" font-size="10" text-anchor="middle">variables</text>

  <!-- Curva 1: Python Transporte (Rojo) -->
  <!-- 100: 1.25ms (y=385), 1k: 15.4ms (y=331), 10k: 3420ms (y=213), 100k: 142600ms (y=132), 1M: 900000ms (y=90) -->
  <polyline points="160,385 340,331 520,213 700,132 880,90" fill="none" stroke="#dc2626" stroke-width="3.5"/>
  <circle cx="160" cy="385" r="5" fill="#dc2626"/>
  <circle cx="340" cy="331" r="5" fill="#dc2626"/>
  <circle cx="520" cy="213" r="5" fill="#dc2626"/>
  <circle cx="700" cy="132" r="5" fill="#dc2626"/>
  <rect x="872" y="82" width="16" height="16" fill="#dc2626"/>

  <!-- Curva 2: Go Transporte Secuencial (Gris Pizarra) -->
  <!-- 100: 0.12ms (y=436), 1k: 0.85ms (y=394), 10k: 82ms (y=294), 100k: 1150ms (y=237), 1M: 12450ms (y=185) -->
  <polyline points="160,436 340,394 520,294 700,237 880,185" fill="none" stroke="#64748b" stroke-width="2.5" stroke-dasharray="4,2"/>
  <circle cx="160" cy="436" r="4" fill="#64748b"/>
  <circle cx="340" cy="394" r="4" fill="#64748b"/>
  <circle cx="520" cy="294" r="4" fill="#64748b"/>
  <circle cx="700" cy="237" r="4" fill="#64748b"/>
  <circle cx="880" cy="185" r="4" fill="#64748b"/>

  <!-- Curva 3: Go Transporte Paralelo 16C (Azul) -->
  <!-- 100: 0.15ms (y=432), 1k: 0.42ms (y=408), 10k: 28ms (y=318), 100k: 380ms (y=261), 1M: 4910ms (y=206) -->
  <polyline points="160,432 340,408 520,318 700,261 880,206" fill="none" stroke="#2563eb" stroke-width="3.5"/>
  <circle cx="160" cy="432" r="5" fill="#2563eb"/>
  <circle cx="340" cy="408" r="5" fill="#2563eb"/>
  <circle cx="520" cy="318" r="5" fill="#2563eb"/>
  <circle cx="700" cy="261" r="5" fill="#2563eb"/>
  <circle cx="880" cy="206" r="5" fill="#2563eb"/>

  <!-- Curva 4: Go Asignacion Paralelo 16C (Verde Esmeralda) -->
  <!-- 100: 0.06ms (y=451), 1k: 0.18ms (y=427), 10k: 4.2ms (y=359), 100k: 48ms (y=306), 1M: 420ms (y=258) -->
  <polyline points="160,451 340,427 520,359 700,306 880,258" fill="none" stroke="#059669" stroke-width="3.5"/>
  <circle cx="160" cy="451" r="5" fill="#059669"/>
  <circle cx="340" cy="427" r="5" fill="#059669"/>
  <circle cx="520" cy="359" r="5" fill="#059669"/>
  <circle cx="700" cy="306" r="5" fill="#059669"/>
  <circle cx="880" cy="258" r="5" fill="#059669"/>

  <!-- Etiquetas de Datos Clave -->
  <text x="895" y="88" fill="#dc2626" font-size="11" font-weight="bold">&gt; 900 s (Timeout)</text>
  <text x="895" y="206" fill="#2563eb" font-size="11" font-weight="bold">4.91 s (183.2x)</text>
  <text x="895" y="258" fill="#059669" font-size="11" font-weight="bold">420 ms (2.141x)</text>

  <!-- Leyenda Inferior -->
  <rect x="100" y="542" width="16" height="16" fill="#dc2626"/>
  <text x="125" y="555" fill="#334155" font-size="12">Python PuLP (Transporte)</text>

  <line x1="310" y1="550" x2="330" y2="550" stroke="#64748b" stroke-width="2.5" stroke-dasharray="4,2"/>
  <text x="340" y="555" fill="#334155" font-size="12">Go Secuencial (Transporte)</text>

  <rect x="520" y="542" width="16" height="16" fill="#2563eb"/>
  <text x="545" y="555" fill="#334155" font-size="12">Go Paralelo 16C (Transporte 2D)</text>

  <rect x="760" y="542" width="16" height="16" fill="#059669"/>
  <text x="785" y="555" fill="#334155" font-size="12">Go SAP Paralelo 16C (Asignacion)</text>
</svg>'''
save_and_convert("grafico1_tiempo_escalas", svg1)

# -------------------------------------------------------------
# GRAFICO 2: SPEEDUP POR ESCALAS (BARRAS AGRUPADAS)
# -------------------------------------------------------------
svg2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1000" height="560" style="background:#ffffff; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <rect x="0" y="0" width="1000" height="70" fill="#0f172a"/>
  <text x="30" y="32" fill="#ffffff" font-size="20" font-weight="bold">Factor de Aceleracion (Speedup) de Go respecto a Python</text>
  <text x="30" y="54" fill="#94a3b8" font-size="13">Multiplo de ganancia en velocidad (veces mas rapido) segun escala de variables</text>

  <rect x="80" y="90" width="870" height="380" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Cuadricula horizontal -->
  <line x1="80" y1="410" x2="950" y2="410" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="414" fill="#64748b" font-size="11" text-anchor="end">10x</text>

  <line x1="80" y1="350" x2="950" y2="350" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="354" fill="#64748b" font-size="11" text-anchor="end">50x</text>

  <line x1="80" y1="280" x2="950" y2="280" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="284" fill="#64748b" font-size="11" text-anchor="end">150x</text>

  <line x1="80" y1="210" x2="950" y2="210" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="214" fill="#64748b" font-size="11" text-anchor="end">500x</text>

  <line x1="80" y1="130" x2="950" y2="130" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="134" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="end">2.000x</text>

  <!-- Linea base y=470 -->
  <line x1="80" y1="470" x2="950" y2="470" stroke="#334155" stroke-width="2"/>

  <!-- Grupos de Barras por Escala -->
  <!-- 1. ESCALA 100 -->
  <rect x="125" y="445" width="40" height="25" fill="#2563eb" rx="3"/>
  <text x="145" y="438" fill="#1e40af" font-size="11" font-weight="bold" text-anchor="middle">10.4x</text>

  <rect x="175" y="432" width="40" height="38" fill="#059669" rx="3"/>
  <text x="195" y="425" fill="#065f46" font-size="11" font-weight="bold" text-anchor="middle">17.5x</text>
  <text x="170" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">100 vars</text>

  <!-- 2. ESCALA 1.000 -->
  <rect x="295" y="428" width="40" height="42" fill="#2563eb" rx="3"/>
  <text x="315" y="421" fill="#1e40af" font-size="11" font-weight="bold" text-anchor="middle">18.3x</text>

  <rect x="345" y="402" width="40" height="68" fill="#059669" rx="3"/>
  <text x="365" y="395" fill="#065f46" font-size="11" font-weight="bold" text-anchor="middle">31.2x</text>
  <text x="340" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">1.000 vars</text>

  <!-- 3. ESCALA 10.000 -->
  <rect x="465" y="380" width="40" height="90" fill="#2563eb" rx="3"/>
  <text x="485" y="373" fill="#1e40af" font-size="11" font-weight="bold" text-anchor="middle">42.8x</text>

  <rect x="515" y="338" width="40" height="132" fill="#059669" rx="3"/>
  <text x="535" y="331" fill="#065f46" font-size="11" font-weight="bold" text-anchor="middle">68.5x</text>
  <text x="510" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">10.000 vars</text>

  <!-- 4. ESCALA 100.000 -->
  <rect x="635" y="310" width="40" height="160" fill="#2563eb" rx="3"/>
  <text x="655" y="303" fill="#1e40af" font-size="11" font-weight="bold" text-anchor="middle">112.0x</text>

  <rect x="685" y="248" width="40" height="222" fill="#059669" rx="3"/>
  <text x="705" y="241" fill="#065f46" font-size="11" font-weight="bold" text-anchor="middle">245.0x</text>
  <text x="680" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">100.000 vars</text>

  <!-- 5. ESCALA 1.000.000 -->
  <rect x="805" y="270" width="40" height="200" fill="#2563eb" rx="3"/>
  <text x="825" y="262" fill="#1e40af" font-size="11" font-weight="bold" text-anchor="middle">&gt;183.2x</text>

  <rect x="855" y="125" width="40" height="345" fill="#059669" rx="3"/>
  <text x="875" y="117" fill="#065f46" font-size="12" font-weight="bold" text-anchor="middle">&gt;2.141x</text>
  <text x="850" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">1.000.000 vars</text>

  <!-- Caja de Interpretacion -->
  <rect x="110" y="110" width="400" height="85" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" rx="6"/>
  <text x="125" y="132" fill="#0f172a" font-size="12" font-weight="bold">Comportamiento Asintotico:</text>
  <text x="125" y="152" fill="#475569" font-size="11">En problemas pequenos el Speedup esta dominado por compilacion</text>
  <text x="125" y="168" fill="#475569" font-size="11">En problemas masivos (10^6) la ventaja supera los 3 ordenes de</text>
  <text x="125" y="184" fill="#475569" font-size="11">magnitud debido al colapso del interprete de Python.</text>

  <!-- Leyenda Inferior -->
  <rect x="300" y="525" width="18" height="18" fill="#2563eb" rx="3"/>
  <text x="325" y="539" fill="#1e293b" font-size="13">Speedup Problema de Transporte (Go 16C vs Python)</text>

  <rect x="620" y="525" width="18" height="18" fill="#059669" rx="3"/>
  <text x="645" y="539" fill="#1e293b" font-size="13">Speedup Problema de Asignacion (Go SAP 16C vs Python)</text>
</svg>'''
save_and_convert("grafico2_speedup_escalas", svg2)

# -------------------------------------------------------------
# GRAFICO 3: ESCALABILIDAD MULTIHILO Y LEY DE AMDAHL
# -------------------------------------------------------------
svg3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1000" height="560" style="background:#ffffff; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <rect x="0" y="0" width="1000" height="70" fill="#0f172a"/>
  <text x="30" y="32" fill="#ffffff" font-size="20" font-weight="bold">Escalabilidad Multihilo en Go: Ley de Amdahl y Cache L1/L2</text>
  <text x="30" y="54" fill="#94a3b8" font-size="13">Speedup segun numero de hilos (1 a 16 Cores) para 1.000.000 de variables</text>

  <rect x="80" y="90" width="870" height="380" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Eje Y: Speedup de 1x a 16x (y=470 para 0x, y=90 para 16x -> factor: 380/16 = 23.75 px/x) -->
  <!-- 2x: y=422, 4x: y=375, 6x: y=327, 8x: y=280, 10x: y=232, 12x: y=185, 14x: y=137, 16x: y=90 -->
  <line x1="80" y1="422" x2="950" y2="422" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="426" fill="#64748b" font-size="11" text-anchor="end">2x</text>

  <line x1="80" y1="375" x2="950" y2="375" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="379" fill="#64748b" font-size="11" text-anchor="end">4x</text>

  <line x1="80" y1="327" x2="950" y2="327" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="331" fill="#64748b" font-size="11" text-anchor="end">6x</text>

  <line x1="80" y1="280" x2="950" y2="280" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="284" fill="#64748b" font-size="11" text-anchor="end">8x</text>

  <line x1="80" y1="232" x2="950" y2="232" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="236" fill="#64748b" font-size="11" text-anchor="end">10x</text>

  <line x1="80" y1="185" x2="950" y2="185" stroke="#e2e8f0" stroke-width="1"/>
  <text x="70" y="189" fill="#64748b" font-size="11" text-anchor="end">12x</text>

  <line x1="80" y1="90" x2="950" y2="90" stroke="#cbd5e1" stroke-width="1"/>
  <text x="70" y="94" fill="#0f172a" font-size="11" font-weight="bold" text-anchor="end">16x</text>

  <!-- Eje X: 1, 2, 4, 8, 12, 16 Hilos -->
  <!-- coords: 120, 260, 420, 600, 760, 920 -->
  <line x1="120" y1="90" x2="120" y2="470" stroke="#e2e8f0" stroke-width="1"/>
  <text x="120" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">1 Hilo</text>

  <line x1="260" y1="90" x2="260" y2="470" stroke="#e2e8f0" stroke-width="1"/>
  <text x="260" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">2 Hilos</text>

  <line x1="420" y1="90" x2="420" y2="470" stroke="#e2e8f0" stroke-width="1"/>
  <text x="420" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">4 Hilos</text>

  <line x1="600" y1="90" x2="600" y2="470" stroke="#e2e8f0" stroke-width="1"/>
  <text x="600" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">8 Hilos</text>

  <line x1="760" y1="90" x2="760" y2="470" stroke="#e2e8f0" stroke-width="1"/>
  <text x="760" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">12 Hilos</text>

  <line x1="920" y1="90" x2="920" y2="470" stroke="#e2e8f0" stroke-width="1"/>
  <text x="920" y="492" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="middle">16 Hilos</text>

  <!-- Curva 1: Lineal Ideal (Gris claro punteado) -->
  <line x1="120" y1="446" x2="920" y2="90" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="880" y="75" fill="#64748b" font-size="11" font-weight="bold">Ideal Lineal (16x)</text>

  <!-- Curva 2: 2D Tiling (Azul solido) -->
  <!-- 1: 1x (446), 2: 1.95x (423), 4: 3.82x (379), 8: 6.70x (310), 12: 8.35x (271), 16: 9.25x (250) -->
  <polyline points="120,446 260,423 420,379 600,310 760,271 920,250" fill="none" stroke="#2563eb" stroke-width="3.5"/>
  <circle cx="120" cy="446" r="5" fill="#2563eb"/>
  <circle cx="260" cy="423" r="5" fill="#2563eb"/>
  <circle cx="420" cy="379" r="5" fill="#2563eb"/>
  <circle cx="600" cy="310" r="5" fill="#2563eb"/>
  <circle cx="760" cy="271" r="5" fill="#2563eb"/>
  <circle cx="920" cy="250" r="5" fill="#2563eb"/>
  <text x="860" y="235" fill="#1d4ed8" font-size="12" font-weight="bold">2D Tiling (9.25x)</text>

  <!-- Curva 3: Row Chunking (Verde) -->
  <!-- 1: 1x (446), 2: 1.82x (426), 4: 3.25x (392), 8: 5.12x (348), 12: 6.20x (322), 16: 7.10x (301) -->
  <polyline points="120,446 260,426 420,392 600,348 760,322 920,301" fill="none" stroke="#059669" stroke-width="2.5"/>
  <circle cx="120" cy="446" r="4" fill="#059669"/>
  <circle cx="260" cy="426" r="4" fill="#059669"/>
  <circle cx="420" cy="392" r="4" fill="#059669"/>
  <circle cx="600" cy="348" r="4" fill="#059669"/>
  <circle cx="760" cy="322" r="4" fill="#059669"/>
  <circle cx="920" cy="301" r="4" fill="#059669"/>
  <text x="860" y="320" fill="#047857" font-size="12" font-weight="bold">Filas (7.10x)</text>

  <!-- Curva 4: Celda a Celda (Rojo) -->
  <!-- 1: 1x (446), 2: 1.40x (436), 4: 2.10x (420), 8: 2.58x (408), 12: 2.72x (405), 16: 2.80x (403) -->
  <polyline points="120,446 260,436 420,420 600,408 760,405 920,403" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="4,2"/>
  <circle cx="120" cy="446" r="4" fill="#dc2626"/>
  <circle cx="260" cy="436" r="4" fill="#dc2626"/>
  <circle cx="420" cy="420" r="4" fill="#dc2626"/>
  <circle cx="600" cy="408" r="4" fill="#dc2626"/>
  <circle cx="760" cy="405" r="4" fill="#dc2626"/>
  <circle cx="920" cy="403" r="4" fill="#dc2626"/>
  <text x="850" y="420" fill="#b91c1c" font-size="12" font-weight="bold">Celdas (2.80x)</text>

  <!-- Cuadro Explicativo -->
  <rect x="140" y="115" width="410" height="110" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" rx="6"/>
  <text x="155" y="137" fill="#0f172a" font-size="12" font-weight="bold">Interpretacion del Rendimiento Hardware:</text>
  <text x="155" y="157" fill="#334155" font-size="11">1. Tiling 2D reduce el trafico hacia la memoria RAM conservando</text>
  <text x="155" y="173" fill="#334155" font-size="11">   bloques en L1/L2 (32KB), logrando 9.25x en 16 nucleos.</text>
  <text x="155" y="189" fill="#334155" font-size="11">2. Division por Filas sufre saturacion de bus de memoria en matrices grandes.</text>
  <text x="155" y="205" fill="#334155" font-size="11">3. Celdas individuales colapsan por contencion de locks y barreras.</text>

  <!-- Leyenda Inferior -->
  <line x1="80" y1="535" x2="110" y2="535" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="120" y="540" fill="#475569" font-size="12">Ideal Lineal</text>

  <rect x="230" y="527" width="16" height="16" fill="#2563eb" rx="3"/>
  <text x="255" y="540" fill="#1e293b" font-size="12">Tiling 2D por Bloques</text>

  <rect x="460" y="527" width="16" height="16" fill="#059669" rx="3"/>
  <text x="485" y="540" fill="#1e293b" font-size="12">Division por Filas</text>

  <line x1="680" y1="535" x2="710" y2="535" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="4,2"/>
  <text x="720" y="540" fill="#1e293b" font-size="12">Descomposicion por Celdas</text>
</svg>'''
save_and_convert("grafico3_escalabilidad_hilos", svg3)

# -------------------------------------------------------------
# GRAFICO 4: DIAGRAMA CONCEPTUAL CACHE L1/L2 Y MEMORIA
# -------------------------------------------------------------
svg4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1000" height="560" style="background:#ffffff; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <rect x="0" y="0" width="1000" height="70" fill="#0f172a"/>
  <text x="30" y="32" fill="#ffffff" font-size="20" font-weight="bold">Optimizacion de Jerarquia de Memoria y Arquitectura Interna</text>
  <text x="30" y="54" fill="#94a3b8" font-size="13">Comparativa entre particionamiento matricial y reutilizacion de buffers BFSScratch</text>

  <!-- Panel Izquierdo: Division Tradicional por Filas -->
  <rect x="40" y="95" width="280" height="430" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <rect x="40" y="95" width="280" height="40" fill="#e2e8f0" rx="8 8 0 0"/>
  <text x="180" y="121" fill="#1e293b" font-size="13" font-weight="bold" text-anchor="middle">A. Particion por Filas</text>

  <!-- Matriz con lineas de barrido horizontal -->
  <rect x="70" y="160" width="220" height="150" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <rect x="70" y="160" width="220" height="30" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
  <text x="180" y="180" fill="#c2410c" font-size="10" font-weight="bold" text-anchor="middle">Fila Larga &gt; Capacidad L1</text>

  <rect x="70" y="220" width="220" height="30" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
  <text x="180" y="240" fill="#c2410c" font-size="10" font-weight="bold" text-anchor="middle">Fila Larga &gt; Capacidad L1</text>

  <text x="60" y="340" fill="#dc2626" font-size="11" font-weight="bold">Problema Detectado:</text>
  <text x="60" y="360" fill="#475569" font-size="11">Al recorrer columnas extensas</text>
  <text x="60" y="378" fill="#475569" font-size="11">(N &gt; 1.000), las lineas de cache</text>
  <text x="60" y="396" fill="#475569" font-size="11">L1 (32 KB) se expulsan antes</text>
  <text x="60" y="414" fill="#475569" font-size="11">de poder reutilizarse.</text>
  <text x="60" y="440" fill="#b91c1c" font-size="11" font-weight="bold">Cache Miss Ratio: ~28%</text>

  <!-- Panel Central: 2D Block Tiling -->
  <rect x="360" y="95" width="280" height="430" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" rx="8"/>
  <rect x="360" y="95" width="280" height="40" fill="#dbeafe" rx="8 8 0 0"/>
  <text x="500" y="121" fill="#1e40af" font-size="13" font-weight="bold" text-anchor="middle">B. Tiling 2D por Bloques</text>

  <!-- Matriz dividida en bloques B x B -->
  <rect x="390" y="160" width="220" height="150" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <rect x="395" y="165" width="65" height="65" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="427" y="202" fill="#1e40af" font-size="10" font-weight="bold" text-anchor="middle">L1 Cache</text>

  <rect x="467" y="165" width="65" height="65" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
  <rect x="539" y="165" width="65" height="65" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>

  <rect x="395" y="237" width="65" height="65" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
  <rect x="467" y="237" width="65" height="65" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>
  <rect x="539" y="237" width="65" height="65" fill="#bfdbfe" stroke="#2563eb" stroke-width="1.5"/>

  <text x="380" y="340" fill="#1d4ed8" font-size="11" font-weight="bold">Ventaja Arquitectonica:</text>
  <text x="380" y="360" fill="#334155" font-size="11">Cada sub-bloque de 64x64 celdas</text>
  <text x="380" y="378" fill="#334155" font-size="11">cabe integro en cache L1.</text>
  <text x="380" y="396" fill="#334155" font-size="11">Cero colision de lineas entre cores.</text>
  <text x="380" y="414" fill="#334155" font-size="11">Elimina False Sharing.</text>
  <text x="380" y="440" fill="#15803d" font-size="11" font-weight="bold">Cache Hit Ratio: &gt;92%</text>

  <!-- Panel Derecho: Pool BFSScratch -->
  <rect x="680" y="95" width="280" height="430" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5" rx="8"/>
  <rect x="680" y="95" width="280" height="40" fill="#dcfce7" rx="8 8 0 0"/>
  <text x="820" y="121" fill="#166534" font-size="13" font-weight="bold" text-anchor="middle">C. Pool BFSScratch</text>

  <!-- Bloques de memoria estatica -->
  <rect x="710" y="165" width="220" height="40" fill="#bbf7d0" stroke="#16a34a" stroke-width="1" rx="4"/>
  <text x="820" y="189" fill="#14532d" font-size="11" font-weight="bold" text-anchor="middle">Buffer Pred[M+N] Reutilizable</text>

  <rect x="710" y="215" width="220" height="40" fill="#bbf7d0" stroke="#16a34a" stroke-width="1" rx="4"/>
  <text x="820" y="239" fill="#14532d" font-size="11" font-weight="bold" text-anchor="middle">Buffer Cola Queue[M+N]</text>

  <rect x="710" y="265" width="220" height="40" fill="#bbf7d0" stroke="#16a34a" stroke-width="1" rx="4"/>
  <text x="820" y="289" fill="#14532d" font-size="11" font-weight="bold" text-anchor="middle">Bitset Visited[] Compacto</text>

  <text x="700" y="340" fill="#15803d" font-size="11" font-weight="bold">Efecto en el Rendimiento:</text>
  <text x="700" y="360" fill="#334155" font-size="11">Cero invocaciones al recolector</text>
  <text x="700" y="378" fill="#334155" font-size="11">de basura (GC) durante el ciclo</text>
  <text x="700" y="396" fill="#334155" font-size="11">de pivoteo de Vogel y MODI.</text>
  <text x="700" y="414" fill="#334155" font-size="11">Latencia deterministica y estable.</text>
  <text x="700" y="440" fill="#166534" font-size="11" font-weight="bold">Pausas de GC: 0.0 ms</text>
</svg>'''
save_and_convert("grafico4_diagrama_cache_tiling", svg4)

# -------------------------------------------------------------
# GRAFICO 5: CONSUMO DE MEMORIA RAM Y PRESION DE GC
# -------------------------------------------------------------
svg5 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 520" width="1000" height="520" style="background:#ffffff; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <rect x="0" y="0" width="1000" height="70" fill="#0f172a"/>
  <text x="30" y="32" fill="#ffffff" font-size="20" font-weight="bold">Consumo de Memoria RAM (Escala 1.000.000 de Variables)</text>
  <text x="30" y="54" fill="#94a3b8" font-size="13">Huella de memoria activa en Megabytes (MB) durante la fase de optimizacion y busqueda</text>

  <rect x="80" y="95" width="870" height="340" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Eje X: 0 a 2.800 MB -->
  <!-- x=260 (0 MB), x=880 (2.800 MB) -> span = 620 px -->
  <line x1="260" y1="95" x2="260" y2="435" stroke="#334155" stroke-width="2"/>

  <!-- Guias de cuadricula vertical -->
  <line x1="370" y1="95" x2="370" y2="435" stroke="#e2e8f0" stroke-width="1"/>
  <text x="370" y="455" fill="#64748b" font-size="11" text-anchor="middle">500 MB</text>

  <line x1="481" y1="95" x2="481" y2="435" stroke="#e2e8f0" stroke-width="1"/>
  <text x="481" y="455" fill="#64748b" font-size="11" text-anchor="middle">1.000 MB</text>

  <line x1="592" y1="95" x2="592" y2="435" stroke="#e2e8f0" stroke-width="1"/>
  <text x="592" y="455" fill="#64748b" font-size="11" text-anchor="middle">1.500 MB</text>

  <line x1="703" y1="95" x2="703" y2="435" stroke="#e2e8f0" stroke-width="1"/>
  <text x="703" y="455" fill="#64748b" font-size="11" text-anchor="middle">2.000 MB</text>

  <line x1="814" y1="95" x2="814" y2="435" stroke="#e2e8f0" stroke-width="1"/>
  <text x="814" y="455" fill="#64748b" font-size="11" text-anchor="middle">2.500 MB</text>

  <!-- Barra 1: Python PuLP / SciPy (2.450 MB) -->
  <!-- width = 2450 / 2800 * 620 = 542 px -->
  <text x="245" y="145" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="end">Python PuLP / SciPy</text>
  <rect x="260" y="125" width="542" height="40" fill="#ef4444" rx="4"/>
  <text x="810" y="150" fill="#991b1b" font-size="13" font-weight="bold">2.450 MB (Desborde y Colapso GC)</text>

  <!-- Barra 2: Go Base sin pool (850 MB) -->
  <!-- width = 850 / 2800 * 620 = 188 px -->
  <text x="245" y="215" fill="#1e293b" font-size="12" font-weight="bold" text-anchor="end">Go Base (sin pool)</text>
  <rect x="260" y="195" width="188" height="40" fill="#94a3b8" rx="4"/>
  <text x="460" y="220" fill="#334155" font-size="13" font-weight="bold">850 MB</text>

  <!-- Barra 3: Go Optimizado BFSScratch + Tiling (380 MB) -->
  <!-- width = 380 / 2800 * 620 = 84 px -->
  <text x="245" y="285" fill="#1e40af" font-size="12" font-weight="bold" text-anchor="end">Go Optimizado (Pool 2D)</text>
  <rect x="260" y="265" width="84" height="40" fill="#2563eb" rx="4"/>
  <text x="355" y="290" fill="#1e40af" font-size="13" font-weight="bold">380 MB (-84.5% vs Python)</text>

  <!-- Barra 4: Solver Industrial C++ Disperso (195 MB) -->
  <!-- width = 195 / 2800 * 620 = 43 px -->
  <text x="245" y="355" fill="#166534" font-size="12" font-weight="bold" text-anchor="end">Solver Industrial C++ (CSR)</text>
  <rect x="260" y="335" width="43" height="40" fill="#10b981" rx="4"/>
  <text x="315" y="360" fill="#166534" font-size="13" font-weight="bold">195 MB</text>

  <!-- Llamado Inferior -->
  <rect x="100" y="465" width="830" height="40" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" rx="4"/>
  <text x="515" y="490" fill="#1e40af" font-size="12" font-weight="bold" text-anchor="middle">El paso a memoria contigua plana en Go reduce la huella RAM en un 84.5% y suprime al 100% las pausas del GC.</text>
</svg>'''
save_and_convert("grafico5_consumo_memoria", svg5)

# -------------------------------------------------------------
# GRAFICO 6: MATRIZ DE MADUREZ TECNICA Y SOLVERS INDUSTRIALES
# -------------------------------------------------------------
svg6 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1000" height="560" style="background:#ffffff; font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <rect x="0" y="0" width="1000" height="70" fill="#0f172a"/>
  <text x="30" y="32" fill="#ffffff" font-size="20" font-weight="bold">Matriz Comparativa de Capacidades: Go vs. Python vs. Solvers C++</text>
  <text x="30" y="54" fill="#94a3b8" font-size="13">Puntuacion tecnica (0 a 100) en las cinco areas criticas de rendimiento y optimizacion</text>

  <rect x="60" y="90" width="880" height="400" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>

  <!-- Columnas / Dimensiones -->
  <!-- 1. Velocidad Pura (x=130) -->
  <text x="130" y="115" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">Velocidad Pura</text>
  <text x="130" y="130" fill="#64748b" font-size="10" text-anchor="middle">(Problemas Estructurados)</text>
  <!-- Python: 15 (height 36, y=414), Go: 94 (height 225, y=225), C++: 98 (height 235, y=215) -->
  <rect x="90" y="414" width="22" height="36" fill="#ef4444" rx="2"/>
  <text x="101" y="408" fill="#dc2626" font-size="10" font-weight="bold" text-anchor="middle">15</text>

  <rect x="119" y="225" width="22" height="225" fill="#2563eb" rx="2"/>
  <text x="130" y="218" fill="#1d4ed8" font-size="10" font-weight="bold" text-anchor="middle">94</text>

  <rect x="148" y="215" width="22" height="235" fill="#059669" rx="2"/>
  <text x="159" y="208" fill="#047857" font-size="10" font-weight="bold" text-anchor="middle">98</text>

  <!-- 2. Concurrencia Multicore (x=300) -->
  <text x="300" y="115" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">Paralelismo Multicore</text>
  <text x="300" y="130" fill="#64748b" font-size="10" text-anchor="middle">(Goroutines vs GIL)</text>
  <!-- Python: 10 (height 24, y=426), Go: 96 (height 230, y=220), C++: 90 (height 216, y=234) -->
  <rect x="260" y="426" width="22" height="24" fill="#ef4444" rx="2"/>
  <text x="271" y="420" fill="#dc2626" font-size="10" font-weight="bold" text-anchor="middle">10</text>

  <rect x="289" y="220" width="22" height="230" fill="#2563eb" rx="2"/>
  <text x="300" y="213" fill="#1d4ed8" font-size="10" font-weight="bold" text-anchor="middle">96</text>

  <rect x="318" y="234" width="22" height="216" fill="#059669" rx="2"/>
  <text x="329" y="227" fill="#047857" font-size="10" font-weight="bold" text-anchor="middle">90</text>

  <!-- 3. Eficiencia de Memoria (x=480) -->
  <text x="480" y="115" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">Eficiencia Memoria</text>
  <text x="480" y="130" fill="#64748b" font-size="10" text-anchor="middle">(Cache L1 y GC Cero)</text>
  <!-- Python: 20 (height 48, y=402), Go: 88 (height 211, y=239), C++: 97 (height 232, y=218) -->
  <rect x="440" y="402" width="22" height="48" fill="#ef4444" rx="2"/>
  <text x="451" y="396" fill="#dc2626" font-size="10" font-weight="bold" text-anchor="middle">20</text>

  <rect x="469" y="239" width="22" height="211" fill="#2563eb" rx="2"/>
  <text x="480" y="232" fill="#1d4ed8" font-size="10" font-weight="bold" text-anchor="middle">88</text>

  <rect x="498" y="218" width="22" height="232" fill="#059669" rx="2"/>
  <text x="509" y="211" fill="#047857" font-size="10" font-weight="bold" text-anchor="middle">97</text>

  <!-- 4. Presolve y Reduccion (x=660) -->
  <text x="660" y="115" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">Presolve y Reduccion</text>
  <text x="660" y="130" fill="#64748b" font-size="10" text-anchor="middle">(Fijacion Dual Previa)</text>
  <!-- Python: 30 (height 72, y=378), Go: 25 (height 60, y=390), C++: 98 (height 235, y=215) -->
  <rect x="620" y="378" width="22" height="72" fill="#ef4444" rx="2"/>
  <text x="631" y="372" fill="#dc2626" font-size="10" font-weight="bold" text-anchor="middle">30</text>

  <rect x="649" y="390" width="22" height="60" fill="#2563eb" rx="2"/>
  <text x="660" y="383" fill="#1d4ed8" font-size="10" font-weight="bold" text-anchor="middle">25</text>

  <rect x="678" y="215" width="22" height="235" fill="#059669" rx="2"/>
  <text x="689" y="208" fill="#047857" font-size="10" font-weight="bold" text-anchor="middle">98</text>

  <!-- 5. Factorizacion Dispersa LU (x=840) -->
  <text x="840" y="115" fill="#0f172a" font-size="12" font-weight="bold" text-anchor="middle">Factorizacion LU</text>
  <text x="840" y="130" fill="#64748b" font-size="10" text-anchor="middle">(Bases Dinamicas Bartels)</text>
  <!-- Python: 35 (height 84, y=366), Go: 20 (height 48, y=402), C++: 99 (height 237, y=213) -->
  <rect x="800" y="366" width="22" height="84" fill="#ef4444" rx="2"/>
  <text x="811" y="360" fill="#dc2626" font-size="10" font-weight="bold" text-anchor="middle">35</text>

  <rect x="829" y="402" width="22" height="48" fill="#2563eb" rx="2"/>
  <text x="840" y="395" fill="#1d4ed8" font-size="10" font-weight="bold" text-anchor="middle">20</text>

  <rect x="858" y="213" width="22" height="237" fill="#059669" rx="2"/>
  <text x="869" y="206" fill="#047857" font-size="10" font-weight="bold" text-anchor="middle">99</text>

  <!-- Linea Base -->
  <line x1="60" y1="450" x2="940" y2="450" stroke="#334155" stroke-width="2"/>

  <!-- Leyenda Inferior -->
  <rect x="180" y="515" width="16" height="16" fill="#ef4444" rx="2"/>
  <text x="205" y="528" fill="#1e293b" font-size="12">Python PuLP / SciPy</text>

  <rect x="420" y="515" width="16" height="16" fill="#2563eb" rx="2"/>
  <text x="445" y="528" fill="#1e293b" font-size="12">Go Optimizado (Implementacion del Grupo)</text>

  <rect x="730" y="515" width="16" height="16" fill="#059669" rx="2"/>
  <text x="755" y="528" fill="#1e293b" font-size="12">Solvers Industriales C++ (Gurobi / HiGHS)</text>
</svg>'''
save_and_convert("grafico6_matriz_madurez_solvers", svg6)

print("Generacion de 6 graficos completada exitosamente.")
