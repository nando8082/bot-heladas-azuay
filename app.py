import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portal de Visualización",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APPS = [
    {
        "nombre": "Visor de Heladas",
        "descripcion": "Visualización interactiva de zonas con riesgo de heladas en Google Earth Engine.",
        "url": "https://entrenamiento-490300.projects.earthengine.app/view/heladas",
        "categoria": "Geoespacial",
        "color": "#1D4ED8",
    },
    {
        "nombre": "Probabilidad de heladas con ML",
        "descripcion": "Visualizador de alerta temprana basado en modelos de aprendizaje automático.",
        "url": "https://entrenamiento-490300.projects.earthengine.app/view/alerta-temprana-ml",
        "categoria": "Machine Learning",
        "color": "#059669",
    },
    {
        "nombre": "Proyección de temperatura mínima nocturna",
        "descripcion": "Visualizador predictivo de heladas para análisis prospectivo en Azuay.",
        "url": "https://azuay-temperatura.projects.earthengine.app/view/tendencia2030",
        "categoria": "Machine Learning",
        "color": "#7C3AED",
    },
]

BOT_URL = "https://bot-heladas-azuay-7vqckud6x8ve7jvsgakm3x.streamlit.app/"

st.markdown(
    """
<style>
/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
}

/* Ocultar elementos por defecto */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero */
.hero-box {
    background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 100%);
    color: white;
    padding: 2.2rem 2rem;
    border-radius: 22px;
    box-shadow: 0 15px 40px rgba(15, 23, 42, 0.18);
    margin-bottom: 1.2rem;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    margin-bottom: 0.35rem;
}
.hero-subtitle {
    font-size: 1rem;
    opacity: 0.9;
    line-height: 1.5;
}

/* Caja de controles */
.control-box {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 18px;
    padding: 1rem 1rem 0.8rem 1rem;
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
    margin-bottom: 1rem;
}

/* Tarjeta lateral */
.card {
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 20px;
    padding: 1.2rem;
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}
.badge {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.8rem;
}
.card-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.45rem;
}
.card-text {
    color: #475569;
    font-size: 0.96rem;
    line-height: 1.5;
}

/* Caja del bot */
.bot-card {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
    color: white;
    border-radius: 20px;
    padding: 1.2rem;
    box-shadow: 0 12px 30px rgba(15,23,42,0.18);
    margin-bottom: 1rem;
}
.bot-card-title {
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}
.bot-card-text {
    font-size: 0.95rem;
    line-height: 1.5;
    opacity: 0.95;
}

/* Visor */
.viewer-box {
    background: white;
    border-radius: 22px;
    padding: 1rem;
    box-shadow: 0 12px 30px rgba(15,23,42,0.1);
    border: 1px solid rgba(148,163,184,0.16);
}

/* Corrección de colores en controles Streamlit */
div[data-testid="stSelectbox"] label,
div[data-testid="stRadio"] label,
div[data-testid="stSelectbox"] p,
div[data-testid="stRadio"] p {
    color: #0f172a !important;
    font-weight: 600;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    color: #0f172a !important;
    background-color: white !important;
}

div[data-testid="stSelectbox"] span,
div[data-testid="stSelectbox"] input,
div[data-testid="stSelectbox"] div {
    color: #0f172a !important;
}

div[role="radiogroup"] label,
div[role="radiogroup"] label p,
div[role="radiogroup"] label div {
    color: #0f172a !important;
}

div[data-testid="stHeading"] h3 {
    color: #0f172a !important;
}

/* Botones Streamlit */
.stLinkButton a {
    border-radius: 12px !important;
    font-weight: 600 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-box">
    <div class="hero-title">Portal Profesional de Visualización</div>
    <div class="hero-subtitle">
        Plataforma para centralizar visores geoespaciales, modelos predictivos y herramientas analíticas.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

nombres_apps = [app["nombre"] for app in APPS]

st.markdown('<div class="control-box">', unsafe_allow_html=True)
col_control_1, col_control_2 = st.columns([2, 1])

with col_control_1:
    app_seleccionada = st.selectbox("Selecciona un visualizador", nombres_apps)

with col_control_2:
    modo_visualizacion = st.radio(
        "Modo",
        ["Embebido", "Abrir enlace"],
        index=0,
        horizontal=False,
    )

st.markdown("</div>", unsafe_allow_html=True)

altura_iframe = 950
app_actual = next(app for app in APPS if app["nombre"] == app_seleccionada)

col1, col2 = st.columns([1, 2.8], gap="large")

with col1:
    st.markdown(
        f"""
        <div class="card">
            <div class="badge" style="background:{app_actual['color']};">
                {app_actual['categoria']}
            </div>
            <div class="card-title">{app_actual['nombre']}</div>
            <div class="card-text">{app_actual['descripcion']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "Abrir visualizador en nueva pestaña",
        app_actual["url"],
        width="stretch",
    )

    st.markdown(
        """
        <div class="bot-card">
            <div class="bot-card-title">Asistente de Heladas</div>
            <div class="bot-card-text">
                Acceda al bot para consultar riesgo de heladas y susceptibilidad por cantón.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "💬 Abrir bot en nueva pestaña",
        BOT_URL,
        width="stretch",
    )

with col2:
    st.markdown('<div class="viewer-box">', unsafe_allow_html=True)
    st.subheader(app_actual["nombre"])

    if modo_visualizacion == "Embebido":
        iframe_html = f"""
        <iframe
            src="{app_actual['url']}"
            width="100%"
            height="{altura_iframe}"
            frameborder="0"
            style="border-radius: 16px; border: 1px solid #e2e8f0;"
            allowfullscreen>
        </iframe>
        """
        components.html(iframe_html, height=altura_iframe + 20, scrolling=True)
    else:
        st.link_button("Ir al visor", app_actual["url"], width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)
