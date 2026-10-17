# Ancien serveur Web — brouillon 05_web_local

Utilise AP_SSID et AP_PASSWORD et une route /etat retournant uptime_ms et heap. Ces constantes diffèrent de LAB_AP_* dans la configuration actuelle.

## Statut et point de départ

Ce dossier est conservé pour étude. Il n'est sélectionné par aucun `build_src_filter` du [projet PlatformIO](../../platformio.ini). La version active à consulter est : [05-wifi-web](../05-wifi-web/README.md).

Le [source](main.cpp) utilise les interfaces historiques [Lab.h et lab_logic.h](../../lib/CardputerLab/README.md). `Lab.h` référence notamment des constantes `SD_*` qui ne sont plus définies par l'actuel `lab_config.h`. Selon le brouillon, d'autres noms (`GROVE_*`, `AP_*`, etc.) et versions de bibliothèques diffèrent. Ce README n'affirme donc pas que le brouillon compile tel quel.

## Lire et adapter le code

1. Comparer `main.cpp` au programme actif associé : touches, broches, format des messages et dépendances.
2. Lire `setup()` pour relever les interfaces matérielles et les réglages, puis `loop()` pour suivre les actions.
3. Créer une cible de construction distincte sélectionnant seulement ce fichier ; rétablir explicitement les constantes et versions requises.
4. Compiler cette cible avant tout essai, puis documenter le matériel, la commande et le résultat réellement observé.

En-têtes utilisés : `Lab.h`, `WiFi.h`, `WebServer.h`.

Touches littérales repérées : voir les conditions de la boucle et les messages affichés. `\n` représente Entrée et `\b` l'effacement dans les variantes qui passent par `Lab::input()`.

## Limites et vérification

La capture série historique `!` n'est pas une capture d'écran validée : le convertisseur annoncé dans l'ancien code est absent et la lecture de la dalle dépend du matériel. Les anciennes trames ESP-NOW/NRF24, les tailles de notes et les temporisations ne sont pas nécessairement compatibles avec les expériences actuelles.

Lire le [catalogue](../README.md), les [paramètres communs](../../include/README.md) et le [guide de dépannage](../../docs/depannage.md). Aucun essai matériel de ce brouillon n'a été ajouté lors de la documentation.
