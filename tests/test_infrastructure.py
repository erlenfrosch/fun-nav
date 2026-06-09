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
    def test_auto_profile_exists(self):
        cfg = _load_yaml("graphhopper/config.yml")
        names = [p["name"] for p in cfg["graphhopper"]["profiles"]]
        assert "auto" in names

    def test_auto_profile_has_custom_model_files(self):
        cfg = _load_yaml("graphhopper/config.yml")
        auto = next(p for p in cfg["graphhopper"]["profiles"] if p["name"] == "auto")
        assert "custom_model_files" in auto

    def test_graph_encoded_values_set(self):
        cfg = _load_yaml("graphhopper/config.yml")
        assert "graph.encoded_values" in cfg["graphhopper"]

    def test_lm_profile_for_auto(self):
        cfg = _load_yaml("graphhopper/config.yml")
        lm_profiles = [p["profile"] for p in cfg["graphhopper"].get("profiles_lm", [])]
        assert "auto" in lm_profiles


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
