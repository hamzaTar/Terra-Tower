"""
Paquete de Visualización
Este paquete contiene toda la lógica de representación gráfica y
gestión de entrada de usuario mediante Pygame.
"""

# Importamos las clases principales para "exponerlas" al exterior
# Esto permite usar: from view import PygameView
from view.View import GameView

# La lista __all__ define qué se exporta cuando alguien hace: from view import *
__all__ = ['GameView']

# Mensaje de inicialización (opcional, útil para depuración pedagógica)
# print("Sistema de Visualización inicializado correctamente")