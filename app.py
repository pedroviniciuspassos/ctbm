from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import DataRequired
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Pasta onde os vídeos estão armazenados
video_folder = "static/videos"

# Função para conectar ao banco de dados
def connect_to_database():
    return sqlite3.connect('video_database.db')

class SearchForm(FlaskForm):
    date = DateField('Selecione uma data (YYYY-MM-DD)', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        date = form.date.data.strftime('%Y-%m-%d')
        return redirect(url_for('search', date=date))
    return render_template('index.html', form=form)

@app.route('/search/<date>', methods=['GET'])
def search(date):
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d")
        videos = []

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_arquivo, caminho_arquivo FROM videos WHERE nome_arquivo LIKE ?", ('%' + date + '%',))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            video_filename, video_path = row
            videos.append((video_filename, video_path))

        return render_template('search_results.html', videos=videos, date=date)
    except ValueError:
        return render_template('index.html', error="Data inválida. Use o formato YYYY-MM-DD.")


@app.route('/download/<video_name>')
def download(video_name):
    video_path = os.path.join(video_folder, video_name)
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
