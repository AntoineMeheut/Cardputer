# Publier Cardputer Lab sur GitHub

Le projet est préparé pour une **publication manuelle**. Aucun dépôt distant n’a été créé, aucun `push` n’a été exécuté et aucun compte GitHub n’a été choisi pendant cette préparation.

Le [bilan de vérification et de nettoyage](VERIFICATIONS.md) décrit les contrôles effectués et les éléments conservés. Après nettoyage, l’environnement `.venv` et les téléchargements tiers sont absents ; les commandes de contrôle de l’export fonctionnent avec un Python système et Git.

## 1. Utiliser la copie prête à partager

Le script [prepare_publication.py](../../tools/prepare_publication.py) crée une archive propre du projet, selon le [.gitignore](../../.gitignore), et vérifie les liens des fichiers réellement distribués. Il utilise Python et Git, sans dépendance Python supplémentaire, sans connexion réseau et sans modifier l’éventuel dépôt Git du dossier de travail.

```sh
# Depuis la racine, avec Python et Git disponibles.
python tools/prepare_publication.py --check
python tools/prepare_publication.py
```

Les sorties locales sont :

```text
output/publication/Cardputer-Lab-GitHub.zip
output/publication/Cardputer-Lab-manifeste.json
```

Le manifeste donne la liste des fichiers, leur taille, leur SHA-256 et l’empreinte du ZIP. Extraire le ZIP dans **un nouveau dossier** : son répertoire `Cardputer-Lab` est la copie conseillée pour le premier envoi. Conserver le manifeste à côté pour contrôler l’archive ; il n’est pas nécessaire de le publier.

| Inclus | Conservé uniquement sur le poste |
|---|---|
| README, programmes, guides, schémas et captures pédagogiques | Environnement Python, PlatformIO et caches |
| Guide PDF de 238 pages | Fichiers temporaires et sauvegardes `build/` |
| Catalogue, manifeste amont et registre des ajouts français | Archives tierces et arbres extraits volumineux |
| Licences, modèles d’issue / PR et workflow de vérification | Configurations personnelles et captures privées |
| Preuves datées copiées dans `docs/code/rapports/` | Journaux bruts contenant les chemins du poste |

Le contrôle refuse les répertoires imprévus, les liens symboliques, les fichiers de plus de 25 Mio et certaines signatures de clés ou jetons. Ce seuil est un choix de ce projet. Le contrôle ne certifie pas l’absence de toute donnée personnelle : relire les fichiers ajoutés après la préparation, en particulier les captures et traces.

## 2. Vérifier la copie extraite

Depuis `Cardputer-Lab`, ce premier contrôle fonctionne sans télécharger les sources tierces :

```sh
python tools/prepare_publication.py --check
```

Pour reproduire les autres vérifications, installer l’environnement suivant le [guide d’installation](../installation.md), puis :

```sh
python tools/fetch_upstream.py
python tools/fetch_upstream.py --verify
python tools/check_docs.py
python tools/check_documentation.py
python tools/test_host.py
python tools/build_all.py
```

La restauration télécharge les révisions exactes et réapplique les commentaires français. Sur GitHub, les liens vers des fichiers sous `upstream/sources/NOM_DU_PROJET/` ne mènent pas à des fichiers versionnés ; ils servent à la lecture locale après restauration. Les [liens des dépôts d’origine](../../upstream/README.md) restent disponibles dans le catalogue. Les fonctions des firmwares tiers et leurs dépendances ne sont pas toutes validées par la compilation des vingt expériences locales.

## 3. Créer le dépôt distant vous-même

Dans GitHub, créer un nouveau dépôt vide. Nom proposé : **`cardputer-lab`**. Choisir vous-même son propriétaire et sa visibilité. Ne pas générer un deuxième README, une licence ou un `.gitignore` : ces fichiers sont déjà présents.

Description proposée :

> Laboratoire M5Stack Cardputer en français : 20 expériences, code commenté, schémas, démonstrations et guide PDF de 238 pages.

Sujets possibles : `cardputer`, `m5stack`, `esp32-s3`, `platformio`, `arduino`, `french`, `embedded`, `rfid`, `gps`.

## 4. Préparer votre premier commit

Ces commandes sont à exécuter par vous dans la **copie extraite neuve**, qui ne contient pas de dossier `.git` :

```sh
git init -b main
git add .
git status --short
git diff --cached --stat
git diff --cached --check
git commit -m "Initialiser Cardputer Lab et sa documentation française"
```

Relire la sélection affichée avant le commit. Si Git demande votre identité, définir le nom et l’adresse de commit de votre choix ; aucun auteur personnel n’est imposé par ce projet. Dans un dépôt déjà existant, conserver son historique et sa branche au lieu de réinitialiser à partir de cette procédure.

## 5. Publier quand vous le décidez

Remplacer `URL_DU_DEPOT` par l’URL du dépôt vide créé à l’étape 3. **Cette étape envoie effectivement les fichiers vers GitHub ; elle n’a pas été exécutée pendant la préparation.**

```sh
git remote add origin URL_DU_DEPOT
git push -u origin main
```

Le workflow [Vérifications du laboratoire](../../.github/workflows/verify.yml) s’exécute après le push et les pull requests si GitHub Actions est activé. Il contrôle la sélection publique, restaure les sources, vérifie les empreintes, lance les tests puis compile les vingt programmes. Consulter son premier résultat avant de présenter la CI comme réussie. Le workflow ne crée ni release, ni site, ni publication de firmware.

Ouvrir ensuite le README sur GitHub, vérifier la bannière et le lien vers le PDF, puis compléter la description et les sujets du dépôt. Les badges de CI dépendant du nom de propriétaire et du dépôt ne sont pas ajoutés avant que ces informations existent.

## Maintenir le paquet

Après modification, relancer les contrôles pertinents puis le script d’export. Il remplace le ZIP et le manifeste locaux, sans supprimer les fichiers sources. Le [guide de contribution](../../CONTRIBUTING.md) et les [licences tierces](../../THIRD_PARTY.md) précisent la provenance à conserver. Le PDF reste une édition datée : sa régénération demande la révision éditoriale décrite par son [générateur](../../tools/guide_pdf/README.md).
