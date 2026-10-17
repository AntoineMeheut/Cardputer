#!/usr/bin/env python3
# Compilation séquentielle des environnements ; aucune commande de téléversement. Voir README.md pour
# les commandes, les sorties et les prérequis.
"""Compile toutes les expériences et conserve un compte rendu JSON."""
import configparser
import datetime
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


# Lit les sections env: de platformio.ini et retourne un code non nul si au moins une compilation
# échoue.
def main():
    config = configparser.ConfigParser()
    config.read(ROOT / 'platformio.ini')
    # La configuration reste la source de vérité : aucun nom d’expérience n’est dupliqué dans ce script.
    environments = [name[4:] for name in config.sections() if name.startswith('env:')]
    output = ROOT / 'build'
    output.mkdir(exist_ok=True)
    results = []
    for env in environments:
        log = output / (env + '.log')
        # Chaque exécution remplace le journal de cette cible ; stdout et stderr sont conservés ensemble pour
        # le diagnostic.
        with log.open('w') as stream:
            # Employer le même interpréteur Python garantit l’utilisation du PlatformIO installé dans
            # l’environnement actif.
            run = subprocess.run([sys.executable, '-m', 'platformio', 'run', '-e', env],
                                 cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
        result = {'environment': env, 'success': run.returncode == 0, 'log': str(log.relative_to(ROOT))}
        results.append(result)
        print(f'{env}: {"OK" if result["success"] else "ECHEC"}', flush=True)
    # Le rapport indique explicitement hardware_tested=False : compiler ne prouve pas que le périphérique
    # fonctionne.
    report = {'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'hardware_tested': False, 'results': results}
    (output / 'compilation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return 0 if all(item['success'] for item in results) else 1


if __name__ == '__main__':
    sys.exit(main())
