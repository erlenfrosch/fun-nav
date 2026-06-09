#!/usr/bin/env bash
# Infrastructure tests — run from repo root
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0

ok()   { echo "PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }

# ---- graphhopper/config.yml ------------------------------------------------

CONFIG="$ROOT/graphhopper/config.yml"

grep -q "name: auto" "$CONFIG" \
  && ok "config: auto profile exists" \
  || fail "config: auto profile exists"

grep -A2 "name: auto" "$CONFIG" | grep -q "custom_model_files" \
  && ok "config: auto profile has custom_model_files" \
  || fail "config: auto profile has custom_model_files"

grep -q "profiles_lm" "$CONFIG" \
  && ok "config: profiles_lm section exists" \
  || fail "config: profiles_lm section exists"

grep -A3 "profiles_lm" "$CONFIG" | grep -q "auto" \
  && ok "config: auto in profiles_lm" \
  || fail "config: auto in profiles_lm"

grep -q "graph.encoded_values" "$CONFIG" \
  && ok "config: graph.encoded_values set" \
  || fail "config: graph.encoded_values set"

# ---- docker-compose.yml ----------------------------------------------------

COMPOSE="$ROOT/docker-compose.yml"

grep -q "graphhopper/graphhopper:latest" "$COMPOSE" \
  && ok "compose: image is graphhopper/graphhopper:latest" \
  || fail "compose: image is graphhopper/graphhopper:latest"

grep -q "healthcheck" "$COMPOSE" \
  && ok "compose: healthcheck defined" \
  || fail "compose: healthcheck defined"

grep -q "8989" "$COMPOSE" && grep -q "health" "$COMPOSE" \
  && ok "compose: healthcheck targets port 8989 /health" \
  || fail "compose: healthcheck targets port 8989 /health"

grep -q "start_period" "$COMPOSE" \
  && ok "compose: healthcheck has start_period" \
  || fail "compose: healthcheck has start_period"

grep -q "service_healthy" "$COMPOSE" \
  && ok "compose: backend depends_on service_healthy" \
  || fail "compose: backend depends_on service_healthy"

# ---- scripts/download-osm.sh -----------------------------------------------

SCRIPT="$ROOT/scripts/download-osm.sh"

grep -qi "geofabrik.de" "$SCRIPT" \
  && ok "script: Geofabrik URL present" \
  || fail "script: Geofabrik URL present"

grep -qi "dach" "$SCRIPT" \
  && ok "script: DACH region configured" \
  || fail "script: DACH region configured"

grep -qi "liechtenstein" "$SCRIPT" \
  && ok "script: Liechtenstein test option retained" \
  || fail "script: Liechtenstein test option retained"

grep -q "map.osm.pbf" "$SCRIPT" \
  && ok "script: target file is map.osm.pbf" \
  || fail "script: target file is map.osm.pbf"

# ---- Summary ---------------------------------------------------------------

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
