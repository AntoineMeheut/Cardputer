# Composition ReportLab du guide, puis ajout des pièces jointes avec PyMuPDF. Voir README.md pour les
# commandes, les sorties et les prérequis.
"""Compose le guide complet et ses annexes ; aucune écriture sur le matériel."""
from pathlib import Path
import sys, json, re, html, textwrap, hashlib, csv, io
from collections import defaultdict
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle, Image, Preformatted, XPreformatted, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage, ImageOps
import pymupdf as fitz
from content import UPSTREAM, DRAFTS, APPS, EXPERIMENT_DETAILS

ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'tmp/pdfs'; OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
ASSETS=ROOT/'tools/guide_pdf/assets'
sys.path.insert(0,str(ROOT/'tools'))
from lab_catalog import EXPERIMENTS
MANIFEST=json.loads((ROOT/'upstream/manifest.json').read_text())['projects']
INV=json.loads((TMP/'inventory.json').read_text())
CARDS={x['id']:x for x in json.loads((TMP/'cards.json').read_text())}
VERIFICATION=json.loads((ASSETS/'verification-sources-2026-10-17.json').read_text())
COMPILE=json.loads((ROOT/'docs/validation-compilation.json').read_text())
PAGES=[]; FIGURES=[]; SOURCES=set(); STORY=[]
W,H=595.276,841.89; M=43; CW=W-2*M
NAVY=colors.HexColor('#102A43'); TEAL=colors.HexColor('#0E8585'); INK=colors.HexColor('#203449'); PALE=colors.HexColor('#EDF4F8'); ORANGE=colors.HexColor('#C87929')
fontdir=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Italic','Arial Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
pdfmetrics.registerFont(TTFont('Mono','/System/Library/Fonts/Menlo.ttc'))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
styles={
'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=14.3,textColor=INK,spaceAfter=7),
'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,textColor=INK,spaceAfter=5),
'tiny':ParagraphStyle('tiny',fontName='Body',fontSize=7,leading=9.2,textColor=INK,spaceAfter=3),
'caption':ParagraphStyle('caption',fontName='Body',fontSize=8,leading=11,textColor=colors.HexColor('#566A7D'),spaceAfter=12),
'h1':ParagraphStyle('h1',fontName='Bold',fontSize=26,leading=30,textColor=NAVY,spaceAfter=14,keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='Bold',fontSize=19,leading=23,textColor=NAVY,spaceBefore=4,spaceAfter=12,keepWithNext=True),
'h3':ParagraphStyle('h3',fontName='Bold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=11,spaceAfter=6,keepWithNext=True),
'h4':ParagraphStyle('h4',fontName='Bold',fontSize=10,leading=14,textColor=TEAL,spaceBefore=8,spaceAfter=4,keepWithNext=True),
'code':ParagraphStyle('code',fontName='Mono',fontSize=8,leading=10.8,textColor=NAVY,backColor=PALE,borderPadding=8,spaceBefore=4,spaceAfter=12),
'tag':ParagraphStyle('tag',fontName='Bold',fontSize=8.2,leading=12,textColor=TEAL,spaceAfter=8),
}

# Normaliser seulement les caractères typographiques qui posent problème à la composition ; ne pas
# employer cette fonction pour réécrire un source.
def clean(t):
    return str(t).replace('\u00a0',' ').replace('\u202f',' ').replace('—','-').replace('–','-').replace('‑','-').replace('→',' > ').replace('≥','>=').replace('≤','<=')

# Échapper le texte avant d’ajouter un sous-ensemble contrôlé de mise en forme ; les liens HTTP
# restent cliquables.
def inline(s):
    s=clean(s)
    # Échapper d’abord, puis appliquer seulement les balises contrôlées.
    s=escape(s)
    s=re.sub(r'`([^`]+)`',lambda m:'<font name="Mono" size="8.5">'+m.group(1)+'</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:('<link href="'+m.group(2).replace('"','%22')+'" color="#0e8585">'+m.group(1)+'</link>') if m.group(2).startswith('http') else m.group(1),s)
    return s

# Créer un paragraphe sans l’ajouter au document ; utile pour les cellules de tableaux et les
# encadrés.
def p(s,style='body'):return Paragraph(inline(s),styles[style])
# Ajouter un paragraphe au flux global STORY, composé ultérieurement en plusieurs passes.
def add(s,style='body'):STORY.append(p(s,style))
# Petit repère de type de programme ou de provenance, distinct des titres du sommaire.
def tag(s):add(s.upper(),'tag')
# Vérifier l’existence de chaque chemin cité et le mémoriser pour l’annexe des sources.
def source(path):
    path=str(path).replace(str(ROOT)+'/','')
    if not (ROOT/path).exists():raise FileNotFoundError('Source citée absente : '+path)
    SOURCES.add(path);add('Source locale : '+path,'caption')
# Associer au titre les métadonnées nécessaires aux signets et aux entrées de sommaire.
def heading(title,level=0,key=None):
    q=p(title,'h1' if level==0 else 'h2');q._toc_level=level;q._toc_title=clean(title);q._bookmark=key or ('s'+str(len(STORY)));STORY.append(q)
# Sous-titre visuel qui ne crée pas de signet PDF supplémentaire.
def sub(title):add(title,'h3')
# Éviter les sauts de page consécutifs qui créeraient des pages blanches.
def page():
    if STORY and not isinstance(STORY[-1],PageBreak):STORY.append(PageBreak())
# Conserver les sauts de ligne et échapper les signes XML ; le retour à 96 colonnes sert seulement à
# l’impression.
def code(s):
    lines=[]
    for l in clean(s).splitlines():
        lines.extend(textwrap.wrap(l, width=96,replace_whitespace=False,drop_whitespace=False,break_long_words=True,break_on_hyphens=False) or [''])
    STORY.append(XPreformatted(escape('\n'.join(lines)),styles['code']))
# Créer un encadré de lecture avec un titre et un texte ; les dimensions suivent la largeur utile A4.
def box(title,text):
    t=Table([[p(title,'h4')],[p(text,'small')]],colWidths=[CW-22]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#CBDBE5')),('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));STORY.extend([t,Spacer(1,12)])
# Les en-têtes doivent être blancs dès la création des Paragraph : changer uniquement le style du
# tableau ne recolore pas leurs fragments.
def table(rows,widths=None,small=True,repeat=1):
    style='small' if small else 'body'
    header_style=ParagraphStyle('th',parent=styles[style],textColor=colors.white,fontName='Bold')
    data=[[Paragraph(inline(str(x)),header_style) if row_index==0 else p(str(x),style) for x in row] for row_index,row in enumerate(rows)]
    t=Table(data,colWidths=widths or [CW/len(rows[0])]*len(rows[0]),repeatRows=repeat,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    STORY.extend([t,Spacer(1,10)])

# Ajuster l’image sans déformer son ratio ; conserver figure et légende ensemble et enregistrer la
# provenance.
def image(path,caption,kind='Capture existante',maxh=260,maxw=CW):
    path=Path(path)
    if not path.is_absolute():path=ROOT/path
    if not path.exists():raise FileNotFoundError(path)
    original=path
    if path.suffix=='.svg':
        dst=TMP/'assets'/f'{path.stem}-styles.png';dst.parent.mkdir(exist_ok=True)
        if not dst.exists():
            # MuPDF ignore certaines règles CSS de SVG : les transférer vers
            # les attributs de présentation, sans changer le dessin d'origine.
            root=ET.fromstring(path.read_bytes());rules={}
            for el in root.iter():
                if el.tag.endswith('}style'):
                    for sel,decl in re.findall(r'([^{}]+)\{([^{}]+)\}',el.text or ''):
                        rules[sel.strip()]={k.strip():v.strip() for k,v in (x.split(':',1) for x in decl.split(';') if ':' in x)}
            for el in root.iter():
                attrs={};attrs.update(rules.get(el.tag.split('}')[-1],{}))
                for cls in el.get('class','').split():attrs.update(rules.get('.'+cls,{}))
                for k,v in attrs.items():
                    if k not in el.attrib:el.set(k,v)
            d=fitz.open(stream=ET.tostring(root),filetype='svg');d[0].get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False).save(dst)
        path=dst
    elif path.suffix.lower() in ['.gif','.webp']:
        dst=TMP/'assets'/f'{path.parent.name}-{path.stem}.png';dst.parent.mkdir(exist_ok=True)
        im=PILImage.open(path);im.seek(min(2,getattr(im,'n_frames',1)-1));im.convert('RGB').save(dst);path=dst
    im=PILImage.open(path);iw,ih=im.size;scale=min(maxw/iw,maxh/ih)
    fig=Image(str(path),width=iw*scale,height=ih*scale);fig.hAlign='CENTER'
    fid=len(FIGURES)+1
    rel=str(original).replace(str(ROOT)+'/','')
    cap=f'Figure {fid:03d} · {kind}. {caption}'
    # Une légende de provenance reste avec son image.
    STORY.append(KeepTogether([fig,Spacer(1,5),p(cap,'caption')]))
    FIGURES.append({'number':fid,'kind':kind,'path':rel,'caption':caption})
    SOURCES.add(rel)

# N’utiliser une capture que si le fichier existe ; sinon produire un extrait explicitement
# documentaire.
def screenshot_or_source(cardid,maxh=290):
    c=CARDS[cardid];shot=ASSETS/f'{cardid}.png'
    if shot.exists():image(shot,'Fiche documentaire du projet ; logiciel non exécuté sur matériel.','Capture navigateur du guide',maxh=maxh)
    else:
        sub('Vue du code ou du document de référence')
        # Extrait textuel, volontairement pas qualifié de capture de firmware.
        if c['source'].endswith('.md'):add('Extrait de la notice originale, conservé dans sa langue ; la présentation française figure ci-dessus.','small')
        add(c['source'],'caption');code(c['code'])

# Petit lecteur du Markdown local : titres, listes simples, tableaux, images et blocs de code. Il ne
# vise pas toute la spécification Markdown.
def md_doc(path,title=None,images=True):
    path=ROOT/path;SOURCES.add(path.relative_to(ROOT).as_posix())
    text=path.read_text();lines=text.splitlines();i=0;buf=[]
    def flush():
        if buf:add(' '.join(buf));buf.clear()
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            flush(); block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            code('\n'.join(block))
        elif line.startswith('# '):
            flush()
            if title is not False:heading(title or line[2:],1)
        elif line.startswith('##'):
            flush();add(line.lstrip('# ').strip(),'h3' if line.startswith('## ') else 'h4')
        elif re.match(r'^!\[',line):
            flush();m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line)
            if m and images:
                pp=(path.parent/m.group(2)).resolve()
                if pp.exists():image(pp,m.group(1),'Schéma du dépôt' if pp.suffix=='.svg' else 'Aperçu pédagogique existant',maxh=225)
        elif line.startswith('|'):
            flush();rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                row=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.match(r'^[-: ]+$',x) for x in row):rows.append(row)
                i+=1
            if rows:table(rows)
            continue
        elif re.match(r'^\s*(\d+\.|[-*]) ',line):
            flush();add(line)
        elif not line.strip():flush()
        else:buf.append(line.strip())
        i+=1
    flush();source(path)

# Couverture dessinée directement sur le canevas ; l’image utilisée reste attribuée à son projet
# d’origine.
class Cover(Flowable):
    def __init__(self):Flowable.__init__(self);self.width=CW;self.height=690
    def draw(self):
        c=self.canv;c.setFillColor(NAVY);c.rect(-M,-90,W,H+90,fill=1,stroke=0)
        c.setFillColor(TEAL);c.rect(0,632,58,6,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#80DED4'));c.setFont('Bold',11);c.drawString(0,660,'CARDPUTER LAB  /  GUIDE DE RÉFÉRENCE')
        c.setFillColor(colors.white);c.setFont('Bold',43);c.drawString(0,566,'Explorer.');c.drawString(0,516,'Comprendre.');c.drawString(0,466,'Expérimenter.')
        c.setFont('Body',15);c.drawString(0,418,'Le projet, ses programmes et ses archives');c.drawString(0,395,'Guide illustré en français')
        pic=ROOT/'upstream/sources/bus-pirate/images/cardputer.jpg'
        c.drawImage(str(pic),18,146,width=365,height=244,preserveAspectRatio=True,mask='auto',anchor='c')
        c.setFillColor(colors.HexColor('#C6D9E6'));c.setFont('Body',8);c.drawString(0,127,'Photographie d’origine : ESP32 Bus Pirate, images/cardputer.jpg.')
        c.setFont('Bold',14);c.setFillColor(colors.white);c.drawString(0,83,'20 expériences  ·  19 brouillons  ·  18 projets tiers')
        c.setFont('Body',12);c.drawString(0,59,'30 applications MicroHydra et catalogue des sous-projets')
        c.setFont('Body',10);c.setFillColor(colors.HexColor('#80DED4'));c.drawString(0,14,'ÉDITION DU 17 OCTOBRE 2026  ·  CIBLE : CARDPUTER K132')

# Gabarit A4 avec pagination et sommaire. multiBuild permet de recalculer les pages des entrées après
# la première composition.
class Doc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=47,bottomMargin=45,title='Cardputer Lab - Guide complet illustré',author='Documentation du projet Cardputer Lab',subject='Guide français : expériences, matériel, firmwares, applications et inventaire',pageCompression=1)
        self.chapter='Cardputer Lab';self.all_entries=[]
        self.addPageTemplates(PageTemplate(id='normal',frames=Frame(M,44,CW,H-96,id='f',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPageEnd=self.decorate))
    # Réinitialiser l’état à chaque passe afin de ne pas accumuler les signets ou les titres de chapitres.
    def beforeDocument(self):self.chapter='Cardputer Lab';self.all_entries=[]
    # Exécuté en fin de page : le pied de page peut alors utiliser le chapitre effectivement rencontré sur
    # cette page.
    def decorate(self,c,doc):
        if doc.page==1:return
        c.saveState();c.setStrokeColor(TEAL);c.setLineWidth(1.2);c.line(M,H-27,W-M,H-27)
        c.setFillColor(NAVY);c.setFont('Bold',7.5);c.drawString(M,H-20,'CARDPUTER LAB  /  GUIDE ILLUSTRÉ')
        c.setFillColor(colors.HexColor('#63788B'));c.setFont('Body',7.5);c.drawRightString(W-M,H-20,'17 OCTOBRE 2026')
        c.setStrokeColor(colors.HexColor('#D5E0E8'));c.setLineWidth(.5);c.line(M,31,W-M,31)
        c.setFont('Body',7);c.drawString(M,19,self.chapter[:100]);c.setFont('Bold',8);c.drawRightString(W-M,19,str(doc.page));c.restoreState()
    # Lorsqu’un titre est placé, publier sa page dans le sommaire et créer la destination du lien interne.
    def afterFlowable(self,f):
        if hasattr(f,'_bookmark'):
            key=f._bookmark;self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f._toc_title,key,f._toc_level,False)
            self.notify('TOCEntry',(f._toc_level,f._toc_title,self.page,key));self.all_entries.append({'title':f._toc_title,'level':f._toc_level,'page':self.page,'key':key})
            if f._toc_level==0:self.chapter=f._toc_title

STORY.append(Cover());page()
add('Sommaire','h1');add('Le sommaire et les signets du lecteur PDF permettent d’accéder directement aux fiches. Les chemins indiqués sont relatifs à la racine Cardputer.','small')
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='Bold',fontSize=10.4,leading=16,textColor=NAVY,spaceBefore=7),ParagraphStyle('toc1',fontName='Body',fontSize=8.6,leading=12.2,textColor=INK,leftIndent=14,firstLineIndent=0,spaceBefore=2)];STORY.append(toc);page()
heading('1. Lire le laboratoire et ce guide')
add('Ce guide présente le contenu local du projet Cardputer au 17 octobre 2026. Il réunit les procédures françaises du dépôt, une lecture des programmes, les projets tiers figés, leurs applications et les répertoires imbriqués. L’objectif est de permettre de choisir une expérience, de la préparer, d’observer un résultat et de retrouver son code.')
box('Périmètre et niveau de preuve','Les 20 environnements actifs ont un rapport de compilation daté du 10 octobre 2026. Les tests sur ordinateur et les liens documentaires ont été revérifiés le 17 octobre. Aucun Cardputer n’a été flashé ni testé pour ce guide. Les firmwares tiers et les applications MicroHydra ne sont pas présentés comme exécutés.')
table([['Famille','Couverture du guide'],['20 dossiers avec tirets','Fiche détaillée par expérience : matériel, commande, manipulation, résultat, lecture du code et dépannage.'],['19 dossiers avec soulignés','Fiche de chaque brouillon, différences et correspondance avec le parcours actif.'],['18 dépôts tiers','Présentation française, point d’entrée, parcours de découverte, captures disponibles et limites.'],['30 applications MicroHydra','Fiche individuelle, compatibilité, installation, usage et source.'],['Sous-projets et exemples','Interfaces Web, projet Android, esclaves ESP32, bibliothèques embarquées et liste de 492 sketches ou exemples Python.'],['Arborescence','Index des 1 322 sous-répertoires de contenu ; inventaire des 6 448 fichiers joint au PDF.']],[125,CW-125])
sub('Comment lire les visuels')
add('Les vues nommées **aperçu pédagogique** proviennent de tools/apercu.html : ce sont des captures du navigateur avec des valeurs fictives, pas des écrans d’un ESP32 exécuté. Les images **amont** sont déjà présentes dans les archives et sont attribuées à leurs auteurs. Les **vues du code** reproduisent un extrait textuel ; elles ne prétendent pas montrer un résultat matériel. Les captures des ateliers HTML montrent des pages autonomes.')
add('Quand aucun écran d’exécution n’est disponible, la fiche fournit une vue du source et un protocole de démonstration à réaliser. Le guide ne fabrique pas de preuve d’exécution pour compléter les images manquantes.')
source('docs/assets/captures/README.md');source('docs/etat-projet.md')
page();heading('Repères dans les répertoires',1)
table([['Répertoire','Rôle concret'],['docs/','Installation, composants, parcours thématiques, dépannage, validation, schémas et ateliers HTML.'],['experiments/','39 dossiers : 20 cibles actives et 19 brouillons. Chaque cible active possède main.cpp et README.md.'],['include/','lab_config.h : paramètres radio/IR ; rfid_lab.h : initialisation et formatage RFID.'],['lib/','CardputerLab : interface et formats communs ; RfidLegacy : adaptation du pilote historique.'],['tools/','Scripts de préparation, tests, compilation, conversion GPS et aperçus Web. tools/guide_pdf est ajouté pour produire ce document.'],['tests/ et fixtures/','Tests de formats et du convertisseur GPX ; trois points GPS fictifs.'],['upstream/','Manifeste, 18 archives compressées et leurs sources extraites.'],['build/','Journaux de compilation, rapport JSON et captures des ateliers.'],['.github/workflows/','Workflow de vérification et de compilation GitHub Actions.'],['.venv / .platformio / .pio / .cache','Dépendances et caches reproductibles ; ce ne sont pas des projets fonctionnels supplémentaires.']],[155,CW-155])
add('Le relevé des répertoires de contenu exclut les caches, __pycache__, les fichiers .DS_Store et les nouveaux fichiers de production du guide. Les caches sont décrits ici au niveau racine : .pio environ 5,8 Go, .platformio 2,4 Go, .cache 557 Mo et .venv 258 Mo, relevés lors de la préparation. Les archives upstream occupent environ 523 Mo ; les sources environ 1 Go. Ces tailles évolueront avec les compilations.','small')
sub('Trois parcours de lecture')
add('**Premier démarrage :** installation, diagnostic, carnet SD, audio. **Modules Grove :** câblage, scan I²C, RFID, capteur réflectif, GPS, puis RF433. **Exploration logicielle :** projets tiers, MicroHydra, applications, sous-projets et index des exemples.')
image('docs/assets/schemas/laboratoire.svg','Vue d’ensemble des fonctions du laboratoire.','Schéma du dépôt',maxh=225)
page();heading('2. Installer et raccorder')
md_doc('docs/installation.md')
page();md_doc('docs/compatibilite.md')
for f in ['cable-grove','cardputer','rf433-emetteur','rf433-recepteur','rfid2','cartes-f08','ir-reflectif','gps-at6668']:
    md_doc('docs/composants/'+f+'.md')
page();heading('3. Les vingt expériences actives')
add('Une cible PlatformIO construit un seul programme. Les commandes de téléversement ci-dessous sont à effectuer par le lecteur sur son port réellement détecté. PORT est un paramètre à remplacer ; aucun téléversement n’a été effectué pendant la rédaction.')
code('pio device list\npio run -e diagnostic\npio run -e diagnostic -t upload --upload-port PORT\npio device monitor --port PORT --baud 115200')
table([['N° / cible','Expérience','Accessoire principal']]+[[x[0][:2]+' / '+x[1],x[2],x[3]] for x in EXPERIMENTS],[105,190,CW-295])
CAPMAP={'wifi-scan':'wifi','ble-scan':'ble','rfid-uid':'rfid','fm-rda5807':'fm'}
SCHEMA={'i2c-scan':'rfid','rfid-uid':'rfid','rfid-bloc':'rfid','ir-reflectif':'ir-reflectif','rf433-rx':'rf433-rx','rf433-tx':'rf433-tx','gps':'gps','gps-sd':'gps','fm-rda5807':'fm','nrf24':'nrf24'}
for folder,env,title,hardware,usage,expected,guide,upstream,screen in EXPERIMENTS:
    page();heading(folder[:2]+'. '+title,1,key='exp-'+env);tag('Programme actif · '+env+' · K132')
    objective,steps,logic,debug=EXPERIMENT_DETAILS[env]
    add(objective);box('Matériel et préparation',hardware+'. Raccorder les accessoires hors tension. Guide détaillé : docs/'+guide+'.')
    img=ROOT/'docs/assets/captures'/(CAPMAP.get(env,env)+'.png')
    if img.exists():image(img,'Valeurs fictives ; lire les étapes ci-dessous pour l’essai réel.','Aperçu pédagogique existant',maxh=300)
    else:
        # Affichage pédagogique imprimé, jamais présenté comme capture matérielle.
        box('Écran attendu - transcription illustrative','<br/>'.join(screen).replace('<br/>',' / '))
    sub('Démonstration pas à pas')
    for i,s in enumerate(steps,1):add(f'{i}. {s}')
    sub('Résultat à vérifier');add(expected)
    page();add(folder[:2]+'. '+title+' - mise en œuvre','h2')
    sub('Compiler, installer, observer')
    code(f'pio run -e {env}\npio run -e {env} -t upload --upload-port PORT\npio device monitor --port PORT --baud 115200')
    sub('Ce que fait réellement le programme');add(logic)
    sub('En cas d’écart');add(debug)
    if env in SCHEMA:image('docs/assets/schemas/'+SCHEMA[env]+'.svg','Raccordement de principe ; vérifier les noms des signaux.','Schéma du dépôt',maxh=185)
    sub('Extrait à repérer dans main.cpp')
    src=ROOT/'experiments'/folder/'main.cpp';s=src.read_text().splitlines()
    # Le setup et les interactions sont préférés au simple début du fichier.
    start=next((i for i,l in enumerate(s) if 'void setup' in l),0)
    code('\n'.join(f'{i+1:>3}  {line}' for i,line in list(enumerate(s))[start:start+11]))
    record=next(x for x in COMPILE['results'] if x['environment']==env)
    add(f'Rapport du 10/10/2026 : compilation réussie ; flash {record["flash_bytes"]:,} octets, RAM statique {record["static_ram_bytes"]:,} octets. Ces valeurs ne représentent pas la consommation totale à l’exécution.'.replace(',',' '),'small')
    source(src);source('experiments/'+folder+'/README.md')

page();heading('4. Parcours thématiques et ateliers Web')
for f in ['television-ir','radio-badges','wifi-bluetooth','fm','nrf24','firmwares']:
    md_doc('docs/experiences/'+f+'.md')
page();heading('Trois portails entièrement fictifs',1)
md_doc('docs/ateliers/portails-fictifs/README.md',title=False,images=False)
image('docs/assets/portails/index-1280.png','Index des trois univers fictifs, capture déjà conservée dans le dépôt.','Capture de page Web',maxh=280)
for name,title in [('bureau','Bureau Atelier'),('banque','Banque Atelier'),('rail','Rail Atelier')]:
    page();add(title,'h2');tag('Page HTML autonome · démonstration locale')
    add('Ouvrir docs/ateliers/portails-fictifs/'+name+'-demo.html dans le navigateur. Lire le bandeau de simulation, choisir le lien Simuler et consulter l’explication locale ; revenir ensuite à l’index.')
    image('docs/assets/portails/'+name+'-demo-1280.png','Le bandeau de simulation distingue clairement cette maquette d’un service réel.','Capture de page Web',maxh=375)
    sub('Observation attendue');add('Le panneau d’explication se déplie. Aucun mot de passe réel n’est demandé et aucun compte n’est créé. L’exercice sert à expliquer l’apparence d’un portail et à discuter les indices visibles avec les participants.')
    source('docs/ateliers/portails-fictifs/'+name+'-demo.html')
page();heading('Modulations OOK, FSK et FM',1)
add('Ouvrir tools/modulation.html. Le tracé turquoise représente la porteuse ; le tracé jaune représente la commande. Le contrôle Déviation change les écarts de fréquence dans les modes FSK et FM.')
image(ASSETS/'modulation-ook.png','Mode OOK effectivement ouvert dans Chrome pour ce guide.','Capture navigateur du guide',maxh=340)
table([['Mode','Manipulation','Ce qu’il faut observer'],['OOK','Sélectionner OOK.','La porteuse est présente pour un bit et coupée pour l’autre.'],['FSK','Sélectionner FSK puis déplacer Déviation.','L’amplitude reste constante ; deux fréquences représentent les bits.'],['FM','Sélectionner FM puis déplacer Déviation.','La fréquence suit une commande analogique continue.']],[55,170,CW-225])
add('Le simulateur n’a pas d’unités RF physiques et ne modélise ni antenne, ni bruit, ni filtres, ni démodulation. Il n’émet aucun signal radio.');source('tools/modulation.html')

page();heading('5. Les dix-neuf brouillons conservés')
add('Les dossiers avec soulignés sont exclus des build_src_filter de platformio.ini. Leurs noms ressemblent aux expériences actives, mais leurs interfaces, dépendances et numéros ne sont pas interchangeables. Chaque fiche ci-dessous décrit le code conservé et le chemin actif le plus proche.')
box('Méthode de reprise','Créer un environnement distinct ou une copie de travail, inventorier les symboles et bibliothèques requis, puis compiler avant tout raccordement. Les raccourcis de capture de Lab.h ne prouvent pas que la dalle ST7789 peut fournir un écran exploitable.')
for folder,title,desc,replacement in DRAFTS:
    page();heading(folder+' - '+title,1);tag('Brouillon · non compilé dans la matrice active')
    add(desc);box('Correspondance active',replacement)
    screenshot_or_source('draft-'+folder)
    sub('Démonstration documentaire');add('Comparer les touches, constantes et appels visibles dans cet extrait avec la fiche active correspondante. Le résultat présenté ici est une lecture de source. Pour obtenir un résultat matériel, adapter et valider ce brouillon séparément.')
    source('experiments/'+folder+'/main.cpp')

page();heading('6. Les dix-huit projets tiers')
add('Les projets sont décrits à leur commit archivé, sans présumer de la version actuellement publiée en ligne. Les liens GitHub pointent vers cette révision précise. Les captures et photographies amont montrent des usages documentés par leurs auteurs ; elles ne sont pas des essais effectués pendant la rédaction.')
table([['Projet','Révision','Licence relevée']]+[[UPSTREAM[e['id']][0],e['commit'][:12],e['license_spdx']] for e in MANIFEST],[235,100,CW-335])
for e in MANIFEST:
    id=e['id'];title,desc,demo,entry,images,limit=UPSTREAM[id]
    page();heading(title,1,key='up-'+id);tag(e['license_spdx']+' · '+e['commit'][:12]);add(desc)
    sub('Parcours de découverte');add(demo)
    box('Compatibilité et limites',limit)
    source('upstream/sources/'+id+'/'+entry)
    add('[Consulter la révision archivée sur GitHub](https://github.com/'+e['repo']+'/tree/'+e['commit']+')','small')
    if images:
        image('upstream/sources/'+id+'/'+images[0],'Image fournie par '+e['repo']+' ; conserver les attributions du projet.','Visuel amont',maxh=290)
    else:screenshot_or_source('up-'+id,maxh=280)
    page();add(title+' - organisation et exemples','h2')
    base=ROOT/'upstream/sources'/id
    direct=[x for x in sorted(base.iterdir()) if x.is_dir() and not x.name.startswith('.')]
    table([['Répertoire','Repère documentaire']]+[[x.name+'/',str(sum(1 for f in x.rglob('*') if f.is_file() and f.name!='.DS_Store'))+' fichiers ; '+({'src':'implémentation de la bibliothèque ou du firmware','examples':'exemples et projets de démonstration','boards':'configurations de cartes et brochages','lib':'bibliothèques embarquées','images':'illustrations et captures d’origine','media':'illustrations, connexions et ressources','docs':'documentation technique','main':'application principale','components':'composants ESP-IDF','app-source':'30 applications détaillées au chapitre suivant','catalog-output':'paquets distribuables et catalogues','utilities':'outils complémentaires sur ordinateur','slave':'sketches pour appareils auxiliaires','SD-Card-File':'ressources destinées à la carte SD','tools':'scripts de préparation ou de construction'}.get(x.name,'voir index complet des répertoires'))] for x in direct],[150,CW-150])
    if len(images)>1:image('upstream/sources/'+id+'/'+images[1],'Autre vue fournie dans l’archive de '+e['repo']+'.','Visuel amont',maxh=240)
    elif images:screenshot_or_source('up-'+id,maxh=200)
    else:
        examples=[s for s in INV['examples'] if s.startswith('upstream/sources/'+id+'/')]
        if examples:
            sub('Exemples présents');add(' ; '.join(x.replace('upstream/sources/'+id+'/','') for x in examples[:15]),'small')
            if len(examples)>15:add(f'{len(examples)} entrées au total : liste intégrale dans l’annexe des exemples.','small')
        sub('Reproduire un essai');add('Choisir une seule cible matérielle, lire le README et les dépendances de l’exemple, adapter les broches puis construire dans un environnement séparé. Noter la version, les réglages et le résultat. Les commandes PlatformIO du laboratoire ne compilent pas automatiquement tous ces exemples.')
    source('upstream/manifest.json')

page();heading('7. Les trente applications MicroHydra')
add('Les fiches sont fondées sur app-source, README.md et details.yml de la révision 72f3e9104b44. Elles décrivent les manipulations à effectuer dans un environnement MicroHydra compatible. Les sources font appel à des modules MicroPython et aux bibliothèques de MicroHydra ; elles ne sont pas directement exécutables avec le Python de l’ordinateur.')
sub('Installation commune');add('1. Vérifier que MicroHydra démarre sur le modèle exact de carte. 2. Choisir le fichier .py ou le dossier applicatif indiqué par la notice. 3. Le copier sous /apps en conservant les fichiers associés. 4. Revenir au lanceur, choisir l’application et effectuer un essai simple. 5. Pour revenir en arrière, conserver une copie des fichiers avant modification.')
box('Cas particuliers','Wardrive vise le Cardputer ADV et un cap GPS U214. CO2_SCD40 exige un capteur additionnel. Music exige des WAV et une SD. InfraRed est représenté dans app-source par ses métadonnées ; consulter le paquet distribuable. La licence d’une application n’est pas automatiquement celle de tout le catalogue.')
for name,(title,usage,hardware) in APPS.items():
    page();heading(name+' - '+title,1,key='app-'+name);tag('MicroHydra · fiche individuelle')
    box('Appareil et accessoires',hardware)
    sub('Manipulation et résultat attendu');add(usage)
    base=ROOT/'upstream/sources/microhydra-apps/app-source'/name
    details=(base/'details.yml').read_text(errors='replace') if (base/'details.yml').exists() else ''
    author=re.search(r'^author:\s*(.+)',details,re.M);version=re.search(r'^app_version:\s*(.+)',details,re.M);license_=re.search(r'^license:\s*(.+)',details,re.M)
    add('Auteur indiqué : '+(author.group(1).strip('"') if author else 'non précisé')+' ; version : '+(version.group(1) if version else 'non précisée')+' ; licence déclarée : '+(license_.group(1).strip('"') if license_ else 'non précisée dans details.yml')+'.','small')
    screenshot_or_source('app-'+name,maxh=270)
    sub('Fichiers à retrouver');add(' ; '.join(p.relative_to(base).as_posix() for p in sorted(base.rglob('*')) if p.is_file() and p.name!='.DS_Store'),'small')
    source(base/'details.yml');source(CARDS['app-'+name]['source'])

page();heading('8. Sous-projets, outils et architecture')
add('Ce chapitre descend dans les instantanés : interfaces Web, projet Android, programmes auxiliaires et bibliothèques intégrées. Les notices distinguent le logiciel hôte, le firmware et les ressources. Les outils suivants ne sont pas exécutés automatiquement par les vingt expériences du laboratoire.')
for cid in ['launcher-web','bus-web','bus-flasher','evil-android','evil-slave','evil-utils','demo-apps']:
    c=CARDS[cid]
    if cid!='launcher-web':page()
    heading(c['title'],1,key=cid);add(c['desc']);add(c['usage'],'small');screenshot_or_source(cid);source(c['source'])
sub('Applications internes de la démo officielle')
table([['Dossier main/apps','Fonction à explorer'],['app_hello','Accueil et prise en main'],['app_keyboard','Clavier et entrée de caractères'],['app_record','Enregistrement audio'],['app_texteditor','Éditeur de texte'],['app_timer','Minuterie'],['app_chat','Messagerie de démonstration'],['app_ir','Infrarouge'],['app_repl','Interpréteur PikaPython et console'],['app_set_wifi','Configuration Wi-Fi'],['app_wifi_scan','Scan de réseaux'],['launcher / utils','Navigation et utilitaires partagés']],[170,CW-170])
page();heading('Outils complémentaires et bibliothèques embarquées',1)
add('Les chemins suivants repèrent les sous-projets autonomes ou les bibliothèques intégrées dans les instantanés. Les métadonnées de construction et les exemples peuvent viser d’autres cartes. Les sous-modules vides sont des références à compléter selon la procédure du dépôt parent.')
roles={
'Bad_Usb_Lib':'gestion de scripts et dispositions clavier USB','CYD-touch':'adaptation tactile CYD','HAL':'abstraction matérielle','PN532_SRIX':'prise en charge NFC/RFID spécifique','RTC':'horloge et calendrier','TFT_eSPI':'affichage TFT et nombreux exemples','TFT_eSPI_QRcode':'génération de QR codes pour écran','mquickjs_headers':'en-têtes du moteur de scripts','utility':'utilitaires communs','93cx6':'EEPROM de famille 93Cxx','EEPROM_SPI_WE':'lecture/écriture EEPROM SPI','IRremote':'autre bibliothèque de réception/émission IR','PN532':'pilote NFC PN532','SmartRC-CC1101-Driver-Lib':'pilote radio CC1101','M5GFX':'référence de composant graphique','infrared_tools':'outils infrarouges de la démo','mooncake':'gestion d’applications de la démo','CCTV-Stream-Scripts':'scripts liés aux flux vidéo de test','FindMyMap':'cartographie de données collectées','Pygle':'traitement de données WiGLE','ReverseTCPControlServer':'serveur de contrôle TCP de laboratoire','WigleOpenFinder':'recherche dans les données WiGLE','compilation_prerequisites':'prérequis de construction','mfkey':'outil d’analyse de clés MIFARE à étudier dans son contexte','pcap2hccapx':'conversion de fichiers de capture réseau','wardriving':'outils de traitement de relevés Wi-Fi/GPS'}
for root in ['upstream/sources/bruce/lib','upstream/sources/bus-pirate/lib','upstream/sources/cardputer-demo/components','upstream/sources/evil-cardputer/utilities']:
    sub(root)
    table([['Sous-répertoire','Rôle / point d’entrée']]+[[x.name,roles.get(x.name,'Ressources du projet parent')+' ; '+str(sum(1 for f in x.rglob('*') if f.is_file()))+' fichiers'] for x in sorted((ROOT/root).iterdir()) if x.is_dir()],[170,CW-170])
page();heading('Démonstrations des utilitaires sur ordinateur',1)
add('Ces outils sont contenus dans upstream/sources/evil-cardputer/utilities. Les scénarios ci-dessous sont des essais à préparer avec ses propres jeux de données. Ils ne sont pas exécutés dans ce guide ; les entrées et sorties sont décrites à partir de leurs notices et de leurs sources.')
utility_details=[
('CCTV-Stream-Scripts','Diffusion vidéo MJPEG','Trois programmes servent une webcam, une région d’écran ou un fichier MP4. Les dépendances incluent OpenCV, NumPy et, pour l’écran, mss.','Pour une démonstration prévisible, choisir une vidéo de test sans données personnelles et lire cctv-mp4.py. Le résultat attendu est un flux MJPEG visualisable dans un navigateur ou par un appareil compatible. Le service local ne comporte pas d’authentification ni de TLS ; vérifier son adresse d’écoute avant de le démarrer.'),
('FindMyMap','Carte temporelle de rapports Find My','Entrées : reports.db et fichiers .keys correspondant aux appareils possédés. Le script déchiffre les rapports compatibles puis génère map.html, filtres, lecture temporelle et exports GPX/JSON.','Démonstration documentaire : suivre dans FindMyMap.py la lecture SQLite, l’association des clés et la construction de points_js. Un essai effectif exige un jeu de données et des clés appropriés ; aucun compte Apple ni rapport de localisation n’a été utilisé ici.'),
('Pygle','Visualisation de relevés Wi-Fi','Entrée data.csv au format de relevé WiGLE ; dépendances Pandas, Folium et chardet. Sortie wifi_map.html avec marqueurs et informations associées.','Sur un CSV de laboratoire, comparer le nombre de lignes valides aux marqueurs. La notice classe le RSSI en vert à partir de -70 dBm, orange de -85 à moins de -70, puis rouge. La génération est locale ; le fonctionnement hors ligne des fonds cartographiques doit être vérifié séparément.'),
('ReverseTCPControlServer','Relais de requêtes entre client et ESP32','Serveur Python asyncio qui reçoit les connexions de l’appareil et relaie requêtes/réponses de clients. La notice le décrit comme utilisant la bibliothèque standard.','Lire la gestion des connexions et les adresses d’écoute dans ReverseTCPControlServer.py. Pour un essai sur son banc, garder serveur et appareil dans le réseau de test et comparer la requête du client à la réponse relayée. Aucun serveur ni redirection de port n’a été mis en place pour ce guide.'),
('WigleOpenFinder','Recherche dans un catalogue Wi-Fi distant','Le programme combine Nominatim et l’API WiGLE ; il requiert requests et un jeton API. Il produit une liste de SSID et un fichier Open-SSID-ville.txt.','Le résultat représente les données du catalogue, pas une observation radio en direct. Pour la lecture du code, repérer la requête de géocodage, les filtres et l’écriture du fichier. Aucun jeton ni appel API n’a été utilisé dans cette documentation.'),
('wardriving','Fusion de journaux CSV','Trois variantes, Python, PowerShell et Bash, regroupent plusieurs CSV et produisent final-wardrive-merged.csv.','Copier des fichiers de test dans un dossier isolé, lire la variante adaptée au poste et contrôler les en-têtes, les doublons et le nombre de lignes du résultat avant toute réutilisation. Le CSV GPS du laboratoire n’a pas automatiquement le schéma WiGLE attendu.'),
('pcap2hccapx','Conversion de captures réseau','Outil Python utilisant tshark et hcxpcapngtool pour transformer des PCAP vers les formats décrits dans sa notice.','Sur une capture autorisée de laboratoire, le contrôle consiste à vérifier que les fichiers dérivés correspondent aux entrées. Ce convertisseur ne capture pas lui-même le trafic et une conversion réussie n’établit pas qu’un secret a été trouvé.'),
('mfkey','Analyse hors ligne de nonces MIFARE','mfkey.h porte la logique de calcul ; mfkey_solve.cpp lit et regroupe les observations pour un traitement sur PC. Le lecteur et les données requis appartiennent au parcours tiers.','Lire le format des enregistrements et les critères de regroupement dans le source. Cette fonction ne fait pas partie de rfid-bloc ; le WS1850S du laboratoire ne doit pas être présenté comme un émulateur NFC compatible avec ce parcours.'),
('Bad_Usb_Lib','Bibliothèque USB HID et dispositions','Contient USBHID, USBHIDKeyboard, plusieurs dispositions linguistiques et des scripts d’intégration au cœur Arduino.','Comparer les tables de dispositions, puis utiliser la démonstration volontaire usb-clavier du laboratoire pour comprendre l’effet du clavier hôte. Ne pas mélanger cette copie avec les en-têtes USB fournis par une autre version de cœur sans projet de compilation distinct.'),
('compilation_prerequisites','Adaptation de la chaîne Arduino','Scripts shell, PowerShell et batch de modification de la chaîne ESP32 pour des fonctions particulières du firmware tiers.','La démonstration de ce guide est une lecture de leur portée et des fichiers visés. Ils modifient l’environnement de construction et ne sont pas nécessaires aux vingt expériences actives. Aucun de ces scripts n’a été exécuté pendant la production du document.')]
for name,title,desc,demo in utility_details:
    sub(name+' - '+title);add(desc);add(demo);source('upstream/sources/evil-cardputer/utilities/'+name+'/README.md')
page();heading('Scripts du laboratoire et formats de données',1)
table([['Fichier','Usage concret'],['tools/fetch_upstream.py','Télécharger sans exécuter ; vérifier SHA-256 de l’archive et de l’arbre ; refuser d’écraser des sources modifiées.'],['tools/build_all.py','Construire chaque environnement de platformio.ini et écrire build/*.log et compilation.json.'],['tools/check_docs.py','Vérifier les liens locaux et la cohérence catalogue/environnements.'],['tools/test_host.py','Lancer les tests Python puis compiler les tests C++ des formats, et relire le WAV généré.'],['tools/gps_csv_to_gpx.py','Convertir un CSV valide en GPX 1.1 local, sans écrasement.'],['tools/lab_catalog.py','Définir les 20 expériences et produire les notices/index ; les données servent aussi aux aperçus.'],['tools/build_assets.py','Produire les schémas et l’aperçu HTML.'],['tools/capture_previews.py','Capturer 16 vues de l’aperçu avec Playwright.'],['tools/apercu.html','Sélecteur de démonstrations fictives dans le navigateur.'],['tools/modulation.html','Comparer OOK, FSK et FM sans radio.']],[170,CW-170])
sub('Démonstration GPS entièrement reproductible sur ordinateur')
code('python tools/gps_csv_to_gpx.py fixtures/trace-exemple.csv trace-guide.gpx')
add('Résultat attendu : trois points convertis. Utiliser un nom de sortie inexistant ; le convertisseur ouvre le fichier en mode exclusif et refuse son écrasement. Le troisième point du jeu de données n’a pas d’altitude.')
code((ROOT/'fixtures/trace-exemple.csv').read_text())
add('Les colonnes utc, latitude, longitude et altitude_m sont obligatoires. Le convertisseur vérifie les bornes des coordonnées, les valeurs finies et une heure UTC ; aucun fichier n’est créé si une ligne est invalide. La colonne satellites du CSV peut être présente sans être exportée dans le GPX.')
source('tools/gps_csv_to_gpx.py');source('fixtures/trace-exemple.csv')
page();heading('Interface commune, tests et automatisation',1)
table([['Fichier / répertoire','Responsabilité'],['lib/CardputerLab/src/CardputerLab.h','Écran, clavier, SD, noms de fichiers et I²C. Broches Grove et SPI centralisées.'],['lib/CardputerLab/src/LabFormats.h','En-tête WAV, garde du bloc RFID 4, structure et validation des paquets ESP-NOW.'],['lib/CardputerLab/src/Lab.h et lab_logic.h','Interfaces historiques utilisées par les brouillons uniquement.'],['include/lab_config.h','SSID/clé de démonstration, code NEC, trame RF433 et canal ESP-NOW.'],['include/rfid_lab.h','Reset logiciel du lecteur, réglages de registres et affichage hexadécimal.'],['lib/RfidLegacy/','Raccordement au pilote MFRC522-I2C téléchargé.'],['tests/test_formats.cpp','Tests C++ de l’en-tête WAV, des bornes d’écriture et des paquets.'],['tests/test_gpx.py','Conversions valides et rejets d’entrées invalides sans fichier résiduel.'],['.github/workflows/','Installation, restauration des sources, vérifications et compilation des vingt cibles.']],[205,CW-205])
sub('Commandes à relancer après une modification')
code('python tools/test_host.py\npython tools/check_docs.py\npython tools/fetch_upstream.py --verify\n# Recompiler la cible modifiée :\npio run -e diagnostic\n# Après changement de dépendances :\npython tools/build_all.py')
add('Le workflow CI est présent mais aucune exécution GitHub n’est attestée dans ce guide. Les compilations historiques sont conservées sous build/ ; une construction réussie ne valide pas le comportement physique.')
source('.github/workflows/verify.yml')

page();heading('9. Validation et dépannage')
sub('Vérifications effectuées le 17 octobre 2026')
table([['Contrôle','Résultat constaté'],['Tests sur ordinateur','Deux tests Python réussis ; tests C++ de formats et relecture WAV réussis.'],['Documentation','49 documents, 393 liens locaux et 20 environnements vérifiés avant ajout du guide.'],['Archives amont','18 archives sur 18 conformes à leurs SHA-256 enregistrés.'],['Arbres extraits','16 sur 18 strictement conformes ; deux arbres diffèrent uniquement par des fichiers .DS_Store ajoutés.'],['Comparaison aux archives','irremote : deux .DS_Store ajoutés ; evil-cardputer : huit ajoutés. Aucun fichier d’origine modifié ou manquant détecté dans ces deux arbres.'],['Matériel','Aucun essai, aucun flash, aucune mesure radio attestée dans cette réalisation.']],[155,CW-155])
add('La commande fetch_upstream.py --verify s’arrête donc actuellement sur irremote. Ce constat est conservé sans supprimer les fichiers de l’utilisateur ni modifier le manifeste. Les empreintes d’arbre incluent tous les fichiers, même les métadonnées du Finder. Le rapport ancien 18/18 doit être lu avec sa date du 10 octobre.')
sub('Compilations historiques consignées')
table([['Environnement','Résultat 10/10','Flash / RAM statique, octets']]+[[x['environment'],'Réussie' if x['success'] else 'Échec',f'{x["flash_bytes"]:,} / {x["static_ram_bytes"]:,}'.replace(',',' ')] for x in COMPILE['results']],[145,95,CW-240])
source('docs/validation-compilation.json');source('docs/validation.md')
page();md_doc('docs/depannage.md')
page();heading('Fiche de constat pour un essai physique',1)
add('Utiliser ce modèle après chaque démonstration. Une photo de l’écran doit montrer le titre et le résultat ; une seconde photo peut présenter les liaisons hors tension. Les captures personnelles pourront compléter les vues pédagogiques de ce guide.')
table([['À consigner','Observation'],['Date, opérateur, version de carte','........................................................................................'],['Environnement et version des sources','........................................................................................'],['Module, alimentation et raccordement','........................................................................................'],['Action effectuée / touches','........................................................................................'],['Résultat attendu puis observé','........................................................................................'],['Fichier produit / référence de photo','........................................................................................'],['Écart, erreur et prochaine vérification','........................................................................................']],[190,CW-190])
add('Pour le GPS, distinguer octets NMEA et fix. Pour les radios, distinguer message d’envoi, accusé matériel et réception applicative. Pour RFID, distinguer identification, authentification, écriture et relecture. Pour l’audio, vérifier le fichier et l’écoute réelle.')

page();heading('10. Catalogue intégral des exemples')
add('Cette annexe recense les 492 fichiers .ino et exemples Python trouvés dans les répertoires de contenu, y compris les bibliothèques embarquées et les sauvegardes historiques. Le nom exact permet de retrouver chaque démonstration. Une entrée n’est pas une certification de compatibilité K132. Les projets ESP-IDF, applications .cpp, paquets et autres points d’entrée sont aussi repérés dans les annexes suivantes.')
groups=defaultdict(list)
for x in INV['examples']:
    parts=x.split('/');g='/'.join(parts[:3]) if x.startswith('upstream/') else '/'.join(parts[:2]);groups[g].append(x[len(g)+1:])
for g,items in groups.items():
    sub(g+' / '+str(len(items))+' entrées')
    for start in range(0,len(items),28):
        # Liste compacte, mais chaque chemin peut se renvoyer à la ligne.
        for rel in items[start:start+28]:add(rel,'small')

page();heading('11. Points de construction imbriqués')
add('Liste des fichiers de métadonnées trouvés : bibliothèques Arduino, paquets Node/Python et projet Android. Ces entrées complètent les chapitres de présentation ; leurs noms de répertoire indiquent leur propriétaire.')
for path in INV['nested']:add(path,'small')
sub('Configurations PlatformIO et projets CMake')
configs=[]
for base in ['experiments','upstream/sources']:
    for x in (ROOT/base).rglob('*'):
        if x.name in ['platformio.ini','CMakeLists.txt'] and x.is_file():configs.append(x.relative_to(ROOT).as_posix())
for path in sorted(configs):add(path,'small')

page();heading('12. Index de tous les répertoires de contenu')
add('1 322 sous-répertoires sont listés ci-dessous. Le nombre entre parenthèses compte les fichiers directement présents, sans additionner les descendants. Les répertoires racines sont décrits au chapitre 1. Les caches de dépendances, fichiers de travail du guide et __pycache__ sont hors de cet index ; leurs fonctions sont documentées dans le guide.')
dirgroups=defaultdict(list)
for row in INV['directories']:
    path=row['path'];parts=path.split('/');g='/'.join(parts[:3]) if path.startswith('upstream/sources/') else parts[0];dirgroups[g].append(row)
for g,rows in dirgroups.items():
    sub(g)
    for row in rows:
        rel=row['path'][len(g):].lstrip('/') or '.'
        add(rel+'  ('+str(row['files'])+')','small')

page();heading('13. Sources, licences et provenance des visuels')
md_doc('THIRD_PARTY.md',title=False,images=False)
sub('Sources documentaires du laboratoire')
md_doc('docs/sources.md',title=False,images=False)
sub('Partage et contribution')
md_doc('CONTRIBUTING.md',title=False,images=False)
sub('Registre des figures')
for f in FIGURES:add(f'{f["number"]:03d} · {f["kind"]} · {f["path"]}','tiny')
sub('Fichiers joints au PDF')
add('Les pièces jointes inventaire-fichiers.csv et inventaire-repertoires.csv permettent une recherche et un tri hors du PDF. Elles recensent les chemins relatifs et les tailles ou comptes, sans copier les données des fichiers. Le registre-visuels.json décrit les images utilisées. Le rapport verification-sources.json conserve la comparaison des archives.')
sub('Sources locales utilisées dans le guide')
for path in sorted(SOURCES):add(path,'tiny')

# Le PDF est d’abord composé sans pièces jointes, puis les quatre annexes sont ajoutées sans
# reconstruire les liens et signets.
dest=OUT/'Cardputer-Guide-complet-FR.pdf'
doc=Doc(TMP/'guide-sans-pieces.pdf');doc.multiBuild(STORY,maxPasses=5)
(TMP/'sommaire.json').write_text(json.dumps(doc.all_entries,ensure_ascii=False,indent=2))
(TMP/'registre-visuels.json').write_text(json.dumps(FIGURES,ensure_ascii=False,indent=2))
# MuPDF ajoute les inventaires sans perdre les liens et les signets du guide.
pdf=fitz.open(TMP/'guide-sans-pieces.pdf')
for filename,path in [('inventaire-fichiers.csv',TMP/'inventaire-fichiers.csv'),('inventaire-repertoires.csv',TMP/'inventaire-repertoires.csv'),('registre-visuels.json',TMP/'registre-visuels.json'),('verification-sources.json',ASSETS/'verification-sources-2026-10-17.json')]:
    pdf.embfile_add(filename,path.read_bytes(),filename=filename,desc='Annexe du guide Cardputer Lab')
pdf.save(dest,garbage=4,deflate=True)
print(json.dumps({'pdf':str(dest),'pages':len(pdf),'figures':len(FIGURES),'bookmarks':len(pdf.get_toc()),'attachments':pdf.embfile_count()},ensure_ascii=False))
