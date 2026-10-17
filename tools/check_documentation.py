#!/usr/bin/env python3
"""Contrôle les README de code et les liens des ajouts français aux projets tiers.

Ce contrôle complète check_docs.py. Il ne rejette pas les anciens liens des
notices amont : seules les sections françaises ajoutées sont de notre ressort.
Les fichiers JSON restent stricts et sont documentés dans leur README voisin.
"""
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import upstream_documentation

ROOT = Path(__file__).resolve().parents[1]
MARKER = '<!-- documentation-code-fr -->'
CODE_SUFFIXES = {'.cpp', '.c', '.h', '.hpp', '.py', '.html', '.ini', '.yml', '.yaml'}


def readme_in(folder):
    """Accepter les variantes historiques Readme.md sur les systèmes sensibles à la casse."""
    return next((p for p in folder.iterdir() if p.is_file() and p.name.lower() == 'readme.md'), None)


def local_links(document, text):
    """Résoudre les liens du document, sans accès au réseau ni analyse des blocs de code."""
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    for destination in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
        uri = urlsplit(destination.strip('<>'))
        if not uri.scheme and uri.path:
            yield destination, (document.parent / unquote(uri.path)).resolve()


def main():
    errors = []
    folders = set()
    # Les caches et les sorties compilées ne sont pas des sources maintenues.
    for scope in ('experiments', 'include', 'lib', 'tools', 'tests', '.github', 'docs/ateliers'):
        for path in (ROOT / scope).rglob('*'):
            if path.is_file() and path.suffix.lower() in CODE_SUFFIXES and '__pycache__' not in path.parts:
                folders.add(path.parent)
    for folder in sorted(folders):
        if readme_in(folder) is None:
            errors.append(f'README absent : {folder.relative_to(ROOT)}')
    inventory = json.loads((ROOT / 'upstream/documentation-fr/inventaire-code.json').read_text())
    for row in inventory:
        path = ROOT / row['path']
        if not path.is_file():
            errors.append(f'Source inventoriée absente : {row["path"]}')
        if readme_in(path.parent) is None:
            errors.append(f'README tiers absent : {path.parent.relative_to(ROOT)}')
    checked = 0
    readmes = 0
    for rel, entry in upstream_documentation.registry().items():
        if entry['kind'] != 'readme':
            continue
        document = ROOT / rel
        if not document.is_file():
            errors.append(f'Notice absente : {rel}')
            continue
        text = document.read_text(errors='replace')
        if MARKER not in text:
            errors.append(f'Section française absente : {rel}')
            continue
        readmes += 1
        for destination, target in local_links(document, text.split(MARKER, 1)[1]):
            checked += 1
            if not target.exists():
                errors.append(f'{rel} : lien absent {destination}')
    if errors:
        print('\n'.join(dict.fromkeys(errors)))
        return 1
    print(f'{len(folders)} répertoires de code local, {len(inventory)} sources/configurations tierces, '
          f'{readmes} README tiers et {checked} liens français vérifiés.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
