import os
from urllib.parse import urlparse
import pytest

# Guard: this suite only ever runs against your own machine.
BASE = os.environ.get("TARGET", "http://localhost:8080")
_host = urlparse(BASE).hostname
if urlparse(BASE).scheme != "http" or _host not in ("localhost", "127.0.0.1"):
    raise SystemExit("This suite is for your local app only. Do not point it at a deployed URL.")

@pytest.fixture(scope="session")
def base():
    return BASE
