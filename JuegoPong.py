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

def eventos():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key in teclas:
                teclas[event.key] = True
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
    pygame.mixer.music.play(-1)  # Repetir indefinidamente
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
        #dibujar en pantalla
        ventana.blit(fondo, (0, 0))
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raqueta1.imagen, (raqueta1.x, raqueta1.y))
        ventana.blit(raqueta2.imagen, (raqueta2.x, raqueta2.y))
        mostrarPuntuacion(ventana, fuente, puntuacionUsuario, puntuacionIa)
        pygame.display.flip()  # Actualiza toda la pantalla
        reloj.tick(fps)
    pygame.quit()

if __name__ == "__main__":
    main()