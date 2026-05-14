import streamlit as st
import random
import time

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Trivia Rock Peruano",
    page_icon="🎸",
    layout="centered",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fondo oscuro */
.stApp {
    background-color: #1a1a1a;
    color: #f0f0f0;
}

/* Título principal */
.titulo-principal {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: #f0f0f0;
    letter-spacing: 0.08em;
    margin-bottom: 0;
    line-height: 1;
}
.titulo-principal span { color: #D82C2C; }

.subtitulo {
    color: #888;
    font-size: 0.9rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Tarjeta de pregunta */
.pregunta-card {
    background: #242424;
    border: 1px solid #3a3a3a;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.5rem;
}

.banda-tag {
    display: inline-block;
    background: #D82C2C;
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 12px;
    border-radius: 4px;
    margin-bottom: 0.7rem;
}

.pregunta-texto {
    font-size: 1.15rem;
    font-weight: 500;
    color: #f0f0f0;
    line-height: 1.45;
    margin-top: 0.4rem;
}

/* Progreso */
.progreso-label {
    font-size: 0.8rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}

/* Feedback correcto/incorrecto */
.feedback-correcto {
    background: #1a2e1a;
    border: 1px solid #4caf5066;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    color: #a5d6a7;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-top: 0.8rem;
}

.feedback-incorrecto {
    background: #2e1a1a;
    border: 1px solid #e5393566;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    color: #ef9a9a;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-top: 0.8rem;
}

/* Resultado final */
.resultado-card {
    background: #242424;
    border: 1px solid #3a3a3a;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
}

.resultado-titulo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
    line-height: 1;
}

.resultado-puntaje {
    font-size: 1.1rem;
    color: #aaa;
    margin-bottom: 1rem;
}

.resultado-desc {
    font-size: 0.95rem;
    color: #888;
    line-height: 1.6;
    max-width: 420px;
    margin: 0 auto 1.5rem;
}

/* Botones Streamlit overrides */
div[data-testid="stButton"] > button {
    background: #D82C2C !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.8rem !important;
    transition: background 0.15s !important;
}
div[data-testid="stButton"] > button:hover {
    background: #b52222 !important;
}

/* Radio buttons estilo oscuro */
div[data-testid="stRadio"] label {
    background: #242424;
    border: 1px solid #3a3a3a;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #e0e0e0 !important;
    font-size: 0.95rem;
    cursor: pointer;
    transition: border-color 0.15s;
    display: block;
    margin-bottom: 0.4rem;
}
div[data-testid="stRadio"] label:hover {
    border-color: #666;
}

/* Ocultar elementos Streamlit por defecto */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Banco de preguntas ───────────────────────────────────────────────────────
PREGUNTAS = [
    {
        "banda": "Leusemia",
        "pregunta": "¿Quién es el vocalista fundador de Leusemia, banda pionera del punk rock peruano?",
        "opciones": ["Daniel F", "Eloy Villanueva", "Pedro Suárez-Vértiz", "Diego Dibós"],
        "respuesta": "Daniel F",
        "dato": "Daniel F (Daniel Valqui) fundó Leusemia en Lima en 1983, siendo una de las figuras más influyentes del rock underground peruano."
    },
    {
        "banda": "Líbido",
        "pregunta": "¿Quién es el vocalista principal de Líbido, banda de rock formada en los 90s en Lima?",
        "opciones": ["Salim Vera", "Toño Jara", "Gonzalo Hermoza", "Christian Meier"],
        "respuesta": "Salim Vera",
        "dato": "Salim Vera es el vocalista y figura central de Líbido desde su formación en Lima en 1994. Su voz es inconfundible en el rock peruano."
    },
    {
        "banda": "Mar de Copas",
        "pregunta": "¿Cuál es el nombre del vocalista de Mar de Copas, banda emblemática del rock peruano de los 90?",
        "opciones": ["Wicho García", "Miki González", "Alex Méndez", "Juan Muñoz"],
        "respuesta": "Wicho García",
        "dato": "Wicho García lidera Mar de Copas desde 1993. La banda es conocida por su sonido melódico y emotivo, fusionando rock con influencias locales."
    },
    {
        "banda": "Arena Hash",
        "pregunta": "¿Quién fue el vocalista de Arena Hash, conocida por el hit 'Ven a mí'?",
        "opciones": ["Pedro Suárez-Vértiz", "Toño Jara", "Manolo Barrios", "Christian Meier"],
        "respuesta": "Pedro Suárez-Vértiz",
        "dato": "Pedro Suárez-Vértiz fue el vocalista de Arena Hash antes de su exitosa carrera solista. La banda fue clave en el pop-rock peruano de los 90."
    },
    {
        "banda": "Turbopótamos",
        "pregunta": "¿Quién es el vocalista de Turbopótamos, banda de rock alternativo limeño activa desde los 2000s?",
        "opciones": ["Gonzalo Hermoza", "Salim Vera", "Diego Dibós", "José Llerena"],
        "respuesta": "Gonzalo Hermoza",
        "dato": "Gonzalo Hermoza lidera Turbopótamos, una de las bandas más queridas del rock independiente peruano, con un sonido que mezcla funk, rock y letras irreverentes."
    },
    {
        "banda": "Nosequién y los Nosecuántos",
        "pregunta": "¿Quién es el vocalista de Nosequién y los Nosecuántos, emblemática banda de rock peruano?",
        "opciones": ["Hugo Bravo", "Wicho García", "Alex Méndez", "Daniel F"],
        "respuesta": "Hugo Bravo",
        "dato": "Hugo Bravo fundó y lidera Nosequién y los Nosecuántos, una banda que desde los 80s combina rock, ska y letras reflexivas con humor."
    },
    {
        "banda": "G3",
        "pregunta": "¿Quién es el vocalista de G3, banda de rock melódico que marcó los 90s peruanos?",
        "opciones": ["Toño Jara", "Salim Vera", "Christian Meier", "Gonzalo Hermoza"],
        "respuesta": "Toño Jara",
        "dato": "Toño Jara es el vocalista de G3, banda activa desde 1991 y pionera del rock melódico en el Perú, con hits que siguen sonando hasta hoy."
    },
]

# ── Estado de sesión ─────────────────────────────────────────────────────────
def inicializar():
    preguntas = random.sample(PREGUNTAS, 5)
    for p in preguntas:
        opciones = p["opciones"][:]
        random.shuffle(opciones)
        p["opciones_shuffled"] = opciones
    st.session_state.preguntas = preguntas
    st.session_state.indice = 0
    st.session_state.puntaje = 0
    st.session_state.respondida = False
    st.session_state.seleccion = None
    st.session_state.terminado = False
    st.session_state.historial = []

if "preguntas" not in st.session_state:
    inicializar()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.3rem">
  <div class="titulo-principal">🎸 TRIVIA <span>ROCK</span> PERUANO</div>
  <div class="subtitulo">¿Cuánto sabes de los vocalistas del rock peruano?</div>
</div>
""", unsafe_allow_html=True)

# ── PANTALLA: JUEGO ──────────────────────────────────────────────────────────
if not st.session_state.terminado:
    idx = st.session_state.indice
    preguntas = st.session_state.preguntas
    p = preguntas[idx]

    # Barra de progreso
    st.markdown(f'<div class="progreso-label">Pregunta {idx + 1} de 5 · Puntaje: {st.session_state.puntaje}</div>', unsafe_allow_html=True)
    st.progress((idx) / 5)

    # Tarjeta de pregunta
    st.markdown(f"""
    <div class="pregunta-card">
        <div class="banda-tag">{p['banda']}</div>
        <div class="pregunta-texto">{p['pregunta']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Opciones (radio)
    if not st.session_state.respondida:
        seleccion = st.radio(
            "Elige una opción:",
            p["opciones_shuffled"],
            index=None,
            label_visibility="collapsed",
            key=f"radio_{idx}"
        )
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Responder", key=f"btn_resp_{idx}"):
                if seleccion:
                    st.session_state.seleccion = seleccion
                    st.session_state.respondida = True
                    if seleccion == p["respuesta"]:
                        st.session_state.puntaje += 1
                    st.session_state.historial.append({
                        "correcta": seleccion == p["respuesta"],
                        "seleccion": seleccion,
                        "respuesta": p["respuesta"]
                    })
                    st.rerun()
                else:
                    st.warning("Selecciona una opción antes de responder.")
    else:
        # Mostrar opciones deshabilitadas con colores
        seleccion = st.session_state.seleccion
        es_correcto = seleccion == p["respuesta"]

        for op in p["opciones_shuffled"]:
            if op == p["respuesta"]:
                st.success(f"✓  {op}")
            elif op == seleccion and not es_correcto:
                st.error(f"✗  {op}")
            else:
                st.markdown(f"""
                <div style="background:#242424;border:1px solid #3a3a3a;border-radius:8px;
                            padding:0.65rem 1rem;color:#555;margin-bottom:0.4rem;font-size:0.95rem;">
                    {op}
                </div>""", unsafe_allow_html=True)

        # Feedback
        if es_correcto:
            st.markdown(f'<div class="feedback-correcto">✓ ¡Correcto! {p["dato"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-incorrecto">✗ La respuesta correcta era <strong>{p["respuesta"]}</strong>. {p["dato"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            label_btn = "Siguiente →" if idx < 4 else "Ver resultado"
            if st.button(label_btn, key=f"btn_next_{idx}"):
                if idx < 4:
                    st.session_state.indice += 1
                    st.session_state.respondida = False
                    st.session_state.seleccion = None
                else:
                    st.session_state.terminado = True
                st.rerun()

# ── PANTALLA: RESULTADO ──────────────────────────────────────────────────────
else:
    puntaje = st.session_state.puntaje

    if puntaje == 5:
        color = "#E8A020"
        titulo = "¡PERFECTO!"
        estrellas = "🎸🎸🎸🎸🎸"
        desc = "¡Acertaste las 5 preguntas! Eres un experto absoluto del rock peruano. Los dioses del riff te saludan."
    elif puntaje == 4:
        color = "#7ddb82"
        titulo = "¡MUY BIEN!"
        estrellas = "🎸🎸🎸🎸⬛"
        desc = "Casi perfecto. Tu pasión por el rock peruano es evidente. ¡Una más y llegas al top!"
    elif puntaje == 3:
        color = "#60b0ff"
        titulo = "¡BUEN INTENTO!"
        estrellas = "🎸🎸🎸⬛⬛"
        desc = "Sabes del rock peruano, pero aún hay mucho por descubrir. ¡Sigue escuchando!"
    elif puntaje == 2:
        color = "#ef9a9a"
        titulo = "SIGUE ESCUCHANDO"
        estrellas = "🎸🎸⬛⬛⬛"
        desc = "Todavía queda mucho camino. Pon el volumen al máximo y vuelve a intentarlo."
    else:
        color = "#888"
        titulo = "¡A PRACTICAR!"
        estrellas = "🎸⬛⬛⬛⬛"
        desc = "Empieza con Leusemia, Líbido y Mar de Copas. ¡No te arrepentirás!"

    # Animación especial si puntaje perfecto
    if puntaje == 5:
        st.balloons()
        time.sleep(0.3)
        st.snow()

    st.markdown(f"""
    <div class="resultado-card">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">{estrellas}</div>
        <div class="resultado-titulo" style="color:{color}">{titulo}</div>
        <div class="resultado-puntaje">{puntaje} de 5 respuestas correctas</div>
        <div class="resultado-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # Detalle de respuestas
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Ver detalle de mis respuestas"):
        for i, (h, p_data) in enumerate(zip(st.session_state.historial, st.session_state.preguntas)):
            icono = "✅" if h["correcta"] else "❌"
            st.markdown(f"**{icono} Pregunta {i+1} — {p_data['banda']}**")
            st.markdown(f"_{p_data['pregunta']}_")
            if not h["correcta"]:
                st.markdown(f"Tu respuesta: ~~{h['seleccion']}~~  →  **{h['respuesta']}**")
            else:
                st.markdown(f"Respuesta: **{h['respuesta']}** ✓")
            st.divider()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Jugar de nuevo"):
        inicializar()
        st.rerun()# Application file
