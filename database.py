
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).with_name("bazar.db")


def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total REAL NOT NULL,
                data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)


def cadastrar_produto(nome, categoria, preco, quantidade):
    with conectar() as conexao:
        conexao.execute("""
            INSERT INTO produtos (nome, categoria, preco, quantidade)
            VALUES (?, ?, ?, ?)
        """, (nome, categoria, preco, quantidade))


def consultar_produtos():
    with conectar() as conexao:
        produtos = conexao.execute("""
            SELECT * FROM produtos ORDER BY nome
        """).fetchall()

    return produtos


def registrar_venda(produto_id, quantidade):
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    with conectar() as conexao:
        produto = conexao.execute("""
            SELECT * FROM produtos WHERE id = ?
        """, (produto_id,)).fetchone()

        if produto is None:
            raise ValueError("Produto não encontrado.")

        atualizacao = conexao.execute("""
            UPDATE produtos
            SET quantidade = quantidade - ?
            WHERE id = ? AND quantidade >= ?
        """, (quantidade, produto_id, quantidade))

        if atualizacao.rowcount == 0:
            raise ValueError("Estoque insuficiente para realizar a venda.")

        preco = produto["preco"]
        total = preco * quantidade

        conexao.execute("""
            INSERT INTO vendas
            (produto_id, quantidade, preco_unitario, total)
            VALUES (?, ?, ?, ?)
        """, (produto_id, quantidade, preco, total))

        return total


def consultar_vendas():
    with conectar() as conexao:
        vendas = conexao.execute("""
            SELECT
                vendas.id,
                produtos.nome,
                vendas.quantidade,
                vendas.preco_unitario,
                vendas.total,
                vendas.data_venda
            FROM vendas
            JOIN produtos ON produtos.id = vendas.produto_id
            ORDER BY vendas.id DESC
        """).fetchall()

    return vendas
