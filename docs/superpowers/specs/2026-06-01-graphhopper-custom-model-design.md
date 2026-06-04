# Spec: GraphHopper Custom Model für Kurvigkeits-Modi

**Issue:** #5  
**Branch:** agent/issue-5  
**Datum:** 2026-06-01

## Ziel

Zwei Routing-Modi implementieren, die kurvige Straßen bevorzugen:
- **kurvenreich**: mäßige Bevorzugung kurvenreicher Straßen
- **sehr kurvenreich**: starke Bevorzugung sehr kurvenreicher Straßen

## Datenmodell

GraphHopper `curvature`-Encoded-Value: `beeline_distance / actual_distance` → Wertebereich 0..1.  
Niedriger Wert = mehr Kurven. Beispiel: `curvature = 0.3` → stark kurvig; `curvature = 0.9` → fast gerade.

## Custom Models

**kurvenreich:**
```json
{"priority": [{"if": "curvature < 0.7", "multiply_by": 1.5}, {"if": "road_class == MOTORWAY", "multiply_by": 0.1}]}
```

**sehr kurvenreich:**
```json
{"priority": [{"if": "curvature < 0.4", "multiply_by": 3.0}, {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": 0.05}]}
```

## Komponenten

| Komponente | Datei | Verantwortung |
|---|---|---|
| GH Config | `graphhopper/config.yml` | Motorcycle-Profil + Custom Model Support |
| Service | `backend/app/services/graphhopper.py` | HTTP Client für POST /route |
| Tests | `backend/tests/test_graphhopper_service.py` | Unit-Tests + Akzeptanzkriterium |

## Akzeptanzkriterium

Unit-Test zeigt: bei gleichem Start/Ziel hat die sehr-kurvenreich-Route einen messbar niedrigeren durchschnittlichen `curvature`-Wert (= mehr Kurven) als die kurvenreich-Route.

## Entscheidungen

- **Profil: motorcycle** — hat `curvature` als Encoded Value; passt zum Use Case (Motorradtouren)
- **Kein CH für motorcycle-Profil** — CH ist inkompatibel mit dynamischen Custom Models
- **`ch.disable: true` per Request** — GH v7 Anforderung für Custom Models
- **httpx** — bereits in requirements.txt, synchroner Client für Backend-Service
- **respx** — httpx-kompatibler Mock für Unit-Tests (keine echte GH-Instanz nötig)
