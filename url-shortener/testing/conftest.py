from os import getenv

import pytest

if getenv("TESTING") != "1":
    error_message = "Environment is not ready for testing"
    raise pytest.exit(error_message)
