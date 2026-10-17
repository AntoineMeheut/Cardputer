# Prépare les inventaires, extraits et fiches HTML nécessaires à la composition PDF. Voir README.md
# pour les commandes, les sorties et les prérequis.
from pathlib import Path
import json, sys, html, csv, hashlib, re, shutil
from collections import Counter
from content import UPSTREAM, DRAFTS, APPS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'tmp/pdfs'
OUT.mkdir(exist_ok=True, parents=True)
(OUT/'captures').mkdir(exist_ok=True)
manifest=json.loads((ROOT/'upstream/manifest.json').read_text())['projects']
cards=[]

# Sélectionner un fichier existant : point d’entrée préféré, programme Python, sketch ou README. Ce
# choix est documentaire, pas un choix de cible de compilation.
def choose_source(base, preferred=None):
    if preferred and (base/preferred).is_file(): return base/preferred
    py=sorted(p for p in base.rglob('*.py') if p.name not in ['keyboard.py','st7789py.py','knight_sprites.py'] and not p.name.startswith('vga'))
    if py: return max(py,key=lambda p:p.stat().st_size)
    src=sorted(base.rglob('*.ino'))+sorted(base.rglob('*.cpp'))
    if src:return src[0]
    return base/'README.md'

# Conserver les numéros de lignes d’origine et limiter l’extrait à 27 lignes ; les longs bandeaux de
# commentaires C sont évités.
def excerpt(path):
    s=path.read_text(errors='replace') if path.exists() else 'Aucun source textuel à cet emplacement.'
    lines=s.splitlines()
    # Préférer le début du programme effectif aux longs bandeaux de licence.
    start=0
    if path.suffix in ['.cpp','.ino','.h']:
        start=next((i for i,l in enumerate(lines) if l.startswith('#include') or l.startswith('void setup')),0)
    if path.suffix=='.py':
        start=next((i for i,l in enumerate(lines) if l.startswith(('import ','from ','class ','def '))),0)
    return '\n'.join(f'{i+1:>3}  {l}' for i,l in list(enumerate(lines))[start:start+27])

# Une fiche par instantané au commit figé ; ne pas assimiler la version téléchargée à la version
# actuelle du projet en ligne.
for e in manifest:
    id=e['id']; title,desc,demo,entry,images,limit=UPSTREAM[id]
    base=ROOT/'upstream/sources'/id
    source=choose_source(base,'src/main.cpp' if id=='bruce' else entry)
    cards.append(dict(id='up-'+id,kind='Projet tiers • instantané local',title=title,desc=desc,usage=demo,limit=limit,source=source.relative_to(ROOT).as_posix(),code=excerpt(source),files=[p.name+('/' if p.is_dir() else '') for p in sorted(base.iterdir()) if not p.name.startswith('.')][:16],revision=e['commit'][:12]))
for folder,title,desc,replacement in DRAFTS:
    base=ROOT/'experiments'/folder; source=choose_source(base,'main.cpp')
    cards.append(dict(id='draft-'+folder,kind='Brouillon conservé • hors PlatformIO',title=title,desc=desc,usage='Version active à consulter : '+replacement,limit='Aucune compilation ni exécution de ce brouillon n’est attestée. Les interfaces Lab.h et lab_logic.h sont distinctes du parcours actif.',source=source.relative_to(ROOT).as_posix(),code=excerpt(source),files=[p.name for p in sorted(base.iterdir())],revision='Brouillon local'))
for name,(title,usage,hardware) in APPS.items():
    base=ROOT/'upstream/sources/microhydra-apps/app-source'/name
    source=choose_source(base)
    cards.append(dict(id='app-'+name,kind='Application MicroHydra • fiche de source',title=name+' / '+title,desc='Compatibilité déclarée dans l’archive : '+hardware,usage=usage,limit='Vue documentaire. Cette application n’a pas été exécutée sur un Cardputer pour le guide.',source=source.relative_to(ROOT).as_posix(),code=excerpt(source),files=[p.relative_to(base).as_posix() for p in sorted(base.rglob('*')) if p.is_file() and p.name!='.DS_Store'][:15],revision='72f3e9104b44'))

# Compléments autonomes présents dans les sous-répertoires.
# Sous-projets autonomes : frontend, application Android, programmes auxiliaires et applications
# internes.
NESTED=[
('launcher-web','upstream/sources/launcher/webUi','Interface Web de Launcher','Pages de connexion, gestion de fichiers et serveur de développement. Le backend appartient à l’interface de développement ; ce n’est pas le firmware.', 'backend/README.md'),
('bus-web','upstream/sources/bus-pirate/webui','Interface Web de Bus Pirate','Interface HTML intégrée dans des en-têtes C pour les fonctions de la console et du stockage. Un appareil compatible doit fournir les services auxquels elle se connecte.','index.h'),
('bus-flasher','upstream/sources/bus-pirate/webflasher','Installateur Web de Bus Pirate','Frontend de programmation. Lire le manifeste de la carte et distinguer fichier d’application et image fusionnée avant toute écriture.','index.html'),
('evil-android','upstream/sources/evil-cardputer/EvilRelayAPK','EvilRelayAPK','Projet Android compagnon : fichiers Gradle et application sous app/. Il ne s’installe pas sur le Cardputer et n’a pas été compilé ici.','README.md'),
('evil-slave','upstream/sources/evil-cardputer/slave','Esclaves ESP32 et variantes C5','Sketches auxiliaires de collecte, GNSS, relais, maillage et fonctions réseau. Chaque fichier cible un matériel et un protocole particuliers.','README.md'),
('evil-utils','upstream/sources/evil-cardputer/utilities','Utilitaires de Evil-Cardputer','Outils PC pour les données, cartographie et protocoles. Le catalogue du guide recense les sous-projets ; leur présence ne signifie pas qu’un service a été démarré.','README.md'),
('demo-apps','upstream/sources/cardputer-demo/main/apps','Applications de la démonstration officielle','Dix applications et un lanceur : clavier, texte, micro, minuteur, Wi-Fi, chat, IR et REPL, assemblés dans un seul firmware ESP-IDF.','apps.h'),
]
for id,path,title,desc,entry in NESTED:
    base=ROOT/path;source=choose_source(base,entry)
    cards.append(dict(id=id,kind='Sous-projet embarqué dans un dépôt tiers',title=title,desc=desc,usage='Point d’entrée : '+path,limit='Présentation documentaire ; installation et exécution non réalisées.',source=source.relative_to(ROOT).as_posix(),code=excerpt(source),files=[p.name+('/' if p.is_dir() else '') for p in sorted(base.iterdir()) if not p.name.startswith('.')][:16],revision='Archive figée'))

(OUT/'cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2))
CSS='''*{box-sizing:border-box}body{margin:0;background:#edf2f7;color:#142439;font:16px Arial,sans-serif}header{background:#11263d;color:white;padding:23px 36px;border-bottom:5px solid #24acac}.label{text-transform:uppercase;letter-spacing:2px;font-size:12px;color:#8de3db}h1{font-size:29px;margin:9px 0}main{padding:22px 36px;display:grid;grid-template-columns:32% 66%;gap:2%}aside p{line-height:1.45;margin:0 0 16px}h2{font-size:16px;color:#177f85;margin:18px 0 9px}ul{padding-left:18px;line-height:1.5;font-size:13px;overflow-wrap:anywhere}pre{background:#102438;color:#edf4fc;padding:18px 20px;border-radius:8px;font:13px/1.45 Menlo,monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:0;max-height:615px;overflow:hidden}.source{font:12px/1.4 Menlo,monospace;overflow-wrap:anywhere;margin:0 0 10px;padding:9px;background:#dce7ef}.limit{border-left:4px solid #d18735;padding:10px;background:#fff5e6;font-size:13px;line-height:1.45}footer{margin:0 36px 24px;color:#526477;font-size:12px;border-top:1px solid #c5d3dd;padding-top:12px}'''
PAGE='''<!doctype html><html lang="fr"><meta charset="utf-8"><title>Atlas documentaire Cardputer</title><style>CSS</style><header><div class="label" id="kind"></div><h1 id="title"></h1><div id="revision"></div></header><main><aside><p id="desc"></p><h2>Démonstration à préparer</h2><p id="usage"></p><div class="limit" id="limit"></div><h2>Repères du répertoire</h2><ul id="files"></ul></aside><section><div class="source" id="source"></div><pre id="code"></pre></section></main><footer>VUE DOCUMENTAIRE • Capture du navigateur, produite à partir des fichiers locaux. Ce visuel ne représente pas l’exécution du firmware. Édition du 17 octobre 2026.</footer><script>const cards=DATA;function draw(){let id=location.hash.slice(1);let c=cards.find(x=>x.id===id)||cards[0];for(let k of ['kind','title','desc','usage','limit','source','code'])document.getElementById(k).textContent=c[k];document.getElementById('revision').textContent='Révision : '+c.revision;document.getElementById('files').replaceChildren(...c.files.map(x=>{let li=document.createElement('li');li.textContent=x;return li}));document.title=c.title+' | Atlas Cardputer';scrollTo(0,0)}window.onhashchange=draw;draw();</script></html>'''
(OUT/'atlas.html').write_text(PAGE.replace('CSS',CSS).replace('DATA',json.dumps(cards,ensure_ascii=False).replace('</',r'<\/')))
(OUT/'fiches').mkdir(exist_ok=True)
for c in cards:
    esc=lambda k:html.escape(c[k])
    body=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{esc('title')}</title><style>{CSS}</style></head><body><header><div class="label">{esc('kind')}</div><h1>{esc('title')}</h1><div>Révision : {esc('revision')}</div></header><main><aside><p>{esc('desc')}</p><h2>Démonstration à préparer</h2><p>{esc('usage')}</p><div class="limit">{esc('limit')}</div><h2>Repères du répertoire</h2><ul>{''.join('<li>'+html.escape(x)+'</li>' for x in c['files'])}</ul></aside><section><div class="source">{esc('source')}</div><pre>{esc('code')}</pre></section></main><footer>VUE DOCUMENTAIRE • Capture du navigateur à partir des fichiers locaux. Application non exécutée sur matériel. 17 octobre 2026.</footer></body></html>'''
    (OUT/'fiches'/f'{c["id"]}.html').write_text(body)

# Inventaire reproductible : chaque répertoire de contenu, chaque fichier et chaque sketch.
# Périmètre de l’inventaire : les caches compilés, environnements virtuels, métadonnées Finder et
# fichiers du générateur lui-même sont exclus.
scopes=['docs','experiments','fixtures','include','lib','tests','tools','upstream/sources','.github']
directories=[]; files=[]; examples=[]; nested=[]
for scope in scopes:
    base=ROOT/scope
    for p in sorted(base.rglob('*')):
        rel=p.relative_to(ROOT).as_posix()
        if '__pycache__' in p.parts or p.name=='.DS_Store' or 'tools/guide_pdf' in rel:continue
        if p.is_dir():
            direct=[x for x in p.iterdir() if x.is_file() and x.name!='.DS_Store']
            directories.append({'path':rel,'files':len(direct)})
        elif p.is_file():
            files.append({'path':rel,'bytes':p.stat().st_size})
            if p.suffix=='.ino' or ('examples' in rel and p.suffix in ['.py']): examples.append(rel)
            if p.name in ['library.properties','library.json','package.json','pyproject.toml','setup.py','build.gradle','build.gradle.kts']:
                nested.append(rel)
for name,rows,fields in [('inventaire-repertoires.csv',directories,['path','files']),('inventaire-fichiers.csv',files,['path','bytes'])]:
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(OUT/'inventory.json').write_text(json.dumps({'directories':directories,'files':files,'examples':examples,'nested':nested},ensure_ascii=False,indent=2))
print(f'{len(cards)} fiches, {len(directories)} répertoires, {len(files)} fichiers, {len(examples)} sketches/exemples Python.')
