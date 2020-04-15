# Importar librerías
import os
import sys
import math
import time
import pygame
import pymunk as pm

# Importar las clases para instanciar en el juego
# Tanto pajaros como niveles
from characters import Bird
from level import Level

# Importar las utilidades para detectar la posición de la mano
from hand_detection import get_frame
from hand_detection import get_hand_position

# Se define la ruta el directorio donde está el main
os.chdir('./src')


pygame.init() # Se inicializa el motor del juego
screen = pygame.display.set_mode((1200, 650)) # Se define la dimensión de la pantalla de juego
redbird = pygame.image.load(
    "../resources/images/red-bird3.png").convert_alpha() # Se carga el recurso de la imagen del pajarito
background2 = pygame.image.load(
    "../resources/images/background3.png").convert_alpha() # Se carga el recurso de la imagen del fondo
sling_image = pygame.image.load(
    "../resources/images/sling-3.png").convert_alpha() # Se carga el recurso de la imagen de la resortera
full_sprite = pygame.image.load(
    "../resources/images/full-sprite.png").convert_alpha() # Se carga el recurso de la imagen de todos los sprites
rect = pygame.Rect(181, 1050, 50, 50) # Se define un rectángulo con la posición del sprite que se desea
cropped = full_sprite.subsurface(rect).copy() # Se recorta el sprite del cerdito
pig_image = pygame.transform.scale(cropped, (30, 30)) # Se ajusta la imagen del cerdito
buttons = pygame.image.load(
    "../resources/images/selected-buttons.png").convert_alpha() # Se carga el recurso de los botones 
pig_happy = pygame.image.load(
    "../resources/images/pig_failed.png").convert_alpha() # Se carga el recurso de la imagen del cerdito contento, que se muestra cuando se falla un nivel
stars = pygame.image.load(
    "../resources/images/stars-edited.png").convert_alpha() # Se carga el recurso de la imagen de las estrellas, que se muestran al finalizar un nivel
rect = pygame.Rect(0, 0, 200, 200)      # Se define un rectángulo para recortar la primera estrella
star1 = stars.subsurface(rect).copy()   # Se recorta la primera estrella
rect = pygame.Rect(204, 0, 200, 200)    # Se define un rectángulo para recortar la segunda estrella
star2 = stars.subsurface(rect).copy()   # Se recorta la segunda estrella
rect = pygame.Rect(426, 0, 200, 200)    # Se define un rectángulo para recortar la tercera estrella
star3 = stars.subsurface(rect).copy()   # Se recorta la tercera estrella
rect = pygame.Rect(164, 10, 60, 60)     # Se define un rectángulo para recortar el botón de pausa
pause_button = buttons.subsurface(rect).copy()  # Se recorta el botón de pausa
rect = pygame.Rect(24, 4, 100, 100)     # Se define un rectángulo para recortar el botón de reiniciar
replay_button = buttons.subsurface(rect).copy() # Se recorta el botón de reiniciar
rect = pygame.Rect(142, 365, 130, 100)  # Se define un rectángulo para recortar el botón de siguiente nivel
next_button = buttons.subsurface(rect).copy()   # Se recorta el botón de siguiente
rect = pygame.Rect(18, 212, 100, 100)   # Se define un rectángulo para recortar el botón de jugar
play_button = buttons.subsurface(rect).copy()   # Se recorta el botón de jugar
clock = pygame.time.Clock()             # Se inicializa un timer que permite visualizar las actualizaciones del juego
running = True                          # Se define una bandera que servirá para correr el juego en un ciclo while


# INICIALIZACIÓN DE VARIABLES NECESARIAS PARA MANEJAR LAS MECÁNICAS DEL JUEGO

space = pm.Space()                                          # Se crea una instancia del espacio de pygame
space.gravity = (0.0, -700.0)                               # Se añade gravedad
pigs = []                                                   # lista de cerdos
birds = []                                                  # lista de pajaritos
balls = []                                                  
polys = []                                                  # lista de poligonos que están repartidos en el espacio
beams = []
columns = []                                                
poly_points = []                                            
ball_number = 0
polys_dict = {}
mouse_distance = 0
rope_lenght = 90
angle = 0
x_mouse = 0
y_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
tick_to_next_circle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)                       
WHITE = (255, 255, 255)
sling_x, sling_y = 135, 450                                    # Posición en reposo de la resortera
sling2_x, sling2_y = 160, 450                                  
score = 0
game_state = 0
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
wall = False

# Static floor
static_body = pm.Body(body_type=pm.Body.STATIC)
static_lines = [pm.Segment(static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
static_lines1 = [pm.Segment(static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
for line in static_lines1:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 3
space.add(static_lines)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)


def vector(p0, p1):
    """Return the vector of the points
    p0 = (xo,yo), p1 = (x1,y1)"""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)


def unit_vector(v):
    """Return the unit vector of the points
    v = (a,b)"""
    h = ((v[0] ** 2) + (v[1] ** 2)) ** 0.5
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)


def distance(xo, yo, x, y):
    """distance between points"""
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def load_music():
    """Load the music"""
    song1 = '../resources/sounds/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


def sling_action():
    """Set up sling behavior"""
    global mouse_distance
    global rope_lenght
    global angle
    global x_mouse
    global y_mouse
    # Se crea un vector entre la posición de la resortera y del centroide de la mano
    v = vector((135, 450), (x_mouse, y_mouse))
    # se normaliza el vector
    uv = unit_vector(v)
    uv1 = uv[0]
    uv2 = uv[1]
    # se calcula la distancia entre el centroide de la mano, determinado por x_mouse y y_mouse
    mouse_distance = distance(135, 450, x_mouse, y_mouse)  # / 800 * 120
    #
    pu = (uv1 * rope_lenght + sling_x, uv2 * rope_lenght + sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20

    # Se verifica si la resortera no se puede estirar mas
    if mouse_distance > rope_lenght:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1 * bigger_rope + sling_x, uv2 * bigger_rope + sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)
    else:
        mouse_distance += 10
        pu3 = (uv1 * mouse_distance + sling_x, uv2 * mouse_distance + sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        screen.blit(redbird, (x_redbird, y_redbird))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)
    # Angle of impulse
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 0.00000000000001
    angle = math.atan((float(dy)) / dx)


def draw_level_cleared():
    """Draw level cleared"""
    global game_state
    global bonus_score_once
    global score
    level_cleared = bold_font3.render("Level Cleared!", 1, WHITE)
    score_level_cleared = bold_font2.render(str(score), 1, WHITE)
    if level.number_of_birds >= 0 and len(pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds - 1) * 10000
        bonus_score_once = False
        game_state = 4
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(level_cleared, (450, 90))
        if level.one_star <= score <= level.two_star:
            screen.blit(star1, (310, 190))
        if level.two_star <= score <= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
        if score >= level.three_star:
            screen.blit(star1, (310, 190))
            screen.blit(star2, (500, 170))
            screen.blit(star3, (700, 200))
        screen.blit(score_level_cleared, (550, 400))
        screen.blit(replay_button, (510, 480))
        screen.blit(next_button, (620, 480))


def draw_level_failed():
    """Draw level failed"""
    global game_state
    failed = bold_font3.render("Level Failed", 1, WHITE)
    if level.number_of_birds <= 0 < len(pigs) and time.time() - t2 > 5:
        game_state = 3
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(failed, (450, 90))
        screen.blit(pig_happy, (380, 120))
        screen.blit(replay_button, (520, 460))


def restart():
    """Delete all objects of the level"""
    pigs_to_remove = []
    birds_to_remove = []
    columns_to_remove = []
    beams_to_remove = []
    for pig in pigs:
        pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    for bird in birds:
        birds_to_remove.append(bird)
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape, column.shape.body)
        columns.remove(column)
    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape, beam.shape.body)
        beams.remove(beam)


def post_solve_bird_pig(arbiter, space, _):
    """Collision between bird and pig"""
    surface = screen
    a, b = arbiter.shapes
    bird_body = a.body
    pig_body = b.body
    p = to_pygame(bird_body.position)
    p2 = to_pygame(pig_body.position)
    r = 30
    pygame.draw.circle(surface, BLACK, p, r, 4)
    pygame.draw.circle(surface, RED, p2, r, 4)
    pigs_to_remove = []
    for pig in pigs:
        if pig_body == pig.body:
            pig.life -= 20
            pigs_to_remove.append(pig)
            global score
            score += 10000
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)


def post_solve_bird_wood(arbiter, space, _):
    """Collision between bird and wood"""
    poly_to_remove = []
    if arbiter.total_impulse.length > 1100:
        a, b = arbiter.shapes
        for column in columns:
            if b == column.shape:
                poly_to_remove.append(column)
        for beam in beams:
            if b == beam.shape:
                poly_to_remove.append(beam)
        for poly in poly_to_remove:
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)
        space.remove(b, b.body)
        global score
        score += 5000


def post_solve_pig_wood(arbiter, space, _):
    """Collision between pig and wood"""
    pigs_to_remove = []
    if arbiter.total_impulse.length > 700:
        pig_shape, wood_shape = arbiter.shapes
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                global score
                score += 10000
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)


# Se agregan los handlers de las colisiones al espacio
# bird and pigs
space.add_collision_handler(0, 1).post_solve = post_solve_bird_pig
# bird and wood
space.add_collision_handler(0, 2).post_solve = post_solve_bird_wood
# pig and wood
space.add_collision_handler(1, 2).post_solve = post_solve_pig_wood
# load_music()

# Se inicializan los niveles
level = Level(pigs, columns, beams, space)
level.number = 0
level.load_level()

# Se inicia el ciclo principal del juego
while running:
    # Set mouse at the current centroid position
    frame = get_frame()

    # Se obtiene el tipo de postura de la mano y su centroide
    x_mouse, y_mouse, shoot = get_hand_position(frame)

    # Se escalan los valores del centroide para mejorar las mecánicas y la interacción
    x_mouse = 40 + ((x_mouse * 190) / 600)
    y_mouse = 150 + ((y_mouse * 400) / 460)

    # Realiza la acción de disparar si detecta que la mano está abierta
    if shoot == 2:
        # Se verifica que aún se tengan pajaritos para disparar
        if level.number_of_birds > 0:
            # Se reduce en 1 la cantidad de pajaritos disponibles
            level.number_of_birds -= 1
            t1 = time.time() * 5000
            xo = 154
            yo = 156
            if mouse_distance > rope_lenght:
                mouse_distance = rope_lenght
            # Si el pajarito está un poco a la izquiera de la resortera, lo dispara hacia la derecha
            if x_mouse < sling_x + 5:
                bird = Bird(mouse_distance, angle, xo, yo, space)
                birds.append(bird)
            # Si no, lo dispara hacia la izquierda
            else:
                bird = Bird(-mouse_distance, angle, xo, yo, space)
                birds.append(bird)
            if level.number_of_birds == 0:
                # Se usa este timer para determinar si, al haber disparado los pajaritos, no se logró completar el nivel
                t2 = time.time()

    # Carga el siguiente nivel si se acabaron con todos los cerditos
    # Y que la postura de la mano sea de tres dedos levantados
    if shoot == 4 and len(pigs) == 0:
        # Build next level
        restart()
        level.number += 1
        game_state = 0
        level.load_level()
        score = 0
        bird_path = []
        bonus_score_once = True
    
    # Reinicia el nivel si el estado del juego es que se falló el nivel
    # Y que la postura de la mano sea de tres dedos levantados
    if shoot == 4 and game_state == 3:
        restart()
        level.load_level()
        game_state = 0
        bird_path = []
        score = 0

    # Draw background
    screen.fill((130, 200, 100))
    screen.blit(background2, (0, -50))

    # Draw first part of the sling
    rect = pygame.Rect(50, 0, 70, 220)
    screen.blit(sling_image, (138, 420), rect)

    # Draw the trail left behind
    for point in bird_path:
        pygame.draw.circle(screen, WHITE, point, 5, 0)

    # Draw the birds in the wait line
    if level.number_of_birds > 0:
        for i in range(level.number_of_birds - 1):
            x = 100 - (i * 35)
            screen.blit(redbird, (x, 508))

    # Draw sling behavior
    if level.number_of_birds > 0:
        sling_action()
    else:
        # Monta un nuevo pajarito en la resortera, si aún queda pájaros
        if time.time() * 1000 - t1 > 300 and level.number_of_birds > 0:
            screen.blit(redbird, (130, 426))
        # Sino, dibuja una línea
        else:
            pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y - 8),
                             (sling2_x, sling2_y - 7), 5)

    # Se definen listas para remover los elementos según sus interacciones
    birds_to_remove = []
    pigs_to_remove = []
    counter += 1
    # Draw birds
    # Se recorre cada uno de los pajaritos y se obtiene su posición 
    # para poder actualizarlo en la pantalla
    for bird in birds:
        if bird.shape.body.position.y < 0:
            birds_to_remove.append(bird)
        p = to_pygame(bird.shape.body.position)
        x, y = p
        x -= 22
        y -= 20
        screen.blit(redbird, (x, y))
        pygame.draw.circle(screen, BLUE,
                           p, int(bird.shape.radius), 2)
        if counter >= 3 and time.time() - t1 < 5:
            bird_path.append(p)
            restart_counter = True
    if restart_counter:
        counter = 0
        restart_counter = False
    # Remove birds and pigs
    # Se recorren las listas de pajaritos y cerdos a borrar, esto se actualiza en las colisiones
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    # Draw static lines
    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])
    i = 0
    # Se recorren los cerditos para dibujarlos
    for pig in pigs:
        i += 1
        pig = pig.shape
        if pig.body.position.y < 0:
            pigs_to_remove.append(pig)

        # Se define la posición del cerdito
        p = to_pygame(pig.body.position)
        x, y = p

        # Se rota el cerdito según vaya rodando
        angle_degrees = math.degrees(pig.body.angle)
        img = pygame.transform.rotate(pig_image, angle_degrees)
        w, h = img.get_size()
        x -= w * 0.5
        y -= h * 0.5
        screen.blit(img, (x, y))
        pygame.draw.circle(screen, BLUE, p, int(pig.radius), 2)
    # Draw columns and Beams
    for column in columns:
        column.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)
    # Update physics
    dt = 1.0 / 50.0 / 2.
    for x in range(2):
        space.step(dt)  # make two updates per frame for better stability
    # Drawing second part of the sling
    rect = pygame.Rect(0, 0, 60, 200)
    screen.blit(sling_image, (120, 420), rect)
    # Draw score
    score_font = bold_font.render("SCORE", 1, WHITE)
    number_font = bold_font.render(str(score), 1, WHITE)
    screen.blit(score_font, (1060, 90))
    if score == 0:
        screen.blit(number_font, (1100, 130))
    else:
        screen.blit(number_font, (1060, 130))
    screen.blit(pause_button, (10, 90))
    # Pause option
    if game_state == 1:
        screen.blit(play_button, (500, 200))
        screen.blit(replay_button, (500, 300))
    draw_level_cleared()
    draw_level_failed()
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
