DRUGS = {
    "Noradrenalina": {
        "short": "Nora",
        "variants": {
            "Padrão — 2 amp": {
                "preparo": "2 amp (4ml × 1mg/ml) + 92ml SG",
                "total_vol_ml": 100.0,
                "conc_mcg_ml": 80.0,              # 8.000 mcg / 100ml
            },
            "Dobrada — 4 amp": {
                "preparo": "4 amp (4ml × 1mg/ml) + 92ml SG",
                "total_vol_ml": 108.0,
                "conc_mcg_ml": round(16_000 / 108, 2),  # ≈ 148.15 mcg/ml
            },
        },
        "rate_default": 5.0,
        "dose_default": 0.10,
        "dose_step": 0.01,
    },
    "Dobutamina": {
        "short": "Dobuta",
        "preparo": "2 amp (20ml × 12,5mg/ml) + 60ml SF",
        "total_vol_ml": 100.0,
        "conc_mcg_ml": 5000.0,        # 500.000 mcg / 100ml
        "rate_default": 5.0,
        "dose_default": 5.0,
        "dose_step": 0.5,
    },
    "Nitroprussiato": {
        "short": "Nipridi",
        "preparo": "1 amp (2ml × 25mg/ml) + 250ml SG 5%",
        "total_vol_ml": 252.0,
        "conc_mcg_ml": round(50_000 / 252, 2),   # ≈ 198.41 mcg/ml
        "rate_default": 10.0,
        "dose_default": 0.5,
        "dose_step": 0.1,
    },
    "Trinitrato": {
        "short": "Tridil",
        "preparo": "1 amp (5ml × 5mg/ml) + 100ml SG",
        "total_vol_ml": 105.0,
        "conc_mcg_ml": round(25_000 / 105, 2),   # ≈ 238.10 mcg/ml
        "rate_default": 10.0,
        "dose_default": 0.5,
        "dose_step": 0.1,
    },
}
