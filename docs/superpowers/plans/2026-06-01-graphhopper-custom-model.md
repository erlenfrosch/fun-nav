# Plan: GraphHopper Custom Model für Kurvigkeits-Modi

**Issue:** #5  
**Spec:** docs/superpowers/specs/2026-06-01-graphhopper-custom-model-design.md  
**Datum:** 2026-06-01

## Recherche-Quellen

- GraphHopper Custom Model Docs: https://docs.graphhopper.com/openapi/custom-model
- GraphHopper Forum – Curvature v5: https://discuss.graphhopper.com/t/setting-curvature-in-v5/7360
- GraphHopper Forum – Curvature Help: https://discuss.graphhopper.com/t/help-on-curvature-settings-in-custom-model/9885
- GH custom-models.md (GitHub): https://raw.githubusercontent.com/graphhopper/graphhopper/master/docs/core/custom-models.md

## Aufgaben

- [ ] `graphhopper/config.yml`: motorcycle-Profil mit `weighting: custom` hinzufügen
- [ ] `backend/app/services/__init__.py`: leeres Init
- [ ] `backend/tests/__init__.py`: leeres Init
- [ ] `backend/requirements.txt`: `pytest` und `respx` ergänzen
- [ ] `backend/tests/test_graphhopper_service.py`: Tests schreiben (RED)
- [ ] `backend/app/services/graphhopper.py`: Service implementieren (GREEN)
- [ ] Tests lokal ausführen, alle grün
- [ ] Commit + Push + PR erstellen

## Entscheidungen

- motorcycle-Profil hat `curvature` Encoded Value ohne zusätzliche Konfiguration
- `profiles_ch` bleibt unverändert (nur `car`) — motorcycle braucht kein CH
- `custom_model: {priority: []}` im config.yml als leeres Default-Modell
- Service-Funktion `get_route(start, end, mode)` mit `mode: Literal["kurvenreich", "sehr_kurvenreich"]`
- `GRAPHHOPPER_URL` als Konstante (Docker Compose Service-Name `graphhopper`)
- Details-Request mit `["road_class", "curvature"]` für spätere Frontend-Auswertung
