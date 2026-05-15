from flask import Flask, render_template, request, redirect, Response
import os
import sqlite3
from camera import gerar_frames

app = Flask(__name__)

PASTA_ROSTOS = 'static/rostos'

if not os.path.exists(PASTA_ROSTOS):
    os.makedirs(PASTA_ROSTOS)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'POST':

        nome = request.form['nome']
        imagem = request.files['imagem']

        caminho = os.path.join(
            PASTA_ROSTOS,
            imagem.filename
        )

        imagem.save(caminho)

        conexao = sqlite3.connect('banco.db')
        cursor = conexao.cursor()

        cursor.execute(
            '''
            INSERT INTO usuarios(nome, imagem)
            VALUES (?, ?)
            ''',
            (nome, imagem.filename)
        )

        conexao.commit()
        conexao.close()

        return redirect('/')

    return render_template('cadastro.html')


@app.route('/video')
def video():

    return Response(
        gerar_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/reconhecimento')
def reconhecimento():
    return render_template('reconhecimento.html')


if __name__ == '__main__':
    app.run(debug=True)