"""Genera y ejecuta notebooks/horizon_scanning_analysis.ipynb."""
from pathlib import Path
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]
nb = nbf.v4.new_notebook()
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

nb.cells = [
    md("# Escaneo de Horizontes · Riesgo geopolítico para México (2026)\n"
       "**Autor:** Max Santana · *Anticipación & Estrategia*\n\n"
       "Notebook reproducible del proyecto: limpieza de la base de señales, codificación en drivers, "
       "clasificación en la Matriz Impacto/Incertidumbre (MIU) y diagnóstico de sesgos en la evaluación."),
    md("## 1. Carga y limpieza\nLa base se construyó en Google Sheets como material del Módulo 4 del curso "
       "de Gestión de Riesgo Geopolítico (Tec de Monterrey, agosto 2026). `clean.py` documenta cada corrección."),
    code("import sys; sys.path.insert(0, '../src')\n"
         "import pandas as pd\nimport clean, analyze, figures\n"
         "pd.set_option('display.max_colwidth', 80)\n"
         "df_clean = clean.main()\n"
         "pd.read_csv('../data/processed/data_quality_log.csv').groupby('campo').size()"),
    code("df_clean[['pestle','horizonte','tipo_hallazgo','efecto','ambito']].apply(lambda s: s.value_counts()).fillna(0).astype(int)"),
    md("## 2. Drivers, MIU e índices\n"
       "- **Drivers:** codificación temática analítica (7 drivers).\n"
       "- **MIU:** Impacto₁₀ = impacto × 2; Incertidumbre₁₀ = (6 − probabilidad) × 2; "
       "umbrales del curso (tendencia pesada, fuerza crítica, fuerza importante).\n"
       "- **Índice de señal débil:** promedio de novedad, (6 − probabilidad) y oportunidad temporal."),
    code("df, summ, corr = analyze.main()\nsumm"),
    code("df[df.miu != 'Monitoreo'][['id','driver_code','impacto','probabilidad','novedad','miu','titulo']]"
         ".sort_values(['miu','impacto'], ascending=[True, False])"),
    md("## 3. Diagnóstico del sesgo de evaluación\n"
       "Si los criterios fueran independientes, la novedad no debería predecir el impacto. "
       "La correlación negativa indica que las señales nuevas o distantes reciben sistemáticamente menos peso."),
    code("corr.sort_values('rho')"),
    code("df.groupby('senal_debil')[['impacto','probabilidad','novedad']].mean().round(2)"
         ".rename(index={True:'Señales débiles (novedad 4-5)', False:'Resto'})"),
    code("df[df.senal_debil][['id','driver_code','impacto','probabilidad','novedad','indice_senal_debil','titulo']]"
         ".sort_values('indice_senal_debil', ascending=False)"),
    md("## 4. Visualizaciones"),
    code("figures.main()\nfrom IPython.display import Image, display\n"
         "for f in ['fig1_miu','fig2_drivers','fig3_sesgo_novedad','fig4_marcos']:\n"
         "    display(Image(f'../figures/{f}.png', width=720))"),
    md("## 5. Lectura\n"
       "1. **Concentración doméstica.** 12 de las 15 tendencias pesadas pertenecen a tres drivers internos "
       "(comercio norteamericano, infraestructura crítica, certidumbre jurídica).\n"
       "2. **Sesgo contra la novedad.** ρ(novedad, impacto) = −0.56; las 10 señales débiles promedian impacto 1.9 "
       "frente a 3.3 del resto. Un escaneo priorizado solo por impacto × probabilidad se convierte en un registro "
       "de riesgos conocidos.\n"
       "3. **Driver bisagra.** La securitización de la relación México-EE. UU. (D2) concentra 2 de las 3 señales "
       "que combinan novedad y probabilidad altas (≥ 4): S39 y S40 (la tercera es S42). La agenda de seguridad empieza a condicionar "
       "la política hídrica y la gobernanza subnacional.\n"
       "4. **Profundidad interpretativa.** 22 de 37 señales clasificadas en CLA se quedan en el nivel *Sistemas*; "
       "solo una llega a *Mitos*. Hay espacio para leer las señales en capas más profundas."),
]
out = ROOT / "notebooks/horizon_scanning_analysis.ipynb"
ExecutePreprocessor(timeout=300, kernel_name="python3").preprocess(nb, {"metadata": {"path": str(out.parent)}})
nbf.write(nb, out)
print("ok", out)
