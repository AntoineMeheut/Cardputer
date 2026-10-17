# Tests sans matériel du convertisseur GPS : données valides, erreurs et absence d’écrasement. Voir
# README.md pour les commandes, les sorties et les prérequis.
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
# Charger le script par son chemin évite de dépendre du répertoire courant ou de créer un paquet
# Python pour un simple outil.
spec = importlib.util.spec_from_file_location('gpx', ROOT / 'tools/gps_csv_to_gpx.py')
gpx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gpx)


class Conversion(unittest.TestCase):
    # Vérifier simultanément les trois points, l’altitude absente et le refus de réutiliser le même
    # fichier de sortie.
    def test_valid_and_missing_altitude(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'trace.gpx'
            self.assertEqual(gpx.convert(ROOT / 'fixtures/trace-exemple.csv', output), 3)
            points = ET.parse(output).findall('.//{*}trkpt')
            self.assertEqual(len(points), 3)
            self.assertIsNone(points[-1].find('{*}ele'))
            with self.assertRaises(FileExistsError):
                gpx.convert(ROOT / 'fixtures/trace-exemple.csv', output)

    # Chaque cas isole une erreur de données et vérifie l’absence de fichier partiellement produit.
    def test_invalid_data_leaves_no_output(self):
        for row in ['2026-01-01T00:00:00Z,nan,2,0', '2026-01-01T00:00:00Z,91,2,0',
                    '2026-01-01T00:00:00,48,2,0', '2026-01-01T00:00:00Z,48,2,inf']:
            with self.subTest(row=row), tempfile.TemporaryDirectory() as directory:
                source, output = Path(directory) / 'input.csv', Path(directory) / 'output.gpx'
                source.write_text('utc,latitude,longitude,altitude_m\n' + row + '\n')
                with self.assertRaises(ValueError):
                    gpx.convert(source, output)
                self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
