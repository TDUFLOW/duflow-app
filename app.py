from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json, os

app = Flask(__name__)
app.secret_key = 'duflow2024secret'
PASSWORD = 'duflow2024'
DATA_FILE = 'data.json'

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect('/')
        error = 'Mot de passe incorrect'
    return render_template_string('''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DU FLOW — Accès</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Montserrat',sans-serif;background:#080808;color:#fff;
  min-height:100vh;display:flex;align-items:center;justify-content:center;}
.box{width:380px;padding:50px;}
.logo{font-size:22px;font-weight:900;letter-spacing:6px;text-align:center;margin-bottom:40px;}
.logo span{color:#c8a96e;}
label{font-size:8px;letter-spacing:2px;color:#fff;display:block;margin-bottom:8px;text-transform:uppercase;}
input{width:100%;background:#111;border:1px solid #1a1a1a;color:#e8e8e8;
  padding:14px;font-family:'Montserrat',sans-serif;font-size:13px;outline:none;margin-bottom:20px;}
input:focus{border-color:#c8a96e;}
button{width:100%;padding:14px;background:#c8a96e;color:#000;font-family:'Montserrat',sans-serif;
  font-size:10px;font-weight:700;letter-spacing:3px;border:none;cursor:pointer;}
button:hover{background:#e0c080;}
.error{color:#ff4444;font-size:9px;letter-spacing:1px;margin-bottom:15px;text-align:center;}
</style></head>
<body>
<div class="box">
  <div class="logo">DU <span>FLOW</span></div>
  {% if error %}<div class="error">{{ error }}</div>{% endif %}
  <form method="POST">
    <label>Mot de passe</label>
    <input type="password" name="password" placeholder="••••••••" autofocus>
    <button type="submit">ACCÉDER</button>
  </form>
</div>
</body></html>''', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

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
  letter-spacing:2px;color:#fff;background:transparent;border:none;cursor:pointer;
  transition:all 0.2s;text-transform:uppercase;}
.nav-btn:hover{color:#ccc;}
.nav-btn.active{color:#c8a96e;}
.nav-right{margin-left:auto;display:flex;align-items:center;gap:12px;}
.btn-logout{padding:9px 16px;background:transparent;color:#fff;font-family:'Montserrat',sans-serif;
  font-size:9px;font-weight:600;letter-spacing:2px;border:1px solid #333;cursor:pointer;transition:all 0.2s;}
.btn-logout:hover{border-color:#fff;}
.btn-gold{padding:9px 20px;background:#c8a96e;color:#000;font-family:'Montserrat',sans-serif;
  font-size:9px;font-weight:700;letter-spacing:2px;border:none;cursor:pointer;transition:all 0.2s;}
.btn-gold:hover{background:#e0c080;}
.page{display:none;padding:50px 40px;}
.page.active{display:block;}
.page-title{font-size:9px;letter-spacing:4px;color:#fff;text-transform:uppercase;margin-bottom:40px;}
.toast{position:fixed;bottom:30px;right:30px;background:#c8a96e;color:#000;
  padding:12px 24px;font-size:9px;letter-spacing:2px;font-weight:700;z-index:999;
  opacity:0;transition:opacity 0.3s;pointer-events:none;}
.toast.show{opacity:1;}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#1a1a1a;margin-bottom:1px;}
.kpi{background:#0a0a0a;padding:32px 28px;}
.kpi-val{font-size:42px;font-weight:900;letter-spacing:-2px;line-height:1;margin-bottom:8px;}
.kpi-val.gold{color:#c8a96e;}
.kpi-val.white{color:#e8e8e8;}
.kpi-lbl{font-size:8px;letter-spacing:3px;color:#fff;text-transform:uppercase;}
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#1a1a1a;margin-bottom:1px;}
.chart-card{background:#0a0a0a;padding:32px;}
.chart-card h4{font-size:8px;letter-spacing:3px;color:#fff;text-transform:uppercase;margin-bottom:25px;}
.chart-wrap{position:relative;height:230px;}
.section-title{font-size:8px;letter-spacing:3px;color:#fff;text-transform:uppercase;
  padding:24px 0 20px;border-bottom:1px solid #0f0f0f;margin-bottom:0;}
.series-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;background:#1a1a1a;}
.sg-card{background:#0a0a0a;padding:24px;cursor:pointer;transition:background 0.2s;}
.sg-card:hover{background:#0f0f0f;}
.sg-nom{font-size:11px;font-weight:700;letter-spacing:3px;margin-bottom:12px;color:#fff;}
.sg-bar-bg{height:1px;background:#1a1a1a;margin-bottom:10px;}
.sg-bar{height:100%;background:#c8a96e;transition:width 0.5s;}
.sg-info{display:flex;justify-content:space-between;font-size:9px;color:#fff;}
.sg-info span:last-child{color:#c8a96e;font-weight:700;}
.series-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1px;background:#1a1a1a;}
.sl-card{background:#0a0a0a;padding:28px;}
.sl-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;}
.sl-nom{font-size:13px;font-weight:900;letter-spacing:3px;color:#fff;}
.sl-count{font-size:28px;font-weight:900;color:#c8a96e;line-height:1;}
.sl-count small{font-size:12px;color:#fff;font-weight:400;}
.sl-info{font-size:9px;color:#fff;letter-spacing:1px;margin-bottom:16px;}
.sl-bar-bg{height:1px;background:#1a1a1a;margin-bottom:16px;}
.sl-bar{height:100%;background:#c8a96e;}
.sl-actions{display:flex;gap:8px;}
.btn-voir{flex:1;padding:10px;background:transparent;border:1px solid #222;color:#fff;
  font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:2px;font-weight:600;
  cursor:pointer;transition:all 0.2s;text-transform:uppercase;}
.btn-voir:hover{border-color:#c8a96e;color:#c8a96e;}
.btn-sup{padding:10px 12px;background:transparent;border:1px solid #1a1a1a;color:#fff;
  font-size:11px;cursor:pointer;transition:all 0.2s;}
.btn-sup:hover{border-color:#ff3333;color:#ff3333;}
table{width:100%;border-collapse:collapse;}
th{font-size:8px;letter-spacing:2px;color:#fff;text-transform:uppercase;
  padding:12px 16px;text-align:left;border-bottom:1px solid #1a1a1a;font-weight:600;}
td{padding:14px 16px;border-bottom:1px solid #0d0d0d;font-size:12px;vertical-align:middle;}
tr:hover td{background:#0a0a0a;}
.back-btn{display:inline-flex;align-items:center;gap:8px;font-size:9px;letter-spacing:2px;
  color:#fff;background:transparent;border:none;cursor:pointer;margin-bottom:32px;
  font-family:'Montserrat',sans-serif;font-weight:600;padding:0;}
.back-btn:hover{color:#c8a96e;}
.detail-hdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:32px;}
.detail-hdr h1{font-size:32px;font-weight:900;letter-spacing:4px;color:#fff;margin-bottom:8px;}
.detail-hdr p{font-size:9px;color:#fff;letter-spacing:2px;}
.detail-right{text-align:right;}
.detail-big{font-size:48px;font-weight:900;color:#fff;line-height:1;}
.detail-big small{font-size:18px;color:#fff;font-weight:400;}
.detail-ca{font-size:13px;color:#c8a96e;font-weight:700;letter-spacing:2px;margin-top:4px;}
.num-cell{width:32px;height:32px;border:1px solid #1e1e1e;display:flex;align-items:center;
  justify-content:center;font-size:9px;font-weight:700;color:#fff;}
.num-cell.sold{border-color:#c8a96e;color:#c8a96e;}
.badge{display:inline-block;padding:3px 10px;font-size:8px;letter-spacing:2px;font-weight:700;}
.b-sold{background:rgba(200,169,110,0.1);color:#c8a96e;}
.b-free{background:#0f0f0f;color:#fff;}
.buyer{font-size:11px;font-weight:700;color:#fff;}
.buyer-s{font-size:9px;color:#fff;margin-top:2px;}
.price{color:#c8a96e;font-weight:700;}
.dim{color:#fff;}
.tb{padding:6px 12px;font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:1px;
  font-weight:600;cursor:pointer;background:transparent;transition:all 0.2s;border:1px solid;}
.tb-sell{border-color:rgba(200,169,110,0.4);color:#c8a96e;}
.tb-sell:hover{background:#c8a96e;color:#000;}
.tb-edit{border-color:#1e1e1e;color:#fff;margin-right:6px;}
.tb-edit:hover{border-color:#fff;color:#fff;}
.tb-del{border-color:#141414;color:#fff;width:30px;height:30px;padding:0;
  display:inline-flex;align-items:center;justify-content:center;}
.tb-del:hover{border-color:#ff3333;color:#ff3333;}
.acts{display:flex;align-items:center;gap:6px;}
.photo-section{margin-top:40px;border:1px solid #1a1a1a;background:#0a0a0a;}
.photo-section-hdr{padding:20px 24px;border-bottom:1px solid #141414;display:flex;justify-content:space-between;align-items:center;}
.photo-section-hdr span{font-size:8px;letter-spacing:3px;color:#fff;text-transform:uppercase;}
.photo-upload-zone{padding:30px;text-align:center;}
.photo-preview{width:100%;max-height:500px;object-fit:contain;display:block;}
.photo-placeholder{border:1px dashed #1e1e1e;padding:50px;cursor:pointer;transition:all 0.2s;display:flex;
  flex-direction:column;align-items:center;gap:12px;}
.photo-placeholder:hover{border-color:#c8a96e;}
.photo-placeholder .icon{font-size:28px;color:#fff;}
.photo-placeholder p{font-size:9px;letter-spacing:2px;color:#fff;text-transform:uppercase;}
.photo-placeholder p small{display:block;font-size:8px;color:#fff;margin-top:4px;}
#photo-input{display:none;}
.photo-actions{display:flex;gap:8px;justify-content:center;margin-top:16px;}
.btn-change-photo{padding:8px 16px;background:transparent;border:1px solid #222;color:#fff;
  font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:2px;cursor:pointer;transition:all 0.2s;}
.btn-change-photo:hover{border-color:#c8a96e;color:#c8a96e;}
.btn-del-photo{padding:8px 12px;background:transparent;border:1px solid #141414;color:#fff;
  font-family:'Montserrat',sans-serif;font-size:8px;cursor:pointer;transition:all 0.2s;}
.btn-del-photo:hover{border-color:#ff3333;color:#ff3333;}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.93);z-index:500;
  align-items:center;justify-content:center;}
.overlay.show{display:flex;}
.modal{background:#0c0c0c;border:1px solid #1e1e1e;width:460px;max-width:95vw;padding:44px;}
.modal-title{font-size:10px;letter-spacing:4px;color:#c8a96e;margin-bottom:32px;text-transform:uppercase;}
.field{margin-bottom:18px;}
.field label{display:block;font-size:8px;letter-spacing:2px;color:#fff;margin-bottom:8px;text-transform:uppercase;}
.field input,.field select{width:100%;background:#111;border:1px solid #1a1a1a;color:#e8e8e8;
  padding:12px 14px;font-family:'Montserrat',sans-serif;font-size:12px;outline:none;transition:border 0.2s;}
.field input:focus,.field select:focus{border-color:#c8a96e;}
.field input::placeholder{color:#fff;}
.field select option{background:#111;}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:15px;}
.modal-foot{display:flex;gap:10px;justify-content:flex-end;margin-top:32px;
  padding-top:22px;border-top:1px solid #111;}
.btn-cancel{padding:10px 20px;background:transparent;border:1px solid #1e1e1e;color:#fff;
  font-family:'Montserrat',sans-serif;font-size:8px;letter-spacing:2px;cursor:pointer;transition:all 0.2s;}
.btn-cancel:hover{color:#e0e0e0;border-color:#fff;}
.ph{display:flex;justify-content:space-between;align-items:center;margin-bottom:35px;}
</style>
</head>
<body><div class="toast" id="toast">✓ SAUVEGARDÉ</div>

<nav class="nav">
  <div class="nav-logo">DU <span>FLOW</span></div>
  <button class="nav-btn active" onclick="showPage(\'dashboard\',this)">Tableau de bord</button>
  <button class="nav-btn" onclick="showPage(\'series\',this)">Mes séries</button>
  <div class="nav-right">
    <button class="btn-gold" onclick="openNewSerie()">+ NOUVELLE SÉRIE</button>
    <a href="/logout"><button class="btn-logout">DÉCONNEXION</button></a>
  </div>
</nav>

<!-- DASHBOARD -->
<div id="page-dashboard" class="page active">
  <div class="page-title">Tableau de bord</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-val gold" id="k-ca">0 €</div><div class="kpi-lbl">Chiffre d\'affaires</div></div>
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
  <button class="back-btn" onclick="showPage(\'series\',null)">← Retour aux séries</button>
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
        <button class="btn-change-photo" onclick="document.getElementById(\'photo-input\').click()">Changer</button>
        <button class="btn-del-photo" onclick="deletePhoto()">Supprimer</button>
      </div>
    </div>
    <div class="photo-upload-zone">
      <div class="photo-placeholder" id="photo-placeholder" onclick="document.getElementById(\'photo-input\').click()">
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
      <button class="btn-cancel" onclick="closeModal(\'modal-vente\')">Annuler</button>
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
      <button class="btn-cancel" onclick="closeModal(\'modal-serie\')">Annuler</button>
      <button class="btn-gold" onclick="saveSerie()">Créer</button>
    </div>
  </div>
</div>

<script>
let DATA = {};
let currentSerieId = null;
let barChart = null, doughnutChart = null;

function showToast(){
  const t = document.getElementById(\'toast\');
  t.classList.add(\'show\');
  setTimeout(()=>t.classList.remove(\'show\'), 2000);
}

async function loadData(){
  const r = await fetch(\'/api/data\');
  DATA = await r.json();
  render();
}

function showPage(name, btn){
  document.querySelectorAll(\'.page\').forEach(p=>p.classList.remove(\'active\'));
  document.getElementById(\'page-\'+name).classList.add(\'active\');
  if(btn){
    document.querySelectorAll(\'.nav-btn\').forEach(b=>b.classList.remove(\'active\'));
    btn.classList.add(\'active\');
  }
  if(name===\'dashboard\') renderDashboard();
  if(name===\'series\') renderSeries();
}

function render(){
  renderDashboard();
  renderSeries();
}

function renderDashboard(){
  if(!DATA.series) return;
  const totalCA = DATA.ventes.reduce((s,v)=>s+v.valeur,0);
  const totalVentes = DATA.ventes.length;
  const totalSeries = DATA.series.length;
  const totalDispo = DATA.series.reduce((s,serie)=>{
    const vendus = DATA.ventes.filter(v=>v.serie_id===serie.id).length;
    return s + (serie.exemplaires - vendus);
  },0);
  document.getElementById(\'k-ca\').textContent = totalCA.toLocaleString(\'fr-FR\')+\' €\';
  document.getElementById(\'k-ventes\').textContent = totalVentes;
  document.getElementById(\'k-series\').textContent = totalSeries;
  document.getElementById(\'k-dispo\').textContent = totalDispo;

  const barLabels = DATA.series.map(s=>s.nom);
  const barVals = DATA.series.map(s=>DATA.ventes.filter(v=>v.serie_id===s.id).reduce((t,v)=>t+v.valeur,0));

  if(barChart) barChart.destroy();
  const ctxBar = document.getElementById(\'chartBar\');
  if(!ctxBar) return;
  barChart = new Chart(ctxBar.getContext(\'2d\'),{
    type:\'bar\',
    data:{labels:barLabels,datasets:[{data:barVals,backgroundColor:\'rgba(200,169,110,0.7)\',borderColor:\'#c8a96e\',borderWidth:1}]},
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw.toLocaleString(\'fr-FR\')+\' €\'}}},
      scales:{
        x:{ticks:{color:\'#fff\',font:{family:\'Montserrat\',size:9}},grid:{color:\'#111\'}},
        y:{ticks:{color:\'#fff\',font:{family:\'Montserrat\',size:9},callback:v=>v+\'€\'},grid:{color:\'#111\'}}
      }
    }
  });

  if(doughnutChart) doughnutChart.destroy();
  const ctxD = document.getElementById(\'chartDoughnut\');
  if(!ctxD) return;
  const colors=[\'#c8a96e\',\'#8b6914\',\'#e0c080\',\'#6b4f0f\',\'#d4b57a\',\'#a07828\',\'#f0d090\',\'#503800\'];
  doughnutChart = new Chart(ctxD.getContext(\'2d\'),{
    type:\'doughnut\',
    data:{labels:barLabels,datasets:[{data:barVals,backgroundColor:colors,borderWidth:0}]},
    options:{
      responsive:true,maintainAspectRatio:false,cutout:\'65%\',
      plugins:{legend:{position:\'right\',labels:{color:\'#fff\',font:{family:\'Montserrat\',size:9},boxWidth:10}}}
    }
  });

  const dashSeries = document.getElementById(\'dash-series\');
  dashSeries.innerHTML = \'\';
  DATA.series.forEach(serie=>{
    const vendus = DATA.ventes.filter(v=>v.serie_id===serie.id).length;
    const pct = Math.round(vendus/serie.exemplaires*100);
    const ca = DATA.ventes.filter(v=>v.serie_id===serie.id).reduce((t,v)=>t+v.valeur,0);
    const div = document.createElement(\'div\');
    div.className=\'sg-card\';
    div.onclick=()=>showDetail(serie.id);
    div.innerHTML=`<div class="sg-nom">${serie.nom}</div>
      <div class="sg-bar-bg"><div class="sg-bar" style="width:${pct}%"></div></div>
      <div class="sg-info"><span>${vendus}/${serie.exemplaires} vendus</span><span>${ca.toLocaleString(\'fr-FR\')} €</span></div>`;
    dashSeries.appendChild(div);
  });
}

function renderSeries(){
  if(!DATA.series) return;
  const list = document.getElementById(\'series-list\');
  list.innerHTML=\'\';
  DATA.series.forEach(serie=>{
    const vendus = DATA.ventes.filter(v=>v.serie_id===serie.id).length;
    const pct = Math.round(vendus/serie.exemplaires*100);
    const ca = DATA.ventes.filter(v=>v.serie_id===serie.id).reduce((t,v)=>t+v.valeur,0);
    const div = document.createElement(\'div\');
    div.className=\'sl-card\';
    div.innerHTML=`
      <div class="sl-top">
        <div class="sl-nom">${serie.nom}</div>
        <div class="sl-count">${vendus}<small>/${serie.exemplaires}</small></div>
      </div>
      <div class="sl-info">${serie.appareil} — ${serie.papier}</div>
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
  const ca = ventes.reduce((t,v)=>t+v.valeur,0);
  document.getElementById(\'d-nom\').textContent = serie.nom;
  document.getElementById(\'d-info\').textContent = serie.appareil+\' — \'+serie.papier;
  document.getElementById(\'d-sold\').textContent = ventes.length;
  document.getElementById(\'d-total\').textContent = serie.exemplaires;
  document.getElementById(\'d-ca\').textContent = ca.toLocaleString(\'fr-FR\')+\' €\';

  const tbody = document.getElementById(\'detail-tbody\');
  tbody.innerHTML = \'\';
  for(let n=1; n<=serie.exemplaires; n++){
    const v = ventes.find(v=>v.numero===n);
    const tr = document.createElement(\'tr\');
    if(v){
      tr.innerHTML = `
        <td><div class="num-cell sold">${n}</div></td>
        <td><span class="badge b-sold">VENDU</span></td>
        <td><div class="buyer">${v.nom}</div><div class="buyer-s">${v.prenom}</div></td>
        <td class="price">${v.valeur.toLocaleString(\'fr-FR\')} €</td>
        <td style="color:#fff">${v.expo||\'—\'}</td>
        <td style="color:#fff">${v.date||\'—\'}</td>
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

  const ph = document.getElementById(\'photo-placeholder\');
  const pi = document.getElementById(\'photo-preview\');
  const pa = document.getElementById(\'photo-actions\');
  if(serie.photo){
    ph.style.display=\'none\';
    pi.src=serie.photo;
    pi.style.display=\'block\';
    pa.style.display=\'flex\';
  } else {
    ph.style.display=\'flex\';
    pi.style.display=\'none\';
    pi.src=\'\';
    pa.style.display=\'none\';
  }

  document.querySelectorAll(\'.nav-btn\').forEach(b=>b.classList.remove(\'active\'));
  document.querySelectorAll(\'.page\').forEach(p=>p.classList.remove(\'active\'));
  document.getElementById(\'page-detail\').classList.add(\'active\');
}

function uploadPhoto(input){
  const file = input.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = async function(e){
    const r = await fetch(\'/api/serie/photo\',{
      method:\'POST\',
      headers:{\'Content-Type\':\'application/json\'},
      body:JSON.stringify({id:currentSerieId, photo:e.target.result})
    });
    DATA = await r.json();
    showToast();
    showDetail(currentSerieId);
  };
  reader.readAsDataURL(file);
}

async function deletePhoto(){
  const r = await fetch(\'/api/serie/photo\',{
    method:\'POST\',
    headers:{\'Content-Type\':\'application/json\'},
    body:JSON.stringify({id:currentSerieId, photo:\'\'})
  });
  DATA = await r.json();
  showToast();
  showDetail(currentSerieId);
}

function openVente(serieId, numero){
  document.getElementById(\'mv-title\').textContent = \'Vente — N° \'+numero;
  document.getElementById(\'mv-vente-id\').value = \'\';
  document.getElementById(\'mv-serie-id\').value = serieId;
  document.getElementById(\'mv-numero\').value = numero;
  [\'mv-nom\',\'mv-prenom\',\'mv-valeur\',\'mv-date\',\'mv-expo\'].forEach(id=>document.getElementById(id).value=\'\');
  document.getElementById(\'modal-vente\').classList.add(\'show\');
}

function editVente(vid){
  const v = DATA.ventes.find(x=>x.id===vid);
  if(!v) return;
  document.getElementById(\'mv-title\').textContent = \'Modifier — N° \'+v.numero;
  document.getElementById(\'mv-vente-id\').value = v.id;
  document.getElementById(\'mv-serie-id\').value = v.serie_id;
  document.getElementById(\'mv-numero\').value = v.numero;
  document.getElementById(\'mv-nom\').value = v.nom;
  document.getElementById(\'mv-prenom\').value = v.prenom;
  document.getElementById(\'mv-valeur\').value = v.valeur;
  document.getElementById(\'mv-date\').value = v.date;
  document.getElementById(\'mv-expo\').value = v.expo;
  document.getElementById(\'modal-vente\').classList.add(\'show\');
}

async function saveVente(){
  const vid = document.getElementById(\'mv-vente-id\').value;
  const payload = {
    serie_id: parseInt(document.getElementById(\'mv-serie-id\').value),
    numero: parseInt(document.getElementById(\'mv-numero\').value),
    nom: document.getElementById(\'mv-nom\').value.toUpperCase(),
    prenom: document.getElementById(\'mv-prenom\').value,
    valeur: parseFloat(document.getElementById(\'mv-valeur\').value)||0,
    date: document.getElementById(\'mv-date\').value,
    expo: document.getElementById(\'mv-expo\').value
  };
  if(vid) payload.id = parseInt(vid);
  const url = vid ? \'/api/vente/edit\' : \'/api/vente/add\';
  const r = await fetch(url,{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify(payload)});
  DATA = await r.json();
  closeModal(\'modal-vente\');
  showToast();
  showDetail(payload.serie_id);
}

async function deleteVente(vid){
  if(!confirm(\'Supprimer cette vente ?\')) return;
  const sid = currentSerieId;
  const r = await fetch(\'/api/vente/delete\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({id:vid})});
  DATA = await r.json();
  showToast();
  showDetail(sid);
}

function openNewSerie(){
  document.getElementById(\'ms-nom\').value=\'\';
  document.getElementById(\'ms-ex\').value=\'10\';
  document.getElementById(\'ms-app\').value=\'\';
  document.getElementById(\'ms-papier\').value=\'Fine art CANSON\';
  document.getElementById(\'modal-serie\').classList.add(\'show\');
}

async function saveSerie(){
  const payload = {
    nom: document.getElementById(\'ms-nom\').value.toUpperCase(),
    exemplaires: parseInt(document.getElementById(\'ms-ex\').value)||10,
    appareil: document.getElementById(\'ms-app\').value,
    papier: document.getElementById(\'ms-papier\').value
  };
  const r = await fetch(\'/api/serie/add\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify(payload)});
  DATA = await r.json();
  closeModal(\'modal-serie\');
  showToast();
  renderSeries();
}

async function deleteSerie(sid){
  if(!confirm(\'Supprimer cette série et toutes ses ventes ?\')) return;
  const r = await fetch(\'/api/serie/delete\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({id:sid})});
  DATA = await r.json();
  showToast();
  renderSeries();
}

function closeModal(id){
  document.getElementById(id).classList.remove(\'show\');
}

document.querySelectorAll(\'.overlay\').forEach(o=>{
  o.addEventListener(\'click\',e=>{if(e.target===o) o.classList.remove(\'show\');});
});

loadData();
</script>
</body></html>'''

@app.route('/')
@login_required
def index():
    return render_template_string(HTML)

@app.route('/api/data')
@login_required
def api_data():
    return jsonify(load_data())

@app.route('/api/vente/add', methods=['POST'])
@login_required
def api_vente_add():
    data = load_data()
    p = request.json
    new_id = max([v['id'] for v in data['ventes']], default=0) + 1
    data['ventes'].append({'id':new_id,'serie_id':p['serie_id'],'numero':p['numero'],
        'nom':p['nom'],'prenom':p['prenom'],'valeur':p['valeur'],'expo':p.get('expo',''),'date':p.get('date','')})
    save_data(data)
    return jsonify(data)

@app.route('/api/vente/edit', methods=['POST'])
@login_required
def api_vente_edit():
    data = load_data()
    p = request.json
    for v in data['ventes']:
        if v['id'] == p['id']:
            v.update({'nom':p['nom'],'prenom':p['prenom'],'valeur':p['valeur'],'expo':p.get('expo',''),'date':p.get('date','')})
    save_data(data)
    return jsonify(data)

@app.route('/api/vente/delete', methods=['POST'])
@login_required
def api_vente_delete():
    data = load_data()
    data['ventes'] = [v for v in data['ventes'] if v['id'] != request.json['id']]
    save_data(data)
    return jsonify(data)

@app.route('/api/serie/add', methods=['POST'])
@login_required
def api_serie_add():
    data = load_data()
    p = request.json
    new_id = max([s['id'] for s in data['series']], default=0) + 1
    data['series'].append({'id':new_id,'nom':p['nom'],'exemplaires':p.get('exemplaires',10),
        'papier':p.get('papier',''),'appareil':p.get('appareil',''),'photo':''})
    save_data(data)
    return jsonify(data)

@app.route('/api/serie/delete', methods=['POST'])
@login_required
def api_serie_delete():
    data = load_data()
    sid = request.json['id']
    data['series'] = [s for s in data['series'] if s['id'] != sid]
    data['ventes'] = [v for v in data['ventes'] if v['serie_id'] != sid]
    save_data(data)
    return jsonify(data)

@app.route('/api/serie/photo', methods=['POST'])
@login_required
def api_serie_photo():
    data = load_data()
    p = request.json
    for s in data['series']:
        if s['id'] == p['id']:
            s['photo'] = p.get('photo','')
    save_data(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
