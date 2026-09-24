# Caso de estudio · Escaneo de Horizontes de riesgo geopolítico para México

**Rol:** diseño metodológico, escaneo, evaluación y análisis · **Contexto:** curso de Gestión de Riesgo Geopolítico, Tecnológico de Monterrey (agosto de 2026) · **Métodos:** horizon scanning, PESTLE, MIU, Kuosa, Dator, Futuros Integrales, CLA · **Herramientas:** Google Sheets, Python (pandas, SciPy, matplotlib)

---

## Problema

Los profesionales de riesgo en México (seguros, farmacéutica, agronegocios, gobierno, retail, fuerzas armadas) monitorean el entorno con reportes de noticias y registros de riesgo. Esos instrumentos capturan bien lo que ya se sabe, pero no tienen un proceso explícito para detectar lo que empieza a cambiar ni para interpretarlo desde marcos de prospectiva. El curso necesitaba un caso real y actual que mostrara el escaneo de horizontes de principio a fin, desde la captura de una señal hasta su priorización, y que pudiera usarse como plantilla en los proyectos de los participantes.

## Intervención

1. **Diseño de la plantilla de escaneo en cuatro bloques:** identificación, clasificación categórica (Hines & Bishop), evaluación semicuantitativa con cinco criterios y marcos avanzados de interpretación (Mad Hatter, Kuosa, Futuros Integrales, FODA, Dator, CLA).
2. **Escaneo y verificación de 43 señales** de 38 fuentes (prensa nacional e internacional, think tanks, dependencias de gobierno, revistas académicas), con enlace, fecha y una ficha de cómo cambia el futuro en formato antes/después.
3. **Codificación en 7 drivers** y **priorización con la Matriz Impacto/Incertidumbre**, con los umbrales del curso: tendencia pesada, fuerza crítica y fuerza importante.
4. **Auditoría del propio proceso con datos.** Limpieza reproducible con bitácora de calidad, índices de riesgo y de señal débil, y correlaciones de Spearman entre criterios para detectar sesgos de evaluación.
5. **Materiales para el curso:** plantilla de actividad para los participantes y un repositorio reproducible como portafolio.

## Resultado

- **15 tendencias pesadas, 1 fuerza crítica y 2 fuerzas importantes** identificadas entre 43 señales. **12 de las 15 tendencias pesadas** se concentran en tres drivers domésticos: comercio norteamericano (T-MEC y nearshoring), fragilidad de infraestructura crítica (ciberseguridad, red eléctrica, agua) y certidumbre jurídica.
- **Se detectó un sesgo sistemático contra la novedad.** ρ(novedad, impacto) = −0.56 (p < 0.001): las 10 señales débiles promedian un impacto de 1.9, frente a 3.3 del resto. Sin corrección, el escaneo termina siendo un registro de riesgos conocidos.
- **Recomendación metodológica: priorización en doble vía.** La MIU se usa para gestionar las tendencias pesadas, y un radar de señales débiles con revisión periódica protege la función anticipatoria del escaneo.
- **Se identificó el driver bisagra:** la securitización de la relación México-EE. UU. concentra 2 de las 3 señales que combinan novedad y probabilidad altas. Por ejemplo, la ayuda en seguridad quedó condicionada al Tratado de Aguas de 1944.
- **La plantilla y la base se usaron como material del Módulo 4** y como modelo de la actividad de escaneo de los participantes.

---

**Para qué sirve este caso:** muestra la capacidad de combinar rigor metodológico en prospectiva con análisis de datos reproducible, y de usar los datos para auditar el método, no solo para ilustrarlo.

Repositorio: `github.com/maxsantana-data2strategy/horizon-scanning-geopolitical-risk-mx`
