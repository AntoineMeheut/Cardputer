# Preuves conservées pour la publication

Ces résultats datent du **17 octobre 2026**. Ils ont été copiés depuis les rapports locaux de préparation afin de rester accessibles après un clone. Après nettoyage, les journaux complets et les originaux locaux sont regroupés dans `output/sauvegardes/preparation-2026-10-17.zip`, une archive privée ignorée par Git.

| Fichier | Portée |
|---|---|
| [Compilation des programmes actifs](compilation-2026-10-17.json) | Succès des 20 environnements, après ajout des commentaires ; les chemins `log` désignent des journaux locaux non distribués. |
| [Comparaison des instructions](instructions-2026-10-17.json) | Comparaisons de tokens C/C++, d’AST Python et de contenu HTML ; outils de maintenance modifiés identifiés. |
| [Rapport initial du 10 octobre](../../validation-compilation.json) | Tailles et empreintes des binaires de la compilation initiale. |

Ces fichiers décrivent des exécutions locales datées. Ils ne constituent pas un résultat de GitHub Actions, ni un essai physique.

## Launcher

La commande `pio run -d upstream/sources/launcher -e m5stack-cardputer` a été tentée dans des répertoires de construction isolés. Elle s’arrête à l’installation de la plateforme pioarduino `55.03.39` : la résolution DNS de GitHub échoue dans l’environnement de préparation. La compilation proprement dite n’a pas commencé. Le journal brut reste local car il contient des chemins propres au poste.

Le [bilan documentaire](../README.md) décrit également la limite de syntaxe du fichier tiers CO2_SCD40 et les autres vérifications effectuées.
