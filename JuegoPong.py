import pygame
from pygame.locals import*
import random
import os.path

#variables para iniciar la ventana de juego
venHori=1600
venVert=900
fps=60
blanco=(255,255,255)
negro=(0,0,0)
#Ruta del directorio de recursos
Recursos=os.path.join(os.path.dirname(__file__),"imagenes")
puntuacionUsuario = 0
puntuacionIa = 0

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
    def __init__(self):
        self.imagen=pygame.image.load(os.path.join(Recursos, "paleta azulF.png")).convert_alpha()#imagen de la raqueta
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
    # Ajustar la dirección de la raqueta según la posición de la pelota
        diferencia = (pelota.y - (self.y + self.alto / 2)) * 0.2
        if self.y + self.alto / 2 > pelota.y:
            self.dir_y = diferencia
        elif self.y + self.alto / 2 < pelota.y:
            self.dir_y = diferencia
        else:
            self.dir_y = 0

    # Actualizar la posición de la raqueta
        self.y += self.dir_y
    # Asegurarse de que la raqueta no se salga de los límites
        if self.y <= 0:
            self.y = 0
        elif self.y + self.alto >= venVert:
            self.y = venVert - self.alto
#funcion que muestra la puntuacion
def mostrarPuntuacion(ventana, fuente, puntuacionUsuario, puntuacionIa):
        texto_usuario = fuente.render(f'Usuario: {puntuacionUsuario}', True, negro)
        texto_ia = fuente.render(f'IA: {puntuacionIa}', True, negro)
        ventana.blit(texto_usuario, (50, 50))
        ventana.blit(texto_ia, (venHori - 200, 50))
#funcion principal
def main():
    #iniciamos Pygame
    pygame.init()
    #iniciamos la superficie de la ventana
    ventana = pygame.display.set_mode((venHori,venVert))
    pygame.display.set_caption("Juego pong")
    fuente = pygame.font.Font(None, 74)
    pelota = pelotaPong(os.path.join(Recursos, "pelotaFinal.png"))
    raqueta1 = raquetaPong()
    raqueta1.x = 30
    raqueta2 = raquetaPong()
    raqueta2.x = venHori -30 - raqueta2.ancho
    #iniciamos puntuaciones
    global puntuacionUsuario, puntuacionIa
    puntuacionUsuario = 0
    puntuacionIa = 0
    #Bucle main
    partida=True
    while partida:
 # Lógica del juego
        pelota.movimiento()
        pelota.rebotar()
        raqueta1.mover()
        raqueta1.golpear(pelota)
        raqueta2.moverIa(pelota)
        raqueta2.golpearIa(pelota)
#dibujar en pantalla
        ventana.fill(blanco)
        ventana.blit(pelota.imagen,(pelota.x, pelota.y))
        ventana.blit(raqueta1.imagen, (raqueta1.x, raqueta1.y))
        ventana.blit(raqueta2.imagen, (raqueta2.x, raqueta2.y))
        mostrarPuntuacion(ventana, fuente, puntuacionUsuario, puntuacionIa)

        for event in pygame.event.get():
            if event.type == QUIT:
                partida  = False

            #ingreso del usuario  mediante el teclado
            #detecta que se pulso una tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta1.dir_y = -7
                if event.key == pygame.K_s:
                    raqueta1.dir_y = 7
            #detecta que se dejo de pulsar la tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    raqueta1.dir_y = 0
                if event.key == pygame.K_s:
                    raqueta1.dir_y = 0

        pygame.display.flip()
        pygame.time.Clock().tick(fps)
    pygame.quit()

if __name__ == "__main__":
    main()