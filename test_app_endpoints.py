"""
Integration tests for Flask routes using Flask's test_client
"""

from app import app
import json


def test_flask_app():
    client = app.test_client()

    print("=" * 60)
    print("TESTING FLASK APPLICATION ROUTES & ENDPOINTS")
    print("=" * 60)

    # 1. Test GET /
    res_home = client.get("/")
    print(f"GET / -> Status {res_home.status_code}")
    assert res_home.status_code == 200, "Home route failed"
    assert b"GrammarGuard" in res_home.data, "Home page content missing"

    # 2. Test GET /api/samples
    res_samples = client.get("/api/samples")
    print(f"GET /api/samples -> Status {res_samples.status_code}")
    assert res_samples.status_code == 200
    samples_data = json.loads(res_samples.data)
    assert len(samples_data["samples"]) > 0

    # 3. Test POST /check with empty input
    res_empty = client.post("/check", json={"sentence": ""})
    print(f"POST /check (empty) -> Status {res_empty.status_code}")
    assert res_empty.status_code == 400
    empty_data = json.loads(res_empty.data)
    assert empty_data["success"] is False

    # 4. Test POST /check with erroneous sentence
    test_sentence = "He go to school with a apple in the the morning."
    res_check = client.post("/check", json={"sentence": test_sentence})
    print(f"POST /check ('{test_sentence}') -> Status {res_check.status_code}")
    assert res_check.status_code == 200
    check_data = json.loads(res_check.data)
    assert check_data["success"] is True
    assert check_data["total_errors"] >= 3
    print(f"  Detected {check_data['total_errors']} errors:")
    for err in check_data["errors"]:
        print(f"  - [{err['rule']}] {err['found']} -> {err['replacement']}")
    print(f"  Corrected: '{check_data['corrected_sentence']}'")

    # 5. Test POST /check with clean sentence
    clean_sentence = "The student completed the assignment diligently."
    res_clean = client.post("/check", json={"sentence": clean_sentence})
    print(f"\nPOST /check ('{clean_sentence}') -> Status {res_clean.status_code}")
    assert res_clean.status_code == 200
    clean_data = json.loads(res_clean.data)
    assert clean_data["total_errors"] == 0
    print("  0 errors detected as expected.")

    print("\nALL FLASK INTEGRATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_flask_app()
