import streamlit as st
import pandas as pd
from datetime import datetime

# ── Configuración de la Página ───────────────────────────────────────────────
st.set_page_config(page_title="FuelTrack Lite", page_icon="⛽", layout="wide")

# ── Estilos CSS Personalizados (Nativos y Minimalistas) ──────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00f2ff !important; font-family: monospace; }
    .stAlert { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Simulación de Base de Datos ──────────────────────────────────────────────
if 'db_combustible' not in st.session_state:
    st.session_state.db_combustible = pd.DataFrame([
        {"fecha": "2026-03-01", "km": 45000, "galones": 10.5, "costo": 165},
        {"fecha": "2026-03-15", "km": 45450, "galones": 11.2, "costo": 178},
        {"fecha": "2026-04-02", "km": 45920, "galones": 10.8, "costo": 170},
        {"fecha": "2026-04-20", "km": 46400, "galones": 12.0, "costo": 190},
    ])
    st.session_state.db_combustible['fecha'] = pd.to_datetime(st.session_state.db_combustible['fecha'])

# Configuración de Mantenimiento
KM_INTERVALO_REVISION = 5000
ULTIMA_REVISION_KM = 42000 

# ── Sidebar: Registro ────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⛽ Carga")
    with st.form("registro_combustible", clear_on_submit=True):
        f_in = st.date_input("Fecha", datetime.now())
        k_in = st.number_input("Kilometraje (km)", min_value=0, step=1)
        g_in = st.number_input("Galones", min_value=0.1, step=0.1)
        c_in = st.number_input("Costo (S/.)", min_value=0.0, step=1.0)
        
        if st.form_submit_button("Guardar"):
            nuevo = pd.DataFrame([{"fecha": pd.to_datetime(f_in), "km": k_in, "galones": g_in, "costo": c_in}])
            st.session_state.db_combustible = pd.concat([st.session_state.db_combustible, nuevo], ignore_index=True)
            st.rerun()

# ── Lógica de Datos ──────────────────────────────────────────────────────────
df = st.session_state.db_combustible.sort_values("km")
df['km_recorridos'] = df['km'].diff()
df['rendimiento'] = df['km_recorridos'] / df['galones']
df['mes'] = df['fecha'].dt.strftime('%Y-%m')

km_actual = df['km'].max()
restante = KM_INTERVALO_REVISION - (km_actual - ULTIMA_REVISION_KM)

# ── Dashboard ────────────────────────────────────────────────────────────────
st.title("🏎️ Panel de Control de Combustible")

# Fila 1: Métricas Principales
m1, m2, m3 = st.columns(3)
m1.metric("Rendimiento Promedio", f"{df['rendimiento'].mean():.2f} km/gal")
m2.metric("Costo Total", f"S/. {df['costo'].sum():.2f}")

if restante > 500:
    m3.metric("Próxima Revisión", f"{restante} km", "Seguro", delta_color="normal")
elif restante > 0:
    m3.warning(f"⚠️ Revisión en {restante} km")
else:
    m3.error(f"🚨 REVISIÓN VENCIDA ({abs(restante)} km)")

st.write("---")

# Fila 2: Gráficos Nativos (No requieren Plotly)
st.subheader("📊 Análisis de Consumo Mensual")
c1, c2 = st.columns(2)

# Preparar datos para gráficos nativos
df_mensual = df.groupby('mes').agg({'km_recorridos': 'sum', 'rendimiento': 'mean'}).fillna(0)

with c1:
    st.write("**Kilómetros por Mes**")
    st.bar_chart(df_mensual['km_recorridos'])

with c2:
    st.write("**Eficiencia (km/gal)**")
    st.line_chart(df_mensual['rendimiento'])

# Fila 3: Tabla
st.write("### Historial")
st.dataframe(df.sort_values("fecha", ascending=False), use_container_width=True)
