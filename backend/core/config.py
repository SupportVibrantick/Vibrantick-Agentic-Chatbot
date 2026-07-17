import os

ENV = os.getenv("APP_ENV", "development")

ENV_FILES = {
    "development": ".env",
    "testing": ".env.test",
    "production": ".env.production",
}

ENV_FILE = ENV_FILES.get(ENV, ".env")