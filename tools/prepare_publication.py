#!/usr/bin/env python3
"""Contrôler et exporter une copie publiable, sans réseau ni modification de Git.

Un dépôt Git temporaire sert uniquement à interpréter les règles .gitignore.
L'archive ZIP et son manifeste sont écrits dans output/publication, exclu de Git.
Les fichiers du projet, son éventuel index Git et ses remotes restent inchangés.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROOTS = {'.github', 'docs', 'experiments', 'fixtures', 'include', 'lib',
                 'tools', 'tests', 'upstream', 'output'}
ROOT_FILES = {'.gitignore', '.gitattributes', 'README.md', 'LICENSE', 'THIRD_PARTY.md',
              'CONTRIBUTING.md', 'platformio.ini', 'project-specifications.md',
              'requirements.txt', 'requirements-dev.txt', '.env.example'}
REQUIRED = {'README.md', 'LICENSE', 'THIRD_PARTY.md', '.gitignore', '.gitattributes',
            'platformio.ini', 'requirements.txt', '.github/workflows/verify.yml',
            'upstream/manifest.json', 'upstream/documentation-fr/ajouts.json.gz',
            'docs/assets/identite/cardputer-lab.svg', 'output/pdf/Cardputer-Guide-complet-FR.pdf'}
# Ces signatures ciblées complètent la sélection des chemins ; elles ne remplacent
# pas une relecture des données que l'on choisit de rendre publiques.
SECRET = re.compile(rb'(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|'
                    rb'gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,}|'
                    rb'AKIA[A-Z0-9]{16})')


def selected_files(root):
    """Lister les fichiers non ignorés sans créer de .git dans le projet."""
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment['GIT_CONFIG_NOSYSTEM'] = '1'
    with tempfile.TemporaryDirectory(prefix='cardputer-publication-') as temporary:
        subprocess.run(['git', 'init', '--quiet', temporary], check=True,
                       capture_output=True, env=environment)
        command = ['git', '-c', f'core.excludesFile={os.devnull}',
                   f'--git-dir={temporary}/.git', f'--work-tree={root}',
                   'ls-files', '--others', '--exclude-standard', '--exclude=.git/', '-z']
        output = subprocess.check_output(command, cwd=root, env=environment)
    return sorted(os.fsdecode(p) for p in output.split(b'\0') if p)


def validate_selection(root, paths):
    """Refuser les éléments inattendus et les liens vers un contenu hors export."""
    errors = []
    for relative in paths:
        path = root / relative
        parts = Path(relative).parts
        # Défense indépendante du .gitignore : une règle supprimée par erreur ne
        # doit pas faire entrer les caches ou un fichier privé dans l'export.
        forbidden_parts = {'.git', '.venv', '.pio', '.platformio', '.cache', '__pycache__',
                           'build', 'tmp', 'captures-privees', '.aws', '.ssh', '.codex', '.agents'}
        if (set(parts) & forbidden_parts or path.name == '.env' or
                (path.name.startswith('.env.') and path.name != '.env.example') or
                relative == 'include/secrets.h' or relative.startswith('upstream/archives/') or
                (relative.startswith('upstream/sources/') and relative not in
                 {'upstream/sources/.gitkeep', 'upstream/sources/README.md'}) or
                (parts[0] == 'output' and relative != 'output/pdf/Cardputer-Guide-complet-FR.pdf')):
            errors.append(f'Fichier privé ou cache interdit : {relative}')
            continue
        if len(parts) == 1 and relative not in ROOT_FILES:
            errors.append(f'Fichier racine non prévu : {relative}')
        elif len(parts) > 1 and parts[0] not in ALLOWED_ROOTS:
            errors.append(f'Répertoire non prévu : {relative}')
        if Path(relative).is_absolute() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            errors.append(f'Lien symbolique ou chemin extérieur : {relative}')
            continue
        if path.stat().st_size > 25 * 1024 * 1024:
            errors.append(f'Fichier dépassant le budget local de 25 Mio : {relative}')
            continue
        if SECRET.search(path.read_bytes()):
            errors.append(f'Signature de secret à examiner : {relative}')
    if errors:
        raise ValueError('\n'.join(errors))


def validate_links(root, paths):
    """Vérifier les liens Markdown de la copie qui sera réellement distribuée.

    Les seules cibles différées sont les sources des projets du manifeste :
    fetch_upstream.py les restaure après le clone. Un lien vers build/ échoue.
    """
    included = set(paths)
    projects = {p['id'] for p in json.loads((root / 'upstream/manifest.json').read_text())['projects']}
    deferred, checked, errors = 0, 0, []
    for relative in paths:
        if not relative.endswith('.md'):
            continue
        text = re.sub(r'```.*?```', '', (root / relative).read_text(encoding='utf-8'), flags=re.S)
        destinations = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
        destinations += re.findall(r'(?:href|src)=["\']([^"\']+)["\']', text)
        for destination in destinations:
            uri = urlsplit(destination.strip('<>'))
            if uri.scheme or not uri.path:
                continue
            target = (root / relative).parent / unquote(uri.path)
            try:
                normalized = target.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                errors.append(f'{relative} : lien extérieur {destination}')
                continue
            if normalized in included or any(p.startswith(normalized + '/') for p in included):
                checked += 1
                continue
            parts = Path(normalized).parts
            if len(parts) >= 3 and parts[:2] == ('upstream', 'sources') and parts[2] in projects:
                deferred += 1
                continue
            errors.append(f'{relative} : cible non distribuée {destination}')
    if errors:
        raise ValueError('\n'.join(errors))
    return {'local_links': checked, 'upstream_links_restored_after_clone': deferred}


def write_bundle(root, paths, output):
    """Produire un ZIP déterministe et vérifier les octets de chaque entrée.

    Un seul dossier racine facilite l'extraction. Les dates et permissions du
    poste ne sont pas divulguées ; chaque fichier est identifié par SHA-256.
    """
    output.mkdir(parents=True, exist_ok=True)
    archive = output / 'Cardputer-Lab-GitHub.zip'
    temporary = archive.with_suffix('.zip.part')
    entries = []
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for relative in sorted(paths):
                data = (root / relative).read_bytes()
                item = zipfile.ZipInfo('Cardputer-Lab/' + relative, date_time=(1980, 1, 1, 0, 0, 0))
                item.create_system = 3
                item.external_attr = 0o100644 << 16
                item.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(item, data, compresslevel=9)
                entries.append({'path': relative, 'bytes': len(data),
                                'sha256': hashlib.sha256(data).hexdigest()})
        with zipfile.ZipFile(temporary) as bundle:
            for entry in entries:
                data = bundle.read('Cardputer-Lab/' + entry['path'])
                if hashlib.sha256(data).hexdigest() != entry['sha256']:
                    raise ValueError(f'Archive incorrecte : {entry["path"]}')
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    report = {'archive': archive.name, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'archive_bytes': archive.stat().st_size, 'file_count': len(entries),
              'uncompressed_bytes': sum(e['bytes'] for e in entries), 'files': entries}
    (output / 'Cardputer-Lab-manifeste.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Contrôler la sélection sans créer de ZIP')
    args = parser.parse_args()
    try:
        paths = selected_files(ROOT)
        missing = REQUIRED - set(paths)
        if missing:
            raise ValueError('Fichiers requis absents : ' + ', '.join(sorted(missing)))
        validate_selection(ROOT, paths)
        checks = validate_links(ROOT, paths)
        print(f'{len(paths)} fichiers sélectionnés ; {checks["local_links"]} liens distribués ; '
              f'{checks["upstream_links_restored_after_clone"]} liens vers les sources à restaurer.')
        if not args.check:
            report = write_bundle(ROOT, paths, ROOT / 'output/publication')
            print(f'output/publication/{report["archive"]} : {report["archive_bytes"]:,} octets')
            print(f'SHA-256 : {report["sha256"]}')
        print('Contrôle local terminé. Aucune publication ni commande réseau exécutée.')
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Échec de préparation : {error}\n')


if __name__ == '__main__':
    main()
