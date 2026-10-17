# CardputerLab : interface commune

Les programmes actifs incluent [src/CardputerLab.h](src/CardputerLab.h). Les formats utilisables sans carte sont dans [src/LabFormats.h](src/LabFormats.h). Les deux anciens en-têtes `Lab.h` et `lab_logic.h` appartiennent aux brouillons et ne doivent pas être mélangés aux interfaces actives : plusieurs noms de fonctions se recouvrent.

## Utilisation dans une expérience

```cpp
#include <CardputerLab.h>
void setup() { Lab::begin("Mon expérience"); }
void loop() {
    M5Cardputer.update();
    if (Lab::enter()) { Lab::body(); Lab::line("Entrée détectée"); }
    delay(5);
}
```

Créer une cible `env:` sélectionnant uniquement ce programme, sur le modèle des [expériences](../../experiments/README.md). `Lab::pressed` et `Lab::enter` lisent les événements déjà mis à jour ; ils ne rappellent pas `M5Cardputer.update`.

## Matériel et sorties

K132 original : Grove jaune G2, blanc G1 ; LED IR G44. SD : CS12, MOSI14, SCK40, MISO39. GPS : RX G1, TX G2, 115200 bauds. `Lab::line` écrit sur l’écran et sur la console ; `body` efface uniquement la zone de contenu. `sdBegin` monte la SD à 10 MHz ; `nextFile` réserve seulement un nom logique, sans ouvrir le fichier.

## Formats et contrôles

`wavHeader(out, dataSize, rate)` exige 44 octets de sortie et décrit du PCM mono 16 bits little-endian. `writableLabBlock` n’accepte que le bloc RFID 4. `decodePacket` contrôle la taille exacte, la signature et un zéro terminal dans le texte de 32 octets. Après un retour faux, ne pas utiliser le paquet de sortie. La signature du paquet ne remplace pas une authentification.

Consulter le [détail de chaque fonction](src/README.md). Vérifier avec `python tools/test_host.py` depuis la racine.

## Interfaces historiques

`Lab.h` offre `screen`, `key`, `input`, `append` et une tentative ancienne de capture. Il dépend de constantes `SD_*` non définies par la configuration actuelle. Le convertisseur `capture_ecran.py` évoqué historiquement est absent ; aucune capture réelle n’est promise. `lab_logic.h` autorise davantage de blocs RFID que le parcours actif et propose un filtre temporel et un tampon de lignes.
