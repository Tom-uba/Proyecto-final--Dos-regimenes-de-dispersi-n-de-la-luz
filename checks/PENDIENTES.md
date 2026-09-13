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
| `4.1` | nubes `P(x)`: 1–3 se solapan, 4 disjunta | solape >0.80 entre 1–3, <0.05 vs 4 | 4 ✅ |
| `5.1` | límites de Mie `x→0` (∝x⁴, con prefactor) y `x→∞` (→2) | potencia ±0.01, prefactor ±0.5 %, ⟨Q⟩ a 2 % de 2 | 5 ✅ |
| `5.2` | `s` predicha vs. medida | signo correcto, factor < 2 | 5 |
| `5.3` | ancla externa (Syurik / beetle) | dentro del error citado | 5 |
| `5.4` | límites exactos de S(q) de Percus–Yevick | S(0) a 2 %, \|S(∞)−1\| < 0.02 | 5 ✅ |
| `5.5` | Monte Carlo: límite balístico exacto, difusión en régimen grueso, conteo | ±0.003; ±10 % vs difusión; sin escapar < 1e-3 | 5 ✅ |
| `6.1` | controles de absorción y espesor | cuantitativos (un número) | 6 |
