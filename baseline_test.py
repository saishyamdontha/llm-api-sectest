"""Scripted baseline. Each test ASSERTS the weakness is absent: FAIL = weakness present.
Local app only (see conftest.py)."""
import uuid, requests

def _reg(base):
    u = {"name": "t", "email": f"{uuid.uuid4().hex}@e.com", "phone": "1",
         "password": "pw", "walletAddress": "0x" + uuid.uuid4().hex[:40],
         "uniqueId": uuid.uuid4().hex}
    r = requests.post(f"{base}/api/auth/register", json=u, timeout=10)
    assert r.status_code in (200, 201), f"SETUP FAILED: register -> {r.status_code} {r.text[:200]}"
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    u["id"] = body.get("id")
    return u

def test_W1_requires_auth(base):
    r = requests.get(f"{base}/api/user/1/properties", timeout=5)
    assert r.status_code in (401, 403), f"W1 present: no-credential read -> {r.status_code}"

def test_W3_no_user_enumeration(base):
    u = _reg(base)
    unknown = requests.post(f"{base}/api/auth/login", json={"email": "nobody@x.com", "password": "x"}, timeout=5)
    wrong = requests.post(f"{base}/api/auth/login", json={"email": u["email"], "password": "wrong"}, timeout=5)
    print("unknown:", unknown.status_code, "wrong-pw:", wrong.status_code)
    assert unknown.status_code == wrong.status_code, \
        f"W3 present: unknown={unknown.status_code} vs wrong-password={wrong.status_code}"

def test_W4_cross_user_read(base):
    a, b = _reg(base), _reg(base)
    assert a["id"] and b["id"], "SETUP FAILED: register did not return ids"
    # No credentials for anyone; ask for B's data by B's id.
    r = requests.get(f"{base}/api/user/{b['id']}/properties", timeout=5)
    assert r.status_code in (401, 403), f"W4 present: unauthenticated read of user {b['id']} -> {r.status_code}"
