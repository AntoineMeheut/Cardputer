#!/usr/bin/env python3
# Vérification des liens locaux et cohérence du catalogue avec PlatformIO. Voir README.md pour les
# commandes, les sorties et les prérequis.
"""Vérifie les liens locaux Markdown, SVG et le catalogue PlatformIO."""
import configparser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from lab_catalog import EXPERIMENTS

ROOT = Path(__file__).resolve().parents[1]
# Parcourir la documentation maintenue par le laboratoire. Les notices originales tierces ont leurs
# propres liens externes et conventions.
files = list(ROOT.glob('*.md')) + list((ROOT / 'upstream').glob('*.md'))
files.extend((ROOT / 'upstream/sources').glob('*.md'))
for folder in ('docs', 'experiments', 'include', 'lib', 'tools', 'tests', 'fixtures', '.github', 'upstream/documentation-fr'):
    files.extend((ROOT / folder).rglob('*.md'))
errors, checked = [], 0
for path in files:
    # Ignorer les exemples entre blocs de code ; leurs crochets et parenthèses ne sont pas nécessairement
    # des liens Markdown.
    text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    for destination in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
        # Les schémas HTTP et les ancres seules ne désignent pas des fichiers locaux à vérifier ici.
        uri = urlsplit(destination.strip('<>'))
        if uri.scheme or not uri.path:
            continue
        checked += 1
        # Résoudre les chemins relativement au document qui porte le lien, après décodage des caractères URL.
        target = (path.parent / unquote(uri.path)).resolve()
        if not target.exists():
            errors.append(f'{path.relative_to(ROOT)} : cible absente {destination}')
for path in (ROOT / 'docs/assets').rglob('*.svg'):
    try:
        ET.parse(path)
    except ET.ParseError as error:
        errors.append(f'{path.name} : SVG invalide {error}')
config = configparser.ConfigParser()
config.read(ROOT / 'platformio.ini')
# Comparer des ensembles détecte aussi bien une cible manquante qu’une cible ajoutée sans entrée de
# catalogue.
environments = {name[4:] for name in config.sections() if name.startswith('env:')}
expected = {entry[1] for entry in EXPERIMENTS}
if environments != expected:
    errors.append(f'Catalogue et environnements différents : {environments ^ expected}')
for folder, env, *_ in EXPERIMENTS:
    for filename in ('main.cpp', 'README.md'):
        if not (ROOT / 'experiments' / folder / filename).is_file():
            errors.append(f'{folder}/{filename} absent')
    if f'+<{folder}/main.cpp>' not in config['env:' + env]['build_src_filter']:
        errors.append(f'{env} : programme sélectionné incorrect')
# Accumuler les erreurs donne un rapport utile en une seule exécution, puis un statut non nul
# utilisable en CI.
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'{len(files)} documents, {checked} liens locaux et {len(expected)} environnements vérifiés.')
