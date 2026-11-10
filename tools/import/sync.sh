#!/usr/bin/env bash
# Stiahne aktuálny obsah z pôvodného webu obce a prenesie ho do nového webu.
set -euo pipefail
cd "$(dirname "$0")/../.."
TMP=$(mktemp -d)
curl -sSfL -A 'Mozilla/5.0' -o "$TMP/index.html" https://www.mostpribratislave.sk/
curl -sSfL -A 'Mozilla/5.0' -o "$TMP/kalendar.html" https://www.mostpribratislave.sk/kalendar
python3 tools/import/crawl.py "$TMP/index.html" "$TMP/data"
python3 tools/import/crawl_subpages.py "$TMP/index.html" "$TMP/data"
python3 tools/import/import.py "$TMP/data" "$TMP/kalendar.html" .
python3 tools/import/gallery.py . || echo "Fotogaléria sa nepodarila aktualizovať"
python3 tools/import/podnety.py . 3 || echo "Podnety sa nepodarilo aktualizovať"
rm -rf "$TMP"
