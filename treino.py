import cv2
import sqlite3
import numpy as np
import os

faces = []
ids = []

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

usuarios = cursor.execute(
    'SELECT id, imagem FROM usuarios'
).fetchall()

for usuario in usuarios:

    id_usuario = usuario[0]
    imagem_nome = usuario[1]

    caminho = os.path.join(
        'static/rostos',
        imagem_nome
    )

    print(f'Lendo: {caminho}')

    imagem = cv2.imread(caminho)

    if imagem is None:
        print('Imagem não encontrada')
        continue

    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    rostos = detector.detectMultiScale(
        cinza,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    print(f'Rostos encontrados: {len(rostos)}')

    for (x, y, w, h) in rostos:

        face = cinza[y:y+h, x:x+w]

        faces.append(face)
        ids.append(id_usuario)

conexao.close()

if len(faces) == 0:
    print('Nenhuma face encontrada')
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(faces, np.array(ids))

recognizer.save('classificador.yml')

print('Treinamento concluído!')