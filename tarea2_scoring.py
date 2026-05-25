import streamlit as st
import math

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Máquina de Puntuación — Letra T",
    page_icon="🔠",
    layout="wide",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

  html, body, [class*="css"] { font-family: 'Syne', sans-serif; background-color: #0d0d0d; color: #f0ede6; }
  .stApp { background: #0d0d0d; }
  h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

  [data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem !important;
    color: #f0c040 !important;
  }
  [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    color: #888 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  [data-testid="metric-container"] {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 10px 14px;
  }

  .stButton > button {
    font-family: 'Space Mono', monospace;
    background: #1a1a1a;
    color: #f0c040;
    border: 1.5px solid #f0c040;
    border-radius: 8px;
    font-weight: 700;
    letter-spacing: 1px;
    transition: all 0.2s;
  }
  .stButton > button:hover { background: #f0c040; color: #0d0d0d; }

  .card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 14px;
  }
  .section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 6px;
  }
  .pixel-on  { display:inline-block; width:32px; height:32px; background:#f0c040; border-radius:4px; margin:2px; }
  .pixel-off { display:inline-block; width:32px; height:32px; background:#1a1a1a; border:1px solid #333; border-radius:4px; margin:2px; }

  .score-pos { color: #5fdf6f; font-family:'Space Mono',monospace; font-size:1.4rem; font-weight:700; }
  .score-neg { color: #df5f5f; font-family:'Space Mono',monospace; font-size:1.4rem; font-weight:700; }
  .score-neu { color: #f0c040; font-family:'Space Mono',monospace; font-size:1.4rem; font-weight:700; }

  hr { border-color: #222; }
</style>
""", unsafe_allow_html=True)


# ─── IMÁGENES PREDEFINIDAS ───────────────────────────────────────────────────────
# Grilla 3x3, fila por fila (9 pixeles)
IMAGES = {
    # ── T reales ──
    "T clásica": {
        "pixels": [1,1,1, 0,1,0, 0,1,0],
        "es_T": True,
        "desc": "Fila superior completa, palo central"
    },
    "T simétrica": {
        "pixels": [1,1,1, 0,1,0, 0,1,0],
        "es_T": True,
        "desc": "Igual que T clásica"
    },
    "T estrecha": {
        "pixels": [0,1,1, 0,1,0, 0,1,0],  # barra superior solo derecha
        "es_T": True,
        "desc": "Barra superior desplazada a la derecha"
    },
    "T ancha": {
        "pixels": [1,1,1, 1,1,1, 0,1,0],
        "es_T": True,
        "desc": "T con segunda fila también activa"
    },
    # ── NO son T ──
    "Cruz (+)": {
        "pixels": [0,1,0, 1,1,1, 0,1,0],
        "es_T": False,
        "desc": "Cruz centrada — NO es T"
    },
    "L invertida": {
        "pixels": [1,0,0, 1,0,0, 1,1,1],
        "es_T": False,
        "desc": "Forma de L — NO es T"
    },
    "Diagonal": {
        "pixels": [1,0,0, 0,1,0, 0,0,1],
        "es_T": False,
        "desc": "Diagonal — NO es T"
    },
    "Llena": {
        "pixels": [1,1,1, 1,1,1, 1,1,1],
        "es_T": False,
        "desc": "Todos los pixeles activos — NO es T"
    },
    "Vacía": {
        "pixels": [0,0,0, 0,0,0, 0,0,0],
        "es_T": False,
        "desc": "Sin pixeles — NO es T"
    },
}

IMAGEN_NOMBRES = list(IMAGES.keys())

# ─── SESSION STATE ───────────────────────────────────────────────────────────────
if "pesos" not in st.session_state:
    # Pesos iniciales: favorecen la fila superior y el palo central
    # pos 0,1,2 = fila 1 | pos 3,4,5 = fila 2 | pos 6,7,8 = fila 3
    st.session_state.pesos = [1.0, 2.0, 1.0,  -1.0, 2.0, -1.0,  -1.0, 2.0, -1.0]

if "threshold" not in st.session_state:
    st.session_state.threshold = 2.0

if "imagen_sel" not in st.session_state:
    st.session_state.imagen_sel = "T clásica"

if "custom_pixels" not in st.session_state:
    st.session_state.custom_pixels = [0]*9

if "modo" not in st.session_state:
    st.session_state.modo = "predefinida"


# ─── FUNCIÓN DE PUNTUACIÓN ───────────────────────────────────────────────────────
def calcular_puntaje(pixels, pesos):
    """y = Σ(wi * xi) — sin librerías externas."""
    total = 0.0
    pasos = []
    for i in range(9):
        contribucion = pesos[i] * pixels[i]
        total += contribucion
        pasos.append((i, pixels[i], pesos[i], contribucion))
    return total, pasos


def pixel_html(val, size=36):
    if val == 1:
        return f'<div style="display:inline-block;width:{size}px;height:{size}px;background:#f0c040;border-radius:5px;margin:2px;"></div>'
    else:
        return f'<div style="display:inline-block;width:{size}px;height:{size}px;background:#1a1a1a;border:1px solid #333;border-radius:5px;margin:2px;"></div>'


def grilla_html(pixels, size=36):
    html = '<div style="line-height:0;">'
    for row in range(3):
        html += '<div>'
        for col in range(3):
            html += pixel_html(pixels[row*3+col], size)
        html += '</div>'
    html += '</div>'
    return html


def peso_html(pesos):
    """Muestra los pesos en grilla 3x3."""
    html = '<div style="line-height:0;">'
    for row in range(3):
        html += '<div>'
        for col in range(3):
            p = pesos[row*3+col]
            color = "#5fdf6f" if p > 0 else "#df5f5f" if p < 0 else "#888"
            html += f'<div style="display:inline-block;width:36px;height:36px;background:#1a1a1a;border:1px solid {color};border-radius:5px;margin:2px;text-align:center;line-height:36px;font-family:\'Space Mono\',monospace;font-size:9px;color:{color};">{p:+.1f}</div>'
        html += '</div>'
    html += '</div>'
    return html


# ─── TÍTULO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 28px 0 6px 0;">
  <div class="section-title">Autómatas, Gramáticas y Lenguajes · Tarea 2</div>
  <h1 style="font-size:2.6rem; margin:4px 0; color:#f0ede6;">
    🔠 Máquina de <span style="color:#f0c040;">Puntuación</span>
  </h1>
  <p style="color:#666; font-family:'Space Mono',monospace; font-size:0.78rem; margin-top:6px;">
    Ajusta los pesos · Prueba imágenes binarias · ¿Cuánto se parece a una T?
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── LAYOUT PRINCIPAL ────────────────────────────────────────────────────────────
col_izq, col_centro, col_der = st.columns([1.2, 1.3, 1.5], gap="large")


# ══════════════════════════════════════════
# COLUMNA IZQUIERDA — Imagen de entrada
# ══════════════════════════════════════════
with col_izq:
    st.markdown("### 🖼️ Imagen de entrada")
    st.markdown('<div class="section-title">Elige o dibuja una imagen 3×3</div>', unsafe_allow_html=True)

    modo = st.radio("Modo", ["Imagen predefinida", "Dibujar mi propia imagen"],
                    horizontal=True, label_visibility="collapsed")
    st.session_state.modo = modo

    if modo == "Imagen predefinida":
        nombre = st.selectbox("Selecciona una imagen", IMAGEN_NOMBRES,
                               index=IMAGEN_NOMBRES.index(st.session_state.imagen_sel))
        st.session_state.imagen_sel = nombre
        datos = IMAGES[nombre]
        pixels_activos = datos["pixels"]
        es_T = datos["es_T"]
        etiqueta = "✅ Es una T" if es_T else "❌ No es una T"
        etiqueta_color = "#5fdf6f" if es_T else "#df5f5f"

        st.markdown(f"""
        <div class="card" style="text-align:center; margin-top:12px;">
          <div class="section-title">Vista previa</div>
          <div style="margin: 12px 0;">{grilla_html(pixels_activos, 44)}</div>
          <div style="font-family:'Space Mono',monospace; font-size:0.75rem; color:#aaa; margin-top:6px;">{datos['desc']}</div>
          <div style="margin-top:10px; font-family:'Space Mono',monospace; font-size:0.85rem; color:{etiqueta_color}; font-weight:700;">{etiqueta}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown('<div class="section-title" style="margin-top:10px;">Haz clic en los pixeles para activarlos/desactivarlos</div>', unsafe_allow_html=True)
        cols_grid = [st.columns(3) for _ in range(3)]
        for row in range(3):
            for col in range(3):
                idx = row * 3 + col
                val = st.session_state.custom_pixels[idx]
                label = "🟡" if val == 1 else "⬛"
                with cols_grid[row][col]:
                    if st.button(label, key=f"px_{idx}", use_container_width=True):
                        st.session_state.custom_pixels[idx] = 1 - val
                        st.rerun()

        pixels_activos = st.session_state.custom_pixels
        es_T = None
        etiqueta = "— Sin etiqueta"

        if st.button("🗑️ Limpiar grilla", use_container_width=True):
            st.session_state.custom_pixels = [0]*9
            st.rerun()

        st.markdown(f"""
        <div class="card" style="text-align:center; margin-top:10px;">
          <div class="section-title">Vista previa</div>
          <div style="margin: 12px 0;">{grilla_html(pixels_activos, 44)}</div>
          <div style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#888;">Imagen personalizada</div>
        </div>
        """, unsafe_allow_html=True)

    # Representación matricial
    st.markdown("#### Representación matricial")
    mat_str = ""
    for row in range(3):
        mat_str += "  ".join(str(pixels_activos[row*3+col]) for col in range(3)) + "\n"
    st.code(mat_str, language=None)


# ══════════════════════════════════════════
# COLUMNA CENTRO — Pesos
# ══════════════════════════════════════════
with col_centro:
    st.markdown("### 🎛️ Ajuste de pesos")
    st.markdown('<div class="section-title">Cada posición de la grilla tiene su propio peso</div>', unsafe_allow_html=True)

    # Presets de pesos
    st.markdown("**Presets rápidos:**")
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        if st.button("🎯 Óptimo T", use_container_width=True):
            st.session_state.pesos = [1.0, 2.0, 1.0, -1.0, 2.0, -1.0, -1.0, 2.0, -1.0]
            st.rerun()
    with pc2:
        if st.button("⚖️ Todos = 1", use_container_width=True):
            st.session_state.pesos = [1.0]*9
            st.rerun()
    with pc3:
        if st.button("🔄 Resetear", use_container_width=True):
            st.session_state.pesos = [0.0]*9
            st.rerun()

    st.markdown("---")

    # Sliders de pesos en grilla 3x3
    POSICIONES = [
        "Fila 1, Col 1", "Fila 1, Col 2", "Fila 1, Col 3",
        "Fila 2, Col 1", "Fila 2, Col 2", "Fila 2, Col 3",
        "Fila 3, Col 1", "Fila 3, Col 2", "Fila 3, Col 3",
    ]

    for row in range(3):
        cols_w = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            with cols_w[col]:
                nuevo = st.slider(
                    f"w[{row+1},{col+1}]",
                    min_value=-3.0, max_value=3.0,
                    value=st.session_state.pesos[idx],
                    step=0.25,
                    key=f"peso_{idx}",
                )
                st.session_state.pesos[idx] = nuevo

    st.markdown("---")
    st.markdown("**Threshold (umbral de decisión):**")
    st.session_state.threshold = st.slider(
        "Umbral θ — si puntaje > θ → Es T",
        min_value=-9.0, max_value=9.0,
        value=st.session_state.threshold,
        step=0.25,
        key="threshold_slider"
    )

    # Vista de pesos en grilla
    st.markdown("#### Mapa de pesos actual")
    st.markdown(f"""
    <div class="card" style="text-align:center;">
      <div class="section-title">Verde = positivo · Rojo = negativo</div>
      <div style="margin:10px 0;">{peso_html(st.session_state.pesos)}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# COLUMNA DERECHA — Resultados
# ══════════════════════════════════════════
with col_der:
    st.markdown("### 📊 Resultados")

    pesos = st.session_state.pesos
    threshold = st.session_state.threshold
    puntaje, pasos = calcular_puntaje(pixels_activos, pesos)
    decision = puntaje > threshold
    decision_str = "✅ Es una T" if decision else "❌ No es una T"
    decision_color = "#5fdf6f" if decision else "#df5f5f"

    # Métricas principales
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Puntaje y", f"{puntaje:+.2f}")
    with m2:
        st.metric("Umbral θ", f"{threshold:+.2f}")
    with m3:
        st.metric("Pixeles ON", sum(pixels_activos))

    st.markdown(f"""
    <div class="card" style="text-align:center; margin-top:8px;">
      <div class="section-title">Decisión final</div>
      <div style="font-size:1.8rem; font-weight:800; color:{decision_color}; margin:8px 0; font-family:'Space Mono',monospace;">
        {decision_str}
      </div>
      <div style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#888;">
        {puntaje:+.2f} {'>' if decision else '≤'} {threshold:+.2f}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Verificación si hay etiqueta conocida
    if es_T is not None:
        correcto = decision == es_T
        st.markdown(f"""
        <div class="card" style="text-align:center; background:{'#152a15' if correcto else '#2a1515'}; border-color:{'#5fdf6f' if correcto else '#df5f5f'};">
          <div style="font-family:'Space Mono',monospace; font-size:0.85rem; color:{'#5fdf6f' if correcto else '#df5f5f'}; font-weight:700;">
            {'✅ CLASIFICACIÓN CORRECTA' if correcto else '❌ CLASIFICACIÓN INCORRECTA'}
          </div>
          <div style="font-size:0.75rem; color:#888; margin-top:4px; font-family:\'Space Mono\',monospace;">
            Etiqueta real: {'Es T' if es_T else 'No es T'} · Predicción: {'Es T' if decision else 'No es T'}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Desglose paso a paso
    st.markdown("#### 🔢 Cálculo paso a paso")
    st.markdown('<div class="section-title">y = Σ(wi · xi) — contribución de cada pixel</div>', unsafe_allow_html=True)

    # Tabla de pasos
    filas_html = ""
    for (i, xi, wi, contrib) in pasos:
        row_n = i // 3 + 1
        col_n = i % 3 + 1
        px_html = pixel_html(xi, 18)
        contrib_color = "#5fdf6f" if contrib > 0 else "#df5f5f" if contrib < 0 else "#888"
        activo = "ON" if xi == 1 else "off"
        activo_color = "#f0c040" if xi == 1 else "#555"
        filas_html += f"""
        <div style="display:grid; grid-template-columns:0.8fr 0.5fr 0.5fr 0.6fr 0.7fr;
                    gap:4px; font-family:'Space Mono',monospace; font-size:0.72rem;
                    color:#ccc; padding:5px 4px; border-bottom:1px solid #1e1e1e; align-items:center;">
          <div>pos [{row_n},{col_n}]</div>
          <div style="color:{activo_color};">{activo}</div>
          <div>x={xi}</div>
          <div>w={wi:+.2f}</div>
          <div style="color:{contrib_color}; font-weight:700;">{contrib:+.2f}</div>
        </div>"""

    st.markdown(f"""
    <div class="card" style="padding:10px 14px;">
      <div style="display:grid; grid-template-columns:0.8fr 0.5fr 0.5fr 0.6fr 0.7fr;
                  gap:4px; font-family:'Space Mono',monospace; font-size:0.65rem;
                  color:#555; text-transform:uppercase; letter-spacing:1px; padding:0 4px 6px 4px;">
        <div>Posición</div><div>Estado</div><div>xᵢ</div><div>wᵢ</div><div>wᵢ·xᵢ</div>
      </div>
      {filas_html}
      <div style="font-family:'Space Mono',monospace; font-size:0.85rem; color:#f0c040;
                  font-weight:700; text-align:right; padding:8px 4px 2px 4px; border-top:1px solid #333; margin-top:6px;">
        TOTAL = {puntaje:+.2f}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Evaluación de todas las imágenes predefinidas
    st.markdown("#### 🏆 Ranking de todas las imágenes")
    ranking = []
    for nombre_img, datos_img in IMAGES.items():
        p, _ = calcular_puntaje(datos_img["pixels"], pesos)
        d = p > threshold
        correcto = d == datos_img["es_T"]
        ranking.append((nombre_img, datos_img["es_T"], p, d, correcto))

    ranking.sort(key=lambda x: x[2], reverse=True)

    total_correctos = sum(1 for r in ranking if r[4])

    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#aaa; margin-bottom:8px;">
      Clasificadas correctamente: <span style="color:#f0c040; font-weight:700;">{total_correctos}/{len(ranking)}</span>
    </div>
    """, unsafe_allow_html=True)

    for (nom, real_T, punt, dec, ok) in ranking:
        ok_sym = "✅" if ok else "❌"
        real_sym = "T" if real_T else "~T"
        punt_color = "#5fdf6f" if punt > threshold else "#df5f5f"
        activo_style = "border-left: 3px solid #f0c040;" if nom == st.session_state.imagen_sel else ""
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:5px 10px; margin-bottom:3px; background:#141414;
                    border-radius:8px; border:1px solid #1e1e1e; {activo_style}">
          <span style="font-family:'Space Mono',monospace; font-size:0.72rem; color:#ccc;">{ok_sym} {nom}</span>
          <span style="font-family:'Space Mono',monospace; font-size:0.7rem; color:#666;">[{real_sym}]</span>
          <span style="font-family:'Space Mono',monospace; font-size:0.75rem; color:{punt_color}; font-weight:700;">{punt:+.2f}</span>
        </div>
        """, unsafe_allow_html=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'Space Mono',monospace; font-size:0.68rem; color:#444; padding:10px 0 20px 0;">
  Máquina de Puntuación · y = Σ(wᵢxᵢ) · Sin librerías de ML · Autómatas, Gramáticas y Lenguajes 2025
</div>
""", unsafe_allow_html=True)
