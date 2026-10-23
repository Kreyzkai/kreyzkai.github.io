#!/usr/bin/env bash
# Rebuild the two downloadable packs for project 028 from the files in this folder.
# Run from anywhere:  bash "028 IELTS Academic Quest/build-packs.sh"
# Keeps the ZIPs in sync with the app + MP3s + PDFs, so they can never drift.
set -euo pipefail

cd "$(dirname "$0")"

APP="028 IELTS Academic Quest.html"
MP3S=(028-script-*.mp3)
PDFS=(IELTS\ Quest\ *.pdf)

for f in "$APP" "${MP3S[@]}" "${PDFS[@]}" README-OFFLINE.txt README-Print-Pack.md; do
    [ -f "$f" ] || { echo "MISSING: $f" >&2; exit 1; }
done

rm -f "028 IELTS Quest Print Pack.zip" "028 IELTS Offline Study Pack.zip"

# 1. Print pack: readme + the 5 A4 PDFs
zip -q -X "028 IELTS Quest Print Pack.zip" README-Print-Pack.md "${PDFS[@]}"

# 2. Offline pack: readme + app + all audio + all PDFs
zip -q -X "028 IELTS Offline Study Pack.zip" README-OFFLINE.txt "$APP" "${MP3S[@]}" "${PDFS[@]}"

echo "Rebuilt:"
unzip -l "028 IELTS Quest Print Pack.zip"    | tail -2
unzip -l "028 IELTS Offline Study Pack.zip"  | tail -2
