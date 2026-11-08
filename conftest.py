import os, pytest
# Guard: this suite only ever runs against your own machine.
BASE = os.environ.get("TARGET", "http://localhost:8080")
assert BASE.startswith(("http://localhost", "http://127.0.0.1")), \
    "This suite is for your local app only. Do not point it at a deployed URL."

@pytest.fixture(scope="session")
def base():
    return BASE
