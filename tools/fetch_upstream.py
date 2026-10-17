#!/usr/bin/env python3
# Restauration des dépendances à partir de commits figés et contrôle d’intégrité. Voir README.md pour
# les commandes, les sorties et les prérequis.
"""Télécharge des instantanés GitHub, sans exécuter leur contenu (Python >= 3.12)."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import urllib.request
import upstream_documentation

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'upstream/manifest.json'


# Requête HTTP identifiée et temporisée ; aucune exécution des fichiers téléchargés.
def request(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'Cardputer-Lab-FR', 'Accept': 'application/vnd.github+json'}), timeout=120)


# SHA-256 calculé par blocs d’un Mio afin de ne pas charger l’archive entière en mémoire.
def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


# L’empreinte inclut l’ordre des chemins, le type lien/fichier et le contenu ; ce n’est pas seulement
# une somme des fichiers.
def tree_digest(path):
    # Reconstituer les octets d'origine à partir des ajouts exactement connus.
    # Toute autre édition continue à invalider l'empreinte du manifeste.
    if upstream_documentation.REGISTRY.exists():
        return upstream_documentation.normalized_tree_digest(path)
    h = hashlib.sha256()
    for item in sorted(path.rglob('*')):
        if item.is_symlink():
            value = 'link:' + str(item.readlink())
        elif item.is_file():
            value = digest(item)
        else:
            continue
        h.update((item.relative_to(path).as_posix() + '\0' + value + '\n').encode())
    return h.hexdigest()


# Traite un projet indépendant : résout éventuellement un commit, valide l’archive, extrait une seule
# racine puis contrôle l’arbre.
def fetch(entry):
    # Copier l’entrée évite de modifier le manifeste partagé depuis les tâches de téléchargement
    # concurrentes.
    entry = dict(entry)
    repo = entry['repo']
    if not entry.get('commit'):
        with request('https://api.github.com/repos/' + repo) as response:
            info = json.load(response)
        repo = entry['repo'] = info['full_name']
        entry['license_spdx'] = (info.get('license') or {}).get('spdx_id', 'NOASSERTION')
        entry['default_branch'] = info['default_branch']
        with request(f'https://api.github.com/repos/{repo}/commits/{info["default_branch"]}') as response:
            entry['commit'] = json.load(response)['sha']
    target = ROOT / 'upstream/sources' / entry['id']
    archive = ROOT / 'upstream/archives' / (entry['id'] + '.tar.gz')
    entry['archive_url'] = f'https://codeload.github.com/{repo}/tar.gz/{entry["commit"]}'
    if archive.exists():
        if entry.get('sha256') and digest(archive) != entry['sha256']:
            raise ValueError(f'{archive}: empreinte incorrecte')
    else:
        archive.parent.mkdir(parents=True, exist_ok=True)
        # Le suffixe .part distingue un transfert incomplet d’une archive validée ; le remplacement final est
        # atomique.
        temporary = archive.with_suffix('.part')
        try:
            with request(entry['archive_url']) as response, temporary.open('wb') as output:
                shutil.copyfileobj(response, output)
            if entry.get('sha256') and digest(temporary) != entry['sha256']:
                raise ValueError(f'{archive}: téléchargement non conforme')
            temporary.replace(archive)
        finally:
            temporary.unlink(missing_ok=True)
    entry['sha256'] = digest(archive)
    entry['archive_bytes'] = archive.stat().st_size
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=target.parent) as temp:
            with tarfile.open(archive) as bundle:
                # Le filtre data de Python >= 3.12 limite les chemins et types d’entrées extraits de l’archive.
                bundle.extractall(temp, filter='data')
            # Refuser une archive avec plusieurs racines évite d’installer silencieusement une arborescence
            # inattendue.
            roots = list(Path(temp).iterdir())
            if len(roots) != 1 or not roots[0].is_dir():
                raise ValueError(f'{repo}: racine inattendue')
            roots[0].rename(target)
    actual = tree_digest(target)
    if entry.get('tree_sha256') and entry['tree_sha256'] != actual:
        raise ValueError(f'{target}: sources locales modifiées')
    entry['tree_sha256'] = actual
    # Un nouveau clone reçoit les mêmes commentaires que cette copie de travail.
    # Le registre ne peut pas remplacer une modification locale inconnue.
    upstream_documentation.apply(entry['id'])
    entry['license_files'] = [str(p.relative_to(target)) for p in target.iterdir()
                              if p.is_file() and p.name.lower().startswith(('license', 'copying', 'notice'))]
    print(f'{entry["id"]}: {entry["commit"][:12]} — {entry["archive_bytes"]:,} octets', flush=True)
    return entry


# --verify est une lecture locale ; sans cet argument le script peut télécharger et écrire les caches
# et le manifeste.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='Vérifier localement, sans réseau')
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    if args.verify:
        for e in manifest['projects']:
            archive = ROOT / 'upstream/archives' / (e['id'] + '.tar.gz')
            if archive.exists() and digest(archive) != e['sha256']:
                raise SystemExit(f'Archive altérée : {e["id"]}')
            if tree_digest(ROOT / 'upstream/sources' / e['id']) != e['tree_sha256']:
                raise SystemExit(f'Sources altérées ou absentes : {e["id"]}')
        if upstream_documentation.REGISTRY.exists():
            count = upstream_documentation.verify()
            print(f'{count} fichiers documentés vérifiés (ajouts réversibles, .DS_Store ignorés).')
        print(f'{len(manifest["projects"])} instantanés vérifiés contre les empreintes originales.')
        return
    # Les archives indépendantes sont téléchargées en parallèle ; le manifeste est écrit une fois.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        manifest['projects'] = list(pool.map(fetch, manifest['projects']))
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
