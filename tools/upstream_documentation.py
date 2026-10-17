#!/usr/bin/env python3
"""Applique ou vérifie les ajouts documentaires français aux instantanés tiers.

Les archives et leur manifeste restent les références d'origine. Le registre
compressé décrit uniquement des insertions d'octets : commentaires dans les
sources et sections README. Chaque version, avant et après, possède son SHA-256.
Une modification inconnue est refusée plutôt que remplacée.
"""
import argparse
import base64
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'upstream/documentation-fr/ajouts.json.gz'


def sha256(data):
    """Empreinte des octets exacts ; aucun décodage ni normalisation de lignes."""
    return hashlib.sha256(data).hexdigest()


@lru_cache(maxsize=1)
def registry():
    """Lire une seule fois les ajouts, partagés par les téléchargements concurrents."""
    if not REGISTRY.exists():
        return {}
    with gzip.open(REGISTRY, 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    if data.get('schema') != 1:
        raise ValueError('Version du registre documentaire inconnue')
    entries = {}
    for entry in data['files']:
        rel = Path(entry['path'])
        # Les destinations doivent rester dans un instantané, jamais dans tools
        # ou dans un chemin absolu fourni par le registre.
        if rel.is_absolute() or '..' in rel.parts or len(rel.parts) < 4 or rel.parts[:2] != ('upstream', 'sources'):
            raise ValueError(f'Chemin documentaire interdit : {rel}')
        if entry['path'] in entries:
            raise ValueError(f'Entrée documentaire dupliquée : {rel}')
        entries[entry['path']] = entry
    return entries


def inserted_bytes(entry):
    """Décoder des insertions ordonnées, exprimées en offsets de l'original."""
    previous = -1
    result = []
    for offset, encoded in entry['insertions']:
        if not isinstance(offset, int) or offset < 0 or offset <= previous:
            raise ValueError('Offsets documentaires non ordonnés')
        result.append((offset, base64.b64decode(encoded, validate=True)))
        previous = offset
    return result


def apply_bytes(original, entry):
    """Insérer sans supprimer ni remplacer le moindre octet du fichier d'origine."""
    expected = entry['original_sha256']
    if expected is None:
        if original:
            raise ValueError('Un nouveau README ne peut pas remplacer un fichier')
    elif sha256(original) != expected:
        raise ValueError('Le fichier ne correspond plus à son original')
    output = bytearray()
    cursor = 0
    for offset, addition in inserted_bytes(entry):
        if offset > len(original):
            raise ValueError('Insertion après la fin du fichier')
        output.extend(original[cursor:offset])
        output.extend(addition)
        cursor = offset
    output.extend(original[cursor:])
    output = bytes(output)
    if sha256(output) != entry['documented_sha256']:
        raise ValueError('Empreinte documentée incohérente')
    return output


def original_bytes(current, entry):
    """Retrouver et vérifier l'original en retirant seulement les ajouts reconnus.

    Retourne None pour un README entièrement ajouté. Les sources d'origine
    sont aussi acceptées pour permettre une restauration depuis les archives.
    """
    digest = sha256(current)
    if digest == entry['original_sha256']:
        return current
    if digest != entry['documented_sha256']:
        raise ValueError('Modification non enregistrée dans la documentation')
    result = bytearray(current)
    total = 0
    ranges = []
    for offset, addition in inserted_bytes(entry):
        start = offset + total
        if current[start:start + len(addition)] != addition:
            raise ValueError('Ajout attendu absent de son emplacement')
        ranges.append((start, len(addition)))
        total += len(addition)
    # Retirer de droite à gauche pour ne pas déplacer les offsets restants.
    for start, length in reversed(ranges):
        del result[start:start + length]
    if entry['original_sha256'] is None:
        if result:
            raise ValueError('Contenu inattendu dans un nouveau README')
        return None
    if sha256(result) != entry['original_sha256']:
        raise ValueError('Original reconstitué non conforme')
    return bytes(result)


def normalized_tree_digest(directory):
    """SHA-256 au format du manifeste, après retrait vérifié des seuls ajouts.

    Les .DS_Store du Finder sont exclus : ils ne sont pas des sources et aucun
    des dix-huit instantanés d'origine n'en contient. Tous les autres fichiers,
    y compris les fichiers inconnus du registre, contribuent à l'empreinte.
    """
    entries = registry()
    digest = hashlib.sha256()
    for path in sorted(directory.rglob('*')):
        if path.name == '.DS_Store':
            continue
        if path.is_symlink():
            value = 'link:' + str(path.readlink())
        elif path.is_file():
            data = path.read_bytes()
            entry = entries.get(path.relative_to(ROOT).as_posix())
            if entry is not None:
                try:
                    data = original_bytes(data, entry)
                except ValueError as error:
                    raise ValueError(f'{path.relative_to(ROOT)} : {error}') from error
                if data is None:
                    continue
            value = sha256(data)
        else:
            continue
        digest.update((path.relative_to(directory).as_posix() + '\0' + value + '\n').encode())
    return digest.hexdigest()


def project_entries(project=None):
    """Sélectionner un instantané ou le registre entier, avec contrôle de chemin."""
    for rel, entry in registry().items():
        if project is not None and Path(rel).parts[2] != project:
            continue
        path = ROOT / rel
        base = ROOT / 'upstream/sources' / Path(rel).parts[2]
        if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
            raise ValueError(f'Destination liée hors du projet : {rel}')
        yield path, entry


def apply(project=None):
    """Appliquer de manière idempotente après validation de toutes les entrées."""
    selected = list(project_entries(project))
    if not selected:
        return 0
    # Valider avant d'écrire évite de commencer une restauration qui écraserait
    # une édition personnelle. Une interruption reste récupérable en relançant.
    for path, entry in selected:
        data = path.read_bytes() if path.exists() else b''
        if path.exists() and sha256(data) == entry['documented_sha256']:
            continue
        apply_bytes(data, entry)
    count = 0
    for path, entry in selected:
        data = path.read_bytes() if path.exists() else b''
        if path.exists() and sha256(data) == entry['documented_sha256']:
            continue
        output = apply_bytes(data, entry)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Une écriture directe conserve les droits existants des scripts.
        path.write_bytes(output)
        count += 1
    return count


def verify():
    """Vérifier que chaque commentaire et README est présent dans sa version enregistrée."""
    count = 0
    for path, entry in project_entries():
        if not path.is_file() or sha256(path.read_bytes()) != entry['documented_sha256']:
            raise ValueError(f'Ajout documentaire absent ou modifié : {path.relative_to(ROOT)}')
        original_bytes(path.read_bytes(), entry)
        count += 1
    if not count:
        raise ValueError('Aucun registre documentaire disponible')
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['apply', 'verify'])
    args = parser.parse_args()
    if args.action == 'apply':
        print(f'{apply()} fichiers documentaires appliqués ; les autres étaient déjà conformes.')
    else:
        print(f'{verify()} fichiers documentés vérifiés ; ajouts réversibles octet par octet.')


if __name__ == '__main__':
    main()
