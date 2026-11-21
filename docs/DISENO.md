# Decisiones de diseño de la presentación

Registro de lo que Zeus fue decidiendo, aspecto por aspecto. Es la base de la futura plantilla pública y de la skill `presentacion`.

## 1 · Paleta (decidido 2026-11-20)
- Sistema **propio en OKLCH**: `scripts/generar_paleta.py` (uv, sin dependencias ni tokens). De un tono salen principal, acento complementario (+180°), fondo, tarjeta, borde, texto y texto suave, en modo claro y oscuro.
- El sorteo solo acepta combinaciones que cumplan: texto/fondo ≥ 7:1, texto suave y acento ≥ 4.5:1, principal (título, texto grande) ≥ 3:1, borde/fondo ≥ 1.15:1 y diferencia de claridad OKLab acento/principal ≥ 0.08 (heurística propia, sin fuente publicada).
- Fondo claro tintado del tono, con variante oscura; el apunte impreso siempre claro.
- El semáforo 🔴🟡🟢 **no aparece** en la presentación.
- Series de gráficas: Okabe-Ito o Paul Tol, solo tras verificar su licencia (pendiente).

## 2 · Tipografía (decidido 2026-11-20)
- **Títulos:** Source Serif 4 (serif editorial, OFL-1.1).
- **Cuerpo, tablas y notas:** Source Sans 3 (OFL-1.1), con tamaño y geometría de espacios ajustados (justificado) en `taller/espacios.html`.
- **Código:** JetBrains Mono (OFL-1.1), dentro de la terminal negra con escritura animada y colores de sintaxis.
- **Fuentes incrustadas** (carpeta `taller/fuentes/`, woff2 de Fontsource) para que el archivo se abra sin internet.

**Tamaño y espacios (lámina 1280×720), decididos:**
```css
:root{ --cuerpo:29px; --titulo:56px; --interlineado:1.38; --ancho-texto:64ch;
       --espacio-parrafo:0.55em; --margen:60px; --alineacion:justify; --guiones:auto; }
```
Párrafos justificados con guiones (español); listas, tablas y tarjetas alineadas a la izquierda.

## 4 · Componentes de código (decidido 2026-11-20)
Principio de Zeus: el código se ve **como en el lugar donde la persona lo usa**, para que se sienta familiar. Cinco componentes en `taller/codigo.html`:
1. **Terminal** — estilo oscuro genérico, comando que se «escribe» solo.
2. **Notebook de Jupyter** — estándar: **JupyterLab / clásico (B)**; VS Code y Colab quedan como alternativas plegadas. Animación escribir y ejecutar (`In [*]` → salida). Colores aproximados, por afinar con capturas reales.
3. **Archivo en el editor** — pestaña y número de línea (YAML/Markdown/`.py`).
4. **Antes y después** — diferencias, rojo lo que sale y verde lo que entra.
5. **Salida o registro** — texto sin comando.

**Velocidad de escritura aprobada:** 28 ms por letra en la terminal, 18 ms en el notebook.
**Botón de copiar (regla de Zeus):** copia **solo la entrada**, nunca la salida: sin `In [1]:`, sin `Out[1]:`, sin el prompt de la terminal y sin los números de línea. Terminal → solo el comando; notebook → solo el código de la celda; editor → el archivo sin numeración; diff → la versión nueva. El código copiable se prueba ejecutándolo (el del notebook se ejecutó con pandas). Se oculta al imprimir.

## Pendiente de decidir
Aspectos 3, 5 y 6: estructura de la diapositiva, diagramas y figuras, uso al presentar.

## Sorteador de estilo (taller/app.html, 2026-11-20)
Decisión de Zeus: el estilo se **sortea una sola vez** y se mantiene igual en toda la presentación. Los **tokens de diseño** (valores con nombre: `--principal`, `--acento`, `--fondo`…, más estilo base y viñeta) se sortean con una semilla y las 8 láminas de prueba los heredan. Se pueden **fijar** por separado la paleta, el estilo base y la viñeta, o **bloquear todo** cuando se decide; el enlace (`#p=…&e=…&v=…`) reproduce el mismo estilo.
- Estilos base en el sorteo (los que eligió Zeus): Suizo, Editorial, Tufte, Cuaderno, Blueprint, Periodismo de datos, Bento plano, Risografía, Neobrutalismo, Bauhaus y Memphis.
- Viñetas: cristal, plana (bento), línea fina, barra lateral y marcador cuadrado; cada estilo solo admite las compatibles.
- Regla nueva de la paleta: el color de sección llena debe tener ≥ 4.5:1 con el fondo o con el texto. El Blueprint usa siempre la paleta oscura.
- Láminas con espacios marcados «AQUÍ IRÁ LA GRÁFICA / LA TABLA» para el aspecto 5.

### Cambios del sorteador tras revisarlo con Zeus
- **Fuera de la lista:** el cristal (glassmorphism) y el gradient mesh, y en general los degradados de fondo: se ven informales. Las viñetas quedan en plana, línea fina, barra lateral y marcador cuadrado.
- **Más variedad real:** el sorteo ya cubría los 360° del tono; lo que se repetía era la estructura (un color y su complementario). Ahora también sortea la **armonía** (complementaria, análoga, triádica, complementaria dividida, monocromática, tetrádica), la **intensidad** del color (suave, media, viva) y los **neutros** (tintados, cálidos, fríos, casi blancos), y añade un **tercer color** (`--terciario`) que se usa en marcadores y decoraciones. En 3 000 semillas: 0 fallos y 2 890 principales distintos.
- Toda combinación sigue pasando las reglas de contraste (`terciario/fondo` ≥ 3:1 incluido).
- Nota: `generar_paleta.py` conserva la versión anterior (solo complementario); la lógica vigente es la de `app.html`.

### Perfil «mínimo» de la paleta (decidido 2026-11-20, a partir de la favorita de Zeus)
Favorita: Bauhaus, principal `#8080b3`, acento `#a0461b`, terciario `#4c9877`, marcador cuadrado. Es una **tríada exacta** (284°, 43°, 163°) apagada: croma .077 / .131 / .092 (total .30) y neutros tintados con el tono del principal. El sorteo anterior daba croma total mediano .39 y solo el 2 % de sus paletas cumplía las reglas derivadas de ella, así que las restricciones están **en los rangos del muestreo**, no en un filtro posterior.
- **Niveles de color (dos):** normal (croma total ≤ .32, máximo ≤ .14) y más apagado (total ≤ .20, máximo ≤ .09). Jerarquía: principal el más suave (cubre más área), acento el más vivo.
- **Armonías permitidas:** triádica exacta (±8°), complementaria dividida, complementaria (el terciario es un matiz apagado del principal), análoga (±20°) y monocromática. **Descartada:** tetrádica (dos voces a 90° se «pelean»).
- **Neutros:** siempre tintados con el tono del principal, croma ≤ .04.
- **Voces distinguibles:** ΔE OKLab ≥ .12 entre colores de tonos lejanos (.10 en el nivel apagado, .08 en las familias de tonos cercanos: análoga, monocromática y complementaria, que por naturaleza están más juntas).
- **Sin colores «sucios»:** se rechaza todo color al que se le recorte más del 12 % del croma al entrar en sRGB (así desaparecen los ocres y olivas turbios).
- Mismas reglas de contraste de siempre; en modo oscuro las claridades se invierten.
- Medición (3 000 semillas por caso): las 5 armonías salen en claro y en oscuro; en claro ~19 % de los tonos no produce paleta (sobre todo amarillos) y el botón de sortear prueba otra semilla; croma total mediano .27 (normal) y .18 (apagado), máximo p90 .13 y .09.
- **Perfil «expresivo»** (reglas anteriores) sigue disponible en el selector del sorteador.
- **Calibración:** botones 👍/👎; los votos se guardan solo en el navegador de Zeus (`localStorage`) y el panel resume croma, armonías, estilos y viñetas de lo que gusta frente a lo que no.
- **Explicador:** `taller/armonias.html` muestra las 6 armonías sobre la rueda de color con un deslizador de tono; con 284° reproduce casi exactamente la favorita.
