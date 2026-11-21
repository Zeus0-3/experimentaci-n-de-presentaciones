# Estado del proyecto

Última actualización: 2026-11-20. Objetivo: un estilo propio de presentaciones (Quarto revealjs), decidido aspecto por aspecto, que termine como plantilla pública y como skill global `presentacion`. El estilo base de partida fue el de Guillermo Barrios del Valle; se quiere uno propio, y la licencia de lo heredado debe revisarse antes de publicar.

## Qué hay hecho
- **Paleta:** sistema propio en OKLCH. El tono genera principal, acento, terciario, fondo, tarjeta, borde y textos, en modo claro y oscuro. Solo se aceptan combinaciones con contraste suficiente (texto/fondo ≥ 7:1; texto suave y acento ≥ 4.5:1; principal ≥ 3:1). Sin semáforo rojo/amarillo/verde.
- **Perfil «mínimo»** (por defecto): colores apagados, armonías triádica, complementaria dividida, complementaria, análoga y monocromática; neutros tintados. Perfil «expresivo» disponible.
- **Sorteador de estilo** (`app.html`): el estilo se sortea una sola vez y se mantiene; se pueden fijar paleta, estilo base y viñeta; enlace reproducible; botones de me gusta / no me gusta guardados solo en el navegador.
- **Explicador de armonías** (`armonias.html`) con rueda de color.
- **Tipografía:** Source Serif 4 (títulos), Source Sans 3 (cuerpo), JetBrains Mono (código), todas OFL-1.1, incrustadas. Lámina 1280×720: cuerpo 29 px, título 56 px, interlineado 1.38, ancho 64ch, justificado con guiones.
- **Componentes de código** (`codigo.html`): terminal, notebook Jupyter, archivo en editor, antes/después, salida o registro. El botón de copiar copia solo la entrada.
- **Estructura de diapositiva:** títulos que afirman una idea; pie con número y total, título corto, autor e institución y sección; secciones con color lleno; portada editorial.
- **Tarjetas:** se probaron cuatro direcciones (sin caja con línea y número, tarjeta limpia con sombra, franja lateral, bloque lleno) y **ninguna convenció** («muy de IA»); se descartaron y se buscó un estilo más minimalista.
- **Estilos explorados:** se compararon 20 estilos (`estilos.html`) y se eligieron 11 para el sorteo: Suizo, Editorial, Tufte, Cuaderno de laboratorio, Plano técnico, Periodismo de datos, Bento plano, Risografía, Neobrutalismo, Bauhaus y Memphis. El cristal (glassmorphism) y el gradient mesh se **descartaron** por informales (`vinetas.html`); las viñetas vigentes son plana, línea fina, barra lateral y marcador cuadrado.
- **Página unificada:** `taller/index.html` reúne todas las apps con navegación; cada página sigue funcionando por separado y sin internet.
- **Registro de decisiones:** [`DISENO.md`](DISENO.md).
- Archivos de apoyo: `scripts/generar_paleta.py` (versión anterior del generador, solo complementaria; la lógica vigente está en `taller/app.html`), galería y temas `.scss` en `taller/paletas/`, y las fuentes woff2 con sus licencias en `taller/fuentes/`.

## Qué falta
1. Aspecto 5: diagramas y figuras (SVG/Mermaid, árbol del repositorio, grafo, capturas).
2. Aspecto 6: uso al presentar (notas, PDF de apunte, QR, navegación, archivo autocontenido que abra sin internet).
3. Contenido y mensaje: integrar los comentarios de Guillermo Barrios del Valle (aún sin recibir) y reescribir la historia a nivel apunte.
4. Tema SCSS/Quarto real, aplicado a una presentación.
5. Plantilla pública con dos perfiles de densidad: `apunte` (mucho texto, se entiende leyendo) y `visual` (poco texto).
6. Pasar la lógica de `app.html` a Python.
7. Probar el modo oscuro y los botones de votación con clics reales; probar contraste y tamaño en proyector real.
8. Skill global `presentacion`.

## Plan y roadmap (en orden, una fase a la vez con aprobación)
0. Diagnóstico del tema actual (qué es de Guillermo y qué es genérico de revealjs).
1. Contenido y mensaje.
2. Taller de diseño: paleta (hecho), tipografía (hecho), estructura (hecho), componentes de código y tarjetas (muestras hechas), diagramas (pendiente), uso al presentar (pendiente).
3. Aplicar el tema y validar: `quarto render` sin avisos, recorrido, PDF, proyector, sin internet, revisión de datos sensibles.
4. Este repositorio como plantilla: `_quarto.yml`, tema propio, plantilla con un ejemplo de cada componente, `DISENO.md`, `README.md`, `LICENSE`, scripts de render. Es la fuente única del tema; la presentación privada lo consume por copia con script. Contenido de ejemplo neutro.
5. Skill global `presentacion` (con explicación previa de qué es una skill), probada con peticiones reales.
6. A futuro: web app para generar diseños a partir del sorteador.

## Decisiones pendientes de Zeus
- Licencia (código frente a contenido; qué heredar del estilo de Guillermo y con qué crédito).
- Licencia de Okabe-Ito y Paul Tol antes de usarlas en gráficas.
- Tarjetas: las cuatro direcciones probadas se rechazaron; falta proponer otras, más minimalistas, y decidir.
- Qué aspecto sigue (5, 6 o la fase 1) y cuándo pasa los comentarios de Guillermo.
- Qué mejoras del proyecto entran a la presentación.
- Nombres definitivos de los repositorios.
