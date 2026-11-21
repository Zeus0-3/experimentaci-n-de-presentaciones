# Experimentación de presentaciones

Un taller para diseñar el estilo de presentaciones hechas con Quarto (formato revealjs).

La idea central: el estilo se **sortea una sola vez** y se mantiene igual en toda la presentación. Misma paleta, misma tipografía, mismo estilo de viñetas. El sorteo es código que corre en el navegador, así que no gasta tokens de IA.

Un **token de diseño** es un valor con nombre (por ejemplo `--principal`, `--acento`, `--fondo`) que toda la presentación reutiliza, en lugar de repetir colores o tamaños sueltos.

> Es un trabajo en curso. Lo que falta está en [Estado y hoja de ruta](#estado-y-hoja-de-ruta).

## Cómo verlo

1. Descarga o clona el repositorio.
2. Abre `taller/index.html` con doble clic.

No hay que instalar nada ni tener internet: las fuentes están incluidas en `taller/fuentes/`. Cada página también se abre sola.

## Recorrido de las páginas

`taller/index.html` es el hub: reúne todas las páginas con un menú lateral.

| Página | Qué hace | Estado |
|---|---|---|
| [`app.html`](taller/app.html) | Sorteador de estilo. Sortea paleta, estilo base y viñeta una sola vez. Incluye 8 láminas de ejemplo. | Vigente |
| [`armonias.html`](taller/armonias.html) | Explica las 6 armonías de color sobre una rueda, con un deslizador de tono. | Vigente |
| [`paletas/galeria.html`](taller/paletas/galeria.html) | Galería de 12 temas con sus razones de contraste. Es salida de la versión anterior del generador. | Vigente (versión anterior, solo complementaria) |
| [`tipografia.html`](taller/tipografia.html) | Familias de títulos probadas, cuerpo, tres fuentes de código y terminal animada. | Vigente |
| [`espacios.html`](taller/espacios.html) | Lámina de 1280×720 con controles de cuerpo, título, interlineado, ancho, justificado y guiones. | Vigente |
| [`codigo.html`](taller/codigo.html) | Terminal, notebook (JupyterLab), editor, diferencias y salida. El botón de copiar copia solo la entrada. | Vigente |
| [`estructura.html`](taller/estructura.html) | Portada, contenido con título-afirmación y pie, y sección de color lleno. | Vigente |
| [`estilos.html`](taller/estilos.html) | Los 20 estilos comparados. Se eligieron 11 para el sorteo. | Explorado y descartado (archivo) |
| [`vinetas.html`](taller/vinetas.html) | Bento, cristal, neumorfismo, mesh y parallax. Cristal y mesh se descartaron por informales. | Explorado y descartado (archivo) |
| [`tarjetas.html`](taller/tarjetas.html) | Cuatro direcciones de tarjetas. Ninguna convenció. | Explorado y descartado (archivo) |

## Decisiones de diseño

Resumen. El registro completo, con fechas y razones, está en [`docs/DISENO.md`](docs/DISENO.md).

- **Paleta en OKLCH.** De un tono salen principal, acento, terciario, fondo, tarjeta, borde y textos, en modo claro y oscuro. OKLCH describe un color con claridad, croma (intensidad) y tono.
- **Perfil «mínimo» por defecto.** Colores apagados, con rangos de croma acotados desde el muestreo. Armonías permitidas: triádica, complementaria dividida, complementaria, análoga y monocromática. La tetrádica se descartó. Los neutros siempre llevan el tono del principal. Existe un perfil «expresivo» en el selector.
- **Contraste WCAG.** Solo se aceptan combinaciones con texto/fondo de al menos 7:1, texto suave y acento de al menos 4.5:1, y principal de al menos 3:1. No hay semáforo rojo/amarillo/verde.
- **Tipografía.** Source Serif 4 para títulos, Source Sans 3 para cuerpo, JetBrains Mono para código. Incrustadas para abrir sin internet.
- **Espacios.** Lámina de 1280×720: cuerpo 29 px, título 56 px, interlineado 1.38, ancho 64ch, párrafos justificados con guiones.
- **Código como en el entorno de uso.** Terminal, notebook, editor y diferencias se ven como donde la persona los usa. El botón de copiar copia solo la entrada: sin prompt, sin `In [1]:`, sin salida, sin números de línea.
- **Estructura de diapositiva.** Títulos que afirman una idea. Pie con número y total, título corto, autoría y sección. Secciones con color lleno.

## Regenerar la galería de paletas

Requiere [uv](https://docs.astral.sh/uv/). El script no tiene dependencias.

```bash
uv run scripts/generar_paleta.py
```

Escribe la galería (`galeria.html`), `paletas.json` y un `.scss` por tema en `taller/paletas/`. Opciones, tomadas del docstring del script:

```bash
uv run scripts/generar_paleta.py --tono 250                  # un tema con ese tono (0-360)
uv run scripts/generar_paleta.py --tono 250 --evolucionar 6  # 6 variantes del mismo tono
uv run scripts/generar_paleta.py --azar 20 --semilla 3       # 20 temas al azar, reproducibles
```

Este script es la **versión anterior** del generador: solo usa armonía complementaria. La lógica vigente (perfil mínimo, varias armonías) está en `taller/app.html`.

## Estructura del repositorio

```
README.md
docs/
  DISENO.md              decisiones de diseño, aspecto por aspecto
  ESTADO.md              qué está hecho, qué falta y plan
scripts/
  generar_paleta.py      generador anterior de paletas (uv)
taller/
  index.html             hub con todas las páginas
  app.html               sorteador de estilo (lógica vigente)
  armonias.html, tipografia.html, espacios.html,
  codigo.html, estructura.html     páginas vigentes
  estilos.html, vinetas.html, tarjetas.html   exploración descartada
  paletas/               galería, paletas.json y temas .scss
  fuentes/               fuentes woff2 incrustadas
    LICENCIAS/           texto de licencia de cada familia
```

## Estado y hoja de ruta

Trabajo en curso. Detalle y plan completo en [`docs/ESTADO.md`](docs/ESTADO.md).

Hecho: paleta, perfil mínimo, sorteador, tipografía, espacios, componentes de código, estructura de diapositiva.

Falta:

- Diagramas y figuras (SVG/Mermaid, capturas).
- Uso al presentar: notas, PDF de apunte, QR, navegación, archivo que abra sin internet.
- Tema SCSS/Quarto real, aplicado a una presentación.
- Plantilla pública con dos perfiles de densidad: `apunte` (mucho texto, se entiende leyendo) y `visual` (poco texto).
- Probar modo oscuro, contraste y tamaño en un proyector real.
- Skill global `presentacion`.

Pendiente de decidir: la licencia y las tarjetas (las cuatro direcciones probadas se rechazaron).

## Licencias

- **Fuentes.** Source Serif 4, Source Sans 3, JetBrains Mono y las demás familias exploradas (Inter, Poppins, Outfit, Plus Jakarta Sans, Fraunces, IBM Plex Sans, IBM Plex Mono, Fira Code) se distribuyen bajo SIL Open Font License 1.1. Los textos están en [`taller/fuentes/LICENCIAS/`](taller/fuentes/LICENCIAS/).
- **Código y contenido propio del repositorio.** Licencia **por definir**. Hasta que se elija una, no se concede ningún permiso de reutilización más allá de lo que permita la ley.
- **Estilo de partida.** El punto de partida fue el estilo de Guillermo Barrios del Valle (repositorio `ecosistema-datos` de AltamarMx). Se busca uno propio. Este README no afirma qué licencia tiene ese estilo; debe revisarse antes de publicar una plantilla.

## Créditos y autoría

Zeus ([Zeus0-3](https://github.com/Zeus0-3)).
