"""
figures.py — Visualizaciones del proyecto (PNG, 200 dpi).

  fig1_miu.png            Matriz Impacto/Incertidumbre (umbrales del curso)
  fig2_drivers.png        Riesgo medio vs. novedad media por driver (paneles espejo)
  fig3_sesgo_novedad.png  Impacto medio según nivel de novedad
  fig4_marcos.png         Distribución de los marcos de interpretación (Bloque 4)
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = Path(__file__).resolve().parents[1]
PROC, FIG = ROOT / "data/processed", ROOT / "figures"
FIG.mkdir(exist_ok=True)

for f in Path.home().joinpath(".fonts").glob("*.ttf"):
    fm.fontManager.addfont(str(f))

NAVY, GOLD = "#1B2847", "#B8893A"
INK, MUTED, GRID = "#1B2847", "#5B6475", "#E4E7EC"
C = {"Tendencia pesada": "#3A5BA0", "Fuerza crítica": "#B5485D",
     "Fuerza importante": "#C08A2E", "Monitoreo": "#C9CED6"}
TEAL = "#2E9E8F"
BLUE = "#3A5BA0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 10,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": GRID, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 12, "figure.facecolor": "white",
})
TITLE = dict(fontfamily="Montserrat", fontweight="bold", color=NAVY)


def fig1_miu(df, figsize=(7.2, 6), out="fig1_miu.png"):
    fig, ax = plt.subplots(figsize=figsize)
    cells = df.groupby(["incertidumbre_10", "impacto_10", "miu"]).agg(
        n=("id", "size"), ids=("id", lambda s: ", ".join(s))).reset_index()
    ax.axhspan(8, 10.8, xmin=0, xmax=(4 - 1) / 9.8, color=C["Tendencia pesada"], alpha=.07, lw=0)
    ax.axhspan(8, 10.8, xmin=(8 - 1) / 9.8, xmax=1, color=C["Fuerza crítica"], alpha=.07, lw=0)
    for v in (4, 8):
        ax.axvline(v, color=GRID, lw=1, zorder=0)
    ax.axhline(8, color=GRID, lw=1, zorder=0)
    for _, r in cells.iterrows():
        ax.scatter(r.incertidumbre_10, r.impacto_10, s=160 + r.n * 170, color=C[r.miu],
                   edgecolor="white", linewidth=2, zorder=3)
        ax.text(r.incertidumbre_10, r.impacto_10, str(r.n), ha="center", va="center",
                color="white" if r.miu != "Monitoreo" else INK, fontsize=9, fontweight="bold", zorder=4)
    ax.set_xlim(1, 10.8); ax.set_ylim(1, 10.8)
    ax.set_xlabel("Incertidumbre (1-10)  ·  (6 - probabilidad) x 2")
    ax.set_ylabel("Impacto (1-10)  ·  impacto x 2")
    ax.text(1.3, 10.4, "TENDENCIAS PESADAS", color=C["Tendencia pesada"], fontsize=8, fontweight="bold")
    ax.text(8.2, 10.4, "FUERZAS CRÍTICAS", color=C["Fuerza crítica"], fontsize=8, fontweight="bold")
    ax.set_title("Matriz Impacto/Incertidumbre · 43 señales", loc="left", **TITLE)
    counts = df["miu"].value_counts()
    handles = [plt.Line2D([], [], marker="o", ls="", ms=9, color=C[k],
                          label=f"{k} ({counts.get(k, 0)})") for k in C]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8.5)
    ax.text(10.7, 1.2, "Número en burbuja = señales en esa celda", ha="right", fontsize=7.5, color=MUTED)
    fig.tight_layout(); fig.savefig(FIG / out, dpi=200); plt.close(fig)


def fig2_drivers(summ, figsize=(9, 4.6), out="fig2_drivers.png"):
    s = summ.sort_values("riesgo_ixp_medio")
    labels = [d.replace(" y ", " y\n", 1) if len(d) > 38 else d for d in s.index]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=figsize, sharey=True,
                                 gridspec_kw={"width_ratios": [1.5, 1]})
    y = range(len(s))
    a1.barh(y, s["riesgo_ixp_medio"], color=BLUE, height=.62)
    a2.barh(y, s["novedad_media"], color=TEAL, height=.62)
    for yi, v, n in zip(y, s["riesgo_ixp_medio"], s["n"]):
        a1.text(v + .3, yi, f"{v:.1f}", va="center", fontsize=8.5, color=INK)
    for yi, v in zip(y, s["novedad_media"]):
        a2.text(v + .06, yi, f"{v:.1f}", va="center", fontsize=8.5, color=INK)
    a1.set_yticks(list(y)); a1.set_yticklabels([f"{l}  (n={n})" for l, n in zip(labels, s["n"])], fontsize=8.5, color=INK)
    a1.set_xlim(0, 25); a2.set_xlim(0, 5)
    a1.set_title("Riesgo medio (impacto x prob., 1-25)", loc="left", fontsize=9.5, color=BLUE, fontweight="bold")
    a2.set_title("Novedad media (1-5)", loc="left", fontsize=9.5, color=TEAL, fontweight="bold")
    for a in (a1, a2):
        a.tick_params(axis="y", length=0); a.grid(axis="x", color=GRID, lw=.8); a.set_axisbelow(True)
    fig.suptitle("Drivers: el riesgo alto y la novedad alta rara vez coinciden", x=0.02, ha="left",
                 fontsize=12.5, **TITLE)
    fig.tight_layout(); fig.savefig(FIG / out, dpi=200); plt.close(fig)


def fig3_sesgo(df):
    g = df.groupby("novedad").agg(imp=("impacto", "mean"), n=("id", "size")).reindex(range(1, 6))
    fig, ax = plt.subplots(figsize=(6.4, 4))
    colors = [BLUE if k < 4 else TEAL for k in g.index]
    ax.bar(g.index, g["imp"], color=colors, width=.6)
    for k, r in g.iterrows():
        ax.text(k, r.imp + .08, f"{r.imp:.1f}\nn={int(r.n)}", ha="center", va="bottom", fontsize=8.5)
    ax.set_ylim(0, 5.2); ax.set_xticks(range(1, 6))
    ax.set_xlabel("Novedad asignada (1-5)"); ax.set_ylabel("Impacto medio asignado (1-5)")
    ax.grid(axis="y", color=GRID, lw=.8); ax.set_axisbelow(True)
    ax.set_title("A mayor novedad, menor impacto asignado  (rho de Spearman = -0.56)", loc="left", fontsize=11, **TITLE)
    ax.text(4.5, 4.7, "Señales débiles\n(novedad 4-5)", ha="center", color=TEAL, fontsize=8.5, fontweight="bold")
    fig.tight_layout(); fig.savefig(FIG / "fig3_sesgo_novedad.png", dpi=200); plt.close(fig)


def fig4_marcos(df):
    cols = {"arquetipo_dator": "Arquetipo de Dator", "nivel_kuosa": "Nivel de Kuosa",
            "futuros_integrales": "Futuros integrales", "cla": "CLA (Inayatullah)"}
    fig, axes = plt.subplots(2, 2, figsize=(9, 6))
    for ax, (c, t) in zip(axes.flat, cols.items()):
        vc = df[c].value_counts()
        vc = pd.concat([vc.reindex(["Sin clasificar"]).dropna(),
                        vc.drop("Sin clasificar", errors="ignore").sort_values()]).astype(int)
        colors = ["#D5D9E0" if k == "Sin clasificar" else BLUE for k in vc.index]
        ax.barh(range(len(vc)), vc.values, color=colors, height=.6)
        ax.set_yticks(range(len(vc))); ax.set_yticklabels(vc.index, fontsize=8)
        for i, v in enumerate(vc.values):
            ax.text(v + .3, i, str(v), va="center", fontsize=8)
        ax.set_title(t, loc="left", fontsize=10, color=NAVY)
        ax.tick_params(axis="y", length=0); ax.set_xlim(0, vc.max() + 4); ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
    fig.suptitle("Bloque 4 · Marcos avanzados de interpretación (n = 43)", x=.02, ha="left", fontsize=12.5, **TITLE)
    fig.tight_layout(); fig.savefig(FIG / "fig4_marcos.png", dpi=200); plt.close(fig)


def main():
    df = pd.read_csv(PROC / "senales_scored.csv")
    summ = pd.read_csv(PROC / "drivers_summary.csv", index_col=0)
    fig1_miu(df); fig2_drivers(summ); fig3_sesgo(df); fig4_marcos(df)
    print("Figuras guardadas en", FIG)


if __name__ == "__main__":
    main()
