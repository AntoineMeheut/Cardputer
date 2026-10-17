# En-têtes de CardputerLab

Lire d’abord le [guide de la bibliothèque](../README.md). Les fonctions sont `inline` pour être incluses dans les différents programmes sans fichier objet propre à la bibliothèque.

| API active | Contrat / résultat |
|---|---|
| `Lab::begin(title)` | Initialiser carte, USB série et écran ; appeler une seule fois dans `setup`. |
| `body()` / `line(text)` | Effacer le contenu puis écrire une ligne à l’écran et sur la console. |
| `pressed(key)` / `enter()` | Tester un nouvel événement après `M5Cardputer.update()`. |
| `sdBegin()` | Monter la carte ; vérifier le booléen avant toute opération de fichier. |
| `nextFile(prefix, extension)` | Chercher de 0 à 9999 ; chaîne vide si tous les noms existent. |
| `i2cBegin()` / `i2cPresent(address)` | Initialiser à 100 kHz puis chercher un ACK ; pas d’identification du module. |
| `put16` / `put32` | Écrire 2 ou 4 octets little-endian dans un tampon suffisamment grand. |
| `wavHeader` | Écrire 44 octets RIFF/WAV ; `dataSize` compte des octets, `rate` des échantillons/s. |
| `writableLabBlock(block)` | Retourner vrai uniquement pour 4. |
| `decodePacket(data, length, out)` | Valider les octets avant d’utiliser `out` ; taille et ABI doivent correspondre aux deux cartes. |

## Anciennes variantes

[Lab.h](Lab.h) gère une seule touche par événement et intercepte `!`. [lab_logic.h](lab_logic.h) expose `lab::elapsed`, `writableF08Block`, `Debouncer` et `LineBuffer<N>`.

`Debouncer.update(value, now, delay)` signale uniquement un front stable vers vrai ; `state()` lit le niveau filtré. `LineBuffer<N>` doit avoir `N > 0`, inclut le zéro final dans sa capacité, ignore CR et termine sur LF. Consommer `value()` puis appeler `clear()` après un retour vrai. Une ligne trop longue est rejetée entièrement à sa fin.

Ces variantes sont décrites pour étude ; elles ne sont pas couvertes automatiquement par les vingt compilations actives. Les tests [test_formats.cpp](../../../tests/test_formats.cpp) visent `LabFormats.h`.
