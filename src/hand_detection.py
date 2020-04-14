import cv2
import math
import numpy as np

# Se instancia la cámara
cap = cv2.VideoCapture(0)

# Se define el intervalo de color que se va a detectar
# Se define un trango para el color amarillo, ya que es el color del guante que vamos a usar
low_yellow = np.array([20, 100, 100], np.uint8)
high_yellow = np.array([30, 255, 255], np.uint8)
count = [0, 0]          # Esta variable es como una doble bandera para definir las acciones que se realizan


def get_hand_position(frame):
    """
        Este método recibe un frame capturado por la cámara a través de OpenCV,
        la procesa para obtener la posición de una mano con un guante amarillo
        y retorna las coordenadas del centroide
    """
    global count
    shoot_bird = 0
    kernel = np.ones((3, 3), np.uint8)

    # Pasamos la imagen al espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crea la máscara de lo que detecte con el color previamente definido
    mask = cv2.inRange(hsv, low_yellow, high_yellow)

    # Llena la imagen de la mano para evitar que tenga puntos negros
    mask = cv2.dilate(mask, kernel, iterations=1)

    # blur the image
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # encuentra los contornos de la mano
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se definen los valores iniciales del centroide y del area encerrada por el contorno
    x, y, area = 0, 0, 0

    if len(contours) != 0:
        # Encontrar el contorno de area maxima(mano)
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        area = cv2.contourArea(cnt)
        if area > 3000:
            # Obtener los momentos 
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                M["m00"] = 1
            
            # Se calcula la posición del centroide a partir de los momentos obtenidos
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])

            # Se dibuja un circulo en donde está ubicado el centroide
            cv2.circle(frame, (x, y), 7, (255, 0, 0), 1)

            # Se define la fuente de la letra con la que se escribirá en pantalla
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Se escribe en pantalla las coordenadas del centroide y el área encerrada por el contorno
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, '{}'.format(area), (x + 10, y + 20), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)

            # Se aplica encuentra un contorno convexo que encierre la mano 
            # a partir del contorno obtenido de la máscara
            new_contour = cv2.convexHull(cnt)
            # Se dibuja el contorno convexo
            cv2.drawContours(frame, [new_contour], 0, (255, 0, 0), 3)

        # permite realizar una pequeña aproximación al contorno de la mano
        # así ser reducen ruidos
        epsilon = 0.0005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Hace una linea convexa alrededor de la mano
        hull = cv2.convexHull(cnt)

        # Se define el área encerrada por el hull y de la mano
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)

        # Se encuentra el porcentaje del area que no está cubierta por la mano
        arearatio = ((areahull - areacnt) / areacnt) * 100

        # Se encuentran los defectos en el area convexa, estos son los huecos que hay entre los dedos
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        # fingers = numero de dedos
        fingers = 0

        # Se encuentra el número de defectos debido a la separación de los dedos
        if defects is not None:
            for i in range(defects.shape[0]):
                # Se definen las coordenadas de los defectos, dónde empiezan dónde terminen y eso
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt = (100, 180)

                # Se encuentran los tamaños de los lados del triángulo
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

                # Se calcula el semiperímetro del triángulo
                s = (a + b + c) / 2

                # Se aplica la fórmula de Herón para encontrar el área
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                # Se calcula la distancia entre el punto y el area convexa
                d = (2 * ar) / a

                # Se aplica la regla del coseno
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # Se ignoran angulos mayores a 90 y defectos que estén muy cerca del área convexa (generalmente se deben a ruido)
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

    # Se muestra la imagen resultante
    cv2.imshow('frame', frame)
    # cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return x, y, shoot_bird

def get_frame():
    """
        Este método se encarga de realizar una captura usando la cámara 
    """
    ret, frame = cap.read()
    return cv2.flip(frame, 1)
