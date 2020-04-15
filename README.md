# Angry Birds Hands Edition

Este juego es el resultado de adaptar el projecto [Angry Birds Python](https://github.com/estevaofon/angry-birds-python) para poder interactuar con él usando la cámara. Para esto se usan  técnicas de procesamiendo digital de imágenes usando OpenCV.

En este [video de YouTube](https://www.youtube.com/watch?v=sY5y-LIGv_Q) se puede encontrar una explicación de las técnicas empleadas para detectar la posición y la postura de la mano.

![Alt text](/resources/images/interfaz.png?raw=true "angry-birds")

# Requisitos
Para ejecutar y jugar el juego es necesario tener un computador con una cámara conectada, y un guante de color amarillo para poder identificar la mano.

# Pasos para ejecutar el proyecto
1. Clonar el proyecto.
2. Dirijirse al directorio del proyecto recién clonado.
3. `pip3 install -r requirements.txt`
4. `python3 src/main.py`

# Instrucciones de uso
Se debe usar un guante amarillo. Para poder interactuar con el juego, la mano debe aparecer en la imagen capturada por la cámara. Hay tres posturas que determinan qué acción se va a realizar
1. Con la mano empuñada se apunta.
2. Con la palma abierta, con los 5 dedos levantados, se dispara.
3. Con tres dedos levantados se reinicia o se avanza de nivel.


# Autores de la adaptación

Desarrollado para el curso de Procesamiento Digital de Imágenes (2019-2), dictado por David Fernández (david.fernandez@udea.edu.co) en la [Universidad de Antioquia](http://udea.edu.co/), por 

| Nombre | GitHub | Correo electrónico |
|---|---| ---|
|Jose David Tello Medina | [@joseda77](https://github.com/joseda77) |  jose.tello@udea.edu.co |
| Carlos Daniel Montoya Hurtado | [@cdanmontoya](https://github.com/cdanmontoya) | carlos.montoyah@udea.edu.co |