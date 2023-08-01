from fastapi.testclient import TestClient
import tests.testutil as utils


def test_get_all_segments_rule(client: TestClient):
    assert client.get("/segments/rules").status_code == 200
