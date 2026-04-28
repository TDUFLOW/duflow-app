from flask import Flask, render_template_string, request, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return get_default_data()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_default_data():
    return {
        "series": [
            {"id":1,"nom":"BEAUBOURG","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":2,"nom":"LAS MANOS","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":3,"nom":"LE TUBE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":4,"nom":"FAIRE FACE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":5,"nom":"MA DOUCE ECOLE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":6,"nom":"SPREAD OF LOVE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7R III","photo":""},
            {"id":7,"nom":"D ACIER ET D OR XXL","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":8,"nom":"LITTLE HOUSE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":9,"nom":"FOG","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":10,"nom":"ENTRE OMBRE ET LUMIERE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":11,"nom":"SHORDITCH","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":12,"nom":"USINE A TOURTEAUX","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":13,"nom":"POINT DE RETRAITE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":14,"nom":"WRAPPED","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":15,"nom":"LA PIERRE","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""},
            {"id":16,"nom":"DU FLOW","exemplaires":10,"papier":"Fine art CANSON","appareil":"SONY A7 III","photo":""}
        ],
        "ventes": [
            {"id":1,"serie_id":7,"numero":1,"nom":"BARRE","prenom":"Laurent","valeur":650,"expo":"","date":""},
            {"id":2,"serie_id":11,"numero":5,"nom":"BRANGER","prenom":"Pascal","valeur":200,"expo":"MAM23","date":""},
            {"id":3,"serie_id":11,"numero":10,"nom":"PHIRMIS","prenom":"Mylene","valeur":350,"expo":"EXPO 2SAINT","date":""},
            {"id":4,"serie_id":15,"numero":1,"nom":"LE BELLEVUE","prenom":"JB","valeur":180,"expo":"EXPO CONCERT","date":""}
        ]
    }

HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DU FLOW</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Montserrat',sans-serif;background:#080808;color:#fff;min-height:100vh;}
.nav{position:sticky;top:0;z-index:200;background:rgba(8,8,8,0.97);backdrop-filter:blur(10px);
  border-bottom:1px solid #1a1a1a;display:flex;align-items:center;padding:0 40px;height:64px;gap:8px;}
.nav-logo{font-size:18px;font-weight:900;letter-spacing:6px;color:#fff;margin-right:30px;}
.nav-logo span{color:#c8a96e;}
.nav-btn{padding:8px 16px;font-family:'Montserrat',sans-serif;font-size:9px;font-weight:600;
  letter-spacing:2px;color:#666;background:transparent;border:none;cursor:pointer;
  transition:all 0.2s;text-transform:uppercase;}
.nav-btn:hover{color:#ccc;}
.nav-btn.active{color:#c8a96e;}
.nav-right{margin-left:auto;}
.btn-gold{padding:9px 20px;background:#c8a96e;color:#000;font-family:'Montserrat',sans-serif;
  font-size:9px;font-weight:700;letter-spacing:2px;border:none;cursor:pointer;transition:all 0.2s;}
.btn-gold:hover{background:#e0c080;}
.page{display:none;padding:50px 40px;}
.page.active{display:block;}
.page-title{font-size:9px;letter-spacing:4px;color:#555;text-transform:uppercase;margin-bottom:40px;}
.toast{position:fixed;bottom:30px;right:30px;background:#c8a96e;color:#000;
  padding:12px 24px;font-size:9px;letter-spacing:2px;font-weight:700;z-index:999;
  opacity:0;transition:opacity 0.3s;pointer-events:none;}
.toast.show{opacity:1;}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#1a1a1a;margin-bottom:1px;}
.kpi{background:#0a0a0a;padding:32px 28px;}
.kpi-val{font-size:42px;font-weight:900;letter-spacing:-2px;line-height:1;margin-bottom:8px;}
.kpi-val.gold{color:#c8a96e;}
.kpi-val.white{color:#e8e8e8;}
.kpi-lbl{font-size:8px;letter-spacing:3px;color:#444;text-transform:uppercase;}
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#1a1a1a;margin-bottom:1px;}
.chart-card{background:#0a0a0a;padding:32px;}
.chart-card h4{font-size:8px;letter-spacing:3px;color:#444;text-transform:uppercase;margin-bottom:25px;}
.chart-wrap{position:relative;height:230px;}
.section-title{font-size:8px;letter-spacing:3px;color:#444;text-transform:uppercase;
  padding:24px 0 20px;border-bottom:1px solid #0f0f0f;margin-bottom:0;}
.series-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;background:#1a1a1a;}
.sg-card{background:#0a0a0a;padding:24px;cursor:pointer;transition:background 0.2s;}
.sg-card:hover{background:#0f0f0f;}
.sg-nom{font-size:11px;font-weight:700;letter-spacing:3px;margin-bottom:12px;color:#e0e0e0;}
.sg-bar-bg{height:1px;background:#1a1a1a;margin-bottom:10px;}
.sg-bar{height:100%;background:#c8a96e;transition:width 0.5s;}
.sg-info{display:flex;justify-content:space-between;font-size:9px;color:#444;}
.sg-info span:last-child{color:#c8a96e;font-weight:700;}
.series-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1px;background:#1a1a1a;}
.sl-card{background:#0a0a0a;padding:28px;}
.sl-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;}
.sl-nom{font-size:13px;font-weight:900;letter-spacing:3px;color:#fff;}
.sl-count{font-size:28px;font-weight:900;color:#c8a96e;line-height:1;}
.sl-count small{font-size:12px;color:#555;font-weight:400;}
.sl-info{font-size:9px;color:#444;letter-spacing:1px;margin-bottom:16px;}
.sl-bar-bg{height:1px;background:#1a1a1a;margin-bottom:16px;}
.sl-bar{height:100%;background:#c8a96e;}
.sl-actions{display:flex;gap:8px;}
.btn-voir{flex:1;padding:10px;background:transparent;border:1px solid #222;color:#888;
  font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:2px;font-weight:600;
  cursor:pointer;transition:all 0.2s;text-transform:uppercase;}
.btn-voir:hover{border-color:#c8a96e;color:#c8a96e;}
.btn-sup{padding:10px 12px;background:transparent;border:1px solid #1a1a1a;color:#333;
  font-size:11px;cursor:pointer;transition:all 0.2s;}
.btn-sup:hover{border-color:#ff3333;color:#ff3333;}
.back-btn{display:inline-flex;align-items:center;gap:8px;font-size:9px;letter-spacing:2px;
  color:#555;cursor:pointer;margin-bottom:35px;background:none;border:none;
  font-family:'Montserrat',sans-serif;transition:color 0.2s;text-transform:uppercase;}
.back-btn:hover{color:#c8a96e;}
.detail-hdr{display:flex;justify-content:space-between;align-items:flex-end;
  padding-bottom:28px;border-bottom:1px solid #1a1a1a;margin-bottom:35px;}
.detail-hdr h1{font-size:36px;font-weight:900;letter-spacing:6px;margin-bottom:6px;color:#f0f0f0;}
.detail-hdr p{font-size:10px;color:#444;letter-spacing:1px;}
.detail-right{text-align:right;}
.detail-big{font-size:48px;font-weight:900;color:#c8a96e;line-height:1;}
.detail-big small{font-size:18px;color:#444;font-weight:400;}
.detail-ca{font-size:12px;color:#555;margin-top:6px;}
table{width:100%;border-collapse:collapse;}
thead tr{border-bottom:1px solid #111;}
thead th{font-size:8px;letter-spacing:2px;color:#333;text-transform:uppercase;padding:12px 16px;text-align:left;font-weight:600;}
tbody tr{border-bottom:1px solid #0a0a0a;transition:background 0.15s;}
tbody tr:hover{background:#0d0d0d;}
tbody td{padding:14px 16px;font-size:11px;vertical-align:middle;}
.num-cell{width:28px;height:28px;border:1px solid #1e1e1e;display:flex;align-items:center;
  justify-content:center;font-size:9px;font-weight:700;color:#444;}
.num-cell.sold{border-color:#c8a96e;color:#c8a96e;}
.badge{display:inline-block;padding:3px 10px;font-size:8px;letter-spacing:2px;font-weight:700;}
.b-sold{background:rgba(200,169,110,0.1);color:#c8a96e;}
.b-free{background:#0f0f0f;color:#333;}
.buyer{font-size:11px;font-weight:700;color:#e0e0e0;}
.buyer-s{font-size:9px;color:#555;margin-top:2px;}
.price{color:#c8a96e;font-weight:700;}
.dim{color:#222;}
.tb{padding:6px 12px;font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:1px;
  font-weight:600;cursor:pointer;background:transparent;transition:all 0.2s;border:1px solid;}
.tb-sell{border-color:rgba(200,169,110,0.4);color:#c8a96e;}
.tb-sell:hover{background:#c8a96e;color:#000;}
.tb-edit{border-color:#1e1e1e;color:#555;margin-right:6px;}
.tb-edit:hover{border-color:#fff;color:#e0e0e0;}
.tb-del{border-color:#141414;color:#2a2a2a;width:30px;height:30px;padding:0;
  display:inline-flex;align-items:center;justify-content:center;}
.tb-del:hover{border-color:#ff3333;color:#ff3333;}
.acts{display:flex;align-items:center;gap:6px;}
.photo-section{margin-top:40px;border:1px solid #1a1a1a;background:#0a0a0a;}
.photo-section-hdr{padding:20px 24px;border-bottom:1px solid #141414;display:flex;justify-content:space-between;align-items:center;}
.photo-section-hdr span{font-size:8px;letter-spacing:3px;color:#444;text-transform:uppercase;}
.photo-upload-zone{padding:30px;text-align:center;}
.photo-preview{width:100%;max-height:500px;object-fit:contain;display:block;}
.photo-placeholder{border:1px dashed #1e1e1e;padding:50px;cursor:pointer;transition:all 0.2s;display:flex;
  flex-direction:column;align-items:center;gap:12px;}
.photo-placeholder:hover{border-color:#c8a96e;}
.photo-placeholder .icon{font-size:28px;color:#333;}
.photo-placeholder p{font-size:9px;letter-spacing:2px;color:#444;text-transform:uppercase;}
.photo-placeholder p small{display:block;font-size:8px;color:#2a2a2a;margin-top:4px;}
#photo-input{display:none;}
.photo-actions{display:flex;gap:8px;justify-content:center;margin-top:16px;}
.btn-change-photo{padding:8px 16px;background:transparent;border:1px solid #222;color:#666;
  font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:2px;cursor:pointer;transition:all 0.2s;}
.btn-change-photo:hover{border-color:#c8a96e;color:#c8a96e;}
.btn-del-photo{padding:8px 12px;background:transparent;border:1px solid #141414;color:#333;
  font-family:'Montserrat',sans-serif;font-size:8px;cursor:pointer;transition:all 0.2s;}
.btn-del-photo:hover{border-color:#ff3333;color:#ff3333;}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.93);z-index:500;
  align-items:center;justify-content:center;}
.overlay.show{display:flex;}
.modal{background:#0c0c0c;border:1px solid #1e1e1e;width:460px;max-width:95vw;padding:44px;}
.modal-title{font-size:10px;letter-spacing:4px;color:#c8a96e;margin-bottom:32px;text-transform:uppercase;}
.field{margin-bottom:18px;}
.field label{display:block;font-size:8px;letter-spacing:2px;color:#555;margin-bottom:8px;text-transform:uppercase;}
.field input,.field select{width:100%;background:#111;border:1px solid #1a1a1a;color:#e8e8e8;
  padding:12px 14px;font-family:'Montserrat',sans-serif;font-size:12px;outline:none;transition:border 0.2s;}
.field input:focus,.field select:focus{border-color:#c8a96e;}
.field input::placeholder{color:#333;}
.field select option{background:#111;}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:15px;}
.modal-foot{display:flex;gap:10px;justify-content:flex-end;margin-top:32px;
  padding-top:22px;border-top:1px solid #111;}
.btn-cancel{padding:10px 20px;background:transparent;border:1px solid #1e1e1e;color:#555;
  font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:2px;cursor:pointer;transition:all 0.2s;}
.btn-cancel:hover{color:#e0e0e0;border-color:#555;}
.ph{display:flex;justify-content:space-between;align-items:center;margin-bottom:35px;}
</style>
</head>
<body>

<div class="toast" id="toast">✓ SAUVEGARDÉ</div>

<nav class="nav">
  <div class="nav-logo">DU <span>FLOW</span></div>
  <button class="nav-btn active" onclick="showPage('dashboard',this)">Tableau de bord</button>
  <button class="nav-btn" onclick="showPage('series',this)">Mes séries</button>
  <div class="nav-right">
    <button class="btn-gold" onclick="openNewSerie()">+ NOUVELLE SÉRIE</button>
  </div>
</nav>

<!-- DASHBOARD -->
<div id="page-dashboard" class="page active">
  <div class="page-title">Tableau de bord</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-val gold" id="k-ca">0 €</div><div class="kpi-lbl">Chiffre d'affaires</div></div>
    <div class="kpi"><div class="kpi-val white" id="k-ventes">0</div><div class="kpi-lbl">Ventes réalisées</div></div>
    <div class="kpi"><div class="kpi-val white" id="k-series">0</div><div class="kpi-lbl">Séries actives</div></div>
    <div class="kpi"><div class="kpi-val gold" id="k-dispo">0</div><div class="kpi-lbl">Tirages disponibles</div></div>
  </div>
  <div class="charts-grid">
    <div class="chart-card"><h4>CA par série</h4><div class="chart-wrap"><canvas id="chartBar"></canvas></div></div>
    <div class="chart-card"><h4>Répartition des ventes</h4><div class="chart-wrap"><canvas id="chartDoughnut"></canvas></div></div>
  </div>
  <div style="background:#1a1a1a;height:1px;"></div>
  <div class="section-title">Aperçu des séries — cliquez pour voir le détail</div>
  <div class="series-grid" id="dash-series"></div>
</div>

<!-- MES SERIES -->
<div id="page-series" class="page">
  <div class="ph">
    <div class="page-title" style="margin-bottom:0;">Mes séries</div>
    <button class="btn-gold" onclick="openNewSerie()">+ NOUVELLE SÉRIE</button>
  </div>
  <div class="series-list" id="series-list"></div>
</div>

<!-- DETAIL SERIE -->
<div id="page-detail" class="page">
  <button class="back-btn" onclick="showPage('series',null)">← Retour aux séries</button>
  <div class="detail-hdr">
    <div>
      <h1 id="d-nom">—</h1>
      <p id="d-info">—</p>
    </div>
    <div class="detail-right">
      <div class="detail-big"><span id="d-sold">0</span><small> / <span id="d-total">10</span></small></div>
      <div class="detail-ca" id="d-ca">0 €</div>
    </div>
  </div>
  <table>
    <thead>
      <tr>
        <th>N°</th><th>Statut</th><th>Acheteur</th><th>Valeur</th><th>Expo</th><th>Date</th><th>Actions</th>
      </tr>
    </thead>
    <tbody id="detail-tbody"></tbody>
  </table>
  <div class="photo-section">
    <div class="photo-section-hdr">
      <span>Photo de la série</span>
      <div class="photo-actions" id="photo-actions" style="display:none;">
        <button class="btn-change-photo" onclick="document.getElementById('photo-input').click()">Changer</button>
        <button class="btn-del-photo" onclick="deletePhoto()">Supprimer</button>
      </div>
    </div>
    <div class="photo-upload-zone">
      <div class="photo-placeholder" id="photo-placeholder" onclick="document.getElementById('photo-input').click()">
        <div class="icon">+</div>
        <p>Ajouter une photo<small>JPG, PNG — cliquez pour choisir</small></p>
      </div>
      <img id="photo-preview" class="photo-preview" src="" style="display:none;">
    </div>
    <input type="file" id="photo-input" accept="image/*" onchange="uploadPhoto(this)">
  </div>
</div>

<!-- MODAL VENTE -->
<div class="overlay" id="modal-vente">
  <div class="modal">
    <div class="modal-title" id="mv-title">Enregistrer une vente</div>
    <input type="hidden" id="mv-vente-id">
    <input type="hidden" id="mv-serie-id">
    <input type="hidden" id="mv-numero">
    <div class="field-row">
      <div class="field"><label>Nom</label><input id="mv-nom" type="text" placeholder="NOM"></div>
      <div class="field"><label>Prénom</label><input id="mv-prenom" type="text" placeholder="Prénom"></div>
    </div>
    <div class="field-row">
      <div class="field"><label>Valeur (€)</label><input id="mv-valeur" type="number" placeholder="0"></div>
      <div class="field"><label>Date</label><input id="mv-date" type="date"></div>
    </div>
    <div class="field"><label>Expo / Contexte</label><input id="mv-expo" type="text" placeholder="ex: MAM 2024"></div>
    <div class="modal-foot">
      <button class="btn-cancel" onclick="closeModal('modal-vente')">Annuler</button>
      <button class="btn-gold" onclick="saveVente()">Enregistrer</button>
    </div>
  </div>
</div>

<!-- MODAL SERIE -->
<div class="overlay" id="modal-serie">
  <div class="modal">
    <div class="modal-title">Nouvelle série</div>
    <div class="field"><label>Nom de la série</label><input id="ms-nom" type="text" placeholder="NOM DE LA SÉRIE"></div>
    <div class="field-row">
      <div class="field"><label>Exemplaires</label><input id="ms-ex" type="number" value="10"></div>
      <div class="field"><label>Appareil</label><input id="ms-app" type="text" placeholder="SONY A7 III"></div>
    </div>
    <div class="field"><label>Papier</label><input id="ms-papier" type="text" value="Fine art CANSON"></div>
    <div class="modal-foot">
      <button class="btn-cancel" onclick="closeModal('modal-serie')">Annuler</button>
      <button class="btn-gold" onclick="saveSerie()">Créer</button>
    </div>
  </div>
</div>

<script>
let DATA = {};
let currentSerieId = null;
let barChart = null, doughnutChart = null;

function showToast(){
  const t = document.getElementById('toast');
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2000);
}

async function loadData(){
  const r = await fetch('/api/data');
  DATA = await r.json();
  render();
}

function showPage(page, btn){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('page-'+page).classList.add('active');
  if(btn) btn.classList.add('active');
  if(page==='dashboard') renderCharts();
}

function render(){
  renderDashboard();
  renderSeries();
}

function renderDashboard(){
  const ca = DATA.ventes.reduce((s,v)=>s+v.valeur,0);
  const dispo = DATA.series.reduce((s,serie)=>{
    const vendus = DATA.ventes.filter(v=>v.serie_id===serie.id).length;
    return s + (serie.exemplaires - vendus);
  },0);
  document.getElementById('k-ca').textContent = ca.toLocaleString('fr-FR')+' €';
  document.getElementById('k-ventes').textContent = DATA.ventes.length;
  document.getElementById('k-series').textContent = DATA.series.length;
  document.getElementById('k-dispo').textContent = dispo;

  const dashGrid = document.getElementById('dash-series');
  dashGrid.innerHTML = '';
  DATA.series.forEach(serie=>{
    const vendus = DATA.ventes.filter(v=>v.serie_id===serie.id).length;
    const pct = Math.round(vendus/serie.exemplaires*100);
    const div = document.createElement('div');
    div.className = 'sg-card';
    div.onclick = ()=>{ showDetail(serie.id); };
    div.innerHTML = `
      <div class="sg-nom">${serie.nom}</div>
      <div class="sg-bar-bg"><div class="sg-bar" style="width:${pct}%"></div></div>
      <div class="sg-info"><span>${vendus} vendu${vendus>1?'s':''}</span><span>${pct}%</span></div>`;
    dashGrid.appendChild(div);
  });

  renderCharts();
}

function renderCharts(){
  const seriesAvecVentes = DATA.series.filter(s=>DATA.ventes.some(v=>v.serie_id===s.id));
  const barLabels = seriesAvecVentes.map(s=>s.nom.length>12?s.nom.substring(0,12)+'…':s.nom);
  const barVals = seriesAvecVentes.map(s=>DATA.ventes.filter(v=>v.serie_id===s.id).reduce((sum,v)=>sum+v.valeur,0));

  if(barChart) barChart.destroy();
  const ctxBar = document.getElementById('chartBar');
  if(!ctxBar) return;
  barChart = new Chart(ctxBar.getContext('2d'),{
    type:'bar',
    data:{labels:barLabels,datasets:[{data:barVals,backgroundColor:'rgba(200,169,110,0.7)',borderColor:'#c8a96e',borderWidth:1}]},
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw.toLocaleString('fr-FR')+' €'}}},
      scales:{
        x:{ticks:{color:'#555',font:{family:'Montserrat',size:9}},grid:{color:'#111'}},
        y:{ticks:{color:'#555',font:{family:'Montserrat',size:9},callback:v=>v+'€'},grid:{color:'#111'}}
      }
    }
  });

  if(doughnutChart) doughnutChart.destroy();
  const ctxD = document.getElementById('chartDoughnut');
  if(!ctxD) return;
  const colors=['#c8a96e','#8b6914','#e0c080','#6b4f0f','#d4b57a','#a07828','#f0d090','#503800'];
  doughnutChart = new Chart(ctxD.getContext('2d'),{
    type:'doughnut',
    data:{labels:barLabels,datasets:[{data:barVals,backgroundColor:colors,borderWidth:0}]},
    options:{
      responsive:true,maintainAspectRatio:false,cutout:'65%',
      plugins:{legend:{position:'right',labels:{color:'#666',font:{family:'Montserrat',size:9},boxWidth:10}}}
    }
  });
}

function renderSeries(){
  const list = document.getElementById('series-list');
  list.innerHTML = '';
  DATA.series.forEach(serie=>{
    const vendus = DATA.ventes.filter(v=>v.serie_id===serie.id).length;
    const pct = Math.round(vendus/serie.exemplaires*100);
    const div = document.createElement('div');
    div.className = 'sl-card';
    div.innerHTML = `
      <div class="sl-top">
        <div class="sl-nom">${serie.nom}</div>
        <div class="sl-count">${vendus}<small>/${serie.exemplaires}</small></div>
      </div>
      <div class="sl-info">${serie.papier} · ${serie.appareil}</div>
      <div class="sl-bar-bg"><div class="sl-bar" style="width:${pct}%"></div></div>
      <div class="sl-actions">
        <button class="btn-voir" onclick="showDetail(${serie.id})">Voir le détail</button>
        <button class="btn-sup" onclick="deleteSerie(${serie.id})">✕</button>
      </div>`;
    list.appendChild(div);
  });
}

function showDetail(sid){
  currentSerieId = sid;
  const serie = DATA.series.find(s=>s.id===sid);
  if(!serie) return;
  const ventes = DATA.ventes.filter(v=>v.serie_id===sid);
  const ca = ventes.reduce((s,v)=>s+v.valeur,0);

  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('page-detail').classList.add('active');

  document.getElementById('d-nom').textContent = serie.nom;
  document.getElementById('d-info').textContent = `${serie.papier} · ${serie.appareil} · ${serie.exemplaires} exemplaires`;
  document.getElementById('d-sold').textContent = ventes.length;
  document.getElementById('d-total').textContent = serie.exemplaires;
  document.getElementById('d-ca').textContent = ca.toLocaleString('fr-FR')+' €';

  const preview = document.getElementById('photo-preview');
  const placeholder = document.getElementById('photo-placeholder');
  const photoActions = document.getElementById('photo-actions');
  if(serie.photo){
    preview.src = serie.photo;
    preview.style.display = 'block';
    placeholder.style.display = 'none';
    photoActions.style.display = 'flex';
  } else {
    preview.style.display = 'none';
    placeholder.style.display = 'flex';
    photoActions.style.display = 'none';
  }

  const tbody = document.getElementById('detail-tbody');
  tbody.innerHTML = '';
  for(let n=1; n<=serie.exemplaires; n++){
    const v = ventes.find(v=>v.numero===n);
    const tr = document.createElement('tr');
    if(v){
      tr.innerHTML = `
        <td><div class="num-cell sold">${n}</div></td>
        <td><span class="badge b-sold">VENDU</span></td>
        <td><div class="buyer">${v.nom}</div><div class="buyer-s">${v.prenom}</div></td>
        <td class="price">${v.valeur.toLocaleString('fr-FR')} €</td>
        <td style="color:#555">${v.expo||'—'}</td>
        <td style="color:#555">${v.date||'—'}</td>
        <td><div class="acts">
          <button class="tb tb-edit" onclick="editVente(${v.id})">Modifier</button>
          <button class="tb tb-del" onclick="deleteVente(${v.id})">✕</button>
        </div></td>`;
    } else {
      tr.innerHTML = `
        <td><div class="num-cell">${n}</div></td>
        <td><span class="badge b-free">LIBRE</span></td>
        <td class="dim">—</td><td class="dim">—</td><td class="dim">—</td><td class="dim">—</td>
        <td><button class="tb tb-sell" onclick="openVente(${sid},${n})">Vendre</button></td>`;
    }
    tbody.appendChild(tr);
  }
}

function uploadPhoto(input){
  const file = input.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = async function(e){
    const r = await fetch('/api/serie/photo',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({id:currentSerieId, photo:e.target.result})
    });
    DATA = await r.json();
    showToast();
    showDetail(currentSerieId);
  };
  reader.readAsDataURL(file);
}

async function deletePhoto(){
  const r = await fetch('/api/serie/photo',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id:currentSerieId, photo:''})
  });
  DATA = await r.json();
  showToast();
  showDetail(currentSerieId);
}

function openVente(serieId, numero){
  document.getElementById('mv-title').textContent = 'Vente — N° '+numero;
  document.getElementById('mv-vente-id').value = '';
  document.getElementById('mv-serie-id').value = serieId;
  document.getElementById('mv-numero').value = numero;
  ['mv-nom','mv-prenom','mv-valeur','mv-date','mv-expo'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('modal-vente').classList.add('show');
}

function editVente(vid){
  const v = DATA.ventes.find(x=>x.id===vid);
  if(!v) return;
  document.getElementById('mv-title').textContent = 'Modifier — N° '+v.numero;
  document.getElementById('mv-vente-id').value = v.id;
  document.getElementById('mv-serie-id').value = v.serie_id;
  document.getElementById('mv-numero').value = v.numero;
  document.getElementById('mv-nom').value = v.nom;
  document.getElementById('mv-prenom').value = v.prenom;
  document.getElementById('mv-valeur').value = v.valeur;
  document.getElementById('mv-date').value = v.date;
  document.getElementById('mv-expo').value = v.expo;
  document.getElementById('modal-vente').classList.add('show');
}

async function saveVente(){
  const vid = document.getElementById('mv-vente-id').value;
  const payload = {
    id: vid ? parseInt(vid) : null,
    serie_id: parseInt(document.getElementById('mv-serie-id').value),
    numero: parseInt(document.getElementById('mv-numero').value),
    nom: document.getElementById('mv-nom').value,
    prenom: document.getElementById('mv-prenom').value,
    valeur: parseFloat(document.getElementById('mv-valeur').value)||0,
    date: document.getElementById('mv-date').value,
    expo: document.getElementById('mv-expo').value
  };
  const url = vid ? '/api/vente/update' : '/api/vente/add';
  const r = await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  DATA = await r.json();
  closeModal('modal-vente');
  showToast();
  showDetail(currentSerieId);
}

async function deleteVente(vid){
  if(!confirm('Supprimer cette vente ?')) return;
  const r = await fetch('/api/vente/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:vid})});
  DATA = await r.json();
  showToast();
  showDetail(currentSerieId);
}

function openNewSerie(){ document.getElementById('modal-serie').classList.add('show'); }

async function saveSerie(){
  const payload = {
    nom: document.getElementById('ms-nom').value.toUpperCase(),
    exemplaires: parseInt(document.getElementById('ms-ex').value)||10,
    appareil: document.getElementById('ms-app').value,
    papier: document.getElementById('ms-papier').value
  };
  const r = await fetch('/api/serie/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  DATA = await r.json();
  closeModal('modal-serie');
  showToast();
  render();
}

async function deleteSerie(sid){
  if(!confirm('Supprimer cette série et toutes ses ventes ?')) return;
  const r = await fetch('/api/serie/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:sid})});
  DATA = await r.json();
  showToast();
  render();
}

function closeModal(id){ document.getElementById(id).classList.remove('show'); }

document.querySelectorAll('.overlay').forEach(o=>{
  o.addEventListener('click',e=>{ if(e.target===o) o.classList.remove('show'); });
});

loadData();
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/data')
def api_data():
    return jsonify(load_data())

@app.route('/api/vente/add', methods=['POST'])
def api_vente_add():
    data = load_data()
    p = request.json
    new_id = max([v['id'] for v in data['ventes']], default=0) + 1
    data['ventes'].append({'id':new_id,'serie_id':p['serie_id'],'numero':p['numero'],
        'nom':p.get('nom',''),'prenom':p.get('prenom',''),'valeur':p.get('valeur',0),
        'expo':p.get('expo',''),'date':p.get('date','')})
    save_data(data)
    return jsonify(data)

@app.route('/api/vente/update', methods=['POST'])
def api_vente_update():
    data = load_data()
    p = request.json
    for v in data['ventes']:
        if v['id'] == p['id']:
            v.update({'nom':p.get('nom',''),'prenom':p.get('prenom',''),
                'valeur':p.get('valeur',0),'expo':p.get('expo',''),'date':p.get('date','')})
    save_data(data)
    return jsonify(data)

@app.route('/api/vente/delete', methods=['POST'])
def api_vente_delete():
    data = load_data()
    data['ventes'] = [v for v in data['ventes'] if v['id'] != request.json['id']]
    save_data(data)
    return jsonify(data)

@app.route('/api/serie/add', methods=['POST'])
def api_serie_add():
    data = load_data()
    p = request.json
    new_id = max([s['id'] for s in data['series']], default=0) + 1
    data['series'].append({'id':new_id,'nom':p['nom'],'exemplaires':p.get('exemplaires',10),
        'papier':p.get('papier',''),'appareil':p.get('appareil',''),'photo':''})
    save_data(data)
    return jsonify(data)

@app.route('/api/serie/delete', methods=['POST'])
def api_serie_delete():
    data = load_data()
    sid = request.json['id']
    data['series'] = [s for s in data['series'] if s['id'] != sid]
    data['ventes'] = [v for v in data['ventes'] if v['serie_id'] != sid]
    save_data(data)
    return jsonify(data)

@app.route('/api/serie/photo', methods=['POST'])
def api_serie_photo():
    data = load_data()
    p = request.json
    for s in data['series']:
        if s['id'] == p['id']:
            s['photo'] = p.get('photo','')
    save_data(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
