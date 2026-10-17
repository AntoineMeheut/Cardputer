/**
 * Adaptateur d’inclusion : expose l’API du pilote MFRC522-I2C aux programmes locaux, sans
 * réimplémenter le protocole.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <Wire.h>
// Adaptateur de construction uniquement ; l'API du pilote n'est pas réimplémentée ici.
#include "../../../upstream/sources/m5rfid-legacy/MFRC522_I2C.h"
