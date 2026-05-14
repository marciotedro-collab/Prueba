import streamlit as st
import random

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Ecuaciones de 1er Grado",
    page_icon="📐",
    layout="centered",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #0f1117;
    color: #e8e8e8;
}

/* Header */
.app-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    margin-bottom: 1rem;
}
.app-title {
    font-family: 'Fira Code', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #e8e8e8;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.app-title span { color: #4fc3f7; }
.app-subtitle {
    font-size: 0.85rem;
    color: #555;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

/* Tarjeta de ecuación */
.eq-card {
    background: #1c1f2b;
    border: 1px solid #2a2e3e;
    border-radius: 16px;
    padding: 2rem 2.2rem 1.5rem;
    margin-bottom: 1.2rem;
    text-align: center;
}
.eq-label {
    font-size: 0.78rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
}
.eq-text {
    font-family: 'Fira Code', monospace;
    font-size: 2.2rem;
    font-weight: 600;
    color: #e8e8e8;
    letter-spacing: 0.04em;
    line-height: 1.3;
}
.eq-text .var-x { color: #4fc3f7; }

/* Tipo de ecuación badge */
.tipo-badge {
    display: inline-block;
    background: #1a2a3a;
    border: 1px solid #4fc3f766;
    color: #4fc3f7;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* Stats bar */
.stats-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1.2rem;
}
.stat-box {
    flex: 1;
    background: #1c1f2b;
    border: 1px solid #2a2e3e;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    text-align: center;
}
.stat-val {
    font-family: 'Fira Code', monospace;
    font-size: 1.5rem;
    font-weight: 600;
    color: #e8e8e8;
    line-height: 1;
}
.stat-val.correct { color: #81c784; }
.stat-val.wrong   { color: #e57373; }
.stat-label {
    font-size: 0.72rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* Feedback */
.feedback-ok {
    background: #1a2e1a;
    border: 1px solid #4caf5055;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #a5d6a7;
    font-size: 0.92rem;
    text-align: center;
    margin-top: 0.6rem;
}
.feedback-err {
    background: #2e1a1a;
    border: 1px solid #ef535355;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #ef9a9a;
    font-size: 0.92rem;
    text-align: center;
    margin-top: 0.6rem;
}

/* Explicación paso a paso */
.pasos-card {
    background: #131620;
    border: 1px solid #2a2e3e;
    border-left: 3px solid #4fc3f7;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    color: #b0bec5;
    line-height: 1.9;
    margin-top: 0.8rem;
}
.pasos-title {
    font-size: 0.72rem;
    color: #4fc3f7;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.6rem;
    font-family: 'DM Sans', sans-serif;
}

/* Botones */
div[data-testid="stButton"] > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.15s !important;
    border: none !important;
}

/* Input número */
div[data-testid="stNumberInput"] input {
    background: #1c1f2b !important;
    border: 1px solid #2a2e3e !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 1.1rem !important;
    text-align: center;
}

/* Ocultar elementos Streamlit */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Generador de ecuaciones ──────────────────────────────────────────────────
def generar_ecuacion():
    """
    Genera una ecuación de primer grado aleatoria.
    La solución x siempre es un entero entre 0 y 10.
    Tipos:
      1) ax + b = c           →  ax = c - b
      2) ax - b = c           →  ax = c + b
      3) ax + b = cx + d      →  (a-c)x = d - b
      4) a(x + b) = c         →  ax + ab = c
      5) ax + b + cx = d      →  (a+c)x = d - b
    """
    x = random.randint(0, 10)
    tipo = random.randint(1, 5)

    if tipo == 1:
        a = random.randint(1, 9)
        b = random.randint(1, 20)
        c = a * x + b
        texto = f"{a}x + {b} = {c}"
        nombre = "Forma básica"
        pasos = [
            f"  {a}x + {b} = {c}",
            f"  {a}x = {c} - {b}",
            f"  {a}x = {a * x}",
            f"  x = {a * x} ÷ {a}",
            f"  x = {x}  ✓",
        ]

    elif tipo == 2:
        a = random.randint(1, 9)
        b = random.randint(1, 20)
        c = a * x - b
        texto = f"{a}x - {b} = {c}"
        nombre = "Con resta"
        pasos = [
            f"  {a}x - {b} = {c}",
            f"  {a}x = {c} + {b}",
            f"  {a}x = {a * x}",
            f"  x = {a * x} ÷ {a}",
            f"  x = {x}  ✓",
        ]

    elif tipo == 3:
        a = random.randint(3, 9)
        c = random.randint(1, a - 1)   # a > c para coef positivo
        b = random.randint(1, 15)
        d = (a - c) * x + b
        texto = f"{a}x + {b} = {c}x + {d}"
        nombre = "Incógnita en ambos lados"
        pasos = [
            f"  {a}x + {b} = {c}x + {d}",
            f"  {a}x - {c}x = {d} - {b}",
            f"  {a - c}x = {d - b}",
            f"  x = {d - b} ÷ {a - c}",
            f"  x = {x}  ✓",
        ]

    elif tipo == 4:
        a = random.randint(1, 9)
        b = random.randint(1, 10)
        c = a * (x + b)
        texto = f"{a}(x + {b}) = {c}"
        nombre = "Con paréntesis"
        pasos = [
            f"  {a}(x + {b}) = {c}",
            f"  {a}x + {a * b} = {c}",
            f"  {a}x = {c} - {a * b}",
            f"  {a}x = {a * x}",
            f"  x = {a * x} ÷ {a}",
            f"  x = {x}  ✓",
        ]

    else:  # tipo 5
        a = random.randint(1, 5)
        c = random.randint(1, 5)
        b = random.randint(1, 20)
        d = (a + c) * x + b
        texto = f"{a}x + {b} + {c}x = {d}"
        nombre = "Términos semejantes"
        pasos = [
            f"  {a}x + {b} + {c}x = {d}",
            f"  ({a} + {c})x + {b} = {d}",
            f"  {a + c}x = {d} - {b}",
            f"  {a + c}x = {(a + c) * x}",
            f"  x = {(a + c) * x} ÷ {a + c}",
            f"  x = {x}  ✓",
        ]

    return {
        "x": x,
        "texto": texto,
        "nombre": nombre,
        "pasos": pasos,
        "tipo": tipo,
    }


# ── Estado de sesión ─────────────────────────────────────────────────────────
def nueva_ecuacion():
    st.session_state.ecuacion = generar_ecuacion()
    st.session_state.verificado = False
    st.session_state.correcto = None
    st.session_state.respuesta_input = 0

if "ecuacion" not in st.session_state:
    nueva_ecuacion()
    st.session_state.aciertos = 0
    st.session_state.errores = 0
    st.session_state.intentos = 0

eq = st.session_state.ecuacion

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div class="app-title">📐 Ecuaciones de <span>1er Grado</span></div>
  <div class="app-subtitle">Resuelve · Verifica · Aprende</div>
</div>
""", unsafe_allow_html=True)

# ── Stats ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-row">
  <div class="stat-box">
    <div class="stat-val">{st.session_state.intentos}</div>
    <div class="stat-label">Intentos</div>
  </div>
  <div class="stat-box">
    <div class="stat-val correct">{st.session_state.aciertos}</div>
    <div class="stat-label">Correctas</div>
  </div>
  <div class="stat-box">
    <div class="stat-val wrong">{st.session_state.errores}</div>
    <div class="stat-label">Incorrectas</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tarjeta de ecuación ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="eq-card">
  <div class="eq-label">Resuelve para x</div>
  <div class="tipo-badge">{eq['nombre']}</div>
  <div class="eq-text">{eq['texto']}</div>
</div>
""", unsafe_allow_html=True)

# ── Input de respuesta ───────────────────────────────────────────────────────
st.markdown("**Tu respuesta — ¿cuánto vale x?**")
respuesta = st.number_input(
    "Valor de x",
    min_value=-50,
    max_value=100,
    value=st.session_state.get("respuesta_input", 0),
    step=1,
    label_visibility="collapsed",
    key="num_input"
)

# ── Botones ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    verificar = st.button("✓  Verificar respuesta", use_container_width=True)

with col2:
    nuevo = st.button("↺  Nueva ecuación", use_container_width=True)

with col3:
    reset = st.button("🗑", use_container_width=True, help="Reiniciar estadísticas")

if nuevo:
    nueva_ecuacion()
    st.rerun()

if reset:
    st.session_state.aciertos = 0
    st.session_state.errores = 0
    st.session_state.intentos = 0
    nueva_ecuacion()
    st.rerun()

if verificar and not st.session_state.verificado:
    st.session_state.intentos += 1
    st.session_state.verificado = True
    if int(respuesta) == eq["x"]:
        st.session_state.correcto = True
        st.session_state.aciertos += 1
    else:
        st.session_state.correcto = False
        st.session_state.errores += 1
    st.rerun()

# ── Feedback ─────────────────────────────────────────────────────────────────
if st.session_state.verificado:
    if st.session_state.correcto:
        st.snow()
        st.markdown(f"""
        <div class="feedback-ok">
            ❄️ ¡Correcto! &nbsp; x = {eq['x']} &nbsp; ✓ &nbsp; ¡Excelente trabajo!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="feedback-err">
            ✗ &nbsp; Respuesta incorrecta. Ingresaste x = {int(respuesta)}, pero la solución correcta es x = {eq['x']}.
        </div>
        """, unsafe_allow_html=True)

    # Solución paso a paso
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📖 Ver solución paso a paso"):
        pasos_html = "\n".join(eq["pasos"])
        st.markdown(f"""
        <div class="pasos-card">
          <div class="pasos-title">Procedimiento</div>
          <pre style="margin:0;background:transparent;color:#b0bec5;font-family:'Fira Code',monospace;font-size:0.88rem">{pasos_html}</pre>
        </div>
        """, unsafe_allow_html=True)

    # Siguiente ecuación
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("→  Siguiente ecuación", use_container_width=False):
        nueva_ecuacion()
        st.rerun()

# ── Pie de página ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<hr style="border:none;border-top:1px solid #2a2e3e;margin:1rem 0">
<div style="text-align:center;font-size:0.75rem;color:#333;letter-spacing:0.08em">
  ECUACIONES DE PRIMER GRADO · SOLUCIONES ENTERAS DEL 0 AL 10
</div>
""", unsafe_allow_html=True)
