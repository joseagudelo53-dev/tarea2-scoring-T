import streamlit as st
import pandas as pd
 
st.set_page_config(page_title="Máquina de Puntuación — Letra T", page_icon="🔠", layout="wide")
 
# ─── IMÁGENES ───────────────────────────────────────────────────────────────────
IMAGES = {
    "T clásica":      {"pixels": [1,1,1, 0,1,0, 0,1,0], "es_T": True},
    "T simétrica":    {"pixels": [1,1,1, 0,1,0, 0,1,0], "es_T": True},
    "T ancha":        {"pixels": [1,1,1, 1,1,1, 0,1,0], "es_T": True},
    "Cruz (+)":       {"pixels": [0,1,0, 1,1,1, 0,1,0], "es_T": False},
    "L invertida":    {"pixels": [1,0,0, 1,0,0, 1,1,1], "es_T": False},
    "Diagonal":       {"pixels": [1,0,0, 0,1,0, 0,0,1], "es_T": False},
    "Llena":          {"pixels": [1,1,1, 1,1,1, 1,1,1], "es_T": False},
    "Vacía":          {"pixels": [0,0,0, 0,0,0, 0,0,0], "es_T": False},
    "Esquina":        {"pixels": [1,1,0, 1,0,0, 0,0,0], "es_T": False},
}
 
NOMBRES = list(IMAGES.keys())
 
# ─── SESSION STATE ───────────────────────────────────────────────────────────────
if "pesos" not in st.session_state:
    st.session_state.pesos = [2.0, 2.0, 2.0, -1.0, 3.0, -1.0, -1.0, 3.0, -1.0]
if "threshold" not in st.session_state:
    st.session_state.threshold = 5.0
if "imagen_sel" not in st.session_state:
    st.session_state.imagen_sel = "T clásica"
 
# ─── FUNCIONES ───────────────────────────────────────────────────────────────────
def calcular_puntaje(pixels, pesos):
    total = 0.0
    for i in range(9):
        total += pesos[i] * pixels[i]
    return total
 
def grilla_texto(pixels):
    lines = []
    for r in range(3):
        lines.append("  ".join(str(pixels[r*3+c]) for c in range(3)))
    return "\n".join(lines)
 
def grilla_html(pixels, size=40):
    html = '<div style="display:inline-block;">'
    for r in range(3):
        html += '<div style="display:flex;">'
        for c in range(3):
            v = pixels[r*3+c]
            if v == 1:
                bg = "#f0c040"; border = "#f0c040"
            else:
                bg = "#f5f5f5"; border = "#ddd"
            html += f'<div style="width:{size}px;height:{size}px;background:{bg};border:2px solid {border};border-radius:4px;margin:2px;"></div>'
        html += '</div>'
    html += '</div>'
    return html
 
# ─── TÍTULO ──────────────────────────────────────────────────────────────────────
st.title("🔠 Máquina de Puntuación — Letra T")
st.caption("Ajusta los pesos manualmente · Observa cómo cambia el puntaje · Sin librerías de ML")
st.divider()
 
# ════════════════════════════════════════════════════
# GALERÍA DE IMÁGENES
# ════════════════════════════════════════════════════
st.header("🖼️ Galería de imágenes")
 
ts = [n for n,d in IMAGES.items() if d["es_T"]]
no_ts = [n for n,d in IMAGES.items() if not d["es_T"]]
 
col_t, col_no = st.columns(2)
 
with col_t:
    st.markdown("### ✅ Son una T")
    cols = st.columns(len(ts))
    for i, nombre in enumerate(ts):
        with cols[i]:
            st.markdown(f"**{nombre}**")
            st.markdown(grilla_html(IMAGES[nombre]["pixels"], 30), unsafe_allow_html=True)
            st.code(grilla_texto(IMAGES[nombre]["pixels"]), language=None)
 
with col_no:
    st.markdown("### ❌ No son una T")
    cols2 = st.columns(min(len(no_ts), 3))
    for i, nombre in enumerate(no_ts):
        with cols2[i % 3]:
            st.markdown(f"**{nombre}**")
            st.markdown(grilla_html(IMAGES[nombre]["pixels"], 30), unsafe_allow_html=True)
            st.code(grilla_texto(IMAGES[nombre]["pixels"]), language=None)
 
st.divider()
 
# ════════════════════════════════════════════════════
# PASO 1 — PESOS
# ════════════════════════════════════════════════════
st.header("🎛️ Paso 1: Ajusta los pesos de cada posición")
st.caption("Cada control deslizante controla el peso de un pixel en la cuadrícula 3x3. Muévelos para ver cómo cambia el puntaje.")
 
col_f1, col_f2, col_f3 = st.columns(3)
pesos = st.session_state.pesos
 
with col_f1:
    st.markdown("**Fila 1**")
    pesos[0] = st.slider("Pos (1,1)", -3.0, 3.0, pesos[0], 0.25, key="p0")
    pesos[3] = st.slider("Pos (2,1)", -3.0, 3.0, pesos[3], 0.25, key="p3")
    pesos[6] = st.slider("Pos (3,1)", -3.0, 3.0, pesos[6], 0.25, key="p6")
 
with col_f2:
    st.markdown("**Fila 2**")
    pesos[1] = st.slider("Pos (1,2)", -3.0, 3.0, pesos[1], 0.25, key="p1")
    pesos[4] = st.slider("Pos (2,2)", -3.0, 3.0, pesos[4], 0.25, key="p4")
    pesos[7] = st.slider("Pos (3,2)", -3.0, 3.0, pesos[7], 0.25, key="p7")
 
with col_f3:
    st.markdown("**Fila 3**")
    pesos[2] = st.slider("Pos (1,3)", -3.0, 3.0, pesos[2], 0.25, key="p2")
    pesos[5] = st.slider("Pos (2,3)", -3.0, 3.0, pesos[5], 0.25, key="p5")
    pesos[8] = st.slider("Pos (3,3)", -3.0, 3.0, pesos[8], 0.25, key="p8")
 
st.session_state.pesos = pesos
 
st.markdown("---")
threshold = st.slider(
    "🎯 Umbral (umbral): puntaje mínimo para considerar que ES una T",
    min_value=-9.0, max_value=15.0,
    value=st.session_state.threshold,
    step=0.25, key="thresh"
)
st.session_state.threshold = threshold
 
# Presets
st.markdown("**Presets rápidos:**")
pc1, pc2, pc3 = st.columns(3)
with pc1:
    if st.button("🎯 Pesos óptimos para T", use_container_width=True):
        st.session_state.pesos = [2.0, 2.0, 2.0, -1.0, 3.0, -1.0, -1.0, 3.0, -1.0]
        st.session_state.threshold = 5.0
        st.rerun()
with pc2:
    if st.button("⚖️ Todos iguales = 1", use_container_width=True):
        st.session_state.pesos = [1.0]*9
        st.rerun()
with pc3:
    if st.button("🔄 Resetear todo a 0", use_container_width=True):
        st.session_state.pesos = [0.0]*9
        st.rerun()
 
st.divider()
 
# ════════════════════════════════════════════════════
# PASO 2 — SELECCIÓN DE IMAGEN
# ════════════════════════════════════════════════════
st.header("🖼️ Paso 2: Elige una imagen para evaluar")
 
nombre_sel = st.selectbox("Imagen a evaluar:", NOMBRES,
                           index=NOMBRES.index(st.session_state.imagen_sel))
st.session_state.imagen_sel = nombre_sel
datos_sel = IMAGES[nombre_sel]
pixels_sel = datos_sel["pixels"]
es_T_real = datos_sel["es_T"]
 
c1, c2 = st.columns([1, 3])
with c1:
    st.markdown(f"**{nombre_sel}**")
    st.markdown(grilla_html(pixels_sel, 44), unsafe_allow_html=True)
    etiq = "✅ Es una T" if es_T_real else "❌ No es una T"
    st.markdown(f"Etiqueta real: **{etiq}**")
with c2:
    st.markdown("**Representación matricial:**")
    st.code(grilla_texto(pixels_sel), language=None)
 
st.divider()
 
# ════════════════════════════════════════════════════
# PASO 3 — CÁLCULO
# ════════════════════════════════════════════════════
st.header("🧮 Cálculo paso a paso")
 
puntaje = calcular_puntaje(pixels_sel, pesos)
 
# Fórmula expandida
terminos = " + ".join(f"({pixels_sel[i]}×{pesos[i]:+.1f})" for i in range(9))
st.markdown(f"**Fórmula:**  y = {terminos}")
 
# Tabla detallada
tabla = []
for i in range(9):
    r, c = i//3+1, i%3+1
    contrib = pesos[i] * pixels_sel[i]
    tabla.append({
        "Posición": f"[{r},{c}]",
        "Pixel xᵢ": pixels_sel[i],
        "Peso wᵢ": f"{pesos[i]:+.2f}",
        "Contribución wᵢ·xᵢ": f"{contrib:+.2f}",
    })
 
st.dataframe(pd.DataFrame(tabla), use_container_width=True, hide_index=True)
 
st.markdown(f"**Puntaje total:** `{puntaje:.2f}`")
st.markdown(f"**Umbral:** `{threshold}`")
 
decision = puntaje >= threshold
if decision:
    st.success(f"✅ Puntaje {puntaje:.2f} ≥ {threshold} → La máquina dice: **ES una T**")
else:
    st.error(f"❌ Puntaje {puntaje:.2f} < {threshold} → La máquina dice: **NO es una T**")
 
correcto = decision == es_T_real
if correcto:
    st.info("🎯 Clasificación correcta para esta imagen.")
else:
    st.warning("⚠️ Clasificación incorrecta para esta imagen. Intenta ajustar los pesos.")
 
st.divider()
 
# ════════════════════════════════════════════════════
# MARCADOR GLOBAL
# ════════════════════════════════════════════════════
st.header("🏆 Marcador: ¿Qué tan bien están calibrados tus pesos?")
 
t_correctas = 0
not_correctas = 0
total_correctas = 0
 
ranking = []
for nombre, datos in IMAGES.items():
    p = calcular_puntaje(datos["pixels"], pesos)
    dec = p >= threshold
    ok = dec == datos["es_T"]
    if ok:
        total_correctas += 1
        if datos["es_T"]:
            t_correctas += 1
        else:
            not_correctas += 1
    ranking.append((nombre, datos["es_T"], p, dec, ok))
 
ranking.sort(key=lambda x: x[2], reverse=True)
 
t_total = sum(1 for d in IMAGES.values() if d["es_T"])
not_total = sum(1 for d in IMAGES.values() if not d["es_T"])
 
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("✅ T reconocidas correctamente", f"{t_correctas} / {t_total}")
with m2:
    st.metric("❌ No-T rechazadas correctamente", f"{not_correctas} / {not_total}")
with m3:
    st.metric("🎯 Precisión total", f"{total_correctas} / {len(IMAGES)}")
 
# Barra de progreso
st.progress(total_correctas / len(IMAGES))
 
if total_correctas == len(IMAGES):
    st.success("🏅 ¡Perfecto! Tus pesos clasifican correctamente todas las imágenes.")
elif total_correctas >= len(IMAGES) * 0.7:
    st.info(f"👍 Buen resultado. Puedes mejorar ajustando más los pesos.")
else:
    st.warning("🔧 Sigue ajustando los pesos para mejorar la clasificación.")
 
# Tabla ranking
st.markdown("#### Tabla de resultados")
df_rank = pd.DataFrame([{
    "Imagen": n,
    "Tipo": "T real" if real else "No T",
    "Puntaje": f"{p:+.2f}",
    "Decisión": "Es T" if dec else "No T",
    "Correcto": "✅" if ok else "❌"
} for (n, real, p, dec, ok) in ranking])
 
st.dataframe(df_rank, use_container_width=True, hide_index=True)
 
st.divider()
st.caption("Máquina de Puntuación · y = Σ(wᵢxᵢ) · Sin librerías de ML · Autómatas, Gramáticas y Lenguajes 2025")
