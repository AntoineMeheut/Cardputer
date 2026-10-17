/**
 * Formats binaires indépendants du matériel, testables avec un compilateur C++ hôte.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <stddef.h>
#include <stdint.h>
#include <string.h>
namespace Lab {
// Écrire un entier 16 bits little-endian dans deux octets fournis par l’appelant ; aucune vérification
// de capacité interne.
inline void put16(uint8_t* p, uint16_t n) { p[0] = n; p[1] = n >> 8; }
// Même contrat pour quatre octets : l’ordre little-endian est imposé par RIFF/WAV, indépendamment du
// processeur hôte.
inline void put32(uint8_t* p, uint32_t n) { for (int i = 0; i < 4; ++i) p[i] = n >> (8 * i); }
// out doit désigner au moins 44 octets. Produit un en-tête PCM mono 16 bits : dataSize est un nombre
// d’octets et rate un nombre d’échantillons par seconde.
inline void wavHeader(uint8_t* out, uint32_t dataSize, uint32_t rate) {
    memset(out, 0, 44);
    memcpy(out, "RIFF", 4); put32(out + 4, 36 + dataSize);
    memcpy(out + 8, "WAVEfmt ", 8); put32(out + 16, 16);
    // Format 1 = PCM ; un canal ; débit en octets = fréquence × 2, alignement = 2 octets, résolution = 16
    // bits.
    put16(out + 20, 1); put16(out + 22, 1); put32(out + 24, rate);
    put32(out + 28, rate * 2); put16(out + 32, 2); put16(out + 34, 16);
    memcpy(out + 36, "data", 4); put32(out + 40, dataSize);
}
// Ce laboratoire ne permet d'écrire que les 16 octets du bloc de données 4.
inline bool writableLabBlock(uint8_t block) { return block == 4; }
// Signature du protocole local. Elle repère le format attendu ; elle ne constitue ni une
// authentification ni un chiffrement.
constexpr uint32_t PACKET_MAGIC = 0x4C414231;
// Format mémoire partagé par les cartes du même firmware. text doit contenir un octet nul parmi ses 32
// octets ; ne pas supposer un protocole portable entre ABI différentes.
struct Packet { uint32_t magic; uint32_t sequence; char text[32]; };
// Valide la longueur avant copie, puis la signature et la terminaison du texte. data doit être lisible
// sur length octets ; out ne doit être utilisé que si le retour est vrai.
inline bool decodePacket(const uint8_t* data, size_t length, Packet& out) {
    if (length != sizeof(Packet)) return false;
    memcpy(&out, data, sizeof(out));
    return out.magic == PACKET_MAGIC && memchr(out.text, 0, sizeof(out.text));
}
}
