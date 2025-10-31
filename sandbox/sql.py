import sqlite3

# ==============================
# 1️⃣ Conectar ou criar um banco de dados
# ==============================
conexao = sqlite3.connect("meubanco.db")  # Cria o arquivo se não existir
cursor = conexao.cursor()  # Cria um objeto para executar comandos SQL

# ==============================
# 2️⃣ Criar uma tabela
# ==============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    cidade TEXT
)
""")

# ==============================
# 3️⃣ Inserir dados
# ==============================
cursor.execute("INSERT INTO pessoas (nome, idade, cidade) VALUES (?, ?, ?)", 
               ("Edson", 22, "São Paulo"))
cursor.execute("INSERT INTO pessoas (nome, idade, cidade) VALUES (?, ?, ?)", 
               ("Ana", 30, "Rio de Janeiro"))

# Confirma as alterações
conexao.commit()

# ==============================
# 4️⃣ Consultar dados
# ==============================
cursor.execute("SELECT * FROM pessoas")
resultados = cursor.fetchall()

print("\n📋 LISTA DE PESSOAS:")
for pessoa in resultados:
    print(pessoa)  # Cada linha é uma tupla (id, nome, idade, cidade)

# ==============================
# 5️⃣ Atualizar dados
# ==============================
cursor.execute("UPDATE pessoas SET cidade = ? WHERE nome = ?", ("Curitiba", "Edson"))
conexao.commit()

# ==============================
# 6️⃣ Deletar dados
# ==============================
cursor.execute("DELETE FROM pessoas WHERE nome = ?", ("Ana",))
conexao.commit()

# ==============================
# 7️⃣ Consultar novamente
# ==============================
cursor.execute("SELECT * FROM pessoas")
for pessoa in cursor.fetchall():
    print(pessoa)

# ==============================
# 8️⃣ Fechar conexão
# ==============================
conexao.close()
