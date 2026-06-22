from abc import ABC, abstractmethod

class Estado(ABC):
    @abstractmethod
    def manejar_eventos(self): pass
    @abstractmethod
    def actualizar(self): pass
    @abstractmethod
    def dibujar(self): pass
