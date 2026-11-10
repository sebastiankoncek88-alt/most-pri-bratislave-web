#!/usr/bin/env bash
# Stiahne aktuálny obsah z pôvodného webu obce a prenesie ho do nového webu.
# Poistka: ak sa stiahne podozrivo málo obsahu (starý web nedostupný), nič sa neprepíše.
set -euo pipefail
cd "$(dirname "$0")/../.."
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
curl -sSfL --retry 3 -A 'Mozilla/5.0' -o "$TMP/index.html" https://www.mostpribratislave.sk/
curl -sSfL --retry 3 -A 'Mozilla/5.0' -o "$TMP/kalendar.html" https://www.mostpribratislave.sk/kalendar
python3 tools/import/crawl.py "$TMP/index.html" "$TMP/data"
python3 tools/import/crawl_subpages.py "$TMP/index.html" "$TMP/data"
python3 - "$TMP/data" <<'PY'
import json, sys
p = len(json.load(open(sys.argv[1] + '/pages.json')))
n = len(json.load(open(sys.argv[1] + '/news.json')))
print(f'stiahnuté: {p} stránok, {n} noviniek')
if p < 120 or n < 15:
    sys.exit('Príliš málo obsahu – starý web je asi nedostupný. Synchronizácia sa preskočila, nič sa neprepísalo.')
PY
python3 tools/import/import.py "$TMP/data" "$TMP/kalendar.html" .
python3 tools/import/gallery.py . || echo "Fotogaléria sa nepodarila aktualizovať"
python3 tools/import/podnety.py . 1 || echo "Podnety sa nepodarilo aktualizovať"
