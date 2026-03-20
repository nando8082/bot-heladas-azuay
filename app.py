from pathlib import Path
import pandas as pd
import streamlit as st

# =========================================================
# CONFIGURACIÓN
# =========================================================
BASE_DIR = Path(__file__).resolve().parent

FILE_RIESGO_72H = BASE_DIR / "Reporte_Heladas_Azuay_Zonal_Stats.xlsx"
FILE_VULNERABILIDAD = BASE_DIR / "Azuay_Vulnerabilidad_por_Canton.xlsx"

CANTONES_ORDENADOS = [
    "Chordeleg",
    "El Pan",
    "Gualaceo",
    "Nabon",
    "Ona",
    "Sevilla de Oro",
    "Paute",
    "Cuenca",
    "Giron",
    "San Fernando",
    "Sigsig",
    "Camilo ponce enriquez",
    "Guachapala",
    "Pucara",
    "Santa Isabel",
]

MENU_PREGUNTAS = {
    "1": "En las próximas 72 horas existe el riesgo de helada?",
    "2": "A largo plazo mi terreno - producción es susceptible a heladas?",
}

MENU_CANTONES = {str(i + 1): canton for i, canton in enumerate(CANTONES_ORDENADOS)}

INTERPRETACIONES_VULNERABILIDAD = {
    "muy baja": """**Muy baja**

**Interpretación:**
- Zonas con mínima probabilidad de afectación por heladas.
- Condiciones climáticas relativamente estables o cálidas.
- Generalmente asociadas a:
  - Altitudes bajas
  - Alta cobertura vegetal protectora
  - Baja exposición térmica

**Implicación técnica:**
- No requieren medidas prioritarias.
- Aptas para agricultura sin riesgo significativo por heladas.""",
    "baja": """**Baja**

**Interpretación:**
- Existe riesgo leve de heladas ocasionales.
- Las condiciones pueden permitir eventos esporádicos.

**Implicación técnica:**
- Se recomienda monitoreo climático.
- Medidas preventivas básicas (calendario agrícola adaptado).""",
    "media": """**Media**

**Interpretación:**
- Zonas con riesgo moderado.
- Heladas pueden ocurrir con cierta frecuencia.

**Características típicas:**
- Transición altitudinal
- Suelos expuestos
- Variabilidad térmica significativa

**Implicación técnica:**
- Necesidad de:
  - Sistemas de alerta temprana
  - Selección de cultivos resistentes
  - Manejo agronómico adaptativo""",
    "alta": """**Alta**

**Interpretación:**
- Alta probabilidad de eventos de heladas.
- Impacto significativo en agricultura y ecosistemas.

**Características:**
- Zonas elevadas
- Baja cobertura vegetal
- Alta pérdida de calor nocturno

**Implicación técnica:**
- Requiere:
  - Estrategias de mitigación (coberturas, riego antiheladas)
  - Planificación territorial
  - Restricción de ciertos cultivos sensibles""",
    "muy alta": """**Muy alta**

**Interpretación:**
- Zonas críticas.
- Heladas frecuentes y severas.

**Características típicas:**
- Alta montaña / páramo
- Alta radiación nocturna
- Condiciones extremas (RCP 8.5 intensifica esto)

**Implicación técnica:**
- Uso del suelo altamente condicionado
- No apto para cultivos sensibles
- Prioridad para:
  - Conservación ecosistémica
  - Sistemas de alerta avanzada
  - Planes de adaptación climática""",
}


# =========================================================
# UTILIDADES
# =========================================================
def normalize_text(text: str) -> str:
    if text is None:
        return ""
    text = str(text).lower().strip()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    return " ".join(text.split())


def read_excel_first_sheet(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    return pd.read_excel(path)


def humanize_probability_percent(canton: str, prob_value) -> str:
    if pd.isna(prob_value):
        return f"No hay un valor disponible de probabilidad promedio para {canton}."

    prob = float(prob_value) * 100
    return (
        f"En {canton}, la probabilidad promedio registrada para heladas "
        f"en las próximas 72 horas es {prob:.2f}%."
    )


def humanize_dominant_class(canton: str, clase):
    if pd.isna(clase) or str(clase).strip() == "":
        return f"No hay una clase dominante disponible para {canton}.", None

    clase = str(clase).strip()
    return (
        f"En {canton}, la susceptibilidad dominante a largo plazo frente a heladas "
        f"corresponde a la categoría **{clase}**.\n\n"
        f"¿Quieres saber qué significa esto?\n"
        f"**1. Sí**\n"
        f"**2. No**"
    ), clase


def get_interpretacion_vulnerabilidad(clase: str) -> str:
    clave = normalize_text(clase)
    return INTERPRETACIONES_VULNERABILIDAD.get(
        clave, f"No tengo una interpretación configurada para la clase **{clase}**."
    )


def menu_preguntas_text() -> str:
    lines = [
        "Bienvenido al bot de consulta de heladas para Azuay.",
        "Seleccione el tipo de consulta escribiendo el número correspondiente:",
        "",
        "1. En las próximas 72 horas existe el riesgo de helada?",
        "2. A largo plazo mi terreno - producción es susceptible a heladas?",
        "",
        "Ejemplo: escriba 1 o 2.",
    ]
    return "\n".join(lines)


def menu_cantones_text() -> str:
    lines = ["Ahora seleccione su cantón escribiendo el número correspondiente:", ""]
    for num, canton in MENU_CANTONES.items():
        lines.append(f"{num}. {canton}")
    lines.append("")
    lines.append("Ejemplo: escriba 8 para consultar Cuenca.")
    return "\n".join(lines)


# =========================================================
# CARGA DE DATOS
# =========================================================
@st.cache_data
def load_riesgo_72h(path: Path) -> pd.DataFrame:
    df = read_excel_first_sheet(path)
    df.columns = [str(c).strip() for c in df.columns]

    required = ["Canton_Parroquia", "Probabilidad_Promedio"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas en riesgo 72h: {missing}")

    df["Canton_Parroquia"] = df["Canton_Parroquia"].astype(str).str.strip()
    df["Probabilidad_Promedio"] = pd.to_numeric(
        df["Probabilidad_Promedio"], errors="coerce"
    )
    df["canton_norm"] = df["Canton_Parroquia"].apply(normalize_text)
    df = df.drop_duplicates(subset=["canton_norm"], keep="first").reset_index(drop=True)
    return df


@st.cache_data
def load_vulnerabilidad(path: Path) -> pd.DataFrame:
    df = read_excel_first_sheet(path)
    df.columns = [str(c).strip() for c in df.columns]

    required = ["Canton", "Clase_dominante"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas en vulnerabilidad: {missing}")

    df["Canton"] = df["Canton"].astype(str).str.strip()
    df["Clase_dominante"] = df["Clase_dominante"].astype(str).str.strip()
    df["canton_norm"] = df["Canton"].apply(normalize_text)
    df = df.drop_duplicates(subset=["canton_norm"], keep="first").reset_index(drop=True)
    return df


def build_map(df: pd.DataFrame, canton_col: str) -> dict:
    return {normalize_text(row[canton_col]): row for _, row in df.iterrows()}


# =========================================================
# RESPUESTAS
# =========================================================
def get_response(
    question_option: str, canton_option: str, map_72h: dict, map_vuln: dict
):
    if question_option not in MENU_PREGUNTAS:
        return "Debe elegir primero 1 o 2.", None

    if canton_option not in MENU_CANTONES:
        return "Debe elegir un cantón con un número del 1 al 15.", None

    canton_menu = MENU_CANTONES[canton_option]
    key = normalize_text(canton_menu)

    if question_option == "1":
        row = map_72h.get(key)
        if row is None:
            return (
                f"No encontré datos de riesgo de helada a 72 horas para {canton_menu}.",
                None,
            )
        return (
            humanize_probability_percent(
                row["Canton_Parroquia"], row["Probabilidad_Promedio"]
            ),
            None,
        )

    if question_option == "2":
        row = map_vuln.get(key)
        if row is None:
            return (
                f"No encontré datos de susceptibilidad a largo plazo para {canton_menu}.",
                None,
            )
        return humanize_dominant_class(row["Canton"], row["Clase_dominante"])

    return "No se pudo procesar la consulta.", None


# =========================================================
# INTERFAZ STREAMLIT
# =========================================================
st.set_page_config(page_title="Bot Heladas Azuay", layout="wide")
st.title("Bot de consulta de heladas - Azuay")

try:
    df_72h = load_riesgo_72h(FILE_RIESGO_72H)
    df_vuln = load_vulnerabilidad(FILE_VULNERABILIDAD)
except Exception as e:
    st.error(str(e))
    st.stop()

map_72h = build_map(df_72h, "Canton_Parroquia")
map_vuln = build_map(df_vuln, "Canton")

with st.sidebar:
    st.header("Opciones de consulta")
    st.markdown(menu_preguntas_text())

    st.header("Cantones")
    st.markdown(menu_cantones_text())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": menu_preguntas_text()}
    ]

if "step" not in st.session_state:
    st.session_state.step = "choose_question"

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

if "pending_class" not in st.session_state:
    st.session_state.pending_class = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Escriba su opción...")

if prompt:
    prompt_clean = prompt.strip()
    prompt_norm = normalize_text(prompt_clean)

    st.session_state.messages.append({"role": "user", "content": prompt_clean})

    with st.chat_message("user"):
        st.markdown(prompt_clean)

    if st.session_state.step == "choose_question":
        if prompt_clean in MENU_PREGUNTAS:
            st.session_state.selected_question = prompt_clean
            st.session_state.step = "choose_canton"
            response = (
                f"Ha seleccionado:\n**{MENU_PREGUNTAS[prompt_clean]}**\n\n"
                f"{menu_cantones_text()}"
            )
        else:
            response = "Entrada no válida. Debe escribir 1 o 2."

    elif st.session_state.step == "choose_canton":
        if prompt_clean in MENU_CANTONES:
            response_main, detected_class = get_response(
                st.session_state.selected_question, prompt_clean, map_72h, map_vuln
            )

            if st.session_state.selected_question == "2" and detected_class:
                st.session_state.pending_class = detected_class
                st.session_state.step = "explain_vulnerability"
                response = response_main
            else:
                response = (
                    f"{response_main}\n\n"
                    f"Si desea hacer otra consulta, escriba **menu**."
                )
                st.session_state.step = "finished"
        else:
            response = "Entrada no válida. Debe escribir un número del 1 al 15."

    elif st.session_state.step == "explain_vulnerability":
        if prompt_clean == "1":
            interpretacion = get_interpretacion_vulnerabilidad(
                st.session_state.pending_class
            )
            response = (
                f"{interpretacion}\n\n"
                f"Si desea hacer otra consulta, escriba **menu**."
            )
            st.session_state.step = "finished"
            st.session_state.pending_class = None

        elif prompt_clean == "2":
            response = "Entendido. Si desea hacer otra consulta, escriba **menu**."
            st.session_state.step = "finished"
            st.session_state.pending_class = None

        else:
            response = "Respuesta no válida. Escriba **1** para Sí o **2** para No."

    else:
        if prompt_norm in {"menu", "inicio", "start", "hola"}:
            st.session_state.step = "choose_question"
            st.session_state.selected_question = None
            st.session_state.pending_class = None
            response = menu_preguntas_text()
        else:
            response = "Escriba **menu** para volver al inicio."

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)
