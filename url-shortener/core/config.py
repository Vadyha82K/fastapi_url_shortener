import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


# Никогда не храните здесь настоящие токены
# Только фейковые значения
API_TOKENS: frozenset[str] = frozenset(
    {
        "4yU3nJOUVRq9JzykON1rRQ",
        "yzwJinC68iFvrd4b7iw9wg",
    }
)

# Only for demo
# No real users in code
USERS_DB: dict[str, str] = {
    # username: password
    "sam": "password",
    "bob": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
