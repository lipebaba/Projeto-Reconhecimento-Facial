import sqlite3

conexao = sqlite3.connect('banco.db')

cursor = conexao.cursor()

cursor.execute(
    "DELETE FROM usuarios WHERE id = 8"
)

conexao.commit()

conexao.close()

print('Usuário removido!')