# Plan: GraphHopper Custom Model für Kurvigkeits-Modi

**Spec:** docs/superpowers/specs/2026-05-31-graphhopper-custom-model-design.md  
**Issue:** #5  
**Branch:** agent/issue-5

## Quellen

- GraphHopper Custom Model API: https://docs.graphhopper.com/#section/Map-Data-and-Routing-Profiles/OpenStreetMap/Customized-Routing-Profiles
- Curvature-Variable (0–1): https://discuss.graphhopper.com/t/setting-curvature-in-v5/7360

## Schritte

### 1. graphhopper/config.yml

Profil `bike_custom` hinzufügen (nach bestehenden Profilen):
```yaml
- name: bike_custom
  vehicle: bike
  weighting: custom
  custom_model_files: []
```
Kein CH-Eintrag für `bike_custom` (custom_model_files: [] ist mit CH inkompatibel).

### 2. backend/app/services/ anlegen

- `backend/app/services/__init__.py` (leer)
- `backend/app/services/graphhopper.py`:
  - Konstante `CUSTOM_MODELS` mit beiden Modi
  - Async-Funktion `route_curvy(start, end, mode, base_url)`
  - `base_url` aus Env `GRAPHHOPPER_URL`, Default `http://graphhopper:8989`
  - Validierung: ValueError bei unbekanntem Modus
  - GH erwartet Punkte als `[lon, lat]` (nicht lat/lon)

### 3. backend/requirements.txt

Hinzufügen:
```
pytest==8.3.4
pytest-asyncio==0.24.0
respx==0.21.1
```

### 4. backend/tests/ anlegen

- `backend/tests/__init__.py` (leer)
- `backend/tests/test_graphhopper_service.py`:
  - `test_route_curvy_sendet_kurvenreich_custom_model`
  - `test_route_curvy_sendet_sehr_kurvenreich_custom_model`
  - `test_sehr_kurvenreich_hat_striktere_schwelle_als_kurvenreich`
  - `test_unbekannter_modus_wirft_valueerror`

### 5. Commit & PR

Commit auf Branch `agent/issue-5`, PR mit "Closes #5".
