from os import getenv

if getenv("TESTING") != "1":
    error_message = "Environment is not ready for testing"
    raise OSError(error_message)
