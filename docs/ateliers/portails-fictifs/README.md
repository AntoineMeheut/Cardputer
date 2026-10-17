# Trois maquettes de portails fictifs

Ouvrir [l'index](index.html) dans un navigateur, puis choisir :

- [Bureau Atelier](bureau-demo.html) : univers bureautique.
- [Banque Atelier](banque-demo.html) : univers bancaire.
- [Rail Atelier](rail-demo.html) : univers Wi-Fi ferroviaire.

Ces maquettes sont des alternatives pédagogiques aux pages d'imitation de marques. Elles ne représentent ni Microsoft, ni la Banque de France, ni la SNCF. Le bandeau « SIMULATION PÉDAGOGIQUE · SITE FICTIF » reste visible dès l'ouverture.

## Utilisation

Chaque page est un fichier HTML autonome, avec styles intégrés. Elle fonctionne hors ligne : ouvrir le fichier directement sur ordinateur ou téléphone. Le lien « Simuler » déplie une explication locale et peut être refermé. Les valeurs de test sont fixes et affichées comme exemples ; aucun identifiant réel n'est demandé.

Les pages n'emploient ni formulaire, ni champ de saisie, ni script, ni cookie, ni stockage local, ni ressource distante. La politique de contenu interdit les soumissions de formulaires et les connexions de scripts. Il n'y a aucun serveur de collecte.

Ces fichiers ne sont pas raccordés au moteur de collecte d'un firmware Evil Portal. Ils ne fournissent pas de portail captif opérationnel ni de connexion Wi-Fi. Les archives originales tierces restent intactes dans `upstream/archives/` ; les commentaires français des sources extraites sont tracés séparément. Le parcours explique les concepts avec des participants informés, sans recueillir leurs secrets.

## Vérification

Rendu contrôlé sur navigateur Chromium aux formats bureau et téléphone. Le dépliage de l'explication, l'absence de champs et l'absence de requêtes secondaires sont vérifiés. Aucun déploiement ou essai sur Cardputer n'est effectué pour ces pages.

## Lire et modifier le code

`index.html` relie les trois univers ; chaque autre fichier contient son propre style et son contenu. Les variables CSS de `:root` règlent les couleurs ; `.layout` passe à une colonne sous 850 px. Le composant HTML natif `details/summary` ouvre le résultat sans JavaScript. Les valeurs sont des descriptions `dl/dt/dd`, pas des champs de formulaire.

Après modification, ouvrir les pages en large et en étroit, suivre les liens et utiliser le clavier pour ouvrir le panneau. Conserver les mentions fictives, l’attribution pédagogique et l’absence de collecte. Les commentaires internes précisent ces choix au voisinage du code concerné.
