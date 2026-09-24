"""infographic.py — Infografía de portafolio (JPG) con la plantilla estándar."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path.home() / ".fonts"
W, M = 1600, 90
NAVY, GOLD, TEAL, BLUE = "#1B2847", "#B8893A", "#2E9E8F", "#3A5BA0"
INK, MUTED, LINE, BG = "#1B2847", "#5B6475", "#E4E7EC", "#FFFFFF"


def F(fam, w, size):
    return ImageFont.truetype(str(FONTS / f"{fam}-{w}.ttf"), size)


def mono(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = word
    lines.append(cur)
    return lines


def para(d, xy, text, font, width, fill=INK, lh=1.45):
    x, y = xy
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * lh)
    return y


def section(d, y, num, title):
    d.text((M, y), num, font=F("montserrat", 700, 22), fill=GOLD)
    d.text((M + 52, y - 4), title.upper(), font=F("montserrat", 700, 28), fill=NAVY)
    d.line([(M, y + 46), (W - M, y + 46)], fill=LINE, width=2)
    return y + 72


def code_image(width):
    code = [
        ("# analyze.py  ·  clasificación MIU y diagnóstico de sesgo", "#8A93A6"),
        ("df['impacto_10']       = df['impacto'] * 2", "#E8ECF3"),
        ("df['incertidumbre_10'] = (6 - df['probabilidad']) * 2", "#E8ECF3"),
        ("", None),
        ("def miu_class(i, u):", "#E8ECF3"),
        ("    if i >= 8 and u <= 4: return 'Tendencia pesada'", "#E8ECF3"),
        ("    if i >= 8 and u >= 8: return 'Fuerza crítica'", "#E8ECF3"),
        ("    if i >= 6 and u >= 6: return 'Fuerza importante'", "#E8ECF3"),
        ("    return 'Monitoreo'", "#E8ECF3"),
        ("", None),
        ("rho, p = spearmanr(df['novedad'], df['impacto'])", "#E8ECF3"),
        ("# rho = -0.56, p < 0.001  ->  la evaluación penaliza la novedad", "#D9B26A"),
    ]
    f = mono(19); lh = 31
    h = 40 + lh * len(code) + 30
    img = Image.new("RGB", (width, h), "#141D33")
    d = ImageDraw.Draw(img)
    for i, c in enumerate(["#E06C75", "#E5C07B", "#98C379"]):
        d.ellipse([22 + i * 24, 16, 36 + i * 24, 30], fill=c)
    y = 50
    for txt, col in code:
        if txt:
            d.text((28, y), txt, font=f, fill=col)
        y += lh
    return img


def main():
    H = 4000
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Encabezado
    d.rectangle([0, 0, W, 12], fill=GOLD)
    d.text((M, 70), "MAX SANTANA  ·  ANTICIPACIÓN & ESTRATEGIA", font=F("montserrat", 600, 20), fill=GOLD)
    y = 112
    for ln in ["Escaneo de Horizontes:", "riesgo geopolítico para México 2026"]:
        d.text((M, y), ln, font=F("montserrat", 800, 60), fill=NAVY); y += 76
    y = para(d, (M, y + 6), "43 señales · 7 drivers · 5 criterios de evaluación · 4 marcos de interpretación",
             F("inter", 500, 26), W - 2 * M, fill=MUTED)
    y += 26
    desc = ("Escaneo estructurado de las señales geopolíticas que pueden reconfigurar el entorno de negocio en "
            "México en un horizonte de 1 a 10 años. La base se construyó como material del curso de Gestión de "
            "Riesgo Geopolítico (Tec de Monterrey, 2026) y se analizó con Python para priorizar las señales y "
            "auditar el propio proceso de evaluación.")
    y = para(d, (M, y), desc, F("inter", 400, 24), W - 2 * M, fill=INK, lh=1.55) + 44

    # Pregunta de negocio
    y = section(d, y, "01", "Pregunta de negocio")
    box_h = 150
    d.rounded_rectangle([M, y, W - M, y + box_h], radius=14, fill="#F5F1E8")
    d.rectangle([M, y, M + 8, y + box_h], fill=GOLD)
    para(d, (M + 40, y + 30), "¿Qué factores geopolíticos deben priorizar las organizaciones con operaciones en "
         "México, y hasta qué punto el propio proceso de evaluación sesga lo que alcanzamos a ver?",
         F("montserrat", 600, 29), W - 2 * M - 80, fill=NAVY, lh=1.4)
    y += box_h + 56

    # Metodología
    y = section(d, y, "02", "Metodología")
    steps = [("Escaneo", "43 señales de 38 fuentes, verificadas con enlace y fecha"),
             ("Clasificación", "PESTLE, tipo de hallazgo, horizonte y efecto (Hines & Bishop)"),
             ("Evaluación", "Impacto, probabilidad, plausibilidad, novedad y oportunidad (1-5)"),
             ("Interpretación", "Kuosa, arquetipos de Dator, Futuros Integrales y CLA"),
             ("Priorización", "7 drivers, Matriz Impacto/Incertidumbre e índice de señal débil"),
             ("Auditoría", "Correlaciones de Spearman entre criterios para detectar sesgos")]
    colw = (W - 2 * M - 40) // 2
    sy = y
    for i, (t, s) in enumerate(steps):
        cx = M if i < 3 else M + colw + 40
        cy = sy + (i % 3) * 104
        d.ellipse([cx, cy, cx + 44, cy + 44], fill=NAVY)
        n = str(i + 1); fn = F("montserrat", 700, 20)
        d.text((cx + 22 - d.textlength(n, font=fn) / 2, cy + 9), n, font=fn, fill="white")
        d.text((cx + 62, cy - 2), t, font=F("montserrat", 700, 23), fill=NAVY)
        para(d, (cx + 62, cy + 32), s, F("inter", 400, 19), colw - 70, fill=MUTED, lh=1.35)
    y = sy + 3 * 104 + 20
    ci = code_image(W - 2 * M)
    img.paste(ci, (M, y)); y += ci.height + 14
    d.text((M, y), "Código representativo, no completo. El flujo reproducible (limpieza, análisis y figuras) "
           "está en el repositorio de GitHub.", font=F("inter", 400, 17), fill=MUTED)
    y += 70

    # Hallazgo principal C-F-I
    y = section(d, y, "03", "Hallazgo principal")
    panels = [
        ("CONTEXTO", NAVY, "43 señales evaluadas con cinco criterios y codificadas en 7 drivers. "
         "15 califican como tendencias pesadas en la Matriz Impacto/Incertidumbre."),
        ("HALLAZGO", GOLD, "12 de las 15 tendencias pesadas se concentran en 3 drivers domésticos. "
         "Además, la evaluación penaliza la novedad (rho = -0.56): las señales débiles promedian un "
         "impacto de 1.9, frente a 3.3 del resto."),
        ("IMPLICACIÓN", TEAL, "Priorizar solo por impacto x probabilidad deja un registro de riesgos "
         "conocidos. Hace falta una doble vía: MIU para las tendencias pesadas y un radar de señales "
         "débiles. La securitización México-EE. UU. es el driver que conecta ambas."),
    ]
    pw = (W - 2 * M - 2 * 28) // 3
    fp = F("inter", 500, 22)
    ph = max(len(wrap(d, t2, fp, pw - 60)) for _, _, t2 in panels) * int(22 * 1.5) + 130
    for i, (t, col, txt) in enumerate(panels):
        x0 = M + i * (pw + 28)
        d.rounded_rectangle([x0, y, x0 + pw, y + ph], radius=16, fill=col)
        d.text((x0 + 30, y + 30), t, font=F("montserrat", 800, 24), fill="white")
        d.line([(x0 + 30, y + 70), (x0 + 90, y + 70)], fill="white", width=3)
        para(d, (x0 + 30, y + 92), txt, fp, pw - 60, fill="white", lh=1.5)
    y += ph + 70

    # Visualización
    y = section(d, y, "04", "Visualización")
    import tempfile, pandas as pd, figures
    tmp = Path(tempfile.mkdtemp()); figures.FIG = tmp
    sc = pd.read_csv(ROOT / "data/processed/senales_scored.csv")
    sm = pd.read_csv(ROOT / "data/processed/drivers_summary.csv", index_col=0)
    figures.fig1_miu(sc, figsize=(5.4, 5.6), out="a.png")
    figures.fig2_drivers(sm, figsize=(7.4, 5.6), out="b.png")
    f1 = Image.open(tmp / "a.png").convert("RGB")
    f2 = Image.open(tmp / "b.png").convert("RGB")
    lw = int((W - 2 * M) * 0.415); rw = W - 2 * M - lw - 30
    f1 = f1.resize((lw, int(f1.height * lw / f1.width)), Image.LANCZOS)
    f2 = f2.resize((rw, int(f2.height * rw / f2.width)), Image.LANCZOS)
    d.rounded_rectangle([M - 20, y - 20, W - M + 20, y + max(f1.height, f2.height) + 70],
                        radius=16, outline=LINE, width=2)
    d.text((M, y), "A · Clasificación MIU de las 43 señales", font=F("montserrat", 700, 19), fill=NAVY)
    d.text((M + lw + 30, y), "B · Riesgo y novedad por driver", font=F("montserrat", 700, 19), fill=NAVY)
    img.paste(f1, (M, y + 40)); img.paste(f2, (M + lw + 30, y + 40 + (f1.height - f2.height) // 2))
    y += max(f1.height, f2.height) + 110

    # Pie
    d.line([(M, y), (W - M, y)], fill=LINE, width=2)
    d.text((M, y + 24), "Fuentes: base propia de 43 señales (agosto de 2026) · Análisis: Python (pandas, SciPy, matplotlib)",
           font=F("inter", 400, 17), fill=MUTED)
    d.text((M, y + 52), "github.com/maxsantana-data2strategy  ·  linkedin.com/in/max-santana-06369273",
           font=F("inter", 600, 17), fill=NAVY)
    y += 100
    d.rectangle([0, y - 12, W, y], fill=GOLD)
    img = img.crop((0, 0, W, y))
    out = ROOT / "docs/infografia_horizon_scanning.jpg"
    img.save(out, quality=92, subsampling=0)
    print(out, img.size)


if __name__ == "__main__":
    main()
