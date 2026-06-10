# Plan: FastAPI Backend Grundstruktur

**Issue:** #3  
**Spec:** docs/superpowers/specs/2026-06-04-fastapi-backend-struktur-design.md  
**Datum:** 2026-06-04

## Recherche-Quellen

- FastAPI Routing: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- GraphHopper Route API: https://docs.graphhopper.com/#operation/getRoute
- respx (httpx-Mocking): https://lundberg.github.io/respx/

## Datei-Struktur (Änderungen)

```
backend/
├── app/
│   ├── __init__.py          (vorhanden)
│   ├── main.py              (anpassen: Router einbinden)
│   ├── config.py            (neu: GRAPHHOPPER_URL aus env)
│   ├── schemas.py           (neu: RouteRequest, RouteResponse)
│   ├── graphhopper.py       (neu: async HTTP-Client)
│   └── routers/
│       ├── __init__.py      (neu)
│       └── route.py         (neu: POST /route)
├── tests/
│   ├── __init__.py          (neu)
│   ├── test_health.py       (neu)
│   └── test_route.py        (neu)
└── requirements.txt         (ergänzen: pytest, respx)
```

## Aufgaben (TDD-Reihenfolge)

- [x] Branch `agent/issue-3` anlegen
- [x] Spec schreiben
- [x] Plan schreiben
- [ ] `requirements.txt` um Test-Deps ergänzen
- [ ] `tests/` + Tests schreiben (schlagen zunächst fehl)
- [ ] `app/config.py` implementieren
- [ ] `app/schemas.py` implementieren
- [ ] `app/graphhopper.py` implementieren
- [ ] `app/routers/__init__.py` + `app/routers/route.py` implementieren
- [ ] `app/main.py` aktualisieren
- [ ] Tests lokal grün
- [ ] Commit + Push + PR

## Entscheidungen

- **Config via `os.getenv`** statt `pydantic-settings` — weniger Dependency
- **`async with httpx.AsyncClient()`** in graphhopper.py — konsistent mit FastAPI async
- **`respx`** für httpx-Mocking in Tests — passt zu httpx, kein Monkey-Patching
- **POST für `/route`** statt GET — Koordinaten als Body klarer als Query-Params
