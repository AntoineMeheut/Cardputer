# État du projet et prochaine reprise

État initial du **10 octobre 2026**, complété le **17 octobre 2026**. Le [cahier des charges original](../project-specifications.md) est conservé. La [préparation GitHub et le nettoyage](publication/VERIFICATIONS.md) ajoutent un README graphique, une copie publiable vérifiée et la suppression des caches reconstituables. Le [bilan documentaire](code/README.md) décrit les commentaires français et les contrôles ultérieurs.

## Réalisé

- README général et guides français pour les huit équipements.
- Installation, dépannage, matrice de compatibilité et parcours thématiques TV/IR, badges RF/RFID, Wi-Fi/BLE, FM, GPS et NRF24.
- Vingt programmes sélectionnables dans PlatformIO, tous compilés avec succès.
- Dix-huit dépôts tiers téléchargés intégralement sous forme d'archives GitHub et extraits localement, avec commits et empreintes ; limites des sous-modules/LFS documentées.
- Neuf schémas SVG et seize captures pédagogiques du navigateur, avec provenance explicite.
- Export CSV vers GPX, visualisation locale OOK/FSK/FM, tests sur ordinateur et workflow CI.
- Licences et attributions, documentation des incompatibilités matérielles et rapport de validation.

## Ce qui n'est pas attesté

Les **essais physiques** et leurs photographies n'ont pas été réalisés. Les captures incluses sont des maquettes d'utilisation. Les montages FM et NRF24 nécessitent des équipements additionnels ; ESP-NOW et un banc RF complet demandent une seconde station. Aucun appareil n'a été flashé et aucun dépôt GitHub distant n'a été créé ou publié.

La sélection de projets couvre les thèmes du cahier des charges, sans prétendre être une collecte exhaustive de tous les dépôts existants. Les projets tiers conservent leurs propres langues, licences, dépendances et instructions ; les guides qui les présentent sont en français.

## Reprendre concrètement

1. Lire [la validation](validation.md) et lancer `diagnostic` sur le Cardputer disponible.
2. Documenter chaque essai matériel avec modèle, branchement et observation, puis ajouter une vraie photo d'écran dans les guides.
3. Tester RFID2/F08 et GPS v1.1 avant d'envisager des montages combinés.
4. Choisir et valider les adaptations FM/NRF24 si l'on ajoute ce matériel.
5. Initialiser et publier le dépôt GitHub au nom choisi par son propriétaire, en suivant [CONTRIBUTING.md](../CONTRIBUTING.md).

## Fichiers conservés de brouillon

Les dossiers `experiments/01_diagnostic` jusqu'à `experiments/19_nrf24_pont` qui emploient des **soulignés** sont conservés sans être intégrés aux cibles actuelles. Ils représentent un autre ensemble de brouillons ; leurs variantes peuvent nécessiter des paramètres absents de la configuration actuelle. Les fichiers `lib/CardputerLab/src/Lab.h` et `lab_logic.h` leur sont associés. Ne pas les supprimer sans examen, et ne pas mélanger ces interfaces avec `CardputerLab.h` / `LabFormats.h` utilisés par les vingt programmes vérifiés.

Le catalogue actuel emploie les dossiers **avec tirets**, par exemple `experiments/01-diagnostic`. Les caches `.venv`, `.platformio`, `.pio`, `.cache`, `build` et les téléchargements `upstream` sont volumineux mais reproductibles ; les documents, programmes originaux et le manifeste sont les fichiers destinés au partage.
