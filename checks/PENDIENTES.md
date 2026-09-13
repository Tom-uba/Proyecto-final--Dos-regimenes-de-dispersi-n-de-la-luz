# Checks pendientes

Se agregan como `check_*.py` a medida que se completa cada etapa. Cada uno define
`run() -> (nombre, ok, evidencia)`. Ver `run_checks.py`.

| id | qué verifica | criterio | etapa |
|---|---|---|---|
| `0.1` | promedio de espectros vs. Fig. 6 | ver `check_0_1_fig6.py` | 0 ✅ |
| `2.1` | `s` robusta a método y a sub-banda | métodos coinciden; orden m4>m1–3 en ambas | 2 ✅ |
| `2.2` | separación de `s` entre {1,2,3} y {4} | > 3·σ_entre (se reporta también σ_ajuste) | 2 ✅ |
| `2.3` | sin deriva de lámpara en la sesión del 02/06 | pendiente del residuo de s vs tiempo < 3σ y cambio < 0.05 | 2 ✅ |
| `3.1` | `P(D)` vs. informe, y ImageJ vs. Python | mediana ±10 % vs. informe; ±15 % entre pipelines | 3 ✅ |
| `3.2` | escala del tag Zeiss vs. barra quemada | < 2 % | 3 ✅ |
| `3.3` | espesor total SEM vs slide 13 | mediana a ±5 %, ≥ 2 imágenes válidas por muestra | 3 ✅ |
| `4.1` | nubes `P(x)`: 1–3 se solapan, 4 disjunta | solape >0.80 entre 1–3, <0.05 vs 4 | 4 ✅ |
| `5.1` | límites de Mie `x→0` (∝x⁴, con prefactor) y `x→∞` (→2) | potencia ±0.01, prefactor ±0.5 %, ⟨Q⟩ a 2 % de 2 | 5 ✅ |
| `5.2` | predicción SIN ajuste: Δs = s₄ − s̄₁₂₃ en rojo (600–745 nm) | signo correcto y ×0.5–2 | 5 ✅ |
| `5.3` | ancla externa Syurik 2017: R_total(600) a 9 / 16 / 53 µm con su morfología publicada | ±0.10 absoluto en los tres | 5 ❌ falla (−0.12, −0.10, −0.06); diagnosticada: factor de estructura PY monodisperso a η = φ apantalla de más (ver log 2026-09-13 e) |
| `5.4` | límites exactos de S(q) de Percus–Yevick | S(0) a 2 %, \|S(∞)−1\| < 0.02 | 5 ✅ |
| `5.5` | Monte Carlo: límite balístico exacto, difusión en régimen grueso, conteo | ±0.003; ±10 % vs difusión; sin escapar < 1e-3 | 5 ✅ |
| `5.6` | aproximación de desacople: β = 1 con poros iguales, β(0) = ⟨D³⟩²/⟨D⁶⟩, 0 < β ≤ 1, S_ef → 1 | 2 % | 5 ✅ |
| `5.7` | hipótesis de polidispersión, pre-registrada (commit 286b7f2): Syurik + s₄ + T de m4 + Δs | los cuatro | 5 ❌ falla: Syurik pasa por el borde, m4 sobrecorregida (s₄ 0.62, rms T 0.229, Δs ×0.46) |
| `6.0` | absorción por peso de camino en el Monte Carlo | balístico con absorción ±0.003; μ_a no altera la corrida | 6 ✅ |
| `6.1` | controles (pre-registrado): espesor y absorción | máx \|ΔΔs\| < 0.25·Δs_med; Q_med < Q_pred,mín − 3σ | 6 ❌ falla: (a) pasa (+0.16 < 0.31); (b) el criterio tenía el signo mal puesto: H_abs predice Q < 1 (0.85 / 0.59) y el medido es 0.952 ± 0.049 (ver log 2026-09-13 h) |
| `6.2` | frontera acotada (pre-registrado) | F1–F3 y F_s dentro de las cotas de los datos; CSV reproducible | 6 ❌ falla: F1–F3 dentro de [0.87, 5.10]; F_s con desacople 0.38–0.41 y monodisperso 1–3 0.82 quedan fuera |
| `6.3` | atribución tamaño vs entorno (pre-registrado) | f_D ≥ 0.75 con los dos cierres | 6 ✅ (0.81 / 0.99) |
| `6.4` | telarañas vs residuos (pre-registrado) | gatea sólo la implementación (±15 %, orden); ρ reportado | 6 ✅ implementación; lectura: "no respaldado" (ρ_T +1, ρ_s +0.5) |
