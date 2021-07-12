import os
import sqlite3


# ----- Data Base path ----- #
path_base_dados = os.path.expanduser(
    "~/Documents/Projeto Leticia/DataBase/DBProjetoLeticia.db")


# --- Variables --- #
retorno_cursor = []


# ----- Database Structure ----- #
def cria_basedados(path):

    conexao = sqlite3.connect(path)
    cursor = conexao.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Usuario(
        id      INTEGER PRIMARY KEY,
        nome    TEXT    COLLATE NOCASE,
        cpf     TEXT    COLLATE NOCASE,
        cargo   TEXT    COLLATE NOCASE,
        email   TEXT    COLLATE NOCASE
        )
        ''')

    conexao.close()

# ----- Search Users ----- #
def pesquisa(input_pesquisa):

    conexao = sqlite3.connect(path_base_dados)
    cursor = conexao.cursor()

    cursor.execute(''' SELECT id, nome, cpf, cargo, email
                        FROM Usuario
                        WHERE nome LIKE '{0}%' 
                        OR cpf = '{0}'
                        OR cargo LIKE '{0}%'
                        OR email = '{0}'
                        ORDER BY nome
                        '''.format(input_pesquisa))

    for res in cursor:
        retorno_cursor.append(res)

    conexao.close()


# ----- Save data ----- #
def cadastrar_dados(nome, cpf, cargo, email):

    conexao = sqlite3.connect(path_base_dados)
    cursor = conexao.cursor()

    # ----- Register the User ----- #
    insert = ''' INSERT INTO Usuario
                (nome, cpf, cargo, email)'''

    values1 = (nome, cpf, cargo, email)

    values2 = ''' VALUES
                ('{}', '{}', '{}', '{}')
                '''.format(*values1)

    cursor.execute(insert + ' ' + values2)
    conexao.commit()
    conexao.close()


def confere_cpf(cpf):

    conexao = sqlite3.connect(path_base_dados)
    cursor = conexao.cursor()

    # ----- Checks if the cpf is already registered ----- #
    cursor.execute(
        ''' SELECT cpf FROM Usuario
            WHERE cpf = '{}' '''.format(cpf))

    if cursor.fetchone() is not None:
        return 'ja_cadastrado'

    conexao.close()
