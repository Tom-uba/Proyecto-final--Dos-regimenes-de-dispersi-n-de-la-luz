# Checks pendientes

Se agregan como `check_*.py` a medida que se completa cada etapa. Cada uno define
`run() -> (nombre, ok, evidencia)`. Ver `run_checks.py`.

| id | qué verifica | criterio | etapa |
|---|---|---|---|
| `0.1` | promedio de espectros vs. Fig. 6 | ver `check_0_1_fig6.py` | 0 ✅ |
| `2.1` | `s` robusta a método y a sub-banda | métodos coinciden; orden m4>m1–3 en ambas | 2 ✅ |
| `2.2` | separación de `s` entre {1,2,3} y {4} | > 3·σ_entre (se reporta también σ_ajuste) | 2 ✅ |
| `3.1` | media de `P(D)` vs. informe | ±10 % (≈1.6 µm en 1–3, ≈0.1 µm en 4) | 3 |
| `3.2` | escala del tag Zeiss vs. barra quemada | < 2 % | 3 |
| `4.1` | bandas de `x`: 1–3 se solapan, 4 disjunta | se cumple | 4 |
| `5.1` | límites de Mie `x→0` (∝x⁴) y `x→∞` (→2) | ambos reproducidos | 5 |
| `5.2` | `s` predicha vs. medida | signo correcto, factor < 2 | 5 |
| `5.3` | ancla externa (Syurik / beetle) | dentro del error citado | 5 |
| `MC` | conservación de energía en el Monte Carlo | \|R+T+A−1\| < 1e-3 | 5 |
| `6.1` | controles de absorción y espesor | cuantitativos (un número) | 6 |
