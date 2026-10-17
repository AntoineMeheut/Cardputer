/**
 * Paramètres modifiables avant compilation ; ne configure pas les variantes historiques.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <stdint.h>
// Réglages de laboratoire ; aucun identifiant Wi-Fi personnel n'est nécessaire.
// Identité du point d’accès autonome de wifi-web ; ces valeurs de démonstration sont affichées par le
// firmware.
constexpr char LAB_AP_SSID[] = "Cardputer-Lab";
constexpr char LAB_AP_PASSWORD[] = "cardputer-lab"; // 8 caractères minimum ; réseau local de démonstration
// Code d'exemple NEC. Remplacer par celui de VOTRE téléviseur : non universel.
constexpr uint32_t LAB_NEC_CODE = 0x20DF10EF;
// Trame synthétique 24 bits, pas un identifiant de badge réel.
constexpr uint32_t LAB_RF_CODE = 0x5A1234;
// Canal Wi-Fi partagé par toutes les cartes ESP-NOW du banc ; le changement exige de recompiler les
// deux programmes.
constexpr uint8_t LAB_ESPNOW_CHANNEL = 1;
