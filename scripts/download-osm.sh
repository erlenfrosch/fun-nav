#!/usr/bin/env bash
set -euo pipefail

TARGET="graphhopper/data/map.osm.pbf"
URL="https://download.geofabrik.de/europe/liechtenstein-latest.osm.pbf"

if [ -f "$TARGET" ]; then
  echo "OSM-Datei bereits vorhanden: $TARGET"
  exit 0
fi

echo "Lade OSM-Testdaten (Liechtenstein, ~1 MB)..."
curl -L -o "$TARGET" "$URL"
echo "Fertig: $TARGET"
