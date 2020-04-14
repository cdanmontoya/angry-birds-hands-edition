import cv2
import math
import numpy as np

cap = cv2.VideoCapture(0)

# Se define el intervalo de color que se va a detectar
low_yellow = np.array([20, 100, 100], np.uint8)
high_yellow = np.array([30, 255, 255], np.uint8)
count = [0, 0]          # Esta variable es como una doble bandera para definir las acciones que se realizan


def get_hand_position(frame):
    global count
    shoot_bird = 0
    kernel = np.ones((3, 3), np.uint8)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define el rango de color de piel en HSV
    lower_skin = np.array([20, 100, 100], dtype=np.uint8)
    upper_skin = np.array([30, 255, 255], dtype=np.uint8)

    # extrae el color de piel de la imagen
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Llena la imagen de la mano para evitar que tenga puntos negros
    mask = cv2.dilate(mask, kernel, iterations=1)

    # blur the image
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # encuentra los contornos
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encuentra el contorno de area maxima(mano)
    if len(contours) != 0:
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

    x, y, area = 0, 0, 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])
            cv2.circle(frame, (x, y), 7, (255, 0, 0), 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, '{}'.format(area), (x + 10, y + 20), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            new_contour = cv2.convexHull(c)
            cv2.drawContours(frame, [new_contour], 0, (255, 0, 0), 3)

        # approx the contour a little   --- ni puta idea de que hace exactamente
        epsilon = 0.0005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Hace una linea convexa alrededor de la mano
        hull = cv2.convexHull(cnt)

        # define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)

        # find the percentage of area not covered by hand in convex hull
        arearatio = ((areahull - areacnt) / areacnt) * 100

        # find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        # fingers = numero de dedos
        fingers = 0

        # code for finding no. of defects due to fingers
        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt = (100, 180)

                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                # distance between point and convex hull
                d = (2 * ar) / a

                # apply cosine rule here
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d > 30:
                    fingers += 1
            fingers += 1

            font = cv2.FONT_HERSHEY_SIMPLEX
            if fingers == 1:
                if areacnt < 2000:  # Para reconocer que no hay mano
                    cv2.putText(frame, 'No se detectó una mano', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    shoot_bird = 0
                else:
                    if arearatio < 12:  # Para reconocer que no esta abierta
                        cv2.putText(frame, 'Arrastrando', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                        shoot_bird = 1
                        count[0] = 1
            elif fingers == 3:
                cv2.putText(frame, 'Aceptar', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                shoot_bird = 4
            elif fingers == 5 and count == [1, 2]:  # Para reconocer la mano abierta
                cv2.putText(frame, 'Disparando', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                count = [0, 0]
                shoot_bird = 2
            else:
                cv2.putText(frame, 'Acción no detectada', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                count[1] = 2

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return x, y, shoot_bird


def get_frame():
    ret, frame = cap.read()
    return cv2.flip(frame, 1)
