#!/usr/bin/env bash
set -euo pipefail

REGION="${1:-liechtenstein}"
TARGET="graphhopper/data/map.osm.pbf"

case "$REGION" in
  liechtenstein)
    URL="https://download.geofabrik.de/europe/liechtenstein-latest.osm.pbf"
    LABEL="Liechtenstein (~1 MB)"
    ;;
  dach)
    URL="https://download.geofabrik.de/europe/dach-latest.osm.pbf"
    LABEL="DACH – Deutschland, Österreich, Schweiz (~5.7 GB)"
    ;;
  *)
    echo "Fehler: Unbekannte Region '${REGION}'. Gültige Werte: liechtenstein, dach" >&2
    exit 1
    ;;
esac

if [ -f "$TARGET" ]; then
  echo "OSM-Datei bereits vorhanden: $TARGET"
  exit 0
fi

echo "Lade OSM-Daten: ${LABEL}..."
curl -L -o "$TARGET" "$URL"
echo "Fertig: $TARGET"
