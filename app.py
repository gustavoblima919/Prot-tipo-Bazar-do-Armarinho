
from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    criar_tabelas,
    cadastrar_produto,
    consultar_produtos,
    registrar_venda,
    consultar_vendas
)

app = Flask(__name__)
app.secret_key = "chave-temporaria-de-desenvolvimento"

criar_tabelas()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        categoria = request.form.get("categoria", "").strip()
        preco_texto = request.form.get("preco", "").strip().replace(",", ".")
        quantidade_texto = request.form.get("quantidade", "").strip()

        if not nome or not categoria or not preco_texto or not quantidade_texto:
            flash("Preencha todos os campos.")
            return redirect(url_for("cadastro"))

        try:
            preco = float(preco_texto)
            quantidade = int(quantidade_texto)

            if not (0 < preco < float("inf")) or quantidade < 0:
                raise ValueError

        except ValueError:
            flash("Informe um preço válido e uma quantidade inteira não negativa.")
            return redirect(url_for("cadastro"))

        cadastrar_produto(nome, categoria, preco, quantidade)

        flash("Produto cadastrado com sucesso!")
        return redirect(url_for("estoque"))

    return render_template("cadastro.html")


@app.route("/estoque")
def estoque():
    produtos = consultar_produtos()
    return render_template("estoque.html", produtos=produtos)


@app.route("/venda", methods=["GET", "POST"])
def venda():
    if request.method == "POST":
        produto_id_texto = request.form.get("produto_id", "")
        quantidade_texto = request.form.get("quantidade", "")

        try:
            produto_id = int(produto_id_texto)
            quantidade = int(quantidade_texto)

            if produto_id <= 0 or quantidade <= 0:
                raise ValueError

            total = registrar_venda(produto_id, quantidade)

            flash(f"Venda registrada com sucesso! Total: R$ {total:.2f}")

        except ValueError as erro:
            flash(str(erro))

        return redirect(url_for("venda"))

    produtos = consultar_produtos()
    vendas = consultar_vendas()

    return render_template(
        "venda.html",
        produtos=produtos,
        vendas=vendas
    )


if __name__ == "__main__":
    app.run(debug=True)
