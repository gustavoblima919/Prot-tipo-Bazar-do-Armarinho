import pytest


def test_cadastrar_produto(banco_teste):
    banco_teste.cadastrar_produto(
        "Colar artesanal",
        "Bijuteria",
        15.00,
        10
    )

    produtos = banco_teste.consultar_produtos()

    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Colar artesanal"
    assert produtos[0]["quantidade"] == 10


def test_registrar_venda_reduz_estoque(banco_teste):
    banco_teste.cadastrar_produto(
        "Colar artesanal",
        "Bijuteria",
        15.00,
        10
    )

    total = banco_teste.registrar_venda(1, 3)

    produtos = banco_teste.consultar_produtos()

    assert total == 45.00
    assert produtos[0]["quantidade"] == 7


def test_impedir_venda_com_estoque_insuficiente(banco_teste):
    banco_teste.cadastrar_produto(
        "Colar artesanal",
        "Bijuteria",
        15.00,
        10
    )

    with pytest.raises(ValueError, match="Estoque insuficiente"):
        banco_teste.registrar_venda(1, 20)


def test_impedir_venda_com_quantidade_zero(banco_teste):
    with pytest.raises(ValueError, match="maior que zero"):
        banco_teste.registrar_venda(1, 0)


def test_impedir_venda_de_produto_inexistente(banco_teste):
    with pytest.raises(ValueError, match="Produto não encontrado"):
        banco_teste.registrar_venda(999, 1)