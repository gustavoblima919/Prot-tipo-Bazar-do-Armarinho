import pytest
import database


@pytest.fixture
def banco_teste(tmp_path, monkeypatch):
    caminho = tmp_path / "bazar_teste.db"

    monkeypatch.setattr(database, "DATABASE", caminho)

    database.criar_tabelas()

    return database


@pytest.fixture
def cliente(banco_teste):
    import app as modulo_app

    modulo_app.app.config["TESTING"] = True

    with modulo_app.app.test_client() as cliente:
        yield cliente