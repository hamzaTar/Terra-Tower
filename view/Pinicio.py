import pygame


# --- Parametros ---
ancho_boton = 200
alto_boton = 55
alto_suelo = 420
titulo = "Build The Castle"
subtitulo = "Proyecto PRE"
nombres = ["Altarhouni Hamzah Husayn Aboulqasim", "Ayala Ledezma Jhon Kevin", "Morata Garcia Lluís"]

# --- Colores ---
c_titulo = (255, 220, 50)
c_subtitulo = (0, 0, 0)
c_boton = (40, 80, 160)
c_boton_encima = (70, 120, 210)
c_boton_texto = (255, 255, 255)

c_cielo_superior = (100, 160, 220)
c_cielo_inferior = (160, 200, 240)
c_suelo = (60, 130, 40)
c_suelo_sombra = (45, 95, 30)
c_nube = (255, 255, 255)

c_torre = (95, 95, 100)
c_torre_sombra = (65, 65, 70)
c_puerta_torre = (40, 40, 40)
c_ventana_torre = (50, 50, 55)

c_castillo = (190, 155, 110)
c_castillo_sombra = (90, 55, 30)
c_castillo_techo = (140, 60, 45)
c_castillo_puerta = (50, 50, 20)
c_ventana_marco = c_ventana_torre
c_ventana_cristal = (220, 230, 250)


class PantallaInicio:
    def __init__(self, aparienza, ancho, alto):
        self.aparienza = aparienza
        self.ancho = ancho
        self.alto = alto
        self.fuente_titulo = pygame.font.SysFont('Arial', 72, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont('Arial', 24)
        self.fuente_boton = pygame.font.SysFont('Arial', 30, bold=True)
        self.boton = self.crear_boton()
        self.relog = pygame.time.Clock()

    def ejecutar(self):
        while True:
            pos_raton =pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "salir"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "salir"
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    accion = self.detectar_clic(pos_raton)
                    if accion:
                        return accion

            self.composicion_pantalla(pos_raton)
            pygame.display.flip()
            self.relog.tick(30)


    def crear_boton(self):
        x =(self.ancho-ancho_boton) // 2
        y =self.alto // 2 + 20
        return {"rect": pygame.Rect(x, y, ancho_boton, alto_boton), "texto": "Jugar", "accion": "jugar"}

    def detectar_clic(self, pos_raton):
        if self.boton["rect"].collidepoint(pos_raton):
            return self.boton["accion"]
        return None

    def composicion_pantalla(self, pos_raton):
        self.dibujar_fondo()
        self.dibujar_titulo()
        self.dibujar_boton(pos_raton)
        self.dibujar_integrantes()

    def dibujar_fondo(self):
        # cielo
        mitad_cielo = alto_suelo // 2
        self.aparienza.fill(c_cielo_superior, pygame.Rect(0, 0, self.ancho, mitad_cielo))
        self.aparienza.fill(c_cielo_inferior, pygame.Rect(0, mitad_cielo, self.ancho, alto_suelo - mitad_cielo))

        #suelo
        self.aparienza.fill(c_suelo, pygame.Rect(0, alto_suelo, self.ancho, self.alto - alto_suelo))
        self.aparienza.fill(c_suelo_sombra, pygame.Rect(0, alto_suelo, self.ancho, 12))

        #nubes
        self.dibujar_nube(120, 60, 90, 28)
        self.dibujar_nube(310, 45, 110, 32)
        self.dibujar_nube(410, 100, 120, 37)
        self.dibujar_nube(570, 80, 80, 25)
        self.dibujar_nube(680, 55, 100, 30)

        #torre
        self.dibujar_torre(60, alto_suelo - 230, 80, 230)

        #castillo
        self.dibujar_castillo(570, alto_suelo - 140, 160, 140)

    def dibujar_nube(self, x, y, ancho, alto):
        a, b = ancho // 2, alto // 2
        pygame.draw.ellipse(self.aparienza, c_nube, pygame.Rect(x - a, y - b // 2, ancho, alto // 2))
        pygame.draw.ellipse(self.aparienza, c_nube, pygame.Rect(x - a + 5, y - b, ancho // 2, alto))
        pygame.draw.ellipse(self.aparienza, c_nube, pygame.Rect(x - a // 2 + 10, y - b, ancho // 2, alto))

    def dibujar_torre(self, x, y, ancho, alto):
        pygame.draw.rect(self.aparienza, c_torre, pygame.Rect(x, y, ancho, alto))
        pygame.draw.rect(self.aparienza, c_torre_sombra, pygame.Rect(x + ancho - 12, y, 12, alto))
        pygame.draw.rect(self.aparienza, c_puerta_torre, pygame.Rect(x + 25, y + 200, 25, 30))

        ancho_almena = ancho // 5
        alto_almena = 22
        n_almenas = 5
        for i in range(n_almenas):
            if i % 2 == 0:
                pygame.draw.rect(self.aparienza, c_torre, pygame.Rect(x + i * ancho_almena, y - alto_almena, ancho_almena, alto_almena))

        ancho_ventana, alto_ventana = 14, 22
        posx_ventana = x + ancho // 2 - ancho_ventana // 2
        for posy_ventana in [y + 55, y + 120]:
            pygame.draw.rect(self.aparienza, c_ventana_torre, pygame.Rect(posx_ventana - 2, posy_ventana - 2, ancho_almena + 4, alto_almena + 4))

    def dibujar_castillo(self, x, y, ancho, alto):
        pygame.draw.rect(self.aparienza, c_castillo, pygame.Rect(x, y, ancho, alto))
        pygame.draw.rect(self.aparienza, c_castillo_sombra, pygame.Rect(x + ancho - 10, y, 10, alto))

        punta = (x + ancho // 2, y - 70)
        pygame.draw.polygon(self.aparienza, c_castillo_techo, [(x - 5, y + 5), (x + ancho + 5, y + 5), punta])

        pygame.draw.rect(self.aparienza, c_castillo_puerta, pygame.Rect(x + ancho // 2 - 14, y + alto - 50, 28, 50))

        ancho_ventana, alto_ventana = 28, 28
        posy_ventana = y + 35
        for posx_ventana in [x + 22, x + ancho - 22 - ancho_ventana]:
            pygame.draw.rect(self.aparienza, c_ventana_marco, pygame.Rect(posx_ventana - 2, posy_ventana - 2, ancho_ventana + 4, alto_ventana + 4))
            pygame.draw.rect(self.aparienza, c_ventana_cristal, pygame.Rect(posx_ventana, posy_ventana, ancho_ventana, alto_ventana))
            pygame.draw.line(self.aparienza, c_ventana_marco,
                             (posx_ventana + ancho_ventana // 2, posy_ventana),
                             (posx_ventana + ancho_ventana // 2, posy_ventana + alto_ventana), 2)
            pygame.draw.line(self.aparienza, c_ventana_marco,
                             (posx_ventana, posy_ventana + alto_ventana // 2),
                             (posx_ventana + ancho_ventana, posy_ventana + alto_ventana // 2), 2)

    def dibujar_titulo(self):
        texto_titulo = self.fuente_titulo.render(titulo, True, c_titulo)
        posx_titulo = (self.ancho -texto_titulo.get_width()) // 2
        posy_titulo = self.alto // 4
        self.aparienza.blit(texto_titulo, (posx_titulo, posy_titulo))

        texto_subtitulo =self.fuente_subtitulo.render(subtitulo, True, c_subtitulo)
        posx_subtitulo = (self.ancho - texto_subtitulo.get_width()) // 2
        posy_subtitulo = posy_titulo + texto_titulo.get_height()
        self.aparienza.blit(texto_subtitulo, (posx_subtitulo, posy_subtitulo))

    def dibujar_integrantes(self):
        x = 0
        y = self.alto - 80
        alto_linea = self.fuente_subtitulo.get_height()
        for i, nombre in enumerate(nombres):
            linea = self.fuente_subtitulo.render(nombre, True, c_subtitulo)
            self.aparienza.blit(linea, (x, y + i * alto_linea))

    def dibujar_boton(self, pos_raton):
        encima = self.boton["rect"].collidepoint(pos_raton)
        color = c_boton_encima if encima else c_boton

        pygame.draw.rect(self.aparienza, color, self.boton["rect"], border_radius = 10)

        texto = self.fuente_subtitulo.render(self.boton["texto"], True, c_boton_texto)
        posx_texto = self.boton["rect"].centerx - texto.get_width() // 2
        posy_texto = self.boton["rect"].centery - texto.get_height() // 2
        self.aparienza.blit(texto, (posx_texto, posy_texto))





