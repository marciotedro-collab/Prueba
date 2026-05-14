import streamlit as st
import pandas as pd
import random

# ── Configuración ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WMS · Localizador de Almacén",
    page_icon="🏭",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #07090f; color: #e2e8f0; }

/* ── Header ── */
.wms-header {
    background: linear-gradient(135deg, #0f1629 0%, #131d35 100%);
    border: 1px solid #1e2d4a;
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
}
.wms-logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: -0.03em;
    line-height: 1;
}
.wms-logo span { color: #64748b; font-weight: 400; }
.wms-tagline { font-size: 0.8rem; color: #475569; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.2rem; }

/* ── Search box ── */
.search-wrap {
    background: #0f1629;
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.search-title {
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
}

/* ── Result card ── */
.result-card {
    background: #0f1629;
    border: 1px solid #1e3a5f;
    border-left: 4px solid #38bdf8;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    animation: slideIn 0.3s ease;
}
.result-card.not-found {
    border-left-color: #ef4444;
    border-color: #3f1515;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-sku {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.3rem;
}
.result-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 1rem;
}
.meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin-bottom: 1rem;
}
.meta-box {
    background: #131d35;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
}
.meta-label { font-size: 0.68rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.25rem; }
.meta-val   { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 600; color: #e2e8f0; }
.meta-val.loc { color: #38bdf8; font-size: 1.1rem; }

/* ── Location path breadcrumb ── */
.loc-path {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 0.4rem;
}
.loc-crumb {
    background: #1e2d4a;
    border: 1px solid #2d4a6b;
    border-radius: 6px;
    padding: 4px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #94a3b8;
}
.loc-crumb.active {
    background: #0c3058;
    border-color: #38bdf8;
    color: #38bdf8;
    font-weight: 600;
}
.loc-arrow { color: #334155; font-size: 0.9rem; }

/* ── Mapa del almacén ── */
.map-section-title {
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
    padding-top: 0.4rem;
}

/* ── Stock badge ── */
.badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.badge.ok  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.badge.low { background: #431407; color: #fb923c; border: 1px solid #9a3412; }
.badge.out { background: #1f0606; color: #f87171; border: 1px solid #7f1d1d; }

/* ── Tabla de inventario ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
div[data-testid="stDataFrame"] {
    border: 1px solid #1e2d4a !important;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Botones ── */
div[data-testid="stButton"] > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    border: 1px solid #1e3a5f !important;
    background: #0f1629 !important;
    color: #38bdf8 !important;
    transition: all 0.15s !important;
}
div[data-testid="stButton"] > button:hover {
    background: #1e3a5f !important;
    border-color: #38bdf8 !important;
}

/* ── Input ── */
div[data-testid="stTextInput"] input {
    background: #131d35 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px #38bdf820 !important;
}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] select,
div[data-testid="stSelectbox"] > div > div {
    background: #131d35 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #07090f;
    border-right: 1px solid #1e2d4a;
}

/* ── Tabs ── */
div[data-baseweb="tab-list"] {
    background: #0f1629;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e2d4a;
    margin-bottom: 1rem;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: #475569 !important;
    font-size: 0.85rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: #1e3a5f !important;
    color: #38bdf8 !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURA DEL ALMACÉN
# Pasillos: A, B, C
# Estantes por pasillo: 1–4
# Columnas por estante: A–D
# Niveles por columna: 1–6  (1=suelo, 6=alto)
# Espacios por nivel: 1–4
#
# Código: PP-EE-CC-NN-SS  → P-A | E-1 | C-A | N-1 | S-1  →  A-1-A-1-1
# ══════════════════════════════════════════════════════════════════════════════

PASILLOS   = ["A", "B", "C"]
ESTANTES   = [1, 2, 3, 4]
COLUMNAS   = ["A", "B", "C", "D"]
NIVELES    = [1, 2, 3, 4, 5, 6]
ESPACIOS   = [1, 2, 3, 4]

def cod_ubicacion(p, e, c, n, s):
    return f"{p}{e}-{c}{n}-{s}"

# ── Catálogo de productos (almacén de materiales de irrigación/construcción) ──
CATALOGO = [
    # Tubería PVC
    {"sku":"TUB-PVC-1/2","nombre":"Tubería PVC 1/2\" SAP","categoria":"Tubería","unidad":"und","peso_kg":0.35},
    {"sku":"TUB-PVC-3/4","nombre":"Tubería PVC 3/4\" SAP","categoria":"Tubería","unidad":"und","peso_kg":0.52},
    {"sku":"TUB-PVC-1\"" ,"nombre":"Tubería PVC 1\" SAP","categoria":"Tubería","unidad":"und","peso_kg":0.78},
    {"sku":"TUB-PVC-2\"" ,"nombre":"Tubería PVC 2\" SAP","categoria":"Tubería","unidad":"und","peso_kg":1.40},
    {"sku":"TUB-PVC-4\"" ,"nombre":"Tubería PVC 4\" SAP","categoria":"Tubería","unidad":"und","peso_kg":3.20},
    {"sku":"TUB-HDPE-32","nombre":"Tubería HDPE 32mm PE100","categoria":"Tubería","unidad":"mt","peso_kg":0.28},
    {"sku":"TUB-HDPE-50","nombre":"Tubería HDPE 50mm PE100","categoria":"Tubería","unidad":"mt","peso_kg":0.55},
    # Accesorios PVC
    {"sku":"ACC-COD-1/2","nombre":"Codo 90° PVC 1/2\"","categoria":"Accesorio","unidad":"und","peso_kg":0.05},
    {"sku":"ACC-COD-3/4","nombre":"Codo 90° PVC 3/4\"","categoria":"Accesorio","unidad":"und","peso_kg":0.08},
    {"sku":"ACC-COD-1\"" ,"nombre":"Codo 90° PVC 1\"","categoria":"Accesorio","unidad":"und","peso_kg":0.12},
    {"sku":"ACC-TEE-1/2","nombre":"Tee PVC 1/2\"","categoria":"Accesorio","unidad":"und","peso_kg":0.06},
    {"sku":"ACC-TEE-3/4","nombre":"Tee PVC 3/4\"","categoria":"Accesorio","unidad":"und","peso_kg":0.09},
    {"sku":"ACC-RED-1X1/2","nombre":"Reducción 1\" x 1/2\" PVC","categoria":"Accesorio","unidad":"und","peso_kg":0.07},
    {"sku":"ACC-UNI-1/2","nombre":"Unión simple PVC 1/2\"","categoria":"Accesorio","unidad":"und","peso_kg":0.04},
    {"sku":"ACC-UNI-3/4","nombre":"Unión simple PVC 3/4\"","categoria":"Accesorio","unidad":"und","peso_kg":0.06},
    # Válvulas
    {"sku":"VAL-BRZ-1/2","nombre":"Válvula de bola bronce 1/2\"","categoria":"Válvula","unidad":"und","peso_kg":0.30},
    {"sku":"VAL-BRZ-3/4","nombre":"Válvula de bola bronce 3/4\"","categoria":"Válvula","unidad":"und","peso_kg":0.45},
    {"sku":"VAL-BRZ-1\"" ,"nombre":"Válvula de bola bronce 1\"","categoria":"Válvula","unidad":"und","peso_kg":0.65},
    {"sku":"VAL-CHK-1/2","nombre":"Válvula check PVC 1/2\"","categoria":"Válvula","unidad":"und","peso_kg":0.18},
    {"sku":"VAL-CHK-1\"" ,"nombre":"Válvula check PVC 1\"","categoria":"Válvula","unidad":"und","peso_kg":0.35},
    # Goteros y microirrigación
    {"sku":"GOT-AUTO-4L","nombre":"Gotero autocompensado 4 L/h","categoria":"Gotero","unidad":"und","peso_kg":0.01},
    {"sku":"GOT-AUTO-8L","nombre":"Gotero autocompensado 8 L/h","categoria":"Gotero","unidad":"und","peso_kg":0.01},
    {"sku":"GOT-CLIC-2L","nombre":"Gotero clic 2 L/h","categoria":"Gotero","unidad":"und","peso_kg":0.01},
    {"sku":"MIC-MAN-180","nombre":"Microaspersor 180° 40 L/h","categoria":"Microirrigación","unidad":"und","peso_kg":0.06},
    {"sku":"MIC-MAN-360","nombre":"Microaspersor 360° 70 L/h","categoria":"Microirrigación","unidad":"und","peso_kg":0.07},
    # Filtros
    {"sku":"FIL-MLL-1\"" ,"nombre":"Filtro de malla 1\" 120 mesh","categoria":"Filtro","unidad":"und","peso_kg":0.28},
    {"sku":"FIL-MLL-2\"" ,"nombre":"Filtro de malla 2\" 120 mesh","categoria":"Filtro","unidad":"und","peso_kg":0.55},
    {"sku":"FIL-DIS-2\"" ,"nombre":"Filtro de disco 2\" 130 mesh","categoria":"Filtro","unidad":"und","peso_kg":0.62},
    # Pegamentos y selladores
    {"sku":"PEG-PVC-250","nombre":"Pegamento PVC 250ml","categoria":"Adhesivo","unidad":"frasco","peso_kg":0.30},
    {"sku":"PEG-PVC-500","nombre":"Pegamento PVC 500ml","categoria":"Adhesivo","unidad":"frasco","peso_kg":0.55},
    {"sku":"SEL-TFE-12M","nombre":"Cinta teflón 12mm x 10m","categoria":"Adhesivo","unidad":"rollo","peso_kg":0.04},
    # Herramientas
    {"sku":"HER-COR-PVC","nombre":"Cortatubos PVC hasta 2\"","categoria":"Herramienta","unidad":"und","peso_kg":0.45},
    {"sku":"HER-LLA-10\"","nombre":"Llave ajustable 10\"","categoria":"Herramienta","unidad":"und","peso_kg":0.38},
    # Bombas
    {"sku":"BOM-CEN-1HP","nombre":"Bomba centrífuga 1 HP 220V","categoria":"Bomba","unidad":"und","peso_kg":8.50},
    {"sku":"BOM-CEN-2HP","nombre":"Bomba centrífuga 2 HP 220V","categoria":"Bomba","unidad":"und","peso_kg":12.0},
    {"sku":"BOM-SUB-1HP","nombre":"Bomba sumergible 1 HP","categoria":"Bomba","unidad":"und","peso_kg":6.50},
    # Cables y eléctricos
    {"sku":"ELE-CAB-4MM","nombre":"Cable THW 4mm² negro","categoria":"Eléctrico","unidad":"mt","peso_kg":0.10},
    {"sku":"ELE-CAB-6MM","nombre":"Cable THW 6mm² negro","categoria":"Eléctrico","unidad":"mt","peso_kg":0.15},
    # Aspersores
    {"sku":"ASP-IMP-3/4","nombre":"Aspersor impacto 3/4\" 360°","categoria":"Aspersor","unidad":"und","peso_kg":0.22},
    {"sku":"ASP-IMP-1\"" ,"nombre":"Aspersor impacto 1\" 360°","categoria":"Aspersor","unidad":"und","peso_kg":0.35},
    # Cinta de riego
    {"sku":"CIN-GOT-16-30","nombre":"Cinta de goteo 16mm 30cm","categoria":"Cinta riego","unidad":"mt","peso_kg":0.05},
    {"sku":"CIN-GOT-16-20","nombre":"Cinta de goteo 16mm 20cm","categoria":"Cinta riego","unidad":"mt","peso_kg":0.05},
    # Manguera
    {"sku":"MAN-JAR-1/2","nombre":"Manguera jardinería 1/2\" reforzada","categoria":"Manguera","unidad":"mt","peso_kg":0.12},
    {"sku":"MAN-JAR-3/4","nombre":"Manguera jardinería 3/4\" reforzada","categoria":"Manguera","unidad":"mt","peso_kg":0.18},
    # Tanques
    {"sku":"TAN-POL-600","nombre":"Tanque polietileno 600L","categoria":"Tanque","unidad":"und","peso_kg":18.0},
    {"sku":"TAN-POL-1100","nombre":"Tanque polietileno 1100L","categoria":"Tanque","unidad":"und","peso_kg":28.0},
    # Conectores
    {"sku":"CON-INS-1/2","nombre":"Conector inserción 1/2\" manguera","categoria":"Conector","unidad":"und","peso_kg":0.02},
    {"sku":"CON-INS-3/4","nombre":"Conector inserción 3/4\" manguera","categoria":"Conector","unidad":"und","peso_kg":0.03},
    {"sku":"CON-LFA-1/2","nombre":"Conector latón femoral 1/2\"","categoria":"Conector","unidad":"und","peso_kg":0.04},
]

# ── Generar inventario asignando ubicaciones únicas ──────────────────────────
@st.cache_data
def generar_inventario():
    random.seed(42)
    todas_ubicaciones = [
        cod_ubicacion(p, e, c, n, s)
        for p in PASILLOS
        for e in ESTANTES
        for c in COLUMNAS
        for n in NIVELES
        for s in ESPACIOS
    ]
    random.shuffle(todas_ubicaciones)

    registros = []
    for i, prod in enumerate(CATALOGO):
        # Cada producto puede tener 1 o 2 ubicaciones
        n_ubic = random.randint(1, 2)
        for j in range(n_ubic):
            idx = i * 2 + j
            if idx >= len(todas_ubicaciones):
                break
            ub = todas_ubicaciones[idx]
            stock = random.randint(0, 200)
            min_stock = random.randint(10, 40)
            registros.append({
                "ubicacion": ub,
                "sku": prod["sku"],
                "nombre": prod["nombre"],
                "categoria": prod["categoria"],
                "unidad": prod["unidad"],
                "peso_kg": prod["peso_kg"],
                "stock": stock,
                "stock_minimo": min_stock,
                "pasillo": ub[0],
                "estante": int(ub[1]),
                "columna": ub[3],
                "nivel": int(ub[4]),
                "espacio": int(ub[6]),
            })

    df = pd.DataFrame(registros)
    return df

df_inv = generar_inventario()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem">
      <div style="font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:600;color:#38bdf8">WMS</div>
      <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em">Warehouse Management</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">Estructura</div>', unsafe_allow_html=True)

    for p in PASILLOS:
        n = len(df_inv[df_inv.pasillo == p])
        st.markdown(f"""
        <div style="background:#0f1629;border:1px solid #1e2d4a;border-radius:8px;
                    padding:0.5rem 0.8rem;margin-bottom:6px;display:flex;
                    justify-content:space-between;align-items:center">
          <span style="font-family:'JetBrains Mono',monospace;color:#38bdf8;font-size:0.9rem">Pasillo {p}</span>
          <span style="font-size:0.78rem;color:#64748b">{n} prod.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem">Resumen</div>', unsafe_allow_html=True)
    total   = len(df_inv)
    sin_stock = len(df_inv[df_inv.stock == 0])
    bajo = len(df_inv[(df_inv.stock > 0) & (df_inv.stock < df_inv.stock_minimo)])
    st.markdown(f"""
    <div style="font-size:0.82rem;color:#94a3b8;line-height:2">
      📦 Total SKUs: <b style="color:#e2e8f0">{total}</b><br>
      🟢 Con stock: <b style="color:#4ade80">{total - sin_stock - bajo}</b><br>
      🟠 Stock bajo: <b style="color:#fb923c">{bajo}</b><br>
      🔴 Sin stock: <b style="color:#f87171">{sin_stock}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:0.68rem;color:#334155;text-align:center;padding-bottom:0.5rem">Código: PP-EE·CC-NN-SS<br>Ej: A1-B3-2</div>', unsafe_allow_html=True)

# ── Header principal ─────────────────────────────────────────────────────────
st.markdown("""
<div class="wms-header">
  <div>
    <div class="wms-logo">WMS<span>·</span>STORE</div>
    <div class="wms-tagline">Sistema de localización de productos en almacén</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍  Buscar producto", "🗺️  Mapa del almacén", "📋  Inventario completo"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — BÚSQUEDA
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_search, col_tip = st.columns([3, 1])

    with col_search:
        st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="search-title">Buscar por código de ubicación o SKU / nombre</div>', unsafe_allow_html=True)
        query = st.text_input(
            "Búsqueda",
            placeholder="Ej: A1-B3-2  ·  TUB-PVC-1/2  ·  gotero",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tip:
        st.markdown("""
        <div style="background:#0f1629;border:1px solid #1e2d4a;border-radius:12px;
                    padding:1rem;font-size:0.75rem;color:#475569;line-height:1.8;margin-top:0">
          <b style="color:#38bdf8">Formato código:</b><br>
          <code style="color:#94a3b8">PP·EE-CC·NN-SS</code><br>
          P = Pasillo (A/B/C)<br>
          E = Estante (1-4)<br>
          C = Columna (A-D)<br>
          N = Nivel (1-6)<br>
          S = Espacio (1-4)
        </div>
        """, unsafe_allow_html=True)

    if query.strip():
        q = query.strip().upper()

        # Buscar por ubicación exacta
        res_ubic = df_inv[df_inv["ubicacion"] == q]

        # Buscar por SKU exacto
        res_sku = df_inv[df_inv["sku"].str.upper() == q]

        # Buscar por texto parcial en nombre, sku o ubicacion
        res_texto = df_inv[
            df_inv["nombre"].str.upper().str.contains(q, na=False) |
            df_inv["sku"].str.upper().str.contains(q, na=False) |
            df_inv["ubicacion"].str.upper().str.contains(q, na=False)
        ]

        resultados = pd.concat([res_ubic, res_sku, res_texto]).drop_duplicates()

        if resultados.empty:
            st.markdown(f"""
            <div class="result-card not-found">
              <div class="result-sku">Sin resultados</div>
              <div class="result-name">No se encontró "<span style="color:#ef4444">{query}</span>"</div>
              <div style="font-size:0.85rem;color:#64748b">Verifica el código de ubicación o intenta con el nombre del producto.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:0.78rem;color:#475569;margin-bottom:0.8rem">{len(resultados)} resultado(s) encontrado(s)</div>', unsafe_allow_html=True)

            for _, row in resultados.iterrows():
                # Stock badge
                if row.stock == 0:
                    badge = '<span class="badge out">Sin stock</span>'
                elif row.stock < row.stock_minimo:
                    badge = '<span class="badge low">Stock bajo</span>'
                else:
                    badge = '<span class="badge ok">En stock</span>'

                # Breadcrumb de ubicación
                p, e, c, n, s = row.pasillo, row.estante, row.columna, row.nivel, row.espacio
                crumbs = [
                    ("Almacén", False),
                    (f"Pasillo {p}", False),
                    (f"Estante {e}", False),
                    (f"Columna {c}", False),
                    (f"Nivel {n}", False),
                    (f"Espacio {s}", True),
                ]
                crumb_html = ""
                for i, (label, active) in enumerate(crumbs):
                    cls = "loc-crumb active" if active else "loc-crumb"
                    crumb_html += f'<span class="{cls}">{label}</span>'
                    if i < len(crumbs) - 1:
                        crumb_html += '<span class="loc-arrow">›</span>'

                st.markdown(f"""
                <div class="result-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem">
                    <div>
                      <div class="result-sku">{row.sku}</div>
                      <div class="result-name">{row.nombre}</div>
                    </div>
                    {badge}
                  </div>

                  <div class="loc-path">{crumb_html}</div>

                  <div class="meta-grid">
                    <div class="meta-box">
                      <div class="meta-label">Código ubicación</div>
                      <div class="meta-val loc">{row.ubicacion}</div>
                    </div>
                    <div class="meta-box">
                      <div class="meta-label">Categoría</div>
                      <div class="meta-val">{row.categoria}</div>
                    </div>
                    <div class="meta-box">
                      <div class="meta-label">Stock actual</div>
                      <div class="meta-val">{row.stock} {row.unidad}</div>
                    </div>
                    <div class="meta-box">
                      <div class="meta-label">Stock mínimo</div>
                      <div class="meta-val">{row.stock_minimo} {row.unidad}</div>
                    </div>
                    <div class="meta-box">
                      <div class="meta-label">Peso unitario</div>
                      <div class="meta-val">{row.peso_kg} kg</div>
                    </div>
                    <div class="meta-box">
                      <div class="meta-label">Pasillo · Estante</div>
                      <div class="meta-val">{row.pasillo} · {row.estante}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Sugerencias rápidas
        st.markdown('<div style="font-size:0.78rem;color:#475569;margin-bottom:0.6rem">Búsquedas de ejemplo:</div>', unsafe_allow_html=True)
        ejemplos = df_inv.sample(6, random_state=7)["ubicacion"].tolist()
        cols = st.columns(6)
        for i, ej in enumerate(ejemplos):
            with cols[i]:
                if st.button(ej, key=f"ej_{ej}"):
                    st.session_state["_query_sug"] = ej
                    st.rerun()

        # Mostrar productos con stock bajo como alerta
        bajos = df_inv[(df_inv.stock > 0) & (df_inv.stock < df_inv.stock_minimo)].head(4)
        if not bajos.empty:
            st.markdown('<div style="font-size:0.72rem;color:#fb923c;text-transform:uppercase;letter-spacing:0.1em;margin:1.2rem 0 0.5rem">⚠ Alertas de stock bajo</div>', unsafe_allow_html=True)
            for _, row in bajos.iterrows():
                st.markdown(f"""
                <div style="background:#1a0f00;border:1px solid #92400e44;border-left:3px solid #fb923c;
                            border-radius:10px;padding:0.65rem 1rem;margin-bottom:6px;
                            display:flex;justify-content:space-between;align-items:center">
                  <div>
                    <span style="font-size:0.75rem;color:#fb923c;font-family:'JetBrains Mono',monospace">{row.ubicacion}</span>
                    <span style="margin-left:10px;font-size:0.9rem;color:#e2e8f0">{row.nombre}</span>
                  </div>
                  <span style="font-size:0.8rem;color:#fb923c">{row.stock}/{row.stock_minimo} {row.unidad}</span>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MAPA DEL ALMACÉN
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="map-section-title">Vista del almacén — selecciona pasillo y estante para inspeccionar</div>', unsafe_allow_html=True)

    col_sel1, col_sel2, col_sel3 = st.columns(3)
    with col_sel1:
        sel_pasillo = st.selectbox("Pasillo", PASILLOS, key="map_p")
    with col_sel2:
        sel_estante = st.selectbox("Estante", ESTANTES, key="map_e")
    with col_sel3:
        sel_columna = st.selectbox("Columna", COLUMNAS, key="map_c")

    # Filtrar para el estante seleccionado
    df_estante = df_inv[
        (df_inv.pasillo == sel_pasillo) &
        (df_inv.estante == sel_estante)
    ]

    # Construir grid visual: filas = niveles (6→1 arriba→abajo), cols = columnas (A-D) × espacios (1-4)
    st.markdown(f"""
    <div style="font-size:0.78rem;color:#475569;margin:1rem 0 0.6rem">
      Estante <b style="color:#38bdf8">Pasillo {sel_pasillo} · Estante {sel_estante}</b>
      — {len(df_estante)} producto(s) ubicado(s)
    </div>
    """, unsafe_allow_html=True)

    # Mapa por columna seleccionada (niveles × espacios)
    df_col = df_estante[df_estante.columna == sel_columna]

    # Encabezado de espacios
    header_cols = st.columns([1] + [2] * 4)
    with header_cols[0]:
        st.markdown('<div style="font-size:0.68rem;color:#334155;text-align:center;padding:4px">NIV.</div>', unsafe_allow_html=True)
    for s in ESPACIOS:
        with header_cols[s]:
            st.markdown(f'<div style="font-size:0.68rem;color:#475569;text-align:center;padding:4px;border-bottom:1px solid #1e2d4a">ESP {s}</div>', unsafe_allow_html=True)

    for nivel in reversed(NIVELES):
        row_cols = st.columns([1] + [2] * 4)
        with row_cols[0]:
            st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#4fc3f7;text-align:center;padding:6px 2px;line-height:2">N{nivel}</div>', unsafe_allow_html=True)
        for espacio in ESPACIOS:
            prod = df_col[(df_col.nivel == nivel) & (df_col.espacio == espacio)]
            with row_cols[espacio]:
                if prod.empty:
                    st.markdown(f"""
                    <div title="Vacío: {cod_ubicacion(sel_pasillo, sel_estante, sel_columna, nivel, espacio)}"
                         style="background:#0a0d15;border:1px dashed #1e2d4a;border-radius:6px;
                                height:54px;display:flex;align-items:center;justify-content:center;
                                font-size:0.62rem;color:#1e2d4a;text-align:center;cursor:default;
                                font-family:'JetBrains Mono',monospace">
                      VACÍO
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    r = prod.iloc[0]
                    loc = cod_ubicacion(sel_pasillo, sel_estante, sel_columna, nivel, espacio)
                    if r.stock == 0:
                        bg, border, txt, stk_color = "#1f0606", "#7f1d1d", "#fca5a5", "#f87171"
                    elif r.stock < r.stock_minimo:
                        bg, border, txt, stk_color = "#1c0f00", "#92400e", "#fcd34d", "#fb923c"
                    else:
                        bg, border, txt, stk_color = "#052018", "#166534", "#86efac", "#4ade80"

                    nombre_corto = r.nombre[:20] + "…" if len(r.nombre) > 20 else r.nombre
                    st.markdown(f"""
                    <div title="{r.nombre} | {r.sku} | Stock: {r.stock} {r.unidad}"
                         style="background:{bg};border:1px solid {border};border-radius:6px;
                                height:54px;padding:4px 5px;cursor:default;overflow:hidden">
                      <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                                  color:#38bdf8;line-height:1.2;margin-bottom:2px">{loc}</div>
                      <div style="font-size:0.62rem;color:{txt};line-height:1.2;overflow:hidden;
                                  text-overflow:ellipsis;white-space:nowrap" title="{r.nombre}">{nombre_corto}</div>
                      <div style="font-size:0.58rem;color:{stk_color};margin-top:2px">{r.stock} {r.unidad}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Leyenda
    st.markdown("""
    <div style="display:flex;gap:16px;margin-top:1rem;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:6px;font-size:0.75rem;color:#64748b">
        <div style="width:12px;height:12px;background:#052018;border:1px solid #166534;border-radius:3px"></div> Con stock
      </div>
      <div style="display:flex;align-items:center;gap:6px;font-size:0.75rem;color:#64748b">
        <div style="width:12px;height:12px;background:#1c0f00;border:1px solid #92400e;border-radius:3px"></div> Stock bajo
      </div>
      <div style="display:flex;align-items:center;gap:6px;font-size:0.75rem;color:#64748b">
        <div style="width:12px;height:12px;background:#1f0606;border:1px solid #7f1d1d;border-radius:3px"></div> Sin stock
      </div>
      <div style="display:flex;align-items:center;gap:6px;font-size:0.75rem;color:#64748b">
        <div style="width:12px;height:12px;background:#0a0d15;border:1px dashed #1e2d4a;border-radius:3px"></div> Vacío
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Vista panorámica de los 3 pasillos
    st.markdown('<div class="map-section-title" style="margin-top:2rem">Vista panorámica — ocupación por pasillo</div>', unsafe_allow_html=True)
    cols_pan = st.columns(3)
    for i, pasillo in enumerate(PASILLOS):
        with cols_pan[i]:
            df_p = df_inv[df_inv.pasillo == pasillo]
            total_slots = 4 * 4 * 6 * 4  # estantes × columnas × niveles × espacios
            ocupados    = len(df_p)
            pct = round(ocupados / total_slots * 100, 1)
            sin_st = len(df_p[df_p.stock == 0])
            st.markdown(f"""
            <div style="background:#0f1629;border:1px solid #1e2d4a;border-radius:12px;padding:1rem 1.2rem;text-align:center">
              <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;font-weight:600;color:#38bdf8">
                Pasillo {pasillo}
              </div>
              <div style="font-size:0.72rem;color:#475569;margin:0.3rem 0 0.8rem;text-transform:uppercase;letter-spacing:0.08em">
                {ocupados} productos · {pct}% ocupado
              </div>
              <div style="background:#131d35;border-radius:6px;height:8px;overflow:hidden;margin-bottom:0.8rem">
                <div style="height:100%;width:{pct}%;background:#38bdf8;border-radius:6px;transition:width 0.5s"></div>
              </div>
              <div style="font-size:0.78rem;color:#64748b">
                Sin stock: <span style="color:#f87171">{sin_st}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — INVENTARIO COMPLETO
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_pasillo = st.selectbox("Pasillo", ["Todos"] + PASILLOS, key="inv_p")
    with col_f2:
        cats = ["Todas"] + sorted(df_inv["categoria"].unique().tolist())
        filtro_cat = st.selectbox("Categoría", cats, key="inv_cat")
    with col_f3:
        filtro_stock = st.selectbox("Estado stock", ["Todos", "Con stock", "Stock bajo", "Sin stock"], key="inv_stk")

    df_show = df_inv.copy()
    if filtro_pasillo != "Todos":
        df_show = df_show[df_show.pasillo == filtro_pasillo]
    if filtro_cat != "Todas":
        df_show = df_show[df_show.categoria == filtro_cat]
    if filtro_stock == "Con stock":
        df_show = df_show[df_show.stock >= df_show.stock_minimo]
    elif filtro_stock == "Stock bajo":
        df_show = df_show[(df_show.stock > 0) & (df_show.stock < df_show.stock_minimo)]
    elif filtro_stock == "Sin stock":
        df_show = df_show[df_show.stock == 0]

    st.markdown(f'<div style="font-size:0.78rem;color:#475569;margin-bottom:0.6rem">{len(df_show)} registros</div>', unsafe_allow_html=True)

    df_tabla = df_show[["ubicacion", "sku", "nombre", "categoria", "stock", "stock_minimo", "unidad", "peso_kg"]].copy()
    df_tabla.columns = ["Ubicación", "SKU", "Nombre", "Categoría", "Stock", "Stock Mín.", "Unidad", "Peso (kg)"]
    st.dataframe(df_tabla, use_container_width=True, height=480, hide_index=True)
