# Documentation française du code — bilan du 17 octobre 2026

Les sources et les répertoires de code ont reçu des commentaires et des README pour comprendre leur rôle et préparer leur utilisation. Les commentaires locaux détaillent les états, les unités, les formats, les conditions d’erreur et le cycle de chaque expérience. Dans les projets tiers, les commentaires d’API originaux sont conservés et complétés par des repères français et des guides par répertoire.

## Périmètre

- **39 programmes locaux** : 20 expériences actives et 19 brouillons, avec une notice individuelle et leur statut de compilation.
- **68 fichiers locaux existants** commentés : C/C++, Python, HTML et configurations.
- **4 613 sources/configurations tierces commentées**, dans 18 projets.
- **1 125 README tiers**, dont 1 010 nouveaux et 115 notices existantes enrichies.
- **84 formats documentés dans les README sans insertion de commentaire**, notamment JSON strict et sauvegardes non retenues comme sources compilables.

L’inventaire parcourt les sources de `experiments`, `include`, `lib`, `tools`, `tests`, les ateliers HTML et `upstream/sources`. Les environnements installés et les sorties reproductibles (`.venv`, `.platformio`, `.pio`, `.cache`, `build`, `tmp`) sont des dépendances ou résultats techniques, pas des projets à commenter. Les archives compressées et les ressources binaires restent les références ; les dossiers contenant du code disposent de README voisins.

## Accès rapide

- [Catalogue des programmes et brouillons](../../experiments/README.md).
- [Bibliothèques locales](../../lib/README.md) et [paramètres](../../include/README.md).
- [Outils](../../tools/README.md), [tests](../../tests/README.md) et [données d’essai](../../fixtures/README.md).
- [Sommaire des sources tierces](../../upstream/sources/README.md).
- [Registre réversible des commentaires](../../upstream/documentation-fr/README.md).

## Couverture des projets tiers

| Projet | Sources/configurations commentées | README français | Dont nouveaux |
|---|---:|---:|---:|
| [m5cardputer](../../upstream/sources/m5cardputer/README.md) | 30 | 24 | 23 |
| [m5unified](../../upstream/sources/m5unified/README.md) | 123 | 38 | 36 |
| [m5gfx](../../upstream/sources/m5gfx/README.md) | 282 | 47 | 44 |
| [cardputer-demo](../../upstream/sources/cardputer-demo/README.md) | 651 | 114 | 105 |
| [m5rfid](../../upstream/sources/m5rfid/README.md) | 156 | 67 | 62 |
| [m5rfid-legacy](../../upstream/sources/m5rfid-legacy/README.md) | 8 | 7 | 6 |
| [tinygpsplus](../../upstream/sources/tinygpsplus/README.md) | 11 | 10 | 9 |
| [rc-switch](../../upstream/sources/rc-switch/README.md) | 14 | 11 | 10 |
| [irremote](../../upstream/sources/irremote/README.md) | 331 | 39 | 36 |
| [rf24](../../upstream/sources/rf24/README.md) | 176 | 53 | 47 |
| [rf24network](../../upstream/sources/rf24network/README.md) | 58 | 25 | 22 |
| [rda5807](../../upstream/sources/rda5807/README.md) | 299 | 57 | 48 |
| [launcher](../../upstream/sources/launcher/README.md) | 280 | 84 | 79 |
| [bruce](../../upstream/sources/bruce/README.md) | 883 | 108 | 98 |
| [evil-cardputer](../../upstream/sources/evil-cardputer/README.md) | 176 | 38 | 19 |
| [bus-pirate](../../upstream/sources/bus-pirate/README.md) | 961 | 321 | 313 |
| [microhydra](../../upstream/sources/microhydra/README.md) | 97 | 36 | 35 |
| [microhydra-apps](../../upstream/sources/microhydra-apps/README.md) | 77 | 46 | 18 |

## Vérifications réalisées

- Les **20 environnements actifs compilent** après les commentaires. Le [rapport](rapports/compilation-2026-10-17.json) consigne cette exécution ; les journaux bruts de préparation sont conservés dans la sauvegarde privée décrite en fin de page.
- **7 tests Python**, les tests C++ des formats et la relecture WAV passent. Les nouveaux tests contrôlent notamment la réversibilité des ajouts et le refus d’écraser une édition personnelle.
- Les **18 archives et arbres d’origine** sont vérifiés avec le manifeste après retrait virtuel des ajouts exactement enregistrés. Les fichiers Finder `.DS_Store` ne participent pas à cette empreinte documentaire.
- Les tokens des **48 sources C/C++ locales** restent identiques après retrait des commentaires. Les six pages HTML gardent leur contenu et leurs scripts ; les changements sont des commentaires.
- L’AST de **194 fichiers Python tiers** reste identique. Un fichier était déjà refusé par CPython 3.14 avant modification : voir la limite ci-dessous.
- La régénération du catalogue préserve les **40 README d’expériences**, y compris les compléments français et les brouillons.
- Les contrôles des liens locaux et de la couverture des README passent. Les détails des instructions sont conservés dans [le contrôle statique](rapports/instructions-2026-10-17.json).

Les changements exécutables concernent uniquement les outils de maintenance : conservation des compléments lors de la génération des README, extension des contrôles de liens et gestion du registre documentaire. Aucun protocole radio, réglage de broche ou comportement de programme embarqué n’a été modifié pour ajouter les explications.

## Limites constatées

**Launcher** : la compilation `m5stack-cardputer` a été tentée, mais s’arrête avant compilation car sa plateforme pioarduino n’est pas installée et GitHub n’est pas résolu dans cet environnement. Le [constat de compilation](rapports/README.md#launcher) décrit cette limite ; le journal complet est inclus dans la sauvegarde privée de préparation. Les autres cibles tierces ne sont pas toutes compilées ; certaines demandent ESP-IDF, Android, MicroPython ou du matériel supplémentaire.

**CO2_SCD40** : l’analyse CPython 3.14 relève un mélange de tabulations et d’espaces dans le source original, ligne 37 avant les nouveaux commentaires. Cette limite est signalée dans [la notice de l’application](../../upstream/sources/microhydra-apps/app-source/CO2_SCD40/README.md). Le code fonctionnel n’a pas été corrigé dans cette opération documentaire.

Aucun firmware n’a été téléversé et aucun essai physique n’est présenté comme réalisé. Le PDF livré précédemment reste une édition datée ; les numéros de ligne et inventaires de cette édition précèdent les nouveaux commentaires.

## Maintenir les explications

```sh
python tools/check_docs.py
python tools/check_documentation.py
python tools/upstream_documentation.py verify
python tools/fetch_upstream.py --verify
python tools/test_host.py
```

Sur le poste de préparation uniquement, la sauvegarde privée `output/sauvegardes/preparation-2026-10-17.zip` conserve les journaux et l’archive `build/documentation-2026-10-17/originaux-locaux.zip` contenant les originaux locaux d’avant intervention. Ce ZIP est exclu du dépôt public. Les caches tiers ont été supprimés après contrôle de leur restauration complète ; le registre permet de réappliquer les ajouts connus et de reconnaître une modification supplémentaire sans l’écraser. Voir le [bilan de préparation](../publication/VERIFICATIONS.md).
