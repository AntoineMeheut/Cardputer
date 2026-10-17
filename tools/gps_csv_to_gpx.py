#!/usr/bin/env python3
# Conversion locale du CSV produit par gps-sd ; aucune requête réseau. Voir README.md pour les
# commandes, les sorties et les prérequis.
"""Convertit les traces de l'expérience 16 en GPX 1.1, sans envoyer de données."""
import argparse
import csv
import datetime
import math
from pathlib import Path
import xml.etree.ElementTree as ET

NS = 'http://www.topografix.com/GPX/1/1'


# Contrat : source est un chemin CSV UTF-8 ; destination doit ne pas exister. Retourne le nombre de
# points, lève ValueError pour une trace invalide et laisse les erreurs de fichiers remonter.
def convert(source, destination):
    # Le namespace GPX 1.1 est placé sur chaque élément pour produire un document interprétable par les
    # lecteurs GPX.
    ET.register_namespace('', NS)
    tag = lambda name: '{' + NS + '}' + name
    root = ET.Element(tag('gpx'), version='1.1', creator='Cardputer Lab FR')
    track = ET.SubElement(root, tag('trk'))
    ET.SubElement(track, tag('name')).text = Path(source).stem
    segment = ET.SubElement(track, tag('trkseg'))
    count = 0
    with open(source, newline='', encoding='utf-8') as stream:
        # Les noms de colonnes sont significatifs ; satellites peut être présent mais n’est pas exporté.
        reader = csv.DictReader(stream)
        if not {'utc', 'latitude', 'longitude', 'altitude_m'} <= set(reader.fieldnames or []):
            raise ValueError('Colonnes CSV requises absentes')
        # Le numéro commence à deux car la première ligne contient les en-têtes. Construire tout le XML en
        # mémoire avant d’ouvrir la destination.
        for line, row in enumerate(reader, 2):
            try:
                # Refuser NaN et l’infini en plus des bornes géographiques ; une simple comparaison ne valide pas
                # toutes les valeurs flottantes.
                lat, lon = float(row['latitude']), float(row['longitude'])
                if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
                    raise ValueError('coordonnées hors limites')
                # Accepter Z ou un décalage UTC nul ; une heure naïve sans fuseau est refusée.
                moment = datetime.datetime.fromisoformat(row['utc'].replace('Z', '+00:00'))
                if moment.utcoffset() != datetime.timedelta(0):
                    raise ValueError('heure UTC requise')
                # Une altitude vide est une information absente, pas une altitude zéro ; le nœud ele est alors omis.
                altitude = float(row['altitude_m']) if row['altitude_m'] else None
                if altitude is not None and not math.isfinite(altitude):
                    raise ValueError('altitude non finie')
            except (ValueError, TypeError) as error:
                raise ValueError(f'Ligne {line} : {error}') from error
            point = ET.SubElement(segment, tag('trkpt'), lat=f'{lat:.6f}', lon=f'{lon:.6f}')
            if altitude is not None:
                ET.SubElement(point, tag('ele')).text = str(altitude)
            ET.SubElement(point, tag('time')).text = moment.isoformat().replace('+00:00', 'Z')
            count += 1
    # Une trace vide est une erreur et ne doit pas créer un fichier GPX sans point.
    if not count:
        raise ValueError('Aucun point dans la trace')
    ET.indent(root)
    # Aucune écriture avant validation complète ; refuse d'écraser un fichier existant.
    with open(destination, 'xb') as stream:
        ET.ElementTree(root).write(stream, encoding='utf-8', xml_declaration=True)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(f'{convert(args.source, args.destination)} points convertis vers {args.destination}')
