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
  [switzerland]="europe/switzerland-latest.osm.pbf|~360 MB"
  [austria]="europe/austria-latest.osm.pbf|~740 MB"
  [dach]="europe/dach-latest.osm.pbf|~800 MB"
  [germany]="europe/germany-latest.osm.pbf|~3.7 GB"
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
