import streamlit as st
from drugs import DRUGS

st.set_page_config(
    page_title="Drogas Vasoativas",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .result-card {
        background: linear-gradient(135deg, #1a3a5c, #0d2137);
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        margin-top: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .result-label {
        color: #90b8e0;
        font-size: 13px;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .result-value {
        color: #ffffff;
        font-size: 52px;
        font-weight: 700;
        line-height: 1;
    }
    .result-unit {
        color: #90b8e0;
        font-size: 18px;
        margin-top: 6px;
    }
    .preparo-card {
        background-color: #f0f4fa;
        border-left: 4px solid #1a3a5c;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin-bottom: 4px;
        color: #1a1a2e;
    }
    .preparo-card b { color: #1a3a5c; }
    .tag {
        display: inline-block;
        background: #e8f0fe;
        color: #1a3a5c;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Drogas Vasoativas")
st.caption("Calculadora de dose · ml/h ↔ mcg/kg/min")

# Seleção de droga com nome curto visível
drug_name = st.selectbox(
    "Droga",
    list(DRUGS.keys()),
    format_func=lambda x: f"{x}  ({DRUGS[x]['short']})",
)
drug_base = DRUGS[drug_name]

# Variante (apenas para drogas que têm mais de uma diluição)
if "variants" in drug_base:
    variant_name = st.radio("Diluição", list(drug_base["variants"].keys()), horizontal=True)
    drug = {**drug_base, **drug_base["variants"][variant_name]}
else:
    drug = drug_base

# Card de preparo
st.markdown(f"""
<div class="preparo-card">
    <b>Preparo:</b> {drug['preparo']}<br>
    <span class="tag">Vol. total: {drug['total_vol_ml']} ml</span>
    <span class="tag">Concentração: {drug['conc_mcg_ml']:.2f} mcg/ml</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# Direção da conversão
direction = st.radio(
    "Conversão",
    ["ml/h  →  mcg/kg/min", "mcg/kg/min  →  ml/h"],
    horizontal=True,
)

# Peso
weight = st.number_input(
    "Peso do paciente (kg)",
    min_value=1.0,
    max_value=300.0,
    value=70.0,
    step=1.0,
    format="%.1f",
)

st.divider()

# Entrada e cálculo
if direction == "ml/h  →  mcg/kg/min":
    rate = st.number_input(
        "Taxa da bomba (ml/h)",
        min_value=0.0,
        max_value=999.0,
        value=drug["rate_default"],
        step=0.1,
        format="%.1f",
    )
    result = (rate * drug["conc_mcg_ml"]) / (weight * 60)
    label = "Dose equivalente"
    value_str = f"{result:.4f}"
    unit = "mcg/kg/min"
else:
    dose = st.number_input(
        "Dose (mcg/kg/min)",
        min_value=0.0,
        max_value=9999.0,
        value=drug["dose_default"],
        step=drug["dose_step"],
        format="%.3f",
    )
    result = (dose * weight * 60) / drug["conc_mcg_ml"]
    label = "Taxa da bomba"
    value_str = f"{result:.2f}"
    unit = "ml/h"

st.markdown(f"""
<div class="result-card">
    <div class="result-label">{label}</div>
    <div class="result-value">{value_str}</div>
    <div class="result-unit">{unit}</div>
</div>
""", unsafe_allow_html=True)
