# Identité visuelle de Cardputer Lab

La [bannière du README](cardputer-lab.svg) associe un titre massif blanc, du rose électrique, un fond presque noir et des annotations vert phosphore. La référence de direction artistique est la typographie cinématographique d’*Atomic Blonde*, notamment les cartons et le générique présentés par [Art of the Title](https://www.artofthetitle.com/title/atomic-blonde/). Le dessin et la composition sont propres à Cardputer Lab ; aucun photogramme, logo du film ou fichier de police n’est intégré.

| Élément | Valeur |
|---|---|
| Fond | `#090A0E` |
| Titre clair | `#F5F2E9` |
| Accent rose | `#FF2C86` |
| Annotations de terminal | `#A5FFB4` |
| Dimensions | 1 600 × 700, SVG vectoriel |
| Typographie de création | Impact et Courier New Bold, installées sur le poste de création |

Le Markdown GitHub ne permet pas d’imposer la police de toute la page. La bannière porte donc la composition typographique et convertit ses lettres en tracés ; les paragraphes restent du texte accessible et sélectionnable. Le SVG ne charge aucune ressource externe, n’exécute aucun script et n’utilise aucune animation. Son texte de remplacement figure dans le README.

## Régénérer

Depuis la racine, avec les dépendances facultatives du [générateur PDF](../../../tools/guide_pdf/README.md) installées :

```sh
python tools/build_branding.py
# Sur un autre système : fournir des polices installées localement.
python tools/build_branding.py --title-font /chemin/titre.ttf --mono-font /chemin/mono.ttf
```

Le script [build_branding.py](../../../tools/build_branding.py) contient les textes, couleurs et formes. Le SVG livré s’affiche sans installer ces polices. Il suffit de modifier le script puis de régénérer pour changer les nombres ou le titre. Cette illustration relève de la licence des créations originales du laboratoire.
