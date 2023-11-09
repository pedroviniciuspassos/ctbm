import os
import sqlite3
from datetime import datetime

# Nome do banco de dados SQLite
db_name = 'video_database.db'

# Função para criar a tabela de vídeos no banco de dados
def create_video_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            nome_arquivo TEXT,
            caminho_arquivo TEXT,
            upload_date DATE
        )
    ''')
    conn.commit()

# Função para inserir informações de vídeo no banco de dados com a data atual
def inserir_video(conn, nome_arquivo, caminho_arquivo):
    cursor = conn.cursor()
    upload_date = datetime.now().date().isoformat()  # Obtém a data atual no formato 'YYYY-MM-DD'
    cursor.execute('INSERT INTO videos (nome_arquivo, caminho_arquivo, upload_date) VALUES (?, ?, ?)',
                   (nome_arquivo, caminho_arquivo, upload_date))
    conn.commit()

# Conectar ao banco de dados
conn = sqlite3.connect(db_name)

# Criar a tabela de vídeos se ela não existir
create_video_table(conn)

# Pasta onde os vídeos estão localizados
pasta_videos = 'static/videos'

# Verifique se a pasta de vídeos existe
if os.path.exists(pasta_videos) and os.listdir(pasta_videos):
    # Percorra os arquivos na pasta de vídeos
    for nome_arquivo in os.listdir(pasta_videos):
        caminho_arquivo = os.path.join(pasta_videos, nome_arquivo)

        # Verifique se o item é um arquivo
        if os.path.isfile(caminho_arquivo):
            # Insira informações do vídeo no banco de dados
            inserir_video(conn, nome_arquivo, caminho_arquivo)

# Feche a conexão com o banco de dados
conn.close()
