class pelota:
        def __init__(self,imagen_pong):
            self.imagen=pygame.image.load(imagen_pong).convert_alpha()
            self.ancho,self,alto*self.imagen.get_size(
            self.x=venHori/2-self.ancho/2
            self.y=venVert/2-self.alto/2
            self.dir_x=random.choice([-5,5])
            self.dir_y=random.choice([-5,5])
            self.puntuacion=0
            self.puntuacionJuego=0
        def movimiento(self):
            self.x+=self