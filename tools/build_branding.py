#!/usr/bin/env python3
"""Dessiner la bannière SVG du README, avec des lettres converties en tracés.

PyMuPDF est une dépendance facultative du générateur PDF. Les polices restent
sur le poste : aucun fichier de police n'est copié dans le dépôt. Voir
docs/assets/identite/README.md pour les paramètres et la direction graphique.
"""
import argparse
from pathlib import Path
import re
from xml.sax.saxutils import escape

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
PINK = '#ff2c86'
GREEN = '#a5ffb4'
WHITE = '#f5f2e9'
DARK = '#090a0e'


def lettering(label, font_path, size, x, baseline, color, identifier, max_width=None):
    """Rendre un texte en courbes pour un affichage identique sur GitHub.

    Une page temporaire fournit les contours des glyphes. Les identifiants SVG
    sont préfixés pour éviter les collisions entre les blocs de texte.
    """
    font = fitz.Font(fontfile=str(font_path))
    scale = min(1, max_width / font.text_length(label, fontsize=size)) if max_width else 1
    with fitz.open() as document:
        page = document.new_page(width=2600, height=700)
        page.insert_font(fontname='local', fontfile=str(font_path))
        rgb = tuple(int(color[n:n + 2], 16) / 255 for n in (1, 3, 5))
        page.insert_text((0, size + 10), label, fontname='local', fontsize=size, color=rgb)
        content = page.get_svg_image(text_as_path=True)
    content = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', content.strip())
    content = re.sub(r'id="([^"]+)"', lambda m: f'id="{identifier}-{m[1]}"', content)
    content = re.sub(r'xlink:href="#([^"]+)"', lambda m: f'xlink:href="#{identifier}-{m[1]}"', content)
    return f'<g aria-label="{escape(label)}" transform="translate({x} {baseline - size - 10}) scale({scale} 1)">{content}</g>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--title-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Impact.ttf'))
    parser.add_argument('--mono-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Courier New Bold.ttf'))
    args = parser.parse_args()
    for path in (args.title_font, args.mono_font):
        if not path.is_file():
            parser.error(f'Police absente : {path}. Fournir le chemin avec les options --*-font.')
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="700" viewBox="0 0 1600 700" role="img" aria-labelledby="title desc">
<title id="title">Cardputer Lab — le laboratoire embarqué en français</title>
<desc id="desc">Typographie massive blanche et rose sur fond noir, repères de terminal verts et dessin original d’un Cardputer. 20 expériences, 18 projets tiers, guide de 238 pages.</desc>
<rect width="1600" height="700" fill="{DARK}"/>
<path d="M0 93H1600M0 565H1600M0 625H1600M1030 93V565" stroke="#292330" stroke-width="1"/>
<rect x="0" y="0" width="10" height="700" fill="{PINK}"/>
<path d="M1518 18v25m-12-12h25M1518 650v25m-12-12h25" stroke="{PINK}" stroke-width="2"/>''']

    def label(text, size, x, y, color=WHITE, title=False, width=None):
        parts.append(lettering(text, args.title_font if title else args.mono_font, size,
                               x, y, color, f't{len(parts)}', width))

    label('DOSSIER 001 / LABORATOIRE EMBARQUÉ', 21, 58, 57, GREEN)
    label('FR / K132', 21, 1330, 57, PINK)
    # L'écho coloré et les fines coupures donnent un aspect imprimé sans animation.
    label('CARDPUTER', 218, 63, 285, '#4b1534', True, 1480)
    label('CARDPUTER', 218, 58, 282, WHITE, True, 1480)
    label('LAB', 249, 56, 515, PINK, True)
    parts.append(f'<path d="M283 179h136M1173 231h155M107 432h115" stroke="{DARK}" stroke-width="3"/>')
    label('LIRE.', 36, 575, 358)
    label('CÂBLER.', 36, 575, 411)
    label('EXPÉRIMENTER.', 36, 575, 464)
    label('DU CODE AU MATÉRIEL', 18, 578, 513, GREEN)

    # Illustration géométrique originale : elle ne représente pas un essai réel.
    parts.append('''<g transform="translate(1080 322) rotate(-4 210 100)">
<rect x="0" y="0" width="425" height="212" rx="18" fill="#131219" stroke="#ff2c86" stroke-width="3"/>
<rect x="15" y="14" width="395" height="85" rx="5" fill="#070b0a" stroke="#39333e"/>
<path d="M33 74h26l9-18 11 28 14-40 13 30h52" fill="none" stroke="#a5ffb4" stroke-width="2"/>
<rect x="371" y="32" width="19" height="5" fill="#a5ffb4"/>
<path d="M189 38h145M189 49h103M189 60h122M189 71h77" stroke="#438259" stroke-width="4"/>''')
    for row in range(4):
        for column in range(14):
            parts.append(f'<rect x="{17 + column * 28}" y="{112 + row * 21}" width="22" height="14" rx="2" fill="#22212a" stroke="#66616d" stroke-width="0.6"/>')
    parts.append('<path d="M91 204h235" stroke="#ff2c86" stroke-width="2"/></g>')
    label('20 EXPÉRIENCES', 23, 58, 604, WHITE)
    label('18 PROJETS TIERS', 23, 580, 604, WHITE)
    label('238 PAGES EN FRANÇAIS', 23, 1110, 604, WHITE, width=430)
    label('ESP32-S3  //  ARDUINO + PLATFORMIO  //  SOURCES COMMENTÉES  //  SCHÉMAS & DÉMONSTRATIONS', 17, 58, 667, GREEN, width=1390)
    parts.append('</svg>')
    target = ROOT / 'docs/assets/identite/cardputer-lab.svg'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    print(target.relative_to(ROOT))


if __name__ == '__main__':
    main()
