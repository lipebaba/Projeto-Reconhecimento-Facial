import cv2
import sqlite3
import os

camera = cv2.VideoCapture(0)

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('classificador.yml')

nomes = {}

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

usuarios = cursor.execute(
    'SELECT id, nome FROM usuarios'
).fetchall()

for usuario in usuarios:
    nomes[usuario[0]] = usuario[1]

conexao.close()


def gerar_frames():

    while True:

        sucesso, frame = camera.read()

        if not sucesso:
            break

        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rostos = detector.detectMultiScale(
            cinza,
            scaleFactor=1.2,
            minNeighbors=5
        )

        for (x, y, w, h) in rostos:

            face = cinza[y:y+h, x:x+w]

            id_usuario, confianca = recognizer.predict(face)

            nome = 'Desconhecido'

            if confianca < 100:
                nome = nomes.get(id_usuario, 'Desconhecido')

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                nome,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0,255,0),
                2
            )

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )