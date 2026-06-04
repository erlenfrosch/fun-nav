# Spec: GraphHopper Custom Model für Kurvigkeits-Modi

**Issue:** #5  
**Branch:** agent/issue-5  
**Datum:** 2026-06-02

## Problem

Der Routing-Dienst verwendet bisher nur statische GraphHopper-Profile (car/bike/foot
mit `weighting: fastest`). Es gibt keine Möglichkeit, die Route nach dem Grad der
Kurvigkeit zu optimieren — z. B. für Motorrad- oder Fahrradfahrer, die bewusst kurvenreiche
Strecken bevorzugen, oder Pendler, die möglichst direkte Wege wollen.

## Lösung

GraphHopper bietet `curvature` als encoded value:
- `curvature = beeline_distance / edge_distance` (Wertebereich 0..1)
- **Kurvig** = niedriger Wert (Luftlinie ≪ tatsächliche Streckenlänge)
- **Gerade** = hoher Wert (Luftlinie ≈ Streckenlänge)

Über das Custom-Model-Feature (POST /route mit `custom_model`) lässt sich die
Priorität kurviger Straßen dynamisch anpassen.

### Drei Routing-Modi

| Modus | Beschreibung | Custom Model |
|---|---|---|
| `fastest` | Schnellste Route (Standard) | keins |
| `kurvig` | Bevorzugt kurvenreiche Straßen | Priorität bei niedrigem `curvature` erhöhen |
| `direkt` | Meidet Kurven, direkter Weg | Priorität bei niedrigem `curvature` senken |

### Custom Model – `kurvig`

```json
{
  "priority": [
    {"if": "curvature < 0.3", "multiply_by": "3.0"},
    {"else_if": "curvature < 0.6", "multiply_by": "2.0"}
  ],
  "distance_influence": 50
}
```

### Custom Model – `direkt`

```json
{
  "priority": [
    {"if": "curvature < 0.3", "multiply_by": "0.1"},
    {"else_if": "curvature < 0.6", "multiply_by": "0.5"}
  ],
  "distance_influence": 0
}
```

## Architektur

```
Frontend → POST /route → Backend → POST /route → GraphHopper
                         ↑ baut custom_model aus Mode
```

### GraphHopper Config

Neue `custom`-Profile neben den bestehenden `fastest`-Profilen:

```yaml
- name: car_custom
  vehicle: car
  weighting: custom
  custom_model_files: []
- name: bike_custom
  vehicle: bike
  weighting: custom
  custom_model_files: []
```

`custom_model_files: []` ermöglicht per-Request Custom Models via POST /route.

### Backend API

```
POST /route
Content-Type: application/json

{
  "points": [[lon1, lat1], [lon2, lat2]],
  "profile": "car" | "bike" | "foot",
  "mode": "fastest" | "kurvig" | "direkt"
}
```

Response: Direkte GraphHopper-Antwort (paths, time, distance, encoded polyline).

## Akzeptanzkriterien

1. `POST /route` mit `mode=fastest` liefert eine Route ohne custom_model
2. `POST /route` mit `mode=kurvig` liefert eine Route mit Kurvigkeits-Boost
3. `POST /route` mit `mode=direkt` liefert eine Route mit Kurvigkeits-Malus
4. Ungültige Profile oder Modi werden mit HTTP 422 abgelehnt
5. GraphHopper-Fehler werden mit HTTP 502 weitergegeben
6. Alle Pfade haben Tests (pytest, TestClient mit gemocktem httpx)

## Recherche-Quellen

- [GraphHopper Custom Models Docs](https://github.com/graphhopper/graphhopper/blob/master/docs/core/custom-models.md)
- [Road Attributes (curvature)](https://docs.graphhopper.com/openapi/custom-model/road-attributes)
- [Forum: Curvature Settings](https://discuss.graphhopper.com/t/help-on-curvature-settings-in-custom-model/9885)
