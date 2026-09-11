# Marco teórico

> Etapa 1. Borrador. Todas las ecuaciones están numeradas y citadas; las que tienen un
> límite conocido se verifican numéricamente en la Etapa 5 (`checks/check_5_1_*`).
> Fichas de las fuentes en `notas/fichas.md`.

El material es una lámina de acetato de celulosa con poros de aire. El objeto que dispersa
es el **poro**, no una partícula: una inclusión de índice bajo (aire) en una matriz de
índice alto (el sólido). Todo lo que sigue está escrito en esos términos.

---

## 1. Parámetro de tamaño y contraste

Para una inhomogeneidad de diámetro `D` iluminada con luz de longitud de onda en vacío `λ`,
el parámetro adimensional que gobierna el régimen de dispersión es

$$x \;=\; \frac{\pi D}{\lambda} \tag{1}$$

y el contraste de índice relevante es

$$m \;=\; \frac{n_\text{aire}}{n_\text{sol}(\lambda)} \;=\; \frac{1}{n_\text{sol}(\lambda)} \;\approx\; 0.68 \tag{2}$$

con `n_sol(λ)` del acetato de celulosa (≈ 1.47, ver `data/refs/n_lambda.md`). Nótese que
`m < 1`: a diferencia de un pigmento, acá el scatterer es **menos** denso ópticamente que
el medio que lo rodea. La física de Mie no cambia por eso — las secciones eficaces dependen
de `|m − 1|`, no del signo — pero conviene tenerlo presente al comparar con la literatura
de TiO₂.

Con `λ` en el visible (400–700 nm) y los diámetros medidos en el Labo 6:

| muestra | `D` (Feret medio) | `x` en 400–700 nm |
|---|---|---|
| 1–3 | ≈ 1.6 µm | **7 – 13** |
| 4 | ≈ 0.1 µm | **0.45 – 0.8** |

Los dos grupos caen en zonas **disjuntas** del eje `x`. Esa es la observación que el
proyecto cuantifica.

---

## 2. Los dos límites

### 2.1 Rayleigh (`x ≪ 1`)

Para `x ≪ 1` y `|m| x ≪ 1` la partícula responde como un dipolo y la eficiencia de
dispersión es (Bohren & Huffman 1983, capítulo de partículas pequeñas):

$$Q_\text{sca} \;=\; \frac{8}{3}\,x^4 \left|\frac{m^2-1}{m^2+2}\right|^2 \tag{3}$$

La sección eficaz es `σ_sca = Q_sca · πD²/4`, de modo que

$$\sigma_\text{sca} \;\propto\; \frac{D^6}{\lambda^4} \tag{4}$$

Ésta es la dependencia espectral fuerte: la luz azul se dispersa ~7 veces más que la roja
entre 400 y 700 nm. **Verificación (check 5.1a):** la rutina de Mie debe reproducir
`Q_sca ∝ x⁴` cuando `x → 0`.

### 2.2 Difracción / óptica geométrica (`x ≫ 1`)

Para `x ≫ 1` la eficiencia de extinción tiende a **2**, no a 1 — la "paradoja de la
extinción": la partícula bloquea su sombra geométrica y además difracta una cantidad igual
de luz. Para un scatterer no absorbente, toda la extinción es dispersión:

$$Q_\text{sca} \;\xrightarrow[x \to \infty]{}\; 2 \tag{5}$$

con oscilaciones ("ripple") que se amortiguan al crecer `x`. Lo decisivo para este proyecto
es que en ese límite `Q_sca` **casi no depende de λ**: la dispersión se vuelve acromática y
la reflectancia sale plana. **Verificación (check 5.1b):** `Q_sca → 2` con `x → ∞`.

### 2.3 La transición (`x ~ 0.5 – 2`)

Entre ambos límites `Q_sca(x)` sube desde `x⁴` hasta su primer máximo (por encima de 2) y
después oscila hacia el plateau. No hay forma cerrada: se calcula con la serie de Mie
(Etapa 5, `src/dosregimenes/mie.py`). Lo que importa acá es que **es justo en esa subida
donde `d ln σ_sca / d ln λ` es máxima en módulo** — es decir, donde la respuesta es más
cromática. La muestra 4 (`x ≈ 0.45–0.8`) está sobre ese flanco.

---

## 3. De la dispersión de un poro a la reflectancia de la lámina

Éste es el eslabón que hace falta para no leer mal lo medido, y merece decirse explícito.

### 3.1 Camino libre medio de transporte

Con `ρ` poros por unidad de volumen, el camino libre medio de transporte es

$$\ell^{*} \;=\; \frac{1}{\rho\,\sigma_\text{sca}\,(1-g)} \tag{6}$$

donde `g = ⟨cos θ⟩` es la anisotropía de la dispersión (también de Mie). Para poros
esféricos de diámetro `D` que ocupan una fracción de volumen `φ`,

$$\rho \;=\; \frac{6\,\phi}{\pi D^{3}} \tag{7}$$

`ℓ*` es la distancia tras la cual la luz "olvidó" su dirección inicial. Es la única
longitud del problema de transporte: la reflectancia de la lámina depende de `d/ℓ*`, no de
`d` y `ℓ*` por separado.

### 3.2 Reflectancia difusa de una lámina

En el régimen difusivo (`d ≫ ℓ*`), la densidad de energía obedece

$$\nabla^{2}\Phi \;-\; \frac{\mu_a}{D_\text{dif}}\,\Phi \;=\; 0, \qquad D_\text{dif} \;=\; \frac{\ell^{*}}{3} \tag{8}$$

y con condiciones de borde extrapoladas en ambas caras se obtiene `R(d/ℓ*)`, monótona
creciente y **acotada por 1**. Los dos límites que sí son seguros:

- `d ≫ ℓ*` → `R` satura: agregar espesor casi no agrega reflectancia.
- `d ≲ ℓ*` → la difusión deja de valer; ahí manda el Monte Carlo (`montecarlo.py`).

La forma cerrada concreta se adopta de la literatura y **se verifica contra el Monte Carlo
en la Etapa 5** (check MC: `|R+T+A−1| < 10⁻³`, y acuerdo con la difusión en su régimen).
No se la afirma acá sin ese contraste.

### 3.3 Por qué `s` medida no es el exponente de `σ_sca`

Consecuencia de que `R` esté acotada y sea una función no lineal y saturante de `d/ℓ*`:

$$\sigma_\text{sca}(\lambda) \;\longrightarrow\; \ell^{*}(\lambda) \;\longrightarrow\; R(\lambda) \tag{9}$$

**comprime los exponentes**. Un medio perfectamente Rayleigh (`σ ∝ λ⁻⁴`) no produce
`s = −d ln R/d ln λ = 4`: produce un `s` bastante menor, porque donde `R` es alta está
cerca de saturar y responde poco a cambios de `ℓ*`.

Esto no es una nota al pie: la Etapa 2 midió `s₄ ≈ 1.3–1.4` para la muestra 4, y sería un
error concluir de ahí que "no es Rayleigh porque no da 4". **La cadena (9) es exactamente
lo que la Etapa 5 tiene que reproducir sin parámetros de ajuste**, y es lo que convierte
una pendiente medida en una afirmación sobre el régimen de dispersión.

---

## 4. Dispersión dependiente

Las ecuaciones (3)–(6) suponen scatterers **diluidos** e independientes. Acá `φ ~ 0.3–0.7`:
los poros están correlacionados y no se puede sumar sus secciones eficaces sin más. La
corrección entra por el **factor de estructura** `S(q)`, con `q = 2k sin(θ/2)` el momento
transferido:

$$\frac{d\sigma}{d\Omega}\bigg|_\text{efectiva} \;=\; \frac{d\sigma}{d\Omega}\bigg|_\text{1 poro} \cdot S(q) \tag{10}$$

Se usa `S(q)` de **Percus–Yevick** para esferas duras a fracción de empaquetamiento `φ`
(forma cerrada de Ashcroft–Lekner; se implementa en `estructura.py`). Los límites que la
implementación debe cumplir:

- `φ → 0` ⟹ `S(q) → 1` (recupera el caso diluido).
- `φ > 0` ⟹ `S(q → 0) < 1`: el orden de corto alcance **suprime la dispersión hacia
  adelante**, lo que en general **reduce** `ℓ*` respecto del cálculo diluido.

El proyecto calcula `ℓ*(λ)` **con y sin** esta corrección, para acotar cuánto pesa en la
conclusión en vez de asumirlo.

---

## 5. Óptimo de blancura

Combinando (3) y (5): la eficiencia de dispersión por unidad de volumen de material crece
como `x⁴` en Rayleigh, satura en el plateau, y por lo tanto tiene un **máximo para `x` de
orden unos pocos**. Es la razón por la que el TiO₂ pigmentario se fabrica en 200–300 nm
(Borgmann §2.2.1) y por la que las escamas del *Cyphochilus* alcanzan `R ≈ 0.5–0.7` con
~7 µm de espesor (Vukusic et al. 2007; Wilts et al. 2018).

En ese mapa: las muestras 1–3 (`x ≈ 7–13`) están **pasadas** del óptimo — dispersan bien y
de forma acromática, pero gastan material; la muestra 4 (`x ≈ 0.45–0.8`) está **corta** —
dispersa fuerte en el azul y poco en el rojo, que es exactamente el peor caso para
"blanco". Ninguna de las dos está en el óptimo, y eso es una predicción contrastable en la
figura de mérito de la Etapa 5.

---

## 6. Definición operacional de la frontera

"El régimen cambia en `x ~ 1`" no es una afirmación verificable hasta decir *qué* se define
como frontera. Tres candidatas:

| | definición | pros / contras |
|---|---|---|
| **F1** | `x = 1` | Convención estándar. No depende de calcular Mie, así que es independiente de las elecciones del modelo. No tiene contenido dinámico. |
| **F2** | el `x` donde `\|d ln σ_sca / d ln λ\|` baja de un umbral (p. ej. 1), o sea donde la respuesta deja de ser fuertemente cromática | Es la que se conecta directamente con el observable `s`. Depende del umbral elegido. |
| **F3** | el `x` del máximo de `\|dQ_sca/dx\|` (flanco de la primera resonancia) | Puramente geométrica de la curva de Mie, sin umbral libre. Menos interpretable físicamente. |

**Se designa F1 como primaria**, y F2 y F3 se calculan en la Etapa 5 y se reportan como
análisis de sensibilidad. Tres razones:

1. F1 no requiere la serie de Mie, así que no hereda las elecciones del modelo (contraste,
   polidispersión, esfericidad). Es el punto de referencia más limpio.
2. F2 y F3 son *refinamientos* de F1: se espera que caigan en `x` de orden 1, y verificarlo
   es en sí un resultado.
3. **Lo decisivo:** las cuatro muestras caen lejos de la frontera por ambos lados
   (`x ≈ 0.45–0.8` vs `x ≈ 7–13`). La conclusión del proyecto **no depende** de dónde
   exactamente se ponga la línea. Con 4 muestras en 2 grupos disjuntos se puede
   *caracterizar* los dos regímenes y *acotar* la frontera, no *medirla* — y conviene que
   la respuesta sea robusta a esa definición en vez de depender de ella.

---

## 7. Qué predice este marco, y qué mide el proyecto

| régimen | `x` | `Q_sca` vs λ | `s = −d ln R/d ln λ` esperada |
|---|---|---|---|
| Rayleigh / transición | ≲ 1 | fuerte (→ `λ⁻⁴`) | **alta** |
| Mie / grande | ≫ 1 | casi plana (`→ 2`) | **baja** |

Medido en la Etapa 2 (banda discriminante 600–745 nm):

- muestras 1–3: `s = 0.21 ± 0.02` → compatible con el plateau acromático.
- muestra 4: `s = 1.44` → compatible con el flanco cromático.

La Etapa 5 cierra el circuito: calcula `s` predicha por (1)–(10) **sin parámetros de
ajuste** y la compara con estos valores (check 5.2).

---

## Referencias

- Bohren, C. F.; Huffman, D. R. *Absorption and Scattering of Light by Small Particles.* Wiley, 1983.
- van de Hulst, H. C. *Light Scattering by Small Particles.* Wiley, 1957.
- Borgmann, L. M. *Bio-inspired white porous polymers fabricated via supercritical CO₂ foaming.* Tesis doctoral, KIT, 2023. (§2.2.1, §2.2.2)
- Syurik, J. et al. *Bio-inspired, large scale, highly scattering films for nanoparticle-alternative white surfaces.* Sci. Rep. **7**, 46637 (2017).
- Vukusic, P.; Hallam, B.; Noyes, J. *Brilliant whiteness in ultrathin beetle scales.* Science **315**, 348 (2007).
- Wilts, B. D. et al. *Evolutionary-optimized photonic network structure in white beetle wing scales.* Adv. Mater. **30**, 1702057 (2018).
- Sultanova, N.; Kasarova, S.; Nikolov, I. *Dispersion properties of optical polymers.* Acta Phys. Pol. A **116**, 585 (2009).
