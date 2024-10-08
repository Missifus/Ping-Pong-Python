import pygame
from pygame.locals import*
import random
import os.path

pygame.init()
pygame.font.init()
pygame.mixer.init()
#variables para iniciar la ventana de juego
venHori, venVert= 1600, 900
fps=60
pygame.display.set_caption("Juego Pong")
fuente = pygame.font.Font(os.path.join('recursos', 'PixelSport-nRVRV.ttf'), 60)
#Ruta del directorio de recursos
Recursos=os.path.join(os.path.dirname(__file__),"recursos")
puntuacionUsuario = 0
puntuacionIa = 0
# Diccionario para el estado de las teclas
teclas ={
    pygame.K_w: False,
    pygame.K_s: False
}

#clase de la pelota
class pelotaPong:
    def __init__(self, pelotaFinal) -> None:
        self.imagen = pygame.image.load(pelotaFinal).convert_alpha()  # imagen de la pelota
        self.ancho, self.alto = self.imagen.get_size()  # dimensiones de la pelota
        # posición de la pelota
        self.x = venHori / 2 - self.ancho / 2
        self.y = venVert / 2 - self.alto / 2
        # dirección de la pelota
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.velocidad = 3  # velocidad inicial de la pelota

    def movimiento(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self):
        global puntuacionIa, puntuacionUsuario
        if self.x <= 0:
            puntuacionIa += 1
            self.reinicio()  # Reiniciar la pelota cuando golpea el lado izquierdo
        elif self.x + self.ancho >= venHori:
            puntuacionUsuario += 1
            self.reinicio()  # Reiniciar la pelota cuando golpea el lado derecho
        if self.y <= 0 or self.y + self.alto >= venVert:
            self.dir_y = -self.dir_y
            self.incrementarVelocidad()  # Incrementar la velocidad cuando rebota en la parte superior o inferior

    def reinicio(self):
        self.x = venHori / 2 - self.ancho / 2
        self.y = venVert / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.velocidad = 3  # restablecer la velocidad inicial

    def incrementarVelocidad(self):
        self.velocidad += 0.5  # Incrementar la velocidad en 0.5
        if self.dir_x > 0:
            self.dir_x = self.velocidad
        else:
            self.dir_x = -self.velocidad
        if self.dir_y > 0:
            self.dir_y = self.velocidad
        else:
            self.dir_y = -self.velocidad
#clase de la raqueta
class raquetaPong:
    #funcion que crea la raqueta
    def __init__(self, imagen_path):
        self.imagen=pygame.image.load(imagen_path).convert_alpha()#imagen de la raqueta
        self.ancho, self.alto = self.imagen.get_size()#dimensiones de la raqueta
        #posicion de la raqueta
        self.x = 0
        self.y = venVert / 2 - self.alto / 2
        #direcion de la raqueta
        self.dir_y = 0
#movimiento de la raqueta
    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= venVert:
            self.y = venVert - self.alto
# la raqueta golpeara cuando las cordenadas de la pelota sean igual a las de la raqueta
    def golpear(self, pelota):
        if(
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
#ia basica como oponente
    def golpearIa(self, pelota):
        if(
            pelota.x + pelota.ancho > self.x 
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho
#movimiento de la raquetaIa
    def moverIa(self, pelota):
        velocidadFija = min(15, pelota.velocidad)  # Limitar la velocidad máxima de la raqueta de la IA
        zonaTolerancia = 10  # Zona de tolerancia alrededor del centro

        if pelota.x > 3 * venHori / 4:
            if self.y + self.alto / 2 < pelota.y - zonaTolerancia:
                self.y += velocidadFija
            elif self.y + self.alto / 2 > pelota.y + zonaTolerancia:
                self.y -= velocidadFija
        else:
            # Mantener la raqueta en el centro si la pelota no está en el cuarto derecho de la pantalla
            if self.y + self.alto / 2 < venVert / 2 - zonaTolerancia:
                self.y += velocidadFija
            elif self.y + self.alto / 2 > venVert / 2 + zonaTolerancia:
                self.y -= velocidadFija

        # Asegurarse de que la raqueta no se salga de los límites
        if self.y <= 0:
            self.y = 0
        elif self.y + self.alto >= venVert:
            self.y = venVert - self.alto
#funcion que muestra la puntuacion
def mostrarPuntuacion(ventana, fuente, puntuacionUsuario, puntuacionIa):
    # Colores
    colorTexto = (255, 255, 255)
    colorFondo = (0, 0, 0)
    
    # Crear superficies de texto
    texto_usuario = fuente.render(f'You: {puntuacionUsuario}', True, colorTexto)
    texto_ia = fuente.render(f'IA: {puntuacionIa}', True, colorTexto)
    
    # Posiciones del texto
    pos_usuario = (300, 30)
    pos_ia = (venHori - 300, 30)
    
    # Dibujar fondo para el texto
    pygame.draw.rect(ventana, colorFondo, (pos_usuario[0] - 10, pos_usuario[1] - 10, texto_usuario.get_width() + 20, texto_usuario.get_height() + 20))
    pygame.draw.rect(ventana, colorFondo, (pos_ia[0] - 10, pos_ia[1] - 10, texto_ia.get_width() + 20, texto_ia.get_height() + 20))
    
    # Dibujar texto en la ventana
    ventana.blit(texto_usuario, pos_usuario)
    ventana.blit(texto_ia, pos_ia)

# Funciones de control de música
def reproducirMusica():
    pygame.mixer.music.play(-1)  # Repetir indefinidamente

def pausarMusica():
    pygame.mixer.music.pause()

def reanudarMusica():
    pygame.mixer.music.unpause()

def detenerMusica():
    pygame.mixer.music.stop()

def subirVolumen():
    volumen_actual = pygame.mixer.music.get_volume()
    nuevo_volumen = min(volumen_actual + 0.1, 1.0)  # Aumentar el volumen en 0.1, máximo 1.0
    pygame.mixer.music.set_volume(nuevo_volumen)

def bajarVolumen():
    volumen_actual = pygame.mixer.music.get_volume()
    nuevo_volumen = max(volumen_actual - 0.1, 0.0)  # Disminuir el volumen en 0.1, mínimo 0.0
    pygame.mixer.music.set_volume(nuevo_volumen)

def silenciarMusica():
    pygame.mixer.music.set_volume(0.0)  # Silenciar la música
def eventos():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key in teclas:
                teclas[event.key] = True
            if event.key == pygame.K_p:  # Pausar música
                pausarMusica()
            if event.key == pygame.K_r:  # Reanudar música
                reanudarMusica()
            if event.key == pygame.K_m:  # Detener música
                detenerMusica()
            if event.key == pygame.K_UP:  # Subir volumen
                subirVolumen()
            if event.key == pygame.K_DOWN:  # Bajar volumen
                bajarVolumen()
            if event.key == pygame.K_0:  # Silenciar música
                silenciarMusica()
        if event.type == pygame.KEYUP:
            if event.key in teclas:
                teclas[event.key] = False
    return True

def actualizarRaqueta(raqueta1, velocidadUsuario):
    if teclas[pygame.K_w]:
        raqueta1.dir_y = -velocidadUsuario
    elif teclas[pygame.K_s]:
        raqueta1.dir_y = velocidadUsuario
    else:
        raqueta1.dir_y = 0
    raqueta1.mover()

def pantallaInicio(ventana, fuente):
    ventana.fill((0, 0, 0))  # Fondo negro
    
    # Mensajes de bienvenida y controles
    mensaje_bienvenida = fuente.render('¡Bienvenido al Juego Pong!', True, (255, 255, 255))
    mensaje_inicio = fuente.render('Presiona cualquier tecla para iniciar', True, (255, 255, 255))
    
    # Fuente más pequeña para los controles
    fuente_controles = pygame.font.Font(os.path.join('recursos', 'PixelSport-nRVRV.ttf'), 30)
    mensaje_controles = fuente_controles.render('Controles:', True, (255, 255, 255))
    mensaje_w = fuente_controles.render('W - Mover arriba', True, (255, 255, 255))
    mensaje_s = fuente_controles.render('S - Mover abajo', True, (255, 255, 255))
    mensaje_p = fuente_controles.render('P - Pausar música', True, (255, 255, 255))
    mensaje_r = fuente_controles.render('R - Reanudar música', True, (255, 255, 255))
    mensaje_up = fuente_controles.render('Flecha arriba - Subir volumen', True, (255, 255, 255))
    mensaje_down = fuente_controles.render('Flecha abajo - Bajar volumen', True, (255, 255, 255))
    mensaje_0 = fuente_controles.render('0 - Silenciar música', True, (255, 255, 255))
    
    # Posicionar los mensajes en la pantalla
    ventana.blit(mensaje_bienvenida, (venHori / 2 - mensaje_bienvenida.get_width() / 2, venVert / 2 - mensaje_bienvenida.get_height() / 2 - 150))
    ventana.blit(mensaje_inicio, (venHori / 2 - mensaje_inicio.get_width() / 2, venVert / 2 - mensaje_inicio.get_height() / 2 - 100))
    ventana.blit(mensaje_controles, (venHori / 2 - mensaje_controles.get_width() / 2, venVert / 2 - mensaje_controles.get_height() / 2))
    ventana.blit(mensaje_w, (venHori / 2 - mensaje_w.get_width() / 2, venVert / 2 - mensaje_w.get_height() / 2 + 40))
    ventana.blit(mensaje_s, (venHori / 2 - mensaje_s.get_width() / 2, venVert / 2 - mensaje_s.get_height() / 2 + 80))
    ventana.blit(mensaje_p, (venHori / 2 - mensaje_p.get_width() / 2, venVert / 2 - mensaje_p.get_height() / 2 + 120))
    ventana.blit(mensaje_r, (venHori / 2 - mensaje_r.get_width() / 2, venVert / 2 - mensaje_r.get_height() / 2 + 160))
    ventana.blit(mensaje_up, (venHori / 2 - mensaje_up.get_width() / 2, venVert / 2 - mensaje_up.get_height() / 2 + 200))
    ventana.blit(mensaje_down, (venHori / 2 - mensaje_down.get_width() / 2, venVert / 2 - mensaje_down.get_height() / 2 + 240))
    ventana.blit(mensaje_0, (venHori / 2 - mensaje_0.get_width() / 2, venVert / 2 - mensaje_0.get_height() / 2 + 280))
    
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                esperando = False

def pantallaFin(ventana, fuente, ganador):
    ventana.fill((0, 0, 0))  # Fondo negro
    mensaje = fuente.render(f'{ganador} gana!', True, (255, 255, 255))
    ventana.blit(mensaje, (venHori / 2 - mensaje.get_width() / 2, venVert / 2 - mensaje.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Esperar 3 segundos antes de cerrar

#funcion principal
def main():
    #iniciamos la superficie de la ventana
    ventana = pygame.display.set_mode((venHori,venVert))
    pygame.display.set_caption("Juego pong")
    pelota = pelotaPong(os.path.join(Recursos, "pelotaFinal.png"))
    raqueta1 = raquetaPong(os.path.join(Recursos, "paleta azulF.png"))
    raqueta2 = raquetaPong(os.path.join(Recursos, "paleta rojaF.png"))
    raqueta1.x = 30
    raqueta2.x = venHori -30 - raqueta2.ancho
    #iniciamos puntuaciones
    global puntuacionUsuario, puntuacionIa
    puntuacionUsuario = 0
    puntuacionIa = 0
    velocidadUsuario = 7
    partida=True
    fondo = pygame.image.load(os.path.join(Recursos, "miau5.png"))
    fondo = pygame.transform.scale(fondo, (venHori, venVert)) 
    reloj = pygame.time.Clock()
    # Cargar y reproducir música
    pygame.mixer.music.load(os.path.join(Recursos, "pong-pong-193380.mp3"))
    pygame.mixer.music.set_volume(0.5)  # Inicializar el volumen al 50%
    # Mostrar pantalla de inicio
    pantallaInicio(ventana, fuente)
        # Reproducir música al iniciar el juego
    reproducirMusica()
    #Bucle main
    while partida:
        # Lógica del juego
        partida = eventos()
        pelota.movimiento()
        pelota.rebotar()
        raqueta1.mover()
        actualizarRaqueta(raqueta1,velocidadUsuario)
        raqueta1.golpear(pelota)
        raqueta2.moverIa(pelota)
        raqueta2.golpearIa(pelota)
        # Verificar si alguien ha ganado
        if puntuacionUsuario >= 14:
            pantallaFin(ventana, fuente, 'Usuario')
            partida = False
        elif puntuacionIa >= 14:
            pantallaFin(ventana, fuente, 'IA')
            partida = False
        #dibujar en pantalla
        ventana.blit(fondo, (0, 0))
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raqueta1.imagen, (raqueta1.x, raqueta1.y))
        ventana.blit(raqueta2.imagen, (raqueta2.x, raqueta2.y))
        mostrarPuntuacion(ventana, fuente, puntuacionUsuario, puntuacionIa)
        pygame.display.flip()  # Actualiza toda la pantalla
        reloj.tick(fps)
    detenerMusica()
    pygame.quit()

if __name__ == "__main__":
    main()