from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import DataRequired
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Pasta onde os vídeos estão armazenados
video_folder = "videos"

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
        for filename in os.listdir(video_folder):
            if filename.startswith("Replay") and filename.endswith(".mp4"):
                video_date_str = filename[7:17]
                video_date = datetime.strptime(video_date_str, "%Y-%m-%d")
                if video_date.date() == selected_date.date():
                    videos.append(filename)
        return render_template('search_results.html', videos=videos, date=date)
    except ValueError:
        return render_template('index.html', error="Data inválida. Use o formato YYYY-MM-DD.")

@app.route('/download/<video_name>')
def download(video_name):
    video_path = os.path.join(video_folder, video_name)
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
