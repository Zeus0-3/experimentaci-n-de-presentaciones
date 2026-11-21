# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Generador de paletas para presentaciones: de UN tono salen principal, acento (complementario), fondo y grises,
en modo claro y oscuro. Sortea claridad y croma y SOLO acepta lo que cumple las reglas de contraste.
Sin dependencias, sin red, sin tokens.

Uso (con uv):
  uv run scripts/generar_paleta.py                      # 4 temas semilla + 8 al azar (semilla 7)
  uv run scripts/generar_paleta.py --tono 250           # un tema con ese tono (0-360, OKLCH)
  uv run scripts/generar_paleta.py --tono 250 --evolucionar 6   # 6 variantes del mismo tono (otra claridad/croma)
  uv run scripts/generar_paleta.py --azar 20 --semilla 3        # 20 temas al azar, reproducibles
Salida: taller/paletas/galeria.html (para elegir con los ojos), paletas.json y un .scss por tema.

Fundamentos: espacio OKLab/OKLCH, Ottosson (2020) https://bottosson.github.io/posts/oklab/ ;
razón de contraste WCAG 2.2 https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio
"""
import argparse
import json
import math
import random
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "taller" / "paletas"
SEMILLAS = {"solar": 75, "edificios": 45, "datos-ia": 275, "ambiente": 160}   # puntos de partida, no reglas
NOMBRES_TONO = [(29, "rojo"), (55, "naranja"), (85, "ambar"), (105, "amarillo"), (127, "lima"), (150, "verde"),
                (180, "turquesa"), (210, "cian"), (250, "azul"), (275, "indigo"), (300, "violeta"),
                (330, "magenta"), (355, "rosa"), (360, "rojo")]

# ───── color: OKLCH <-> sRGB (fórmulas de Ottosson) ─────
def _a_srgb(c):
    c = min(1.0, max(0.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklch_a_lineal(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_, m_, s_ = L + 0.3963377774 * a + 0.2158037573 * b, L - 0.1055613458 * a - 0.0638541728 * b, L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def en_gama(rgb):
    return all(-0.0005 <= c <= 1.0005 for c in rgb)


def color(L, C, h):
    """Devuelve (hex, rgb_lineal) recortando el croma si el color no cabe en sRGB."""
    lo, hi = 0.0, C
    rgb = oklch_a_lineal(L, hi, h)
    if not en_gama(rgb):
        for _ in range(24):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if en_gama(oklch_a_lineal(L, mid, h)) else (lo, mid)
        rgb = oklch_a_lineal(L, lo, h)
    hexa = "#" + "".join(f"{round(_a_srgb(c) * 255):02x}" for c in rgb)
    return hexa, tuple(min(1.0, max(0.0, c)) for c in rgb)


def luminancia(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def nombre_tono(h):
    return min(NOMBRES_TONO, key=lambda t: min(abs(t[0] - h % 360), 360 - abs(t[0] - h % 360)))[1]


# ───── reglas de aceptación (cada una explica de dónde sale) ─────
REGLAS = {   # nombre: (mínimo, de dónde sale)
    "texto/fondo": (7.0, "WCAG AAA para proyección (mínimo AA = 4.5)"),
    "suave/fondo": (4.5, "WCAG 1.4.3 texto normal"),
    "principal/fondo": (3.0, "WCAG 1.4.3 texto grande (títulos ≥ 24 px): 3:1"),
    "acento/fondo": (4.5, "WCAG 1.4.3 si el acento se usa como texto"),
    "principal/tarjeta": (3.0, "WCAG 1.4.3 texto grande sobre la superficie de las tarjetas"),
    "acento/tarjeta": (4.5, "WCAG 1.4.3 sobre la superficie de las tarjetas"),
    "borde/fondo": (1.15, "separar tarjeta y fondo sin ruido (heurística)"),
}
SEPARACION_GRIS = 0.08   # heurística (sin fuente): acento y principal difieren en claridad OKLab (L) para no volverse el mismo gris al imprimir


def armar(h, modo, rng, intentos=800):
    """Sortea claridad y croma y devuelve el primer tema que cumple todas las reglas, o None."""
    claro = modo == "claro"
    ha = (h + 180) % 360
    for n in range(intentos):
        j = lambda lo, hi: rng.uniform(lo, hi)
        Lp = j(.50, .68) if claro else j(.66, .84)
        La = j(.46, .60) if claro else j(.72, .86)
        t = {
            "fondo": color(j(.975, .993) if claro else j(.15, .20), j(.006, .02), h),
            "tarjeta": color(j(.94, .965) if claro else j(.21, .26), j(.015, .04), h),
            "borde": color(j(.86, .91) if claro else j(.30, .36), j(.02, .05), h),
            "texto": color(j(.18, .27) if claro else j(.93, .97), j(.01, .04), h),
            "suave": color(j(.40, .50) if claro else j(.74, .82), j(.02, .05), h),
            "principal": color(Lp, j(.12, .22), h),
            "acento": color(La, j(.12, .24), ha),
        }
        r = {"texto/fondo": contraste(t["texto"][1], t["fondo"][1]), "suave/fondo": contraste(t["suave"][1], t["fondo"][1]),
             "principal/fondo": contraste(t["principal"][1], t["fondo"][1]), "acento/fondo": contraste(t["acento"][1], t["fondo"][1]),
             "principal/tarjeta": contraste(t["principal"][1], t["tarjeta"][1]), "acento/tarjeta": contraste(t["acento"][1], t["tarjeta"][1]),
             "borde/fondo": contraste(t["borde"][1], t["fondo"][1])}
        sep = abs(La - Lp)
        if all(r[k] >= REGLAS[k][0] for k in REGLAS) and sep >= SEPARACION_GRIS:
            return {"colores": {k: v[0] for k, v in t.items()}, "razones": {k: round(v, 2) for k, v in r.items()},
                    "separacion_gris": round(sep, 3), "intentos": n + 1}
    return None


def tema(h, rng, nombre=None):
    claro, oscuro = armar(h, "claro", rng), armar(h, "oscuro", rng)
    if not (claro and oscuro):
        return None
    return {"nombre": nombre or f"{nombre_tono(h)}-{int(h)}", "tono": round(h, 1), "acento_tono": round((h + 180) % 360, 1),
            "claro": claro, "oscuro": oscuro}


# ───── salidas ─────
def scss(t):
    def bloque(modo, d):
        return "\n".join(f"  --{k}: {v};" for k, v in d["colores"].items()) if modo else ""
    def sass(modo):
        return "\n".join(f"${k}-{modo}: {v};" for k, v in t[modo]["colores"].items())
    return (f"// Tema «{t['nombre']}» · tono {t['tono']} · acento {t['acento_tono']} (complementario)\n// Generado por generar_paleta.py; no editar a mano.\n"
            f"{sass('claro')}\n{sass('oscuro')}\n\n:root {{\n{bloque(1, t['claro'])}\n}}\n"
            f":root.oscuro {{\n{bloque(1, t['oscuro'])}\n}}\n")


def galeria(temas):
    def mini(modo, d):
        c = d["colores"]
        estilo = "".join(f"--{k}:{v};" for k, v in c.items())
        filas = "".join(f"<tr><td>{k}</td><td class='{'ok' if v >= REGLAS[k][0] else 'mal'}'>{v}</td><td>{REGLAS[k][0]}</td></tr>" for k, v in d["razones"].items())
        chips = "".join(f"<i style='background:{c[k]}' title='{k} {c[k]}'></i>" for k in c)
        return (f"<div class='mini' style='{estilo}'><b>{modo}</b><h3>Una idea que se entiende</h3>"
                f"<p>Texto de apunte con <a>un acento</a> y <em>énfasis suave</em>.</p><div class='tarj'>Tarjeta con borde</div>"
                f"<div class='chips'>{chips}</div></div><table><tr><th>par</th><th>razón</th><th>mín.</th></tr>{filas}</table>")
    tarjetas = "".join(f"<section><h2>{t['nombre']} <small>tono {t['tono']}° · acento {t['acento_tono']}°</small></h2>"
                       f"<div class='par'><div>{mini('claro', t['claro'])}</div><div>{mini('oscuro', t['oscuro'])}</div></div></section>" for t in temas)
    return f"""<!doctype html><meta charset="utf-8"><title>Galería de paletas</title>
<style>body{{font:15px system-ui;margin:2rem;background:#fff;color:#222}}section{{margin:0 0 2.5rem}}h2 small{{font-weight:400;color:#666;font-size:.6em}}
.par{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}.mini{{background:var(--fondo);color:var(--texto);padding:1rem 1.2rem;border-radius:10px;border:1px solid #ccc}}
.mini h3{{color:var(--principal);margin:.3rem 0}}.mini a{{color:var(--acento);font-weight:600;text-decoration:underline}}.mini em{{color:var(--suave)}}
.tarj{{background:var(--tarjeta);border:1px solid var(--borde);border-radius:8px;padding:.5rem .8rem;margin:.5rem 0}}.chips i{{display:inline-block;width:1.6rem;height:1.6rem;border-radius:50%;margin-right:.3rem;border:1px solid #8884}}
table{{border-collapse:collapse;font-size:12px;margin-top:.4rem}}td,th{{border:1px solid #ddd;padding:2px 8px}}.ok{{color:#176b3a}}.mal{{color:#b00;font-weight:700}}</style>
<h1>Galería de paletas</h1><p>{len(temas)} temas. Cada color pasó las reglas de contraste (razones en las tablas). Elige con los ojos; pide «evolucionar» el tono que te guste.</p>{tarjetas}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tono", type=float, help="tono OKLCH 0-360 de un tema concreto")
    ap.add_argument("--evolucionar", type=int, default=0, help="N variantes del mismo --tono (sortea claridad y croma)")
    ap.add_argument("--azar", type=int, default=8, help="cuántos temas al azar además de los semilla")
    ap.add_argument("--semilla", type=int, default=7, help="semilla del azar (misma semilla = mismos temas)")
    a = ap.parse_args()
    rng = random.Random(a.semilla)
    if a.tono is not None:
        n = max(1, a.evolucionar)
        pedidos = [(a.tono, f"{nombre_tono(a.tono)}-{int(a.tono)}-v{i + 1}") for i in range(n)]
    else:
        pedidos = [(h, n) for n, h in SEMILLAS.items()] + [(rng.uniform(0, 360), None) for _ in range(a.azar)]
    temas, fallidos = [], 0
    for h, nombre in pedidos:
        t = tema(h, rng, nombre)
        temas.append(t) if t else None
        fallidos += 0 if t else 1
    SALIDA.mkdir(exist_ok=True)
    for f in SALIDA.glob("*.scss"):
        f.unlink()
    for t in temas:
        (SALIDA / f"{t['nombre']}.scss").write_text(scss(t), encoding="utf-8")
    (SALIDA / "paletas.json").write_text(json.dumps(temas, indent=2, ensure_ascii=False), encoding="utf-8")
    (SALIDA / "galeria.html").write_text(galeria(temas), encoding="utf-8")
    print(f"{len(temas)} temas aceptados, {fallidos} descartados (ninguna combinación cumplió las reglas).")
    print(f"Galería: {SALIDA / 'galeria.html'}")


main()
