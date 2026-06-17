// ── Dados das drogas (portado de drugs.py) ────────────────────────────────
const DRUGS = {
  'Noradrenalina': {
    short: 'Nora',
    variants: {
      'Padrão — 2 amp': { preparo: '2 amp (4ml × 1mg/ml) + 92ml SG',  total_vol_ml: 100, conc: 80     },
      'Dobrada — 4 amp': { preparo: '4 amp (4ml × 1mg/ml) + 92ml SG', total_vol_ml: 108, conc: 148.15 },
    },
    unit: 'mcg/kg/min', needs_weight: true,
    rate_default: 5, dose_default: 0.10, dose_step: 0.01,
  },
  'Dobutamina': {
    short: 'Dobuta',
    preparo: '2 amp (20ml × 12,5mg/ml) + 60ml SF',
    total_vol_ml: 100, conc: 5000,
    unit: 'mcg/kg/min', needs_weight: true,
    rate_default: 5, dose_default: 5, dose_step: 0.5,
  },
  'Nitroprussiato': {
    short: 'Nipride',
    preparo: '1 amp (2ml × 25mg/ml) + 250ml SG 5%',
    total_vol_ml: 252, conc: 198.41,
    unit: 'mcg/kg/min', needs_weight: true,
    rate_default: 10, dose_default: 0.5, dose_step: 0.1,
  },
  'Trinitrato': {
    short: 'Tridil',
    preparo: '1 amp (5ml × 5mg/ml) + 100ml SG',
    total_vol_ml: 105, conc: 238.10,
    unit: 'mcg/kg/min', needs_weight: true,
    rate_default: 10, dose_default: 0.5, dose_step: 0.1,
  },
  'Vasopressina': {
    short: 'Vaso',
    preparo: '1 amp (1ml × 20 UI/ml) + 99ml SF 0,9%',
    total_vol_ml: 100, conc: 0.2,
    unit: 'UI/h', needs_weight: false,
    rate_default: 10, dose_default: 1, dose_step: 0.1,
  },
};

// ── Estado da aplicação ───────────────────────────────────────────────────
const state = {
  mode: 'padrao',
  drugName: 'Noradrenalina',
  variantName: 'Padrão — 2 amp',
  direction: 'rate_to_dose',
};

// ── Helpers ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const val = id => parseFloat($(id).value) || 0;

function getActiveDrug() {
  if (state.mode === 'manual') return getManualDrug();
  const base = DRUGS[state.drugName];
  return base.variants ? { ...base, ...base.variants[state.variantName] } : base;
}

function getManualDrug() {
  const nAmp      = val('n-amp');
  const concAmp   = val('conc-amp');
  const unitAmp   = $('drug-unit-amp').value;
  const volAmp    = val('vol-amp');
  const volDil    = val('vol-diluente');
  const doseUnit  = $('dose-unit-manual').value;

  const totalDrug = nAmp * concAmp * volAmp;
  const totalVol  = (nAmp * volAmp) + volDil;
  const isMg      = unitAmp === 'mg/ml';
  const conc      = totalVol > 0 ? (isMg ? totalDrug * 1000 / totalVol : totalDrug / totalVol) : 0;
  const concLabel = isMg ? 'mcg' : 'UI';

  $('manual-conc-info').innerHTML =
    `<strong>Total:</strong> ${totalDrug.toFixed(2)} ${isMg ? 'mg' : 'UI'} &nbsp;|&nbsp; ` +
    `<strong>Vol. total:</strong> ${totalVol.toFixed(1)} ml &nbsp;|&nbsp; ` +
    `<strong>Concentração:</strong> ${conc.toFixed(2)} ${concLabel}/ml`;

  return {
    conc, unit: doseUnit,
    needs_weight: doseUnit !== 'UI/h',
    rate_default: 5,
    dose_default: doseUnit === 'mcg/kg/min' ? 0.1 : 1,
    dose_step:    doseUnit === 'mcg/kg/min' ? 0.01 : 0.1,
  };
}

// ── Cálculo ───────────────────────────────────────────────────────────────
function calculate() {
  const drug   = getActiveDrug();
  const unit   = drug.unit;
  const input  = val('main-input');
  const weight = val('weight');
  const rtd    = state.direction === 'rate_to_dose';

  let result;
  if (rtd) {
    result = unit === 'mcg/kg/min'
      ? (input * drug.conc) / (weight * 60)
      : input * drug.conc;
  } else {
    if (unit === 'mcg/kg/min') result = (input * weight * 60) / drug.conc;
    else if (unit === 'mcg/min') result = (input * 60) / drug.conc;
    else result = input / drug.conc;
  }

  $('result-label').textContent = rtd ? 'Dose equivalente' : 'Taxa da bomba';
  $('result-unit').textContent  = rtd ? unit : 'ml/h';

  const dec = (rtd && unit === 'mcg/kg/min') ? 4 : 2;
  $('result-value').textContent = (isNaN(result) || !isFinite(result)) ? '—' : result.toFixed(dec);
}

// ── Atualização de UI ─────────────────────────────────────────────────────
function updateUI() {
  const drug = getActiveDrug();
  const unit = drug.unit;
  const rtd  = state.direction === 'rate_to_dose';

  $('weight-card').style.display = drug.needs_weight ? 'block' : 'none';

  const [btn0, btn1] = document.querySelectorAll('#direction-toggle .toggle');
  btn0.textContent = `ml/h → ${unit}`;
  btn1.textContent = `${unit} → ml/h`;

  $('input-label').textContent = rtd ? 'Taxa da bomba (ml/h)' : `Dose (${unit})`;
  $('main-input').step = rtd ? 0.1 : drug.dose_step;

  calculate();
}

function updateDrugUI() {
  const base = DRUGS[state.drugName];
  const drug = getActiveDrug();

  // Variante
  const variantCard = $('variant-card');
  if (base.variants) {
    variantCard.style.display = 'block';
    const vt = $('variant-toggle');
    vt.innerHTML = '';
    Object.keys(base.variants).forEach(name => {
      const btn = document.createElement('button');
      btn.className = 'toggle' + (name === state.variantName ? ' active' : '');
      btn.textContent = name;
      btn.dataset.value = name;
      btn.onclick = () => {
        state.variantName = name;
        vt.querySelectorAll('.toggle').forEach(b => b.classList.toggle('active', b.dataset.value === name));
        updateUI();
      };
      vt.appendChild(btn);
    });
  } else {
    variantCard.style.display = 'none';
  }

  // Preparo card
  const concLabel = drug.unit === 'UI/h' ? 'UI' : 'mcg';
  $('preparo-text').innerHTML = `<strong>Preparo:</strong> ${drug.preparo}`;
  $('preparo-tags').innerHTML =
    `<span class="tag">Vol. total: ${drug.total_vol_ml} ml</span>` +
    `<span class="tag">Concentração: ${drug.conc.toFixed(2)} ${concLabel}/ml</span>`;

  updateUI();
}

// ── Toggle genérico ───────────────────────────────────────────────────────
function initToggle(groupId, onChange) {
  $(groupId).addEventListener('click', e => {
    const btn = e.target.closest('.toggle');
    if (!btn) return;
    $(groupId).querySelectorAll('.toggle').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    onChange(btn.dataset.value);
  });
}

// ── Init ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Popula select de drogas
  const sel = $('drug-select');
  Object.entries(DRUGS).forEach(([name, d]) => {
    const opt = document.createElement('option');
    opt.value = name;
    opt.textContent = `${name}  (${d.short})`;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', () => {
    state.drugName    = sel.value;
    state.variantName = DRUGS[sel.value].variants
      ? Object.keys(DRUGS[sel.value].variants)[0] : null;
    updateDrugUI();
  });

  // Modo
  initToggle('mode-toggle', value => {
    state.mode = value;
    $('padrao-section').style.display = value === 'padrao' ? 'block' : 'none';
    $('manual-section').style.display = value === 'manual' ? 'block' : 'none';
    updateUI();
  });

  // Direção
  initToggle('direction-toggle', value => {
    state.direction = value;
    const drug = getActiveDrug();
    $('main-input').value = value === 'rate_to_dose' ? drug.rate_default : drug.dose_default;
    updateUI();
  });

  // Inputs ao vivo
  ['weight', 'main-input', 'n-amp', 'conc-amp', 'vol-amp', 'vol-diluente'].forEach(id => {
    $(id).addEventListener('input', updateUI);
  });
  $('drug-unit-amp').addEventListener('change', updateUI);
  $('dose-unit-manual').addEventListener('change', updateUI);

  // Hint de instalação iOS
  const isIos = /iphone|ipad|ipod/.test(navigator.userAgent.toLowerCase());
  const isStandalone = window.navigator.standalone;
  if (isIos && !isStandalone) $('install-hint').style.display = 'block';

  updateDrugUI();

  // Service Worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js').catch(console.error);
  }
});
