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
    .conc-info {
        background-color: #eef6ee;
        border-left: 4px solid #2e7d32;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-bottom: 4px;
        color: #1a1a2e;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Drogas Vasoativas")
st.caption("Calculadora de dose · ml/h ↔ mcg/kg/min · UI/h")

# Modo de operação
modo = st.radio(
    "Modo",
    ["Padrão HR", "Cálculo Manual"],
    horizontal=True,
)

st.divider()

# ── MODO PADRÃO HR ──────────────────────────────────────────────────────────
if modo == "Padrão HR":
    drug_name = st.selectbox(
        "Droga",
        list(DRUGS.keys()),
        format_func=lambda x: f"{x}  ({DRUGS[x]['short']})",
    )
    drug_base = DRUGS[drug_name]

    if "variants" in drug_base:
        variant_name = st.radio("Diluição", list(drug_base["variants"].keys()), horizontal=True)
        drug = {**drug_base, **drug_base["variants"][variant_name]}
    else:
        drug = drug_base

    st.markdown(f"""
    <div class="preparo-card">
        <b>Preparo:</b> {drug['preparo']}<br>
        <span class="tag">Vol. total: {drug['total_vol_ml']} ml</span>
        <span class="tag">Concentração: {drug['conc']:.2f} {drug['unit'].split('/')[0]}/ml</span>
    </div>
    """, unsafe_allow_html=True)

# ── MODO CÁLCULO MANUAL ──────────────────────────────────────────────────────
else:
    st.subheader("Configuração da solução")

    col1, col2, col3 = st.columns(3)
    n_amp = col1.number_input("Nº de ampolas", min_value=1, max_value=20, value=2, step=1)
    conc_amp = col2.number_input("Conc. por ampola", min_value=0.01, value=1.0, step=0.5, format="%.2f")
    drug_unit_amp = col3.selectbox("Unidade", ["mg/ml", "UI/ml"])

    col4, col5 = st.columns(2)
    vol_amp = col4.number_input("Volume por ampola (ml)", min_value=0.1, value=4.0, step=0.5, format="%.1f")
    vol_diluente = col5.number_input("Volume do diluente (ml)", min_value=0.0, value=92.0, step=1.0, format="%.1f")

    dose_unit = st.selectbox("Unidade da dose", ["mcg/kg/min", "UI/h", "mcg/min"])

    # Cálculos derivados
    total_drug = n_amp * conc_amp * vol_amp
    total_vol = (n_amp * vol_amp) + vol_diluente
    is_mg = drug_unit_amp == "mg/ml"
    conc_final = (total_drug * 1000 / total_vol) if is_mg else (total_drug / total_vol)
    conc_unit_label = "mcg" if is_mg else "UI"

    st.markdown(f"""
    <div class="conc-info">
        <b>Total de droga:</b> {total_drug:.2f} {'mg' if is_mg else 'UI'} &nbsp;|&nbsp;
        <b>Volume total:</b> {total_vol:.1f} ml &nbsp;|&nbsp;
        <b>Concentração:</b> {conc_final:.2f} {conc_unit_label}/ml
    </div>
    """, unsafe_allow_html=True)

    drug = {
        "conc": conc_final,
        "unit": dose_unit,
        "needs_weight": dose_unit in ("mcg/kg/min", "mcg/min"),
        "rate_default": 5.0,
        "dose_default": 0.1 if dose_unit == "mcg/kg/min" else 1.0,
        "dose_step": 0.01 if dose_unit == "mcg/kg/min" else 0.1,
    }

# ── CONVERSÃO (comum aos dois modos) ────────────────────────────────────────
st.divider()

unit = drug["unit"]
direction = st.radio(
    "Conversão",
    [f"ml/h  →  {unit}", f"{unit}  →  ml/h"],
    horizontal=True,
)

if drug["needs_weight"]:
    weight = st.number_input(
        "Peso do paciente (kg)",
        min_value=1.0,
        max_value=300.0,
        value=70.0,
        step=1.0,
        format="%.1f",
    )
else:
    weight = None

st.divider()

if direction == f"ml/h  →  {unit}":
    rate = st.number_input(
        "Taxa da bomba (ml/h)",
        min_value=0.0,
        max_value=999.0,
        value=drug["rate_default"],
        step=0.1,
        format="%.1f",
    )
    if unit == "mcg/kg/min":
        result = (rate * drug["conc"]) / (weight * 60)
    elif unit == "mcg/min":
        result = rate * drug["conc"]
    else:  # UI/h
        result = rate * drug["conc"]

    label = "Dose equivalente"
    value_str = f"{result:.4f}" if unit == "mcg/kg/min" else f"{result:.2f}"
    result_unit = unit

else:
    dose = st.number_input(
        f"Dose ({unit})",
        min_value=0.0,
        max_value=9999.0,
        value=drug["dose_default"],
        step=drug["dose_step"],
        format="%.3f" if unit == "mcg/kg/min" else "%.1f",
    )
    if unit == "mcg/kg/min":
        result = (dose * weight * 60) / drug["conc"]
    elif unit == "mcg/min":
        result = (dose * 60) / drug["conc"]
    else:  # UI/h
        result = dose / drug["conc"]

    label = "Taxa da bomba"
    value_str = f"{result:.2f}"
    result_unit = "ml/h"

st.markdown(f"""
<div class="result-card">
    <div class="result-label">{label}</div>
    <div class="result-value">{value_str}</div>
    <div class="result-unit">{result_unit}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Desenvolvido por Gustavo Roncolato")
