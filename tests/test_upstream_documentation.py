"""Tests du registre documentaire avec des fichiers temporaires, sans réseau."""
import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('documentation', ROOT / 'tools/upstream_documentation.py')
documentation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(documentation)


def entry_for(path, original, additions):
    """Construire un petit registre indépendant des milliers de fichiers réels."""
    data = original or b''
    result = bytearray(data)
    for offset, addition in reversed(additions):
        result[offset:offset] = addition
    return {'path': path, 'original_sha256': documentation.sha256(original) if original is not None else None,
            'documented_sha256': documentation.sha256(result),
            'insertions': [[i, base64.b64encode(b).decode()] for i, b in additions]}


class Documentation(unittest.TestCase):
    def test_round_trip_preserves_every_original_byte(self):
        original = b'#!/usr/bin/env python3\r\nprint("original")\r\n'
        entry = entry_for('upstream/sources/demo/main.py', original,
                          [(23, '# Explication française\r\n'.encode()), (len(original), b'# fin\r\n')])
        result = documentation.apply_bytes(original, entry)
        self.assertEqual(documentation.original_bytes(result, entry), original)
        self.assertEqual(documentation.original_bytes(original, entry), original)

    def test_modified_comment_or_instruction_is_rejected(self):
        original = b'int value = 1;\n'
        entry = entry_for('upstream/sources/demo/main.cpp', original, [(0, b'/* note */\n')])
        result = documentation.apply_bytes(original, entry)
        for altered in [result.replace(b'value = 1', b'value = 2'), result.replace(b'note', b'edit')]:
            with self.assertRaises(ValueError):
                documentation.original_bytes(altered, entry)

    def test_new_readme_has_no_original_source_bytes(self):
        entry = entry_for('upstream/sources/demo/README.md', None, [(0, b'# Guide\n')])
        result = documentation.apply_bytes(b'', entry)
        self.assertIsNone(documentation.original_bytes(result, entry))
        with self.assertRaises(ValueError):
            documentation.apply_bytes(b'personal notes', entry)

    def test_apply_is_idempotent_and_preflight_preserves_personal_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = ['upstream/sources/demo/a.cpp', 'upstream/sources/demo/b.cpp']
            original = b'int n = 1;\n'
            entries = {p: entry_for(p, original, [(0, b'/* doc */\n')]) for p in files}
            for p in files:
                (root / p).parent.mkdir(parents=True, exist_ok=True)
                (root / p).write_bytes(original)
            with mock.patch.object(documentation, 'ROOT', root), mock.patch.object(documentation, 'registry', return_value=entries):
                (root / files[1]).write_bytes(b'personal edit')
                with self.assertRaises(ValueError):
                    documentation.apply()
                self.assertEqual((root / files[0]).read_bytes(), original)
                (root / files[1]).write_bytes(original)
                self.assertEqual(documentation.apply(), 2)
                self.assertEqual(documentation.apply(), 0)
                self.assertEqual(documentation.verify(), 2)

    def test_tree_hash_ignores_only_verified_additions_and_finder_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / 'upstream/sources/demo'
            base.mkdir(parents=True)
            original = b'int n = 1;\n'
            (base / 'main.cpp').write_bytes(original)
            entries = {
                'upstream/sources/demo/main.cpp': entry_for('upstream/sources/demo/main.cpp', original, [(0, b'/* doc */\n')]),
                'upstream/sources/demo/README.md': entry_for('upstream/sources/demo/README.md', None, [(0, b'# Guide\n')]),
            }
            with mock.patch.object(documentation, 'ROOT', root), mock.patch.object(documentation, 'registry', return_value=entries):
                before = documentation.normalized_tree_digest(base)
                documentation.apply()
                (base / '.DS_Store').write_bytes(b'Finder metadata')
                self.assertEqual(documentation.normalized_tree_digest(base), before)
                (base / 'unexpected.txt').write_text('new source content')
                self.assertNotEqual(documentation.normalized_tree_digest(base), before)


if __name__ == '__main__':
    unittest.main()
