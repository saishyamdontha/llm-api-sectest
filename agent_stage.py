"""LLM picks checks from an allowlist; the harness runs them. Local app only."""
import json, sys, uuid, requests
from conftest import BASE            # reuses the localhost guard
MODEL = "qwen3:8b"
ENDPOINTS = json.load(open("endpoints.json"))
MENU = {
  "no_credential_read": "GET an endpoint with no credentials; weakness if it returns 200.",
  "login_status_diff":  "Compare login status for unknown email vs wrong password; weakness if they differ.",
}
PROMPT = f"""You are planning security checks for a REST API you own.
Endpoints: {json.dumps(ENDPOINTS)}
Allowed check types: {json.dumps(MENU)}
Return ONLY JSON: {{"checks":[{{"check":<type>,"method":"GET|POST","path":<endpoint path exactly as listed>,"reason":<short>}}]}}
Only propose checks that fit the allowed types."""

def plan():
    r = requests.post("http://localhost:11434/api/chat", timeout=600, json={
        "model": MODEL, "stream": False, "format": "json", "think": False,
        "options": {"temperature": 0}, "messages": [{"role": "user", "content": PROMPT}]})
    return json.loads(r.json()["message"]["content"])["checks"]

def reg():
    u = {"name":"t","email":f"{uuid.uuid4().hex}@e.com","phone":"1","password":"pw",
         "walletAddress":"0x"+uuid.uuid4().hex[:40],"uniqueId":uuid.uuid4().hex}
    r = requests.post(f"{BASE}/api/auth/register", json=u, timeout=10); r.raise_for_status()
    return u, r.json()

def run(c):
    listed = {(e["method"], e["path"]) for e in ENDPOINTS}
    if c.get("check") not in MENU or (c.get("method"), c.get("path")) not in listed:
        return "INVALID"                       # hallucinated check or endpoint
    if c["check"] == "no_credential_read":
        if c["method"] != "GET": return "REFUSED"
        u, body = reg()
        path = c["path"].replace("{userId}", str(body["id"])).replace("{propertyId}", "1")
        return "WEAK" if requests.get(BASE+path, timeout=5).status_code == 200 else "OK"
    if c["check"] == "login_status_diff":
        u, _ = reg()
        a = requests.post(f"{BASE}/api/auth/login", json={"email":"nobody@x.com","password":"x"}, timeout=5)
        b = requests.post(f"{BASE}/api/auth/login", json={"email":u["email"],"password":"wrong"}, timeout=5)
        return "WEAK" if a.status_code != b.status_code else "OK"

if __name__ == "__main__":
    out = [{**c, "result": run(c)} for c in plan()]
    json.dump(out, open("results_agent.json", "w"), indent=1)
    for o in out: print(o["result"], o["check"], o["path"])
