# Automatisation GitHub

Le [workflow](workflows/README.md) décrit les contrôles lors d’un push ou d’une proposition de modification. Ce répertoire configure GitHub Actions ; il n’est pas téléversé dans le Cardputer.

Les [modèles d’issue](ISSUE_TEMPLATE/README.md) et le [modèle de pull request](pull_request_template.md) demandent les informations utiles à une contribution. Le [guide de publication](../docs/publication/README.md) explique la première mise en ligne manuelle.

Les mêmes étapes peuvent être exécutées localement depuis la racine : `python tools/check_docs.py`, `python tools/test_host.py`, `python tools/fetch_upstream.py --verify` puis `python tools/build_all.py`.
