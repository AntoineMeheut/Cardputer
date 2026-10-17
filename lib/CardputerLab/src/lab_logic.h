/**
 * Utilitaires historiques sans dépendance Arduino ; les vingt programmes actifs emploient
 * LabFormats.h.
 * Consulter le README.md de ce répertoire pour les prérequis, les contrats et les exemples
 * d’utilisation.
 */
#pragma once
#include <stddef.h>
#include <stdint.h>

namespace lab {
// Comparaison non signee : fonctionne egalement au debordement de millis().
inline bool elapsed(uint32_t now, uint32_t since, uint32_t interval) {
    return uint32_t(now - since) >= interval;
}
// Ancienne politique : blocs de données 4 à 62 sauf trailers. Elle est plus large que la garde active
// writableLabBlock, limitée strictement à 4.
inline bool writableF08Block(unsigned block) {
    return block >= 4 && block < 64 && block % 4 != 3;
}
// Filtre un booléen : un changement doit rester stable pendant delay millisecondes ; update ne signale
// que le passage stable à vrai.
class Debouncer {
    bool raw_ = false, stable_ = false;
    uint32_t changed_ = 0;
public:
    // value est la mesure brute et now le compteur de millisecondes. Le retour est une impulsion de
    // détection, tandis que state expose l’état mémorisé.
    bool update(bool value, uint32_t now, uint32_t delay = 30) {
        if (raw_ != value) { raw_ = value; changed_ = now; }
        if (raw_ != stable_ && elapsed(now, changed_, delay)) {
            stable_ = raw_;
            return stable_;
        }
        return false;
    }
    // Lire le dernier état stabilisé, distinct du résultat ponctuel de update.
    bool state() const { return stable_; }
};
// Ligne bornée pour les liaisons serie : une ligne trop longue est rejetee entiere.
// Capacité N incluant le zéro terminal ; N doit être strictement positif. Une ligne trop longue est
// abandonnée à son LF, sans exposer un préfixe tronqué.
template<size_t N> class LineBuffer {
    char data_[N] = {};
    size_t size_ = 0;
    bool overflow_ = false;
public:
    // Fournir les caractères un par un. Retourne vrai uniquement sur LF d’une ligne valide ; appeler clear
    // après consommation de value avant de commencer une nouvelle ligne.
    bool push(char c) {
        if (c == '\r') return false;
        if (c == '\n') {
            if (overflow_) { clear(); return false; }
            data_[size_] = 0;
            return true;
        }
        if (size_ + 1 < N && !overflow_) data_[size_++] = c;
        else overflow_ = true;
        return false;
    }
    // Pointeur vers le tampon interne ; ne pas le conserver au-delà d’un clear ou d’une nouvelle saisie.
    const char *value() const { return data_; }
    void clear() { size_ = 0; overflow_ = false; data_[0] = 0; }
};
}
