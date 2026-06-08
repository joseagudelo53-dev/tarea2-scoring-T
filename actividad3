import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(page_title="Clasificador Automático de la Letra T", page_icon="🔠", layout="wide")

# ─── IMÁGENES ───────────────────────────────────────────────────────────────────
IMAGES = {
    # T reales
    "T normal":    {"pixels": [1,1,1, 0,1,0, 0,1,0], "es_T": True},
    "T centrada":  {"pixels": [1,1,1, 0,1,0, 0,1,0], "es_T": True},
    "T variante":  {"pixels": [1,1,1, 0,1,0, 0,1,0], "es_T": True},
    # No T
    "Cruz (+)":    {"pixels": [0,1,0, 1,1,1, 0,1,0], "es_T": False},
    "L invertida": {"pixels": [1,0,0, 1,0,0, 1,1,1], "es_T": False},
    "Diagonal":    {"pixels": [1,0,0, 0,1,0, 0,0,1], "es_T": False},
    "Cuadrado":    {"pixels": [1,1,1, 1,0,1, 1,1,1], "es_T": False},
    "Fila central":{"pixels": [0,0,0, 1,1,1, 0,0,0], "es_T": False},
    "T invertida": {"pixels": [0,1,0, 0,1,0, 1,1,1], "es_T": False},
}

# ─── SESSION STATE ───────────────────────────────────────────────────────────────
if "pesos" not in st.session_state:
    st.session_state.pesos = [2.0, 2.0, 2.0, -3.0, 3.0, -3.0, -3.0, 3.0, -3.0]
if "threshold" not in st.session_state:
    st.session_state.threshold = 5.0

# ─── FUNCIONES ───────────────────────────────────────────────────────────────────
def calcular_puntaje(pixels, pesos):
    return sum(pesos[i] * pixels[i] for i in range(9))

def clasificar(puntaje, threshold):
    return puntaje > threshold

def grilla_html(pixels, pesos=None, size=60):
    html = '<div style="display:inline-block; border-radius:8px; overflow:hidden;">'
    for r in range(3):
        html += '<div style="display:flex;">'
        for c in range(3):
            idx = r*3+c
            v = pixels[idx]
            bg = "#3B82F6" if v == 1 else "#E5E7EB"
            txt_color = "white" if v == 1 else "#9CA3AF"
            html += f'<div style="width:{size}px;height:{size}px;background:{bg};display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:1.1rem;color:{txt_color};border:1px solid #D1D5DB;">{v}</div>'
        html += '</div>'
    html += '</div>'
    return html

def pesos_texto(pesos):
    lines = []
    for r in range(3):
        lines.append("  ".join(f"{pesos[r*3+c]:+.1f}" for c in range(3)))
    return "\n".join(lines)

# ─── TÍTULO ──────────────────────────────────────────────────────────────────────
st.title("🔠 Clasificador Automático de la Letra T")
st.subheader("Actividad 3 — Autómatas, Gramáticas y Lenguaje")
st.divider()

st.markdown("""
**¿Qué hace esta aplicación?**

En la actividad anterior construimos una máquina que calculaba un puntaje para cada imagen. Ahora esa máquina da un paso más: **decide sola** si la imagen es una T o no, comparando el puntaje con un umbral.

**¿Cómo funciona?**
- Cada imagen es una cuadrícula de 3x3 píxeles (1 = activo, 0 = apagado)
- La máquina multiplica cada píxel por su peso y suma todo → obtiene un **puntaje**
- Compara ese puntaje con el **umbral** de decisión
- Si el puntaje supera el umbral → dice automáticamente ✅ **ES una T**
- Si no lo supera → dice automáticamente ❌ **NO es una T**
""")
st.divider()

# ════════════════════════════════════════════════════
# PASO 1 — PESOS
# ════════════════════════════════════════════════════
st.header("🎛️ Paso 1: Ajusta los pesos de cada posición")
st.caption("Igual que en la actividad anterior, cada slider controla el peso de un píxel en la cuadrícula 3x3.")

# Presets
pc1, pc2, pc3 = st.columns(3)
with pc1:
    if st.button("🎯 Pesos óptimos", use_container_width=True):
        st.session_state.pesos = [2.0, 2.0, 2.0, -3.0, 3.0, -3.0, -3.0, 3.0, -3.0]
        st.session_state.threshold = 5.0
        st.rerun()
with pc2:
    if st.button("⚖️ Todos = 1", use_container_width=True):
        st.session_state.pesos = [1.0]*9
        st.rerun()
with pc3:
    if st.button("🔄 Resetear", use_container_width=True):
        st.session_state.pesos = [0.0]*9
        st.rerun()

pesos = st.session_state.pesos
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("**Fila 1 (barra superior de la T)**")
    pesos[0] = st.slider("Pos (1,1)", -5.0, 5.0, pesos[0], 0.5, key="p0")
    pesos[3] = st.slider("Pos (2,1)", -5.0, 5.0, pesos[3], 0.5, key="p3")
    pesos[6] = st.slider("Pos (3,1)", -5.0, 5.0, pesos[6], 0.5, key="p6")

with col_f2:
    st.markdown("**Fila 2 (columna central)**")
    pesos[1] = st.slider("Pos (1,2)", -5.0, 5.0, pesos[1], 0.5, key="p1")
    pesos[4] = st.slider("Pos (2,2)", -5.0, 5.0, pesos[4], 0.5, key="p4")
    pesos[7] = st.slider("Pos (3,2)", -5.0, 5.0, pesos[7], 0.5, key="p7")

with col_f3:
    st.markdown("**Fila 3 (barra superior de la T)**")
    pesos[2] = st.slider("Pos (1,3)", -5.0, 5.0, pesos[2], 0.5, key="p2")
    pesos[5] = st.slider("Pos (2,3)", -5.0, 5.0, pesos[5], 0.5, key="p5")
    pesos[8] = st.slider("Pos (3,3)", -5.0, 5.0, pesos[8], 0.5, key="p8")

st.session_state.pesos = pesos
st.divider()

# ════════════════════════════════════════════════════
# PASO 2 — UMBRAL
# ════════════════════════════════════════════════════
st.header("🎯 Paso 2: Define el umbral de decisión")
st.markdown("""
El umbral es el **límite** que usa la máquina para decidir.
- Si el puntaje de la imagen es **mayor** al umbral → la máquina dice **ES una T**
- Si el puntaje es **menor o igual** al umbral → la máquina dice **NO es una T**
""")

col_slider, col_num = st.columns([4, 1])
with col_slider:
    threshold = st.slider("Umbral de decisión", -10.0, 20.0,
                          st.session_state.threshold, 0.5, key="thresh",
                          label_visibility="visible")
with col_num:
    threshold = st.number_input("Valor exacto", value=threshold, step=0.5, key="thresh_num")

st.session_state.threshold = threshold
st.info(f"📌 Regla actual: Si puntaje > **{threshold}** → ✅ ES una T | Si puntaje ≤ **{threshold}** → ❌ NO es una T")
st.divider()

# ════════════════════════════════════════════════════
# PASO 3 — CLASIFICACIÓN AUTOMÁTICA
# ════════════════════════════════════════════════════
st.header("🤖 Paso 3: Clasificación automática")
st.markdown("Aquí es donde la máquina **decide sola**. No necesitas que tú le digas si es una T o no. Ella calcula el puntaje de cada imagen y lo compara con el umbral automáticamente.")

ts   = {n: d for n, d in IMAGES.items() if d["es_T"]}
no_ts = {n: d for n, d in IMAGES.items() if not d["es_T"]}

# T reales
st.subheader("✅ Imágenes que SÍ son T")
st.caption("La máquina debe reconocer estas como T (puntaje mayor al umbral).")
cols_t = st.columns(len(ts))
for i, (nombre, datos) in enumerate(ts.items()):
    p = calcular_puntaje(datos["pixels"], pesos)
    dec = clasificar(p, threshold)
    ok = dec == True
    color_title = "green" if ok else "red"
    dec_text = "✅ ES una T" if dec else "❌ NO es una T"
    with cols_t[i]:
        st.markdown(f'<div style="background:white;border-radius:10px;padding:10px;text-align:center;border:2px solid {"#22c55e" if ok else "#ef4444"};">'
                    f'<div style="color:{color_title};font-weight:bold;font-size:0.8rem;">{nombre}</div>'
                    f'<div style="color:{color_title};font-size:0.75rem;">Puntaje: {p} | {dec_text}</div>'
                    f'{grilla_html(datos["pixels"], size=45)}'
                    f'</div>', unsafe_allow_html=True)

st.markdown("")

# No T
st.subheader("❌ Imágenes que NO son T")
st.caption("La máquina debe rechazar estas como NO-T (puntaje menor o igual al umbral).")
cols_not = st.columns(len(no_ts))
for i, (nombre, datos) in enumerate(no_ts.items()):
    p = calcular_puntaje(datos["pixels"], pesos)
    dec = clasificar(p, threshold)
    ok = dec == False
    color_title = "green" if ok else "red"
    dec_text = "✅ NO es una T" if not dec else "❌ ES una T"
    with cols_not[i]:
        st.markdown(f'<div style="background:white;border-radius:10px;padding:10px;text-align:center;border:2px solid {"#22c55e" if ok else "#ef4444"};">'
                    f'<div style="color:{color_title};font-weight:bold;font-size:0.8rem;">{nombre}</div>'
                    f'<div style="color:{color_title};font-size:0.75rem;">Puntaje: {p} | {dec_text}</div>'
                    f'{grilla_html(datos["pixels"], size=45)}'
                    f'</div>', unsafe_allow_html=True)

st.divider()

# ════════════════════════════════════════════════════
# PASO 4 — EVALUACIÓN DE ERRORES
# ════════════════════════════════════════════════════
st.header("📊 Paso 4: Evaluación de errores")
st.markdown("Aquí puedes ver qué tan bien está funcionando tu configuración. El objetivo es llegar a **9/9** con **100% de precisión**.")

t_ok, not_ok, total_ok = 0, 0, 0
falsos_pos, falsos_neg = [], []

for nombre, datos in IMAGES.items():
    p = calcular_puntaje(datos["pixels"], pesos)
    dec = clasificar(p, threshold)
    ok = dec == datos["es_T"]
    if ok:
        total_ok += 1
        if datos["es_T"]: t_ok += 1
        else: not_ok += 1
    else:
        if dec and not datos["es_T"]: falsos_pos.append(nombre)
        elif not dec and datos["es_T"]: falsos_neg.append(nombre)

t_total   = sum(1 for d in IMAGES.values() if d["es_T"])
not_total = sum(1 for d in IMAGES.values() if not d["es_T"])
precision = total_ok / len(IMAGES) * 100

m1, m2, m3, m4 = st.columns(4)
m1.metric("✅ T reconocidas",       f"{t_ok} / {t_total}")
m2.metric("❌ NO-T rechazadas",     f"{not_ok} / {not_total}")
m3.metric("🎯 Total correctos",     f"{total_ok} / {len(IMAGES)}")
m4.metric("📈 Precisión",           f"{precision:.0f}%")

st.progress(total_ok / len(IMAGES))

# Errores
st.markdown("#### 🔍 ¿Qué errores cometió la máquina?")
st.markdown("""
- **Falso Positivo:** La máquina dijo ES una T, pero NO lo era
- **Falso Negativo:** La máquina dijo NO es una T, pero SÍ lo era
""")
col_fp, col_fn = st.columns(2)
with col_fp:
    st.markdown("⚠️ **Falsos Positivos**")
    if falsos_pos:
        for n in falsos_pos:
            st.error(f"❌ {n}: la máquina dijo ES T, pero NO lo es")
    else:
        st.success("✅ ¡Ninguno! La máquina rechazó correctamente todas las NO-T")
with col_fn:
    st.markdown("⚠️ **Falsos Negativos**")
    if falsos_neg:
        for n in falsos_neg:
            st.error(f"❌ {n}: la máquina dijo NO es T, pero SÍ lo es")
    else:
        st.success("✅ ¡Ninguno! La máquina reconoció correctamente todas las T")

if total_ok == len(IMAGES):
    st.success("🏆 ¡Configuración perfecta! La máquina clasifica correctamente todas las imágenes.")

st.divider()

# ════════════════════════════════════════════════════
# PASO 5 — CÁLCULO DETALLADO
# ════════════════════════════════════════════════════
st.header("🔢 Paso 5: Ve el cálculo detallado paso a paso")
st.caption("Selecciona cualquier imagen y verás exactamente cómo la máquina tomó su decisión.")

nombre_sel = st.selectbox("Selecciona una imagen:", list(IMAGES.keys()))
datos_sel  = IMAGES[nombre_sel]
pixels_sel = datos_sel["pixels"]
p_sel      = calcular_puntaje(pixels_sel, pesos)
dec_sel    = clasificar(p_sel, threshold)

col_img, col_calc = st.columns(2)

with col_img:
    st.subheader("📐 Imagen seleccionada")
    st.code("\n".join("  ".join(str(pixels_sel[r*3+c]) for c in range(3)) for r in range(3)), language=None)
    st.subheader("⚖️ Pesos actuales")
    st.code(pesos_texto(pesos), language=None)

with col_calc:
    st.subheader("🧮 ¿Cómo decidió la máquina?")
    terminos = " + ".join(f"({pixels_sel[i]}x{pesos[i]:+.1f})" for i in range(9))
    st.markdown(f"**1. Fórmula:** y = {terminos}")
    st.markdown(f"**2. Puntaje calculado:** `{p_sel:.2f}`")
    st.markdown(f"**3. Umbral definido:** `{threshold}`")
    st.markdown(f"**4. Comparación:** `{p_sel:.2f} {'>' if dec_sel else '≤'} {threshold}`")
    st.markdown("**5. Decisión automática:**")
    if dec_sel:
        st.success(f"✅ Como {p_sel:.2f} > {threshold} → La máquina dice: **ES una T**")
    else:
        st.error(f"❌ Como {p_sel:.2f} ≤ {threshold} → La máquina dice: **NO es una T**")

    # Tabla detallada
    tabla = [{"Pos": f"[{i//3+1},{i%3+1}]", "xᵢ": pixels_sel[i],
              "wᵢ": f"{pesos[i]:+.1f}", "wᵢ·xᵢ": f"{pesos[i]*pixels_sel[i]:+.2f}"}
             for i in range(9)]
    st.dataframe(pd.DataFrame(tabla), use_container_width=True, hide_index=True)

st.divider()

# ════════════════════════════════════════════════════
# GRÁFICA
# ════════════════════════════════════════════════════
st.header("📈 Gráfica: Puntajes vs Umbral de Decisión")
st.markdown("Esta gráfica muestra el puntaje de cada imagen. La línea naranja es el umbral. Las barras **por encima** de la línea son clasificadas como T, las que están **por debajo** son clasificadas como NO-T.")

nombres = list(IMAGES.keys())
puntajes = [calcular_puntaje(IMAGES[n]["pixels"], pesos) for n in nombres]
colores  = ["#3B82F6" if IMAGES[n]["es_T"] else "#EF4444" for n in nombres]

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(nombres, puntajes, color=colores, edgecolor="white", linewidth=0.5)
ax.axhline(y=threshold, color="orange", linestyle="--", linewidth=2, label=f"Umbral = {threshold}")
for bar, val in zip(bars, puntajes):
    ax.text(bar.get_x() + bar.get_width()/2, val + (0.3 if val >= 0 else -0.7),
            str(round(val, 1)), ha="center", va="bottom" if val >= 0 else "top", fontsize=9, fontweight="bold")
ax.set_ylabel("Puntaje")
ax.set_title("Puntajes de cada imagen vs Umbral de Decisión")
ax.set_xticklabels(nombres, rotation=20, ha="right")
patch_t   = mpatches.Patch(color="#3B82F6", label="Imágenes T")
patch_not = mpatches.Patch(color="#EF4444", label="Imágenes NO-T")
ax.legend(handles=[ax.get_lines()[0], patch_t, patch_not])
ax.axhline(y=0, color="black", linewidth=0.5)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()
st.caption("Clasificador Automático · y = Σ(wᵢxᵢ) · Sin librerías de ML · Autómatas, Gramáticas y Lenguaje 2025")
