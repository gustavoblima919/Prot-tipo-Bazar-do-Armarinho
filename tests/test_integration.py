def test_fluxo_completo_de_cadastro_e_venda(cliente, banco_teste):

    resposta_cadastro = cliente.post(
        "/cadastro",
        data={
            "nome": "Colar artesanal",
            "categoria": "Bijuteria",
            "preco": "15.00",
            "quantidade": "10"
        },
        follow_redirects=True
    )

    assert resposta_cadastro.status_code == 200
    assert b"Colar artesanal" in resposta_cadastro.data

    resposta_venda = cliente.post(
        "/venda",
        data={
            "produto_id": "1",
            "quantidade": "3"
        },
        follow_redirects=True
    )

    assert resposta_venda.status_code == 200
    assert b"Venda registrada com sucesso" in resposta_venda.data

    produtos = banco_teste.consultar_produtos()

    assert produtos[0]["quantidade"] == 7


def test_impedir_venda_acima_do_estoque(cliente, banco_teste):

    banco_teste.cadastrar_produto(
        "Colar artesanal",
        "Bijuteria",
        15.00,
        10
    )

    resposta = cliente.post(
        "/venda",
        data={
            "produto_id": "1",
            "quantidade": "20"
        },
        follow_redirects=True
    )

    assert resposta.status_code == 200
    assert b"Estoque insuficiente" in resposta.data

    produtos = banco_teste.consultar_produtos()

    assert produtos[0]["quantidade"] == 10