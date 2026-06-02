from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = "postgresql+psycopg://olapi:olapi@postgres:5432/olapi"
    keycloak_url: str = "http://keycloak:8080"
    keycloak_realm: str = "olapi"
    keycloak_client_id: str = "olapi-api"
    keycloak_admin_user: str = "admin"
    keycloak_admin_password: str = "admin"


settings = Settings()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom": {
            "class": "logging.Formatter",
            "datefmt": "%H:%M:%S",
            "format": "%(levelname)s | %(name)s:%(lineno)d | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "custom",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "httpx": {"level": "WARNING"},
        "uvicorn": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "uvicorn.access": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "uvicorn.error": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
}
