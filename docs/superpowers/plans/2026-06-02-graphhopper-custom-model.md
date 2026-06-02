# Plan: GraphHopper Custom Model für Kurvigkeits-Modi

**Issue:** #5  
**Spec:** docs/superpowers/specs/2026-06-02-graphhopper-custom-model-design.md  
**Branch:** agent/issue-5  
**Datum:** 2026-06-02

## Recherche-Quellen

- [Custom Models Docs](https://github.com/graphhopper/graphhopper/blob/master/docs/core/custom-models.md)
- [Road Attributes: curvature](https://docs.graphhopper.com/openapi/custom-model/road-attributes)
- GraphHopper 7 config-example.yml: custom_model_files: []

## Aufgaben

- [x] Branch `agent/issue-5` anlegen
- [x] Spec schreiben
- [x] Plan schreiben
- [ ] `graphhopper/config.yml` — car_custom + bike_custom Profile ergänzen
- [ ] `backend/requirements.txt` — pytest + pytest-asyncio hinzufügen
- [ ] `backend/tests/__init__.py` anlegen
- [ ] `backend/tests/test_routing.py` — Tests schreiben (TDD: erst Tests, dann Impl.)
- [ ] `backend/app/routing.py` — Custom-Model-Logik + GH-API-Call
- [ ] `backend/app/main.py` — POST /route Endpoint verdrahten
- [ ] Alle Tests grün
- [ ] Commit
- [ ] PR öffnen (Closes #5)

## Entscheidungen

- Profile `car_custom` / `bike_custom` mit `weighting: custom` und `custom_model_files: []`
  → ermöglicht per-Request Custom Model ohne statische JSON-Datei
- `foot`-Profil bekommt kein `_custom`-Gegenstück (Fußgänger profitieren nicht von Kurvigkeit)
- `fastest`-Modus verwendet Original-Profile (kein `ch.disable: true` nötig, CH-Cache nutzbar)
- `kurvig`/`direkt` verwenden `*_custom`-Profile + `ch.disable: true`
- Backend gibt die rohe GraphHopper-Antwort durch — keine eigene Datenmodellierung jetzt
- Fehler von GraphHopper (non-2xx) werden als HTTP 502 an den Client weitergeleitet
