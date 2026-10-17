# Radio 433 MHz, badges et protocoles

## Trois familles à distinguer

| Objet | Technologie possible | Instrument adapté ici |
|---|---|---|
| Télécommande à bouton / badge radio | 433,92 MHz ASK/OOK, ou un autre système | RF433R uniquement si fréquence et modulation correspondent |
| Carte F08 sans pile | RFID HF 13,56 MHz | RFID2 WS1850S |
| Badge de proximité différent | 125 kHz, UHF, BLE, etc. | Identifier la technologie avant tout achat ou branchement |

Le mot « badge » ne désigne pas un protocole. Les [guides RF433](../composants/rf433-recepteur.md) et [RFID](../composants/rfid2.md) ne sont donc pas interchangeables.

## Banc RF433 de référence

Station A : Cardputer + RF433T, environnement `rf433-tx`. Station B : second contrôleur + RF433R, `rf433-rx` si c'est un Cardputer, sinon adapter l'exemple rc-switch à ses broches. Le récepteur est sur **G1**, l'émetteur sur **G2**. Un seul Cardputer et un seul câble ne fournissent pas deux stations.

Envoyer dix messages espacés, noter les codes décodés, le nombre de bits, le protocole et le nombre de pressions réussies. Les répétitions d'une même pression ne représentent pas des messages applicatifs distincts. Pour mesurer des pertes, ajouter un numéro de séquence à un protocole de test personnel.

## Codes fixes et codes tournants

Une télécommande à code fixe peut répéter la même trame. Un système à code tournant ajoute un état qui évolue ; reproduire un ancien signal ne constitue pas un fonctionnement normal de ce système. Le laboratoire ne réalise ni synchronisation forcée, ni contournement de contrôle d'accès. Le test TX fourni émet une donnée synthétique indépendante des captures.

Des variations observées ne permettent pas, à elles seules, d'identifier le système. Un décodeur peut ignorer un protocole pourtant présent sur l'air. Les unités SYN115/SYN531R sont des composants ASK/OOK à fréquence dédiée : elles ne remplacent pas un émetteur-récepteur FSK programmable ni un SDR.

## Sources et pistes

- [rc-switch](../../upstream/sources/rc-switch) : timings, encodage et exemples de télécommandes simples.
- [Bruce](../../upstream/sources/bruce) : modules RF, GPS et interfaces de périphériques ; matériel et brochages à sélectionner explicitement.
- [RF24](../../upstream/sources/rf24) et [RF24Network](../../upstream/sources/rf24network) : paquets numériques à 2,4 GHz avec modules supplémentaires, [guide dédié](nrf24.md).
- [RDA5807](../../upstream/sources/rda5807) : réception FM audio, [guide dédié](fm.md).
- [ESP32-Bus-Pirate](../../upstream/sources/bus-pirate) : étude de bus numériques et échanges UART/I²C ; ce n'est pas un récepteur de toutes les bandes RF.

Pour les émissions en France, vérifier les informations actuelles de l'[ANFR](https://www.anfr.fr/) et les paramètres de son montage. Ce dépôt ne fixe pas une puissance ou un rapport cyclique valable pour tous les pays et tous les modules.
