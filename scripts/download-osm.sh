#!/usr/bin/env bash
set -euo pipefail

TARGET="graphhopper/data/map.osm.pbf"
REGION="${OSM_REGION:-dach}"

case "$REGION" in
  dach)
    URL="https://download.geofabrik.de/europe/dach-latest.osm.pbf"
    SIZE="~3.6 GB"
    ;;
  germany)
    URL="https://download.geofabrik.de/europe/germany-latest.osm.pbf"
    SIZE="~4 GB"
    ;;
  austria)
    URL="https://download.geofabrik.de/europe/austria-latest.osm.pbf"
    SIZE="~600 MB"
    ;;
  switzerland)
    URL="https://download.geofabrik.de/europe/switzerland-latest.osm.pbf"
    SIZE="~400 MB"
    ;;
  test|liechtenstein)
    URL="https://download.geofabrik.de/europe/liechtenstein-latest.osm.pbf"
    SIZE="~1 MB"
    ;;
  *)
    echo "Unbekannte Region: $REGION" >&2
    echo "Gültige Werte: dach, germany, austria, switzerland, test" >&2
    exit 1
    ;;
esac

if [ -f "$TARGET" ]; then
  echo "OSM-Datei bereits vorhanden: $TARGET"
  exit 0
fi

echo "Lade OSM-Daten für Region '$REGION' ($SIZE)..."
curl -L --progress-bar -o "$TARGET" "$URL"
echo "Fertig: $TARGET"
