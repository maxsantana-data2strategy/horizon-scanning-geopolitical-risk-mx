"""
analyze.py — Priorización y lectura de la base de señales.

Pasos:
  1. Codificación temática: cada señal se asigna a un driver (codificación analítica
     cualitativa, documentada en DRIVERS).
  2. Matriz Impacto/Incertidumbre (MIU) con los umbrales del curso (escala 1-10):
        Impacto_10       = impacto * 2
        Incertidumbre_10 = (6 - probabilidad) * 2
        Tendencia pesada  : I >= 8 y U <= 4
        Fuerza crítica    : I >= 8 y U >= 8
        Fuerza importante : I >= 6 y U >= 6
        Monitoreo         : resto
  3. Índice de riesgo clásico = impacto x probabilidad (1-25).
  4. Índice de señal débil = promedio(novedad, 6 - probabilidad, oportunidad_temporal).
  5. Diagnóstico del sesgo de evaluación: correlaciones de Spearman entre criterios.

Salida: data/processed/senales_scored.csv, data/processed/drivers_summary.csv,
        data/processed/correlations.csv
"""
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data/processed"

DRIVERS = {
    "D1 Reconfiguración comercial norteamericana":
        ["S01", "S05", "S08", "S09", "S16", "S31", "S32", "S41"],
    "D2 Securitización de la relación México-EE. UU.":
        ["S02", "S10", "S26", "S37", "S39", "S40"],
    "D3 Fragilidad de infraestructura crítica":
        ["S14", "S15", "S17", "S19", "S43", "S44"],
    "D4 Erosión institucional y certidumbre jurídica":
        ["S04", "S23", "S24", "S25"],
    "D5 Ecosistema informacional y cohesión social":
        ["S11", "S12", "S33", "S34", "S42"],
    "D6 Competencia geoeconómica y nuevas fronteras":
        ["S06", "S07", "S13", "S22", "S27", "S28", "S29", "S35", "S36"],
    "D7 Riesgo físico-ambiental y gobernanza global":
        ["S03", "S18", "S20", "S21", "S30"],
}
SCORES = ["impacto", "probabilidad", "plausibilidad", "novedad", "oportunidad_temporal"]


def miu_class(i10: int, u10: int) -> str:
    if i10 >= 8 and u10 <= 4:
        return "Tendencia pesada"
    if i10 >= 8 and u10 >= 8:
        return "Fuerza crítica"
    if i10 >= 6 and u10 >= 6:
        return "Fuerza importante"
    return "Monitoreo"


def main():
    df = pd.read_csv(PROC / "senales_clean.csv")
    id2d = {s: d for d, ids in DRIVERS.items() for s in ids}
    assert set(id2d) == set(df["id"]), set(df["id"]) ^ set(id2d)
    df["driver"] = df["id"].map(id2d)
    df["driver_code"] = df["driver"].str[:2]

    df["impacto_10"] = df["impacto"] * 2
    df["incertidumbre_10"] = (6 - df["probabilidad"]) * 2
    df["miu"] = [miu_class(i, u) for i, u in zip(df["impacto_10"], df["incertidumbre_10"])]
    df["riesgo_ixp"] = df["impacto"] * df["probabilidad"]
    df["indice_senal_debil"] = ((df["novedad"] + (6 - df["probabilidad"])
                                 + df["oportunidad_temporal"]) / 3).round(2)
    df["senal_debil"] = (df["novedad"] >= 4)
    df.to_csv(PROC / "senales_scored.csv", index=False)

    # Resumen por driver
    g = df.groupby("driver")
    summ = pd.DataFrame({
        "n": g.size(),
        "impacto_medio": g["impacto"].mean().round(2),
        "probabilidad_media": g["probabilidad"].mean().round(2),
        "novedad_media": g["novedad"].mean().round(2),
        "riesgo_ixp_medio": g["riesgo_ixp"].mean().round(1),
        "pct_mexico": g["ambito"].apply(lambda s: (s != "Global").mean() * 100).round(0),
        "tendencias_pesadas": g["miu"].apply(lambda s: (s == "Tendencia pesada").sum()),
        "senales_debiles": g["senal_debil"].sum(),
    }).sort_values("riesgo_ixp_medio", ascending=False)
    summ.to_csv(PROC / "drivers_summary.csv")

    # Correlaciones de Spearman
    rows = []
    for a in SCORES:
        for b in SCORES:
            if a < b:
                r, p = spearmanr(df[a], df[b])
                rows.append((a, b, round(r, 2), round(p, 4)))
    corr = pd.DataFrame(rows, columns=["criterio_a", "criterio_b", "rho", "p"])
    corr.to_csv(PROC / "correlations.csv", index=False)

    print(summ.to_string())
    print("\nMIU:\n", df["miu"].value_counts().to_string())
    print("\nCorrelaciones:\n", corr.to_string(index=False))
    return df, summ, corr


if __name__ == "__main__":
    main()
