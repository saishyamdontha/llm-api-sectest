# Results log (scored against ground_truth.yaml as written; key not edited after seeing results)

## Run 1 — agent_stage.py, qwen3:8b, temperature 0, n=1 (commit ffc9584)
- Black-box set W1/W3/W4: agent 1/3 (W1 only). Oracle baseline 3/3 by construction.
- Proposals: 8; hallucinated endpoint: 1; refused by harness (non-GET): 3 (W5/W6/W7 endpoints).
- WEAK flags: 4, all within the key's W1 scope (key says ALL /api/user/* and /ledger/*).
- Never proposed login_status_diff (W3) or GET /api/user/{userId}/properties (W4).
- Limitation: W1 "ALL" includes endpoints that may be intentionally public.
