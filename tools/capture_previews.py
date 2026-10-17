#!/usr/bin/env python3
# Captures de maquettes HTML : les pixels obtenus ne prouvent aucune exécution du firmware. Voir
# README.md pour les commandes, les sorties et les prérequis.
"""Captures du véritable rendu navigateur de maquettes, pas du Cardputer."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(ROOT / '.cache/playwright'))
# Associer le nom de fichier historique de la capture à l’identifiant de l’expérience sélectionnée
# dans l’URL.
mapping = {'installation':'installation', 'diagnostic':'diagnostic', 'notes-sd':'notes-sd',
           'micro-wav':'micro-wav', 'wifi':'wifi-scan', 'wifi-web':'wifi-web', 'ble':'ble-scan',
           'ir-tv':'ir-tv', 'ir-reflectif':'ir-reflectif', 'rf433-rx':'rf433-rx',
           'rf433-tx':'rf433-tx', 'rfid':'rfid-uid', 'gps':'gps', 'gps-sd':'gps-sd',
           'fm':'fm-rda5807', 'nrf24':'nrf24'}
with sync_playwright() as p:
    # Playwright et son navigateur Chromium doivent être installés ; un environnement interdisant les
    # processus graphiques peut bloquer cette étape.
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width':1280, 'height':940}, device_scale_factor=1)
    for filename, env in mapping.items():
        page.goto((ROOT / 'tools/apercu.html').as_uri() + '#' + env)
        # Attendre que le sélecteur reflète le hash évite de capturer l’écran de la mauvaise expérience.
        page.wait_for_function('(id) => document.querySelector("#choice").value === id', arg=env)
        # Les fichiers existants de même nom sont remplacés ; garder le bandeau visible de démonstration.
        page.screenshot(path=str(ROOT / 'docs/assets/captures' / (filename + '.png')), full_page=True)
    browser.close()
print(f'{len(mapping)} captures pédagogiques générées.')
