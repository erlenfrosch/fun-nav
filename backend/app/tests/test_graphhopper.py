from app.services.graphhopper import CURVY_MODEL, VERY_CURVY_MODEL


def _find_rule(rules: list[dict], keyword: str) -> dict | None:
    return next((r for r in rules if keyword in r["if"]), None)


def test_kurvenreich_curvature_regel():
    rule = _find_rule(CURVY_MODEL["priority"], "curvature")
    assert rule is not None
    assert "< 0.7" in rule["if"]
    assert rule["multiply_by"] == 1.5


def test_sehr_kurvenreich_curvature_regel():
    rule = _find_rule(VERY_CURVY_MODEL["priority"], "curvature")
    assert rule is not None
    assert "< 0.4" in rule["if"]
    assert rule["multiply_by"] == 3.0


def test_sehr_kurvenreich_hat_hoehere_gewichtung():
    """sehr_kurvenreich bevorzugt Kurvenstraßen stärker als kurvenreich."""
    k_boost = _find_rule(CURVY_MODEL["priority"], "curvature")["multiply_by"]
    sk_boost = _find_rule(VERY_CURVY_MODEL["priority"], "curvature")["multiply_by"]
    assert sk_boost > k_boost


def test_sehr_kurvenreich_hat_strengere_schwelle():
    """sehr_kurvenreich selektiert nur stärker gewundene Straßen."""
    k_threshold = float(_find_rule(CURVY_MODEL["priority"], "curvature")["if"].split("< ")[1])
    sk_threshold = float(_find_rule(VERY_CURVY_MODEL["priority"], "curvature")["if"].split("< ")[1])
    assert sk_threshold < k_threshold


def test_sehr_kurvenreich_bestraft_motorway_und_trunk():
    rule = _find_rule(VERY_CURVY_MODEL["priority"], "MOTORWAY")
    assert rule is not None
    assert "TRUNK" in rule["if"]
    assert rule["multiply_by"] == 0.05


def test_kurvenreich_bestraft_nur_motorway():
    rule = _find_rule(CURVY_MODEL["priority"], "MOTORWAY")
    assert rule is not None
    assert "TRUNK" not in rule["if"]
    assert rule["multiply_by"] == 0.1
