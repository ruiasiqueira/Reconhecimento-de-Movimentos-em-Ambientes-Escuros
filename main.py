import cv2
import json  
import numpy as np

video_path = "IMG_7227.MOV"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERRO: Não foi possível abrir IMG_7227.MOV")
    exit()

BRIGHT_ALPHA = 1.0
BRIGHT_BETA  = 150

MIN_CONTOUR_AREA = 1000

prev_gray = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo ou erro ao ler frame.")
        break

    frame = cv2.resize(frame, (500, 500))

    frame_claro = cv2.convertScaleAbs(frame, alpha=BRIGHT_ALPHA, beta=BRIGHT_BETA)
    hsv = cv2.cvtColor(frame_claro, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    frame_proc = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    gray = cv2.cvtColor(frame_proc, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (7, 7), 0)

    if prev_gray is None:
        prev_gray = gray_blur
        cv2.imshow("Sensor de Movimento no Escuro", frame_proc)
        if cv2.waitKey(30) & 0xFF == 27:
            break
        continue

    diff = cv2.absdiff(prev_gray, gray_blur)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    movimento_detectado = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_CONTOUR_AREA:
            continue

        movimento_detectado = True

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame_proc, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for pt in cnt:
            px, py = pt[0]
            cv2.circle(frame_proc, (px, py), 3, (0, 255, 255), -1)

    if movimento_detectado:
        print("ALERTA:MOVIMENTO DETECTADO")
        print(json.dumps({"movimento": 1}))

        text = "ALERTA:MOVIMENTO DETECTADO"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.6
        thickness = 2
        color = (0, 0, 255)

        (text_width, text_height), _ = cv2.getTextSize(text, font, scale, thickness)
        padding = 5
        x0, y0 = 10, 30

        cv2.rectangle(frame_proc,
                      (x0 - padding, y0 - text_height - padding),
                      (x0 + text_width + padding, y0 + padding),
                      (0, 0, 0),
                      -1)
        cv2.putText(frame_proc, text, (x0, y0), font, scale, color, thickness)
    else:
        print(json.dumps({"movimento": 0}))

    prev_gray = gray_blur.copy()

    cv2.imshow("Sensor de Movimento no Escuro", frame_proc)
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
