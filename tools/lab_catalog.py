# Données éditoriales partagées par les README et les aperçus. Voir README.md pour les commandes, les
# sorties et les prérequis.
"""Catalogue des programmes ; utilisé pour les index et les aperçus pédagogiques."""
# Chaque tuple contient : dossier, cible PlatformIO, titre, matériel, manipulation, résultat, guide
# relatif à docs/, projet tiers et lignes d’écran fictives.
EXPERIMENTS = [
('01-diagnostic', 'diagnostic', 'Diagnostic du Cardputer', 'Cardputer seul', 'Taper des lettres, presser s pour un bip, puis G0.', 'Écran, clavier, tension batterie et bouton sont affichés.', 'composants/cardputer.md', 'm5cardputer', ['Ecran / clavier / batterie / son','Batterie : 4020 mV','Touches : Bonjour','s : bip     G0 : bouton']),
('02-notes-sd', 'notes-sd', 'Carnet sur microSD', 'Cardputer et microSD FAT32', 'Saisir une note de 80 caractères maximum, corriger avec effacement, valider par Entrée.', 'Chaque note est ajoutée à /notes.txt ; lire le fichier sur ordinateur après extinction.', 'composants/cardputer.md', 'm5cardputer', ['SD prete','Saisir puis ENTREE pour ajouter','> Ma premiere note','/notes.txt']),
('03-micro-wav', 'micro-wav', 'Enregistrer et écouter un WAV', 'Cardputer ; microSD facultative pour conserver le fichier', 'Presser r, parler une seconde, puis p pour écouter la prise. Répéter r crée un nouveau fichier.', 'Un signal mono 16 kHz / 16 bits est conservé en RAM et, si disponible, sur SD.', 'composants/cardputer.md', 'm5cardputer', ['r : enregistrer 1 s','p : ecouter','/micro-0.wav','Micro et haut-parleur alternes']),
('04-wifi-scan', 'wifi-scan', 'Observer les réseaux Wi-Fi', 'Cardputer ; point d’accès 2,4 GHz pour vérifier', 'Attendre le scan passif ; n change de page, s relance.', 'SSID, canal et RSSI sont visibles ; les réseaux 5 GHz seuls sont absents.', 'experiences/wifi-bluetooth.md', 'cardputer-demo', ['3 reseaux | n : suite | s : scan','Reseau-de-test','ch 6   -48 dBm','Donnees de demonstration']),
('05-wifi-web', 'wifi-web', 'Serveur Web local', 'Cardputer et navigateur sur téléphone ou PC', 'Rejoindre Cardputer-Lab avec le mot de passe affiché, puis ouvrir son adresse HTTP.', 'La page et /api/status retournent durée de fonctionnement et tension batterie.', 'experiences/wifi-bluetooth.md', 'cardputer-demo', ['Cardputer-Lab','Mot de passe : cardputer-lab','http://192.168.4.1','Tableau de bord local']),
('06-ble-scan', 'ble-scan', 'Écouter les annonces BLE', 'Cardputer ; balise BLE ou téléphone pour l’essai', 'Attendre quatre secondes ; s recommence. Consulter le moniteur pour tous les résultats.', 'Noms annoncés et RSSI ; un appareil sans nom n’est pas forcément absent.', 'experiences/wifi-bluetooth.md', 'bruce', ['Annonces BLE | s : relancer','Cardputer-Lab  -42 dBm','(sans nom)     -71 dBm','Ecoute passive']),
('07-ble-balise', 'ble-balise', 'Émettre une balise BLE', 'Cardputer et second appareil de scan BLE', 'Chercher Cardputer-Lab avec le scanner ; Espace coupe ou rétablit les annonces.', 'Une balise non connectable, sans service GATT, apparaît dans un scanner BLE.', 'experiences/wifi-bluetooth.md', 'bruce', ['Nom : Cardputer-Lab','Annonce BLE active','Espace : marche / arret']),
('08-ir-tv', 'ir-tv', 'Télécommande TV infrarouge', 'Cardputer, votre TV et un code NEC compatible connu', 'Renseigner LAB_NEC_CODE, viser votre TV puis presser Entrée.', 'Une trame NEC est émise ; la réaction de la TV valide le code, pas le seul texte à l’écran.', 'experiences/television-ir.md', 'irremote', ['Configurer LAB_NEC_CODE','Viser votre TV puis ENTREE','Code de demonstration','Une trame NEC sur demande']),
('09-i2c-scan', 'i2c-scan', 'Détecter le RFID2 sur I²C', 'Cardputer, Grove et RFID2', 'Brancher hors tension, lancer le programme ; s refait le scan.', 'Le RFID2 doit répondre à 0x28 sur SDA G2 / SCL G1.', 'composants/rfid2.md', 'm5rfid', ['SDA=G2 / SCL=G1','Adresse : 0x28','1 reponse | s : relancer']),
('10-ir-reflectif', 'ir-reflectif', 'Mesurer et compter les approches', 'Cardputer, Grove et U175', 'Approcher une feuille blanche puis noire ; observer AO/DO et presser r pour remettre le compteur à zéro.', 'La mesure change avec la réflexion ; le compteur détecte les approches lentes.', 'composants/ir-reflectif.md', 'm5unified', ['DO G2 : 0','AO G1 : 1240 / 4095','Approches : 3','r : remettre a zero']),
('11-rf433-rx', 'rf433-rx', 'Recevoir une trame ASK/OOK', 'Cardputer, RF433R et émetteur de test compatible', 'Déclencher la source de test ; comparer code, bits, protocole et durée.', 'Une trame compatible s’affiche ; l’absence de décodage ne prouve pas l’absence de signal.', 'composants/rf433-recepteur.md', 'rc-switch', ['Code : 5902900','Hex : 0x5a1234','Bits : 24 | Protocole : 1','Impulsion : 350 us']),
('12-rf433-tx', 'rf433-tx', 'Envoyer une trame RF de laboratoire', 'Cardputer, RF433T et une station réceptrice séparée', 'Attendre cinq secondes, presser Entrée et vérifier la réception sur la seconde station.', 'Trois répétitions de la trame synthétique 0x5A1234 ; aucune émission automatique.', 'composants/rf433-emetteur.md', 'rc-switch', ['TX G2 / jaune','Trame de test : 0x5a1234','ENTREE : 3 repetitions','Intervalle minimal : 5 s']),
('13-rfid-uid', 'rfid-uid', 'Lire l’identifiant des cartes F08', 'Cardputer, RFID2, Grove et carte F08', 'Présenter une seule carte, relever son UID, puis la retirer avant une nouvelle lecture.', 'UID, SAK et type sont affichés, sans écriture sur la carte.', 'composants/rfid2.md', 'm5rfid-legacy', ['UID : 04 11 22 33','SAK : 0x08','MIFARE 1KB','Exemple fictif']),
('14-rfid-bloc', 'rfid-bloc', 'Lire et écrire le bloc 4 de test', 'Cardputer, RFID2 et F08 vierge réservée au laboratoire', 'Lire d’abord sans w. Retirer la carte ; w arme dix secondes, puis représenter la carte TEST.', 'Le bloc 4 seul est remplacé puis relu ; les trailers et le bloc constructeur ne sont pas écrits.', 'composants/cartes-f08.md', 'm5rfid-legacy', ['Carte de TEST uniquement','w : armer ecriture 10 s','Bloc 4 uniquement','Lecture par defaut']),
('15-gps', 'gps', 'Afficher position et heure UTC', 'Cardputer, Grove et GPS/BDS v1.1', 'Sortir, orienter l’antenne vers le ciel, vérifier les octets NMEA et attendre une position récente.', 'Latitude, longitude, satellites, altitude/vitesse disponibles et heure UTC.', 'composants/gps-at6668.md', 'tinygpsplus', ['Satellites : 8','Lat : 48.000000','Lon : 2.000000','UTC 10:00:00 | fictif']),
('16-gps-sd', 'gps-sd', 'Journal GPS et export GPX', 'Cardputer, GPS v1.1, Grove et microSD FAT32', 'Attendre une position, marcher, presser q pour fermer, éteindre puis copier le CSV.', 'Un fichier /trace-N.csv sans écrasement ; conversion locale avec tools/gps_csv_to_gpx.py.', 'composants/gps-at6668.md', 'tinygpsplus', ['/trace-0.csv','12 points enregistres','q : fermer le journal','Positions fictives ici']),
('17-espnow', 'espnow', 'Messages entre deux Cardputer', 'Deux Cardputer ; adaptation possible sur un second ESP32', 'Téléverser le même programme sur les deux ; presser Entrée alternativement.', 'Le pair reçoit Bonjour ; le retour d’envoi seul ne garantit pas la réception applicative.', 'experiences/wifi-bluetooth.md', 'cardputer-demo', ['Canal : 1','ENTREE : envoyer Bonjour','Recu #1','Bonjour du Cardputer']),
('18-usb-clavier', 'usb-clavier', 'Phrase au clavier USB', 'Cardputer, câble USB de données et éditeur de texte', 'Ouvrir un éditeur vide sur son poste ; presser Entrée sur le Cardputer.', 'Une phrase fixe est saisie une fois par pression ; disposition US de la bibliothèque HID.', 'composants/cardputer.md', 'm5cardputer', ['Ouvrir un editeur sur le PC','ENTREE : saisir Bonjour','Aucun envoi automatique']),
('19-fm-rda5807', 'fm-rda5807', 'Radio FM avec module additionnel', 'RDA5807, adaptation 3,3 V, antenne et audio externe ; absents de la liste initiale', 'Vérifier le montage documenté ; + / - règlent la fréquence par pas de 0,1 MHz.', 'La station est entendue sur la sortie audio du module FM, pas sur le haut-parleur interne.', 'experiences/fm.md', 'rda5807', ['FM : 99.5 MHz','+ / - : pas de 0.1 MHz','Audio sur module FM','Materiel additionnel']),
('20-nrf24', 'nrf24', 'Paquets NRF24 à deux stations', 'Deux NRF24, deux contrôleurs, adaptateur microSD/SPI et alimentation 3,3 V', 'Retirer SD, vérifier le câblage du guide, presser Entrée sur une seule station à la fois.', 'Le pair affiche Salut N ; l’émetteur indique si l’accusé matériel a été reçu.', 'experiences/nrf24.md', 'rf24', ['2440 MHz | 1 Mbit/s','ENTREE : message','Accuse NRF24 recu','Materiel additionnel']),
]


# Importer ce module ne réécrit aucun README. Seule l’exécution directe lance la génération du
# catalogue.
def write_readme(path, generated):
    """Régénérer le catalogue en conservant le complément de lecture du code.

    Le marqueur sépare les données produites par EXPERIMENTS des explications
    françaises ajoutées lors de l'étude des sources. Seule la première partie
    est remplacée ; un nouveau dossier sans README fonctionne également.
    """
    marker = '<!-- documentation-code-fr -->'
    previous = path.read_text() if path.exists() else ''
    if marker in previous:
        generated = generated.rstrip() + '\n\n' + marker + previous.split(marker, 1)[1]
    path.write_text(generated)


if __name__ == '__main__':
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    rows = []
    # Une cible ne doit sélectionner qu’un main.cpp ; check_docs.py contrôle cet accord avec
    # platformio.ini.
    for folder, env, title, hardware, usage, expected, guide, upstream, screen in EXPERIMENTS:
        number = folder.split('-')[0]
        content = f'''# {number} — {title}

Matériel : **{hardware}**. Lire [le guide détaillé](../../docs/{guide}) et [l'installation](../../docs/installation.md) avant le raccordement. Les schémas sont dans le guide.

## Compiler et installer

Depuis la racine du projet, après activation de l'environnement Python et téléchargement des sources :

```sh
pio run -e {env}
pio run -e {env} -t upload --upload-port PORT
pio device monitor --port PORT --baud 115200
```

Remplacer `PORT` par la valeur de `pio device list`. Brancher les modules hors tension. Une seule expérience est installée à la fois.

## Manipulation

{usage}

Résultat attendu : {expected}

Si le résultat diffère, consulter [le dépannage](../../docs/depannage.md) et le guide du composant. Comparer d'abord l'alimentation, le brochage et les paramètres de protocole.

## Code et prolongements

Le [programme local](main.cpp) est une expérience originale utilisant les bibliothèques du projet. Le dépôt [amont associé](../../upstream/sources/{upstream}) fournit d'autres exemples ; sa présence n'implique pas qu'il a été compilé entièrement. Voir [les sources et licences](../../upstream/README.md).

La compilation est contrôlée dans [le rapport de validation](../../docs/validation.md). Les essais physiques restent à réaliser. L'[aperçu navigateur](../../tools/apercu.html#{env}) est une démonstration avec données fictives, pas un émulateur de l'ESP32.
'''
        write_readme(root / 'experiments' / folder / 'README.md', content)
        rows.append(f'| {number} | [{title}]({folder}/README.md) | `{env}` | {hardware} |')
    write_readme(root / 'experiments/README.md', '''# Catalogue des 20 expériences

Tous les programmes sont indépendants et destinés au **Cardputer K132**. Commencer par 01, puis suivre le guide du composant. Les expériences 19 et 20 exigent du matériel supplémentaire ; 17 demande deux stations. Les opérations SD nécessitent une carte ajoutée à l’inventaire initial.

| N° | Expérience | Environnement PlatformIO | Matériel |
|---|---|---|---|
''' + '\n'.join(rows) + '''

## Continuer les explorations

Après ces bases : graphe du signal micro, synthétiseur au clavier, lecteur WAV, dessin sur écran, jeu de mémoire RFID, inventaire de cartes, histogramme du capteur réflectif, protocole RF avec compteur, pertes radio selon la distance, favoris TV, RSSI selon la position, API HTTP locale, échange ESP-NOW avec accusé, horloge UTC, distance GPS filtrée, export cartographique, RDS FM et réseau de capteurs NRF24.

Ces prolongements sont des pistes à adapter, pas des programmes supplémentaires présentés comme terminés. Les [projets téléchargés](../upstream/README.md) donnent les bases correspondantes.

Les dossiers avec soulignés, comme `01_diagnostic`, sont des brouillons conservés hors de cette matrice. Voir [l'état du projet](../docs/etat-projet.md) avant de les reprendre.
''')
