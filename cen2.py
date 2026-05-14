import streamlit as st
import pandas as pd
import random

# ── Configuración de la Página ───────────────────────────────────────────────
st.set_page_config(
    page_title="WMS · Localizador de Almacén Pro",
    page_icon="🏭",
    layout="wide",
)

# ── CSS Personalizado (Estética Atractiva y Moderna) ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #07090f; color: #e2e8f0; }

/* Header Estilo Industrial */
.wms-header {
    background: linear-gradient(135deg, #0f1629 0%, #131d35 100%);
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
}
.wms-logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 600;
    color: #38bdf8;
}

/* Contenedor de Espacios (El Cuadrilátero que pediste) */
.bin-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 3px;
    background: #1e2d4a;
    padding: 4px;
    border-radius: 6px;
    border: 1px solid #2d4a6b;
    margin-bottom: 8px;
    transition: all 0.3s ease;
}

.bin {
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    background: #0f1629;
    color: #475569;
    border-radius: 3px;
}

/* Colores de estado */
.occupied { background: #0c3058; color: #38bdf8; border: 1px solid #38bdf844; }

/* Resaltado Neón para búsqueda exitosa */
.target-found {
    background: #ff007a !important;
    color: white !important;
    box-shadow: 0 0 15px #ff007a;
    transform: scale(1.1);
    z-index: 10;
    font-weight: bold;
}

.level-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #64748b;
    margin-bottom: 2px;
}

/* Inputs y Botones */
div[data-testid="stTextInput"] input {
    background: #131d35 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    padding: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Estructura y Datos ───────────────────────────────────────────────────────
PASILLOS = ["A", "B", "C"]
ESTANTES = [1, 2, 3, 4]
COLUMNAS = ["A", "B", "C", "D"]
NIVELES = [6, 5, 4, 3, 2, 1]  # Invertido para que el 6 esté arriba
ESPACIOS = [1, 2, 3, 4]

def cod_ubicacion(p, e, c, n, s):
    return f"{p}{e}-{c}{n}-{s}"

@st.cache_data
def generar_inventario():
    random.seed(42)
    productos = [
        {"sku": "TUB-PVC-1/2", "nombre": "Tubería PVC 1/2 SAP"},
        {"sku": "VAL-BRZ-3/4", "nombre": "Válvula Bronce 3/4"},
        {"sku": "GOT-AUTO-4L", "nombre": "Gotero Auto 4L/h"},
        {"sku": "BOM-CEN-1HP", "nombre": "Bomba Centrífuga 1HP"},
        {"sku": "FIL-DIS-2", "nombre": "Filtro de Disco 2"},
        {"sku": "PEG-PVC-500", "nombre": "Pegamento PVC 500ml"}
    ]
    
    registros = []
    # Generar 100 ubicaciones ocupadas aleatoriamente
    for _ in range(100):
        p, e, c, n, s = (random.choice(PASILLOS), random.choice(ESTANTES), 
                         random.choice(COLUMNAS), random.choice(NIVELES), random.choice(ESPACIOS))
        prod = random.choice(productos)
        loc = cod_ubicacion(p, e, c, n, s)
        registros.append({
            "ubicacion": loc,
            "sku": prod["sku"],
            "nombre": prod["nombre"],
            "pasillo": p, "estante": e, "columna": c, "nivel": n, "espacio": s,
            "stock": random.randint(5, 100)
        })
    return pd.DataFrame(registros).drop_duplicates('ubicacion')

df_inv = generar_inventario()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="wms-header">
    <div class="wms-logo">WMS · VISION PRO</div>
    <div style="color: #64748b; letter-spacing: 2px; font-size: 0.8rem;">SISTEMA DE LOCALIZACIÓN ESPACIAL</div>
</div>
""", unsafe_allow_html=True)

# ── Buscador e Inteligencia de Navegación ────────────────────────────────────
c_search, c_info = st.columns([2, 1])

with c_search:
    query = st.text_input("🔍 BUSCAR UBICACIÓN O SKU", placeholder="Ej: A1-B3-2 o SKU...").upper().strip()

# Lógica para extraer datos si se encuentra el producto
target_data = None
if query:
    # Buscar coincidencia exacta por ubicación
    match = df_inv[df_inv["ubicacion"] == query]
    if not match.empty:
        target_data = match.iloc[0]
        st.success(f"✅ Localizado: {target_data['nombre']} en {query}")
    else:
        # Buscar por SKU
        match_sku = df_inv[df_inv["sku"] == query]
        if not match_sku.empty:
            target_data = match_sku.iloc[0]
            query = target_data["ubicacion"] # Reasignar query para iluminar el mapa
            st.success(f"✅ SKU Localizado en: {query}")
        else:
            st.error("❌ No se encontró el código o el espacio está vacío.")

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_mapa, tab_data = st.tabs(["🗺️ MAPA DEL ESTANTE", "📋 INVENTARIO"])

with tab_mapa:
    # Selectores: Si hubo búsqueda exitosa, se ponen automáticamente en la posición del producto
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        sel_p = st.selectbox("Seleccionar Pasillo", PASILLOS, 
                             index=PASILLOS.index(target_data['pasillo']) if target_data is not None else 0)
    with col_s2:
        sel_e = st.selectbox("Seleccionar Estante", ESTANTES, 
                             index=ESTANTES.index(target_data['estante']) if target_data is not None else 0)

    st.markdown(f"### 📍 Visualizando: Pasillo {sel_p} · Estante {sel_e}")
    st.markdown("---")

    # Generar el GRID del Estante (Columnas A, B, C, D)
    estante_cols = st.columns(len(COLUMNAS))

    for i, col_name in enumerate(COLUMNAS):
        with estante_cols[i]:
            st.markdown(f"<div style='text-align:center; color:#38bdf8; font-weight:600; margin-bottom:10px;'>COLUMNA {col_name}</div>", unsafe_allow_html=True)
            
            for niv in NIVELES:
                st.markdown(f"<div class='level-label'>Nivel {niv}</div>", unsafe_allow_html=True)
                
                # Dibujar el cuadrilátero subdividido (Espacios 1 al 4)
                html_cuadrilatero = '<div class="bin-container">'
                for esp in ESPACIOS:
                    loc_id = cod_ubicacion(sel_p, sel_e, col_name, niv, esp)
                    
                    # Determinar estado para el CSS
                    is_occupied = not df_inv[df_inv["ubicacion"] == loc_id].empty
                    is_target = (loc_id == query)
                    
                    class_name = "bin"
                    if is_occupied: class_name += " occupied"
                    if is_target: class_name += " target-found"
                    
                    # Contenido visual
                    label = f"E{esp}" if not is_target else "★"
                    html_cuadrilatero += f'<div class="{class_name}" title="{loc_id}">{label}</div>'
                
                html_cuadrilatero += '</div>'
                st.markdown(html_cuadrilatero, unsafe_allow_html=True)

with tab_data:
    st.dataframe(df_inv, use_container_width=True, hide_index=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛠️ REFERENCIA")
    st.info("""
    **Formato de Código:**
    `P-E-C-N-S`
    - **P**: Pasillo
    - **E**: Estante
    - **C**: Columna
    - **N**: Nivel
    - **S**: Espacio
    """)
    st.write("---")
    st.markdown("**LEYENDA DEL MAPA:**")
    st.markdown("🟦 Ocupado | ⬛ Vacío | 💗 Buscado")
