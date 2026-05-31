#!/usr/bin/env bash
set -euo pipefail

REGION="${REGION:-liechtenstein}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --region) REGION="$2"; shift 2 ;;
    *) echo "Unbekannte Option: $1" >&2; exit 1 ;;
  esac
done

declare -A REGIONS=(
  [liechtenstein]="europe/liechtenstein-latest.osm.pbf|~1 MB"
  [switzerland]="europe/switzerland-latest.osm.pbf|~507 MB"
  [austria]="europe/austria-latest.osm.pbf|~763 MB"
  [dach]="europe/dach-latest.osm.pbf|~5.7 GB"
  [germany]="europe/germany-latest.osm.pbf|~4.4 GB"
)

if [[ -z "${REGIONS[$REGION]+set}" ]]; then
  echo "Unbekannte Region: $REGION" >&2
  echo "Verfügbar: ${!REGIONS[*]}" >&2
  exit 1
fi

IFS="|" read -r path size <<< "${REGIONS[$REGION]}"

TARGET="graphhopper/data/map.osm.pbf"
URL="https://download.geofabrik.de/${path}"

if [ -f "$TARGET" ]; then
  echo "OSM-Datei bereits vorhanden: $TARGET"
  exit 0
fi

echo "Lade OSM-Daten: ${REGION} (${size})..."
echo "URL: $URL"
curl -L --progress-bar -o "$TARGET" "$URL"
echo "Fertig: $TARGET"
