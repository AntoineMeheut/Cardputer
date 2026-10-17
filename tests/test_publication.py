"""Vérifier les frontières de l'export : fichiers privés, liens et intégrité ZIP."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import prepare_publication as publication


class PublicationTests(unittest.TestCase):
    def test_ignore_rules_without_local_git(self):
        """Les caches et .env ne doivent pas entrer dans la sélection initiale."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / '.gitignore').write_text('.env\nbuild/\nupstream/sources/*\n!upstream/sources/README.md\n')
            for relative in ('README.md', '.env', 'build/test.bin',
                             'upstream/sources/README.md', 'upstream/sources/vendor/main.cpp'):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('exemple')
            self.assertEqual(publication.selected_files(root),
                             ['.gitignore', 'README.md', 'upstream/sources/README.md'])
            self.assertFalse((root / '.git').exists())
            # Le garde indépendant du .gitignore couvre une règle effacée par erreur.
            with self.assertRaisesRegex(ValueError, 'interdit'):
                publication.validate_selection(root, ['.env'])

    def test_export_links_and_external_symlink(self):
        """Un cache amont déclaré est différé ; un rapport build/ est une erreur."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'upstream').mkdir()
            (root / 'upstream/manifest.json').write_text(json.dumps({'projects': [{'id': 'demo'}]}))
            (root / 'README.md').write_text('[source](upstream/sources/demo/main.cpp)')
            paths = ['README.md', 'upstream/manifest.json']
            self.assertEqual(publication.validate_links(root, paths)['upstream_links_restored_after_clone'], 1)
            (root / 'README.md').write_text('[rapport](build/rapport.json)')
            with self.assertRaisesRegex(ValueError, 'non distribuée'):
                publication.validate_links(root, paths)
            (root / 'README.md').unlink()
            (root / 'README.md').symlink_to(root.parent / 'fichier-exterieur')
            with self.assertRaisesRegex(ValueError, 'Lien symbolique'):
                publication.validate_selection(root, ['README.md'])

    def test_bundle_roundtrip_and_determinism(self):
        """L'archive redistribue les octets français sans métadonnées du poste."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data = 'Écran, clavier, données fictives.\n'.encode()
            (root / 'README.md').write_bytes(data)
            output = root / 'output'
            first = publication.write_bundle(root, ['README.md'], output)
            second = publication.write_bundle(root, ['README.md'], output)
            self.assertEqual(first, second)
            self.assertEqual(first['files'][0]['sha256'], hashlib.sha256(data).hexdigest())
            with zipfile.ZipFile(output / first['archive']) as bundle:
                self.assertEqual(bundle.namelist(), ['Cardputer-Lab/README.md'])
                self.assertEqual(bundle.read('Cardputer-Lab/README.md'), data)


if __name__ == '__main__':
    unittest.main()
