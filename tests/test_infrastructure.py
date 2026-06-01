import yaml
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _load_yaml(path):
    with open(ROOT / path) as f:
        return yaml.safe_load(f)


def _read_script(path):
    return (ROOT / path).read_text()


class TestGraphHopperConfig:
    def test_car_profile_exists(self):
        cfg = _load_yaml("graphhopper/config.yml")
        names = [p["name"] for p in cfg["graphhopper"]["profiles"]]
        assert "car" in names

    def test_car_custom_profile_exists(self):
        cfg = _load_yaml("graphhopper/config.yml")
        names = [p["name"] for p in cfg["graphhopper"]["profiles"]]
        assert "car_custom" in names

    def test_car_custom_profile_uses_custom_weighting(self):
        cfg = _load_yaml("graphhopper/config.yml")
        car_custom = next(
            p for p in cfg["graphhopper"]["profiles"] if p["name"] == "car_custom"
        )
        assert car_custom["weighting"] == "custom"

    def test_car_custom_profile_has_custom_model(self):
        cfg = _load_yaml("graphhopper/config.yml")
        car_custom = next(
            p for p in cfg["graphhopper"]["profiles"] if p["name"] == "car_custom"
        )
        assert "custom_model" in car_custom

    def test_lm_profile_for_car_custom(self):
        cfg = _load_yaml("graphhopper/config.yml")
        lm_profiles = [p["profile"] for p in cfg["graphhopper"].get("profiles_lm", [])]
        assert "car_custom" in lm_profiles


class TestDockerCompose:
    def test_graphhopper_image_is_latest(self):
        cfg = _load_yaml("docker-compose.yml")
        image = cfg["services"]["graphhopper"]["image"]
        assert image == "graphhopper/graphhopper:latest"

    def test_graphhopper_has_healthcheck(self):
        cfg = _load_yaml("docker-compose.yml")
        assert "healthcheck" in cfg["services"]["graphhopper"]

    def test_healthcheck_tests_health_endpoint(self):
        cfg = _load_yaml("docker-compose.yml")
        test_cmd = cfg["services"]["graphhopper"]["healthcheck"]["test"]
        cmd_str = " ".join(test_cmd) if isinstance(test_cmd, list) else test_cmd
        assert "8989" in cmd_str
        assert "health" in cmd_str

    def test_healthcheck_has_start_period(self):
        cfg = _load_yaml("docker-compose.yml")
        hc = cfg["services"]["graphhopper"]["healthcheck"]
        assert "start_period" in hc

    def test_backend_depends_on_graphhopper_healthy(self):
        cfg = _load_yaml("docker-compose.yml")
        depends = cfg["services"]["backend"]["depends_on"]
        if isinstance(depends, dict):
            assert depends.get("graphhopper", {}).get("condition") == "service_healthy"
        else:
            pytest.fail("depends_on should be a dict with condition")


class TestDownloadScript:
    def test_dach_url_present(self):
        script = _read_script("scripts/download-osm.sh")
        assert "geofabrik.de" in script
        assert "dach" in script.lower()

    def test_liechtenstein_still_available_as_test(self):
        script = _read_script("scripts/download-osm.sh")
        assert "liechtenstein" in script.lower()

    def test_target_file_is_map_osm_pbf(self):
        script = _read_script("scripts/download-osm.sh")
        assert "map.osm.pbf" in script
