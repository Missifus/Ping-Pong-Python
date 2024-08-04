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

#clase de la pelota
class PelotaPong:
    def __init__(self,pelotaFinal) -> None:
        self.imagen=pygame.image.load(pelotaFinal).convert_alpha()#imagen de la pelota
        self.ancho, self.alto = self.imagen.get_size()#dimensiones de la pelota
        #posicion de la pelota
        self.x = venHori / 2 - self.ancho / 2
        self.y = venVert / 2 - self.alto / 2
        #direcion de la pelota
        self.dir_x = random.choice([-5,5])
        self.dir_y = random.choice([-5,5])

    def movimiento(self):
        self.x += self.dir_x
        self.y += self.dir_y
    
    def rebotar(self):
        if self.x <= 0:
            self.reinicio()
        if self.x + self.ancho >= venHori:
            self.reinicio()
        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.alto >= venVert:
            self.dir_y = -self.dir_y        

    def reinicio(self):
        self.x = venHori / 2 -self.ancho / 2
        self.y = venVert / 2 -self.alto / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5,5])
#clase de la raqueta
class Raqueta:
    def __init__(self):
        self.imagen=pygame.image.load(os.path.join(Recursos, "paleta azulF.png")).convert_alpha()#imagen de la raqueta
        self.ancho, self.alto = self.imagen.get_size()#dimensiones de la pelota
        #posicion de la raqueta
        self.x = 0
        self.y = venVert / 2 - self.alto / 2
        #direcion de la raqueta
        self.dir_y = 0

    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= venVert:
            self,y = venVert - self.alto

def main():
    #iniciamos Pygame
    pygame.init()
    #iniciamos la superficie de la ventana
    ventana=pygame.display.set_mode((venHori,venVert))
    pygame.display.set_caption("Juego pong")
    pelota = PelotaPong(os.path.join(Recursos, "pelotaFinal.png"))
    raqueta1 = Raqueta()
    raqueta1.x = 30
    raqueta2 = Raqueta()
    raqueta2.x = venHori -30 - raqueta2.ancho

    #Bucle main
    partida=True
    while partida:
        pelota.movimiento()
        pelota.rebotar()
        raqueta1.mover()

        ventana.fill(blanco)
        ventana.blit(pelota.imagen,(pelota.x, pelota.y))
        ventana.blit(raqueta1.imagen, (raqueta1.x, raqueta1.y))
        ventana.blit(raqueta2.imagen, (raqueta2.x, raqueta2.y))

        for event in pygame.event.get():
            if event.type == QUIT:
                partida  = False

            #ingreso del usuario  mediante el teclado
            #detecta que se pulso una tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta1.dir_y = -5
                if event.key == pygame.K_s:
                    raqueta1.dir_y = 5
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