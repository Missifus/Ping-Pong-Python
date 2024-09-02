# Pong Game

Este es un juego de Pong desarrollado en Python utilizando la biblioteca Pygame.

## Descripción

El juego de Pong es un clásico juego de arcade en el que dos jugadores controlan paletas para golpear una pelota de un lado a otro. Este proyecto incluye una implementación básica del juego con una paleta controlada por el usuario y otra controlada por una IA simple.

## Características

- Control de la paleta del usuario con las teclas `W` y `S`.
- IA básica para la paleta oponente.
- Puntuación para el usuario y la IA.
- Incremento de la velocidad de la pelota con cada rebote.
- Música de fondo durante el juego.
- Pantalla de inicio con mensaje de bienvenida y controles.
- El juego termina cuando el usuario o la IA alcanzan los 14 puntos.
- Controles de música para reproducir, pausar, reanudar, detener, subir/bajar volumen y silenciar.

## Requisitos

- Python 3.x
- Pygame

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/Missifus/Ping-Pong-Python
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd Ping-Pong-Python
    ```
3. Instala las dependencias:
    ```bash
    pip install pygame
    ```

## Uso

1. Ejecuta el script principal para iniciar el juego:
    ```bash
    python JuegoPong.py
    ```
## Controles

- `W`: Mover arriba
- `S`: Mover abajo
- `P`: Pausar música
- `R`: Reanudar música
- `Flecha arriba`: Subir volumen
- `Flecha abajo`: Bajar volumen
- `0`: Silenciar música

## Métodos del Programa

### Clase `pelotaPong`
- **`__init__(self, pelotaFinal)`**: Inicializa la pelota con su imagen, posición y dirección aleatoria.
- **`movimiento(self)`**: Actualiza la posición de la pelota según su dirección.
- **`rebotar(self)`**: Gestiona los rebotes de la pelota en los bordes de la ventana y actualiza la puntuación.
- **`reinicio(self)`**: Reinicia la posición y dirección de la pelota al centro de la ventana.
- **`incrementarVelocidad(self)`**: Incrementa la velocidad de la pelota tras cada rebote.

### Clase `raquetaPong`
- **`__init__(self, imagen_path)`**: Inicializa la raqueta con su imagen y posición.
- **`mover(self)`**: Actualiza la posición de la raqueta según su dirección.
- **`golpear(self, pelota)`**: Gestiona el rebote de la pelota cuando golpea la raqueta del usuario.
- **`golpearIa(self, pelota)`**: Gestiona el rebote de la pelota cuando golpea la raqueta de la IA.
- **`moverIa(self, pelota)`**: Controla el movimiento de la raqueta de la IA para seguir la pelota.

### Funciones Globales
- **`mostrarPuntuacion(ventana, fuente, puntuacionUsuario, puntuacionIa)`**: Muestra la puntuación del usuario y de la IA en la ventana del juego.
- **`eventos()`**: Gestiona los eventos de teclado y ventana.
- **`actualizarRaqueta(raqueta1, velocidadUsuario)`**: Actualiza la dirección de la raqueta del usuario según las teclas presionadas.
- **`pantallaInicio(ventana, fuente)`**: Muestra la pantalla de inicio con un mensaje de bienvenida y los controles del juego.
- **`pantallaFin(ventana, fuente, ganador)`**: Muestra la pantalla de fin del juego con el ganador.
- **`reproducirMusica()`**: Reproduce la música de fondo.
- **`pausarMusica()`**: Pausa la música de fondo.
- **`reanudarMusica()`**: Reanuda la música de fondo.
- **`detenerMusica()`**: Detiene la música de fondo.
- **`subirVolumen()`**: Sube el volumen de la música de fondo.
- **`bajarVolumen()`**: Baja el volumen de la música de fondo.
- **`silenciarMusica()`**: Silencia la música de fondo.

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la lógica del juego.
- `recursos/`: Directorio que contiene las imágenes y la música del juego.
    - `pelotaFinal.png`: Imagen de la pelota.
    - `paleta azulF.png`: Imagen de la paleta del usuario.
    - `paleta rojaF.png`: Imagen de la paleta de la IA.
    - `miau5.png`: Imagen de fondo.
    - `pong-pong-193380.mp3`: Música de fondo.
    - `PixelSport-nRVRV.ttf`: Fuente utilizada en el juego.

## Créditos

made with love by Missifus <3

## diagrama de flujo.
<img width="614" alt="diagrama de flujo" src="https://github.com/user-attachments/assets/ab976621-46b6-4362-b6fa-72d56a576a94">
