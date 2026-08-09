from backend.database import (
    DEFAULT_DATABASE_URL,
    get_database_url,
    normalize_database_url,
)


def test_database_url_defaults_to_sqlite(
    monkeypatch,
) -> None:
    monkeypatch.delenv(
        "DATABASE_URL",
        raising=False,
    )

    assert (
        get_database_url()
        == DEFAULT_DATABASE_URL
    )


def test_database_url_uses_psycopg_for_postgresql(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        (
            "postgresql://"
            "user:password@localhost/taskforge"
        ),
    )

    assert get_database_url() == (
        "postgresql+psycopg://"
        "user:password@localhost/taskforge"
    )


def test_database_url_preserves_sqlite() -> None:
    database_url = (
        "sqlite:///./another.db"
    )

    assert (
        normalize_database_url(
            database_url,
        )
        == database_url
    )