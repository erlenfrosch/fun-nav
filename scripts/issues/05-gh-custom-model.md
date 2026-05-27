## Beschreibung
GraphHopper Custom Models für beide Kurvigkeits-Modi implementieren und testen.

## Modi
**kurvenreich:**
```json
{"priority": [{"if": "curvature < 0.7", "multiply_by": 1.5}, {"if": "road_class == MOTORWAY", "multiply_by": 0.1}]}
```
**sehr kurvenreich:**
```json
{"priority": [{"if": "curvature < 0.4", "multiply_by": 3.0}, {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": 0.05}]}
```

## Aufgaben
- [ ] `graphhopper/config.yml` um Custom Model Support erweitern
- [ ] `backend/services/graphhopper.py`: HTTP Client für GH Routing API
- [ ] Unit-Tests: Route kurvenreich vs. sehr kurvenreich vergleichen (gleicher Start/Ziel)

## Quellen
- https://discuss.graphhopper.com/t/setting-curvature-in-v5/7360
- https://docs.graphhopper.com/openapi/map-data-and-routing-profiles/openstreetmap/customized-routing-profiles

## Akzeptanzkriterium
Test zeigt: sehr-kurvenreich Route hat messbar höheren Kurvenanteil als kurvenreich Route.
