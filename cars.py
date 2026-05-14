import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ── Configuración de la Página ───────────────────────────────────────────────
st.set_page_config(page_title="FuelTrack Pro", page_icon="⛽", layout="wide")

# ── Estilos CSS Personalizados ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .main-card {
        background: linear-gradient(145deg, #1e2630, #161b22);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        color: #00f2ff;
    }
    .status-ok { color: #4ade80; }
    .status-warn { color: #fbbf24; }
    .status-alert { color: #f87171; }
</style>
""", unsafe_allow_html=True)

# ── Simulación de Base de Datos ──────────────────────────────────────────────
if 'db_combustible' not in st.session_state:
    # Datos iniciales de ejemplo
    st.session_state.db_combustible = pd.DataFrame([
        {"fecha": "2026-03-01", "km": 45000, "galones": 10.5, "costo": 165},
        {"fecha": "2026-03-15", "km": 45450, "galones": 11.2, "costo": 178},
        {"fecha": "2026-04-02", "km": 45920, "galones": 10.8, "costo": 170},
        {"fecha": "2026-04-20", "km": 46400, "galones": 12.0, "costo": 190},
    ])
    st.session_state.db_combustible['fecha'] = pd.to_datetime(st.session_state.db_combustible['fecha'])

# Parámetros de Mantenimiento (Configurables)
KM_REVISION = 5000  # Cada cuántos km toca revisión
ULTIMA_REVISION_KM = 42000 

# ── Sidebar: Registro de Datos ───────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/814/814402.png", width=80)
    st.header("⛽ Registro de Carga")
    
    with st.form("registro_combustible", clear_on_submit=True):
        fecha_input = st.date_input("Fecha de carga", datetime.now())
        km_input = st.number_input("Kilometraje Actual (km)", min_value=0, step=1)
        gal_input = st.number_input("Galones repostados", min_value=0.1, step=0.1)
        costo_input = st.number_input("Costo Total (S/.)", min_value=0.0, step=1.0)
        
        submit = st.form_submit_button("Guardar Registro")
        
        if submit:
            nuevo_dato = {
                "fecha": pd.to_datetime(fecha_input),
                "km": km_input,
                "galones": gal_input,
                "costo": costo_input
            }
            st.session_state.db_combustible = pd.concat([
                st.session_state.db_combustible, 
                pd.DataFrame([nuevo_dato])
            ], ignore_index=True)
            st.rerun()

# ── Lógica de Cálculos ───────────────────────────────────────────────────────
df = st.session_state.db_combustible.sort_values("km")
df['km_recorridos'] = df['km'].diff()
df['rendimiento'] = df['km_recorridos'] / df['galones']
df['mes'] = df['fecha'].dt.strftime('%Y-%m')

# Metas y Alertas
km_actual = df['km'].max()
km_desde_revision = km_actual - ULTIMA_REVISION_KM
progreso_revision = min(km_desde_revision / KM_REVISION, 1.0)

# ── Dashboard Principal ──────────────────────────────────────────────────────
st.title("🏎️ FuelTrack Dashboard")

# Fila 1: KPIs y Alertas
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    rendimiento_avg = df['rendimiento'].mean()
    st.markdown(f"""
    <div class="main-card">
        <div style="font-size:0.8rem; color:#8b949e">RENDIMIENTO PROMEDIO</div>
        <div class="metric-val">{rendimiento_avg:.2f} <span style="font-size:1rem">km/gal</span></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    costo_km = df['costo'].sum() / (df['km'].max() - df['km'].min())
    st.markdown(f"""
    <div class="main-card">
        <div style="font-size:0.8rem; color:#8b949e">COSTO POR KM</div>
        <div class="metric-val">S/. {costo_km:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    status_class = "status-ok" if progreso_revision < 0.8 else "status-warn" if progreso_revision < 0.95 else "status-alert"
    restante = KM_REVISION - km_desde_revision
    
    st.markdown(f"""
    <div class="main-card">
        <div style="font-size:0.8rem; color:#8b949e">PRÓXIMA REVISIÓN TÉCNICA</div>
        <div class="metric-val {status_class}">{restante} <span style="font-size:1rem">km restantes</span></div>
        <div style="background:#30363d; height:8px; border-radius:5px; margin-top:10px">
            <div style="background:currentColor; width:{progreso_revision*100}%; height:100%; border-radius:5px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Fila 2: Gráficos Mensuales
st.subheader("📊 Análisis Mensual")
col_graph1, col_graph2 = st.columns(2)

# Agrupado por mes
df_mensual = df.groupby('mes').agg({
    'km_recorridos': 'sum',
    'galones': 'sum',
    'costo': 'sum',
    'rendimiento': 'mean'
}).reset_index()

with col_graph1:
    fig_km = px.bar(df_mensual, x='mes', y='km_recorridos', 
                    title="Kilómetros Recorridos por Mes",
                    color_discrete_sequence=['#00f2ff'])
    fig_km.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_km, use_container_width=True)

with col_graph2:
    fig_perf = px.line(df_mensual, x='mes', y='rendimiento', 
                       title="Tendencia de Rendimiento (km/gal)",
                       markers=True, line_shape="spline")
    fig_perf.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)')
    fig_perf.update_traces(line_color='#4ade80')
    st.plotly_chart(fig_perf, use_container_width=True)

# Fila 3: Tabla de Histórico
with st.expander("📄 Ver Historial de Cargas Completo"):
    st.dataframe(df[['fecha', 'km', 'galones', 'costo', 'km_recorridos', 'rendimiento']]
                 .sort_values("fecha", ascending=False), 
                 use_container_width=True)

# ── Tips de Conducción (Valor Agregado) ──────────────────────────────────────
st.write("---")
st.markdown("### 💡 Tips para mejorar el rendimiento")
t1, t2, t3 = st.columns(3)
t1.info("Mantén la presión de las llantas según el manual para ahorrar hasta un 3% de combustible.")
t2.success("Evita aceleraciones bruscas; mantener una velocidad constante es la clave del ahorro.")
t3.warning("El uso excesivo del aire acondicionado en ciudad puede aumentar el consumo en un 10%.")
