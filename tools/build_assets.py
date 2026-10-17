#!/usr/bin/env python3
# Production des schémas SVG et de tools/apercu.html depuis le catalogue. Voir README.md pour les
# commandes, les sorties et les prérequis.
"""Génère des SVG originaux et un aperçu HTML pédagogique (sans matériel)."""
from html import escape
import json
from pathlib import Path
from lab_catalog import EXPERIMENTS

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets/schemas'
ASSETS.mkdir(parents=True, exist_ok=True)


# Construire un canevas SVG autonome ; escape protège les titres injectés dans les balises et les
# attributs.
def svg_start(title, subtitle, height=430):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 {height}" role="img" aria-label="{escape(title)}">
<rect width="1100" height="{height}" rx="20" fill="#101e31"/>
<style>text{{font-family:Arial,sans-serif;fill:#edf4ff}}.title{{font-size:27px;font-weight:bold}}.sub{{font-size:16px;fill:#a8bdd5}}.pin{{font-size:18px}}.small{{font-size:14px;fill:#b7cadd}}</style>
<text class="title" x="40" y="48">{escape(title)}</text><text class="sub" x="40" y="80">{escape(subtitle)}</text>'''


# Relier les quatre signaux électriques du Grove ; la position dessinée n’est pas un plan physique des
# contacts.
def wiring(filename, title, target, labels, note):
    s = svg_start(title, 'Cardputer K132 · câble droit · raccorder hors tension')
    s += '<rect x="40" y="115" width="295" height="235" rx="15" fill="#223750"/><rect x="755" y="115" width="305" height="235" rx="15" fill="#223750"/>'
    s += f'<text class="pin" x="62" y="146">Cardputer — Grove</text><text class="pin" x="773" y="146">{escape(target)}</text>'
    colors = ['#b5bfcd', '#ff7979', '#f7d26a', '#ffffff']
    left = ['GND / noir', '5 V / rouge', 'G2 / jaune', 'G1 / blanc']
    # L’ordre noir, rouge, jaune, blanc doit rester cohérent avec les libellés et les guides de câblage.
    for i, (source, dest, color) in enumerate(zip(left, labels, colors)):
        y = 190 + 43 * i
        dash = ' stroke-dasharray="8 7"' if dest == 'Non connecté' else ''
        s += f'<text class="pin" x="62" y="{y+5}">{escape(source)}</text><path d="M335 {y}H755" stroke="{color}" stroke-width="4"{dash}/><circle cx="335" cy="{y}" r="5" fill="{color}"/><text class="pin" x="775" y="{y+5}">{escape(dest)}</text>'
    s += f'<text class="small" x="40" y="390">{escape(note)}</text></svg>'
    (ASSETS / (filename + '.svg')).write_text(s)


wiring('grove', 'Les quatre fils du port Grove', 'Unité M5Stack', ['Masse commune', 'Alimentation 5 V', 'Signal configurable', 'Signal configurable'], 'Schéma électrique de principe : ce dessin ne représente pas la vue des contacts du connecteur.')
wiring('rf433-tx', 'Émettre une trame RF433', 'RF433T · SYN115', ['GND', '5 V', 'RF_TX (entrée)', 'Non connecté'], '433,92 MHz ASK/OOK · GPIO 2 commande les impulsions · récepteur séparé nécessaire au contrôle.')
wiring('rf433-rx', 'Recevoir une trame RF433', 'RF433R · U113', ['GND', '5 V', 'Non connecté', 'RF_RX (sortie)'], '433,92 MHz ASK/OOK · GPIO 1 reçoit les impulsions · pas de mesure RSSI ni de réception universelle.')
wiring('rfid', 'Lire une carte F08 avec le RFID2', 'RFID2 · WS1850S', ['GND', '5 V', 'SDA · I²C', 'SCL · I²C'], 'Adresse 0x28 · présenter une seule carte près de l’antenne · la carte ne se raccorde à aucun fil.')
wiring('ir-reflectif', 'Mesurer une réflexion infrarouge', 'U175 · IR réflectif', ['GND', '5 V', 'DO · sortie numérique', 'AO · sortie analogique'], 'AO/DO référencés au 3,3 V interne de l’U175 · ce capteur ne décode pas les télécommandes TV.')
wiring('gps', 'Recevoir les données du GPS v1.1', 'GPS/BDS · AT6668', ['GND', '5 V', 'RX du module ← G2 TX', 'TX du module → G1 RX'], 'UART : 115200 bauds, 8N1 · RX du Cardputer = G1 · orienter l’antenne vers le ciel.')


# Variante pour les extensions dont le câblage dépasse les quatre fils du Grove ; la hauteur dépend du
# nombre de lignes.
def table_diagram(name, title, subtitle, rows, footer):
    height = 175 + 44 * len(rows)
    s = svg_start(title, subtitle, height)
    for i, (a,b) in enumerate(rows):
        y = 112 + i * 44
        s += f'<rect x="40" y="{y-23}" width="1020" height="39" rx="6" fill="{"#223750" if i%2==0 else "#192b42"}"/><text class="pin" x="58" y="{y+3}">{escape(a)}</text><text class="pin" x="510" y="{y+3}">{escape(b)}</text>'
    s += f'<text class="small" x="40" y="{height-22}">{escape(footer)}</text></svg>'
    (ASSETS / (name + '.svg')).write_text(s)


table_diagram('nrf24', 'NRF24 : extension par adaptateur microSD / SPI', 'Matériel supplémentaire · aucune carte SD · deux stations', [
('Grove 5 V → régulateur 3,3 V','Sortie 3,3 V → VCC du NRF24'),('GND','GND du NRF24 et du régulateur'),('microSD CLK / G40','SCK du NRF24'),('microSD CMD / MOSI / G14','MOSI du NRF24'),('microSD DAT0 / MISO / G39','MISO du NRF24'),('Grove G2 / jaune','CE du NRF24'),('Grove G1 / blanc','CSN du NRF24'),('G12 maintenu haut ; IRQ libre','Vérifier les signaux de l’adaptateur')], 'Ne jamais alimenter le NRF24 nu directement avec le 5 V Grove. Montage de principe à valider.')
table_diagram('fm', 'Écouter la FM avec un RDA5807', 'Matériel supplémentaire · réception uniquement', [
('Grove 5 V → régulateur 3,3 V','3,3 V → module RDA5807 compatible'),('GND','Masse commune'),('G2 / jaune','SDA, résistances de rappel vers 3,3 V'),('G1 / blanc','SCL, résistances de rappel vers 3,3 V'),('Antenne et sortie audio du module','Casque / amplificateur adapté')], 'Vérifier le breakout exact. Le haut-parleur intégré ne reçoit pas automatiquement cet audio.')

s = svg_start('CARDPUTER LAB', 'Un atelier en français · 20 programmes · 8 équipements documentés', 460)
for i,(title,body) in enumerate([('CARDPUTER SEUL','Clavier · écran · son · Wi-Fi · BLE'),('UNITÉS GROVE','RF433 · RFID · IR réflectif · GPS'),('EXTENSIONS','FM · NRF24 · matériel additionnel')]):
    x = 40 + i * 347
    s += f'<rect x="{x}" y="130" width="325" height="210" rx="16" fill="#223750"/><rect x="{x+20}" y="152" width="55" height="6" rx="3" fill="#62dfcf"/><text class="pin" x="{x+20}" y="200">{title}</text>'
    words=body.split(' · ')
    for j,word in enumerate(words):
        s += f'<text class="small" x="{x+20}" y="{230+22*j}">{escape(word)}</text>'
s += '<text class="sub" x="40" y="408">Comprendre le câblage. Compiler une expérience. Observer et documenter le résultat.</text></svg>'
(ASSETS / 'laboratoire.svg').write_text(s)

# Transformer les tuples en objets nommés pour le JavaScript de l’aperçu ; les valeurs screen sont
# fictives.
data = [dict(folder=f, env=e, title=t, hardware=h, usage=u, expected=r, guide=g, source=s, screen=v) for f,e,t,h,u,r,g,s,v in EXPERIMENTS]
# Le HTML et son JavaScript sont générés ici. Modifier ce modèle avant de régénérer tools/apercu.html,
# sinon les changements directs seront perdus.
html = '''<!doctype html><!-- Généré par tools/build_assets.py depuis lab_catalog.py ; valeurs fictives, aucun firmware exécuté. --><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cardputer Lab — aperçu pédagogique</title>
<style>
*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,sans-serif;background:#0c1727;color:#eaf3ff}main{max-width:1180px;margin:32px auto;padding:28px}.eyebrow{letter-spacing:.15em;font-size:13px;color:#6bdfcf}h1{font-size:38px;line-height:1.15;margin:16px 0}h2{font-size:19px}p{color:#b7c9df}select,button{font:inherit;background:#213b58;color:#fff;border:1px solid #456080;border-radius:8px;padding:12px;max-width:100%}.banner{border-left:4px solid #ebbd63;background:#292a2e;padding:13px 18px;color:#f1dbb2;margin:25px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.panel{background:#182b43;padding:28px;border:1px solid #2a405b;border-radius:16px}.screen{background:#000;border:14px solid #364354;border-radius:13px;width:508px;max-width:100%;height:298px;font:19px/1.7 monospace;overflow:hidden}.screen .bar{font-size:17px;background:#004aa8;padding:5px 8px;color:white}.screen pre{white-space:pre-wrap;margin:14px;color:#fff;font:17px/1.7 monospace}.keys{display:grid;grid-template-columns:repeat(10,1fr);gap:5px;margin-top:15px}.keys span{background:#33455b;text-align:center;border-radius:4px;font:12px monospace;padding:8px 0}.caption{font-size:13px;color:#d8bd88;margin-top:16px}code{font-family:monospace;color:#75e0d0}.command{font:14px/1.9 monospace;white-space:pre-wrap;background:#0c1727;padding:16px;border-radius:8px;overflow-wrap:anywhere}a{color:#79dbff}.footer{margin-top:24px;font-size:13px;color:#809dbd}.install{display:none}.install li{margin:14px 0}@media(max-width:850px){.grid{grid-template-columns:1fr}h1{font-size:30px}}
</style><main><div class="eyebrow">CARDPUTER LAB / GUIDE VISUEL</div><h1 id="title">Une expérience à la fois</h1><p>Choisir le matériel, suivre le guide, puis comparer avec son essai réel.</p>
<select id="choice" aria-label="Choisir une expérience"><option value="installation">Installation et compilation</option></select>
<div class="banner">DÉMONSTRATION — ces vues sont des maquettes pédagogiques. Valeurs fictives, aucun appareil connecté.</div>
<div class="grid" id="experiment"><div class="panel"><div class="screen"><div class="bar" id="bar"></div><pre id="screen"></pre></div><div class="keys" aria-hidden="true"></div><div class="caption">Écran représenté à titre indicatif ; ce navigateur n’émule pas l’ESP32.</div></div><div class="panel"><h2>Préparer</h2><p id="hardware"></p><h2>Manipuler</h2><p id="usage"></p><h2>Résultat attendu</h2><p id="expected"></p><pre class="command" id="command"></pre><a id="guide">Lire le guide détaillé</a></div></div>
<div class="panel install" id="installation"><h2>Du projet au premier diagnostic</h2><ol><li>Créer l’environnement Python, puis installer PlatformIO.</li><li>Télécharger les sources aux commits du manifeste.</li><li>Compiler le diagnostic avant de connecter un accessoire.</li><li>Détecter le port USB réel, puis téléverser.</li></ol><pre class="command">python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/fetch_upstream.py
pio run -e diagnostic
pio device list
pio run -e diagnostic -t upload --upload-port PORT</pre><p>PORT est une valeur à remplacer. L’image ne représente pas une exécution de ces commandes.</p></div>
<div class="footer">K132 d’origine · guides en français · sources et limites documentées dans le dépôt</div></main>
<script>const data=CATALOG;
const choice=document.querySelector('#choice');for(const item of data){let option=new Option(item.folder.slice(0,2)+' — '+item.title,item.env);choice.add(option)}
document.querySelector('.keys').innerHTML='Q W E R T Y U I O P A S D F G H J K L ↵ Z X C V B N M , . ␣'.split(' ').map(x=>'<span>'+x+'</span>').join('');
function draw(){let id=location.hash.slice(1)||'diagnostic';let item=data.find(x=>x.env===id);choice.value=item?id:'installation';document.querySelector('#experiment').style.display=item?'grid':'none';document.querySelector('#installation').style.display=item?'none':'block';document.querySelector('#title').textContent=item?item.title:'Installation et premier démarrage';if(!item)return;document.querySelector('#bar').textContent=item.folder.slice(0,2)+' | '+item.title;document.querySelector('#screen').textContent=item.screen.join('\\n');for(let key of ['hardware','usage','expected'])document.getElementById(key).textContent=item[key];document.querySelector('#command').textContent='pio run -e '+item.env+'\\npio run -e '+item.env+' -t upload --upload-port PORT';document.querySelector('#guide').href='../docs/'+item.guide}
choice.addEventListener('change',()=>location.hash=choice.value);window.addEventListener('hashchange',draw);draw();</script></html>'''
(ROOT / 'tools/apercu.html').write_text(html.replace('CATALOG', json.dumps(data, ensure_ascii=False)))
print('9 schémas SVG et aperçu HTML générés.')
