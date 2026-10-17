#!/usr/bin/env python3
# Tests des formats indépendants du matériel et vérification croisée du WAV. Voir README.md pour les
# commandes, les sorties et les prérequis.
"""Tests sur ordinateur : format WAV, bornes RFID, trames ESP-NOW et GPX."""
from pathlib import Path
import subprocess
import sys
import tempfile
import wave

ROOT = Path(__file__).resolve().parents[1]
# La découverte unittest exécute les fichiers test_*.py ; check=True arrête le script dès un échec.
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT, check=True)
# Le binaire C++ et le WAV ne restent pas dans le dépôt après la sortie du contexte.
with tempfile.TemporaryDirectory() as temp:
    executable, wav = Path(temp) / 'formats', Path(temp) / 'test.wav'
    subprocess.run(['c++', '-std=c++11', '-I', str(ROOT / 'lib/CardputerLab/src'),
                    str(ROOT / 'tests/test_formats.cpp'), '-o', str(executable)], check=True)
    subprocess.run([str(executable), str(wav)], check=True)
    # Relire avec le module standard wave fournit un contrôle indépendant des octets écrits par le code
    # C++.
    with wave.open(str(wav), 'rb') as reader:
        assert (reader.getnchannels(), reader.getsampwidth(), reader.getframerate(), reader.getnframes()) == (1, 2, 16000, 16000)
print('Tests sur ordinateur réussis. Aucun matériel testé.')
