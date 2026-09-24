"""
clean.py — Limpieza y estandarización de la base de señales de Escaneo de Horizontes.

Entrada : data/raw/senales_raw.csv  (exportación directa del Google Sheet del curso)
Salida  : data/processed/senales_clean.csv
          data/processed/data_quality_log.csv

Decisiones documentadas (ver README > Calidad de datos):
  1. Nombres de columna a snake_case sin acentos.
  2. S39 tenía un desplazamiento de celdas en Bloque 1-2 (descripción → "cómo cambia",
     "cómo cambia" → stakeholder). Se reubican los textos y se marca el stakeholder
     como pendiente.
  3. Fechas de publicación capturadas como año 1905 (error de formato de Sheets al
     escribir solo día/mes) y fechas con solo año se dejan como NaT y se registran.
  4. Valores "?" o vacíos en marcos de Bloque 4 se tratan como "Sin clasificar".
  5. Las puntuaciones 0-5 se convierten a entero.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/senales_raw.csv"
OUT = ROOT / "data/processed"

RENAME = {
    "ID_Señal": "id",
    "Categoría_PESTLE": "pestle",
    "Título preciso de la señal": "titulo",
    "Autor": "autor",
    "Fuente / Medio": "fuente",
    "Enlace_URL": "url",
    "Fecha_Publicación": "fecha_publicacion",
    "Fecha_Captura": "fecha_captura",
    "Palabras_Clave": "palabras_clave",
    "Alcance_Geográfico": "alcance",
    "Horizonte_Temporal": "horizonte",
    "Tipo_Hallazgo": "tipo_hallazgo",
    "Descripción_Breve": "descripcion",
    "Cómo_Cambia_el_Futuro": "como_cambia",
    "Stakeholder_Afectado": "stakeholders",
    "Efecto_General": "efecto",
    "Impacto (0-5)": "impacto",
    "Probabilidad (0-5)": "probabilidad",
    "Plausibilidad (0-5)": "plausibilidad",
    "Novedad (0-5)": "novedad",
    "Oportunidad_Temporal_Años (0-5)": "oportunidad_temporal",
    "Sombrero_Mad_Hatter": "sombrero_mad_hatter",
    "Nivel_Kuosa": "nivel_kuosa",
    "Cuadrante_Futuros_Integrales": "futuros_integrales",
    "Cuadrante_FODA": "foda",
    "Arquetipo_Dator": "arquetipo_dator",
    "Causal_Layared_Analysis": "cla",
}
SCORES = ["impacto", "probabilidad", "plausibilidad", "novedad", "oportunidad_temporal"]
FRAMEWORKS = ["sombrero_mad_hatter", "nivel_kuosa", "futuros_integrales",
              "foda", "arquetipo_dator", "cla"]


def main() -> pd.DataFrame:
    df = pd.read_csv(RAW, dtype=str).fillna("")
    df.columns = [c.replace("\\", "") for c in df.columns]
    df = df.rename(columns=RENAME)
    for c in df.columns:
        df[c] = df[c].str.replace("\\", "", regex=False).str.strip()

    log = []

    # 2. Corrección del desplazamiento de celdas en S39
    m = df["id"] == "S39"
    if m.any() and df.loc[m, "stakeholders"].iloc[0].startswith("Antes:"):
        df.loc[m, "descripcion"] = df.loc[m, "como_cambia"]
        df.loc[m, "como_cambia"] = df.loc[m, "stakeholders"]
        df.loc[m, "stakeholders"] = ("Gobiernos de México y EE. UU., CILA, "
                                     "productores agrícolas de la frontera norte")
        log.append(("S39", "descripcion/como_cambia/stakeholders",
                    "Celdas desplazadas; reubicadas. Stakeholders reconstruidos a partir de la descripción (validar)."))

    # 3. Fechas
    for col in ["fecha_publicacion", "fecha_captura"]:
        parsed = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")
        bad = parsed.isna() | (parsed.dt.year < 2000)
        for i in df.index[bad]:
            log.append((df.at[i, "id"], col, f"Fecha no válida '{df.at[i, col]}' → NaT"))
        df[col] = parsed.where(~bad)

    # 4. Marcos avanzados
    for c in FRAMEWORKS:
        empty = df[c].isin(["", "?"])
        for i in df.index[empty]:
            log.append((df.at[i, "id"], c, f"Valor '{df.at[i, c]}' → 'Sin clasificar'"))
        df.loc[empty, c] = "Sin clasificar"

    # 5. Puntuaciones
    for c in SCORES:
        df[c] = pd.to_numeric(df[c], errors="raise").astype(int)

    # Horizonte ordinal
    df["horizonte_ord"] = df["horizonte"].map(
        {"Corto (1-3 años)": 1, "Mediano (3-6 años)": 2, "Largo (6-10 años)": 3})
    df["ambito"] = df["alcance"].apply(lambda s: "México" if s.startswith("México") and "Global" not in s and "mundo" not in s
        else ("México y el mundo" if s.startswith("México") else "Global"))

    # IDs faltantes en la secuencia
    ids = set(df["id"])
    for n in range(1, 45):
        if f"S{n:02d}" not in ids:
            log.append((f"S{n:02d}", "id", "ID ausente en la base (depurada o no registrada)"))

    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "senales_clean.csv", index=False)
    pd.DataFrame(log, columns=["id", "campo", "nota"]).to_csv(OUT / "data_quality_log.csv", index=False)
    print(f"{len(df)} señales limpias · {len(log)} incidencias registradas")
    return df


if __name__ == "__main__":
    main()
