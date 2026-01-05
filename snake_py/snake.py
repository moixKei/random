import pygame
import random
import time
import sys
import os

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake Pro 🐍")

NEGRO = (0, 0, 0)
VERDE = (50, 205, 50)
VERDE_OSCURO = (0, 100, 0)
ROJO = (255, 50, 50)
BLANCO = (255, 255, 255)
AZUL = (30, 144, 255)
AMARILLO = (255, 215, 0)
NARANJA = (255, 165, 0)
MORADO = (147, 112, 219)
GRIS = (40, 40, 40)
GRIS_CLARO = (70, 70, 70)

IZQUIERDA = (-1, 0)
DERECHA = (1, 0)
ARRIBA = (0, -1)
ABAJO = (0, 1)

BLOQUE = 25
FILAS = ALTO // BLOQUE
COLUMNAS = ANCHO // BLOQUE

try:
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_grande = pygame.font.Font(None, 48)
    fuente_normal = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 28)
except:
    fuente_titulo = pygame.font.SysFont('arial', 72, bold=True)
    fuente_grande = pygame.font.SysFont('arial', 48)
    fuente_normal = pygame.font.SysFont('arial', 36)
    fuente_pequena = pygame.font.SysFont('arial', 28)

sonido_comida = None
sonido_game_over = None
try:
    sonido_comida = pygame.mixer.Sound(buffer=bytes([128] * 1000))  # Sonido simple
    sonido_game_over = pygame.mixer.Sound(buffer=bytes([128] * 2000))
    sonido_comida.set_volume(0.3)
    sonido_game_over.set_volume(0.5)
except:
    print("No se pudieron cargar sonidos")

def cargar_puntuacion_alta():
    try:
        if os.path.exists("snake_highscore.txt"):
            with open("snake_highscore.txt", "r") as f:
                return int(f.read().strip())
    except:
        pass
    return 0

def guardar_puntuacion_alta(puntuacion):
    try:
        with open("snake_highscore.txt", "w") as f:
            f.write(str(puntuacion))
    except:
        pass

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color = color_normal
        self.hover = False
        
    def dibujar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        self.color = self.color_hover if self.hover else self.color_normal
        
        pygame.draw.rect(superficie, GRIS, self.rect.move(5, 5), border_radius=10)
        pygame.draw.rect(superficie, self.color, self.rect, border_radius=10)
        pygame.draw.rect(superficie, BLANCO, self.rect, 2, border_radius=10)
        
        texto_surf = fuente_normal.render(self.texto, True, BLANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def esta_presionado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.hover
        return False

class Comida:
    def __init__(self):
        self.pos = self.generar_nueva_posicion()
        self.tipo = random.choice(["normal", "bonus", "especial"])
        self.tiempo_aparicion = time.time()
        
    def generar_nueva_posicion(self, serpiente=None):
        while True:
            x = random.randrange(0, COLUMNAS) * BLOQUE
            y = random.randrange(0, FILAS) * BLOQUE
            if serpiente is None or (x, y) not in serpiente:
                return (x, y)
    
    def dibujar(self, superficie):
        if self.tipo == "normal":
            color = ROJO
            pygame.draw.rect(superficie, color, 
                           (self.pos[0] + 2, self.pos[1] + 2, BLOQUE - 4, BLOQUE - 4))
            pygame.draw.rect(superficie, (255, 100, 100), 
                           (self.pos[0] + 5, self.pos[1] + 5, 10, 10))
        elif self.tipo == "bonus":
            color = AMARILLO
            pygame.draw.rect(superficie, color, 
                           (self.pos[0] + 2, self.pos[1] + 2, BLOQUE - 4, BLOQUE - 4))
            puntos = [
                (self.pos[0] + BLOQUE//2, self.pos[1] + 5),
                (self.pos[0] + BLOQUE - 5, self.pos[1] + BLOQUE//2),
                (self.pos[0] + BLOQUE//2, self.pos[1] + BLOQUE - 5),
                (self.pos[0] + 5, self.pos[1] + BLOQUE//2)
            ]
            pygame.draw.polygon(superficie, NARANJA, puntos)
        else:
            color = MORADO
            pygame.draw.rect(superficie, color, 
                           (self.pos[0] + 2, self.pos[1] + 2, BLOQUE - 4, BLOQUE - 4))
            pygame.draw.circle(superficie, (200, 100, 255), 
                             (self.pos[0] + BLOQUE//2, self.pos[1] + BLOQUE//2), 5)

class Serpiente:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.cuerpo = [(COLUMNAS // 2 * BLOQUE, FILAS // 2 * BLOQUE)]
        self.direccion = DERECHA
        self.nueva_direccion = DERECHA
        self.largo = 1
        self.puntuacion = 0
        self.nivel = 1
        self.velocidad = 10
        self.crecimiento_pendiente = 0
        self.invencible = False
        self.tiempo_invencible = 0
        
    def mover(self):
        dx, dy = self.nueva_direccion
        if (dx, dy) != (-self.direccion[0], -self.direccion[1]):
            self.direccion = self.nueva_direccion
        
        cabeza_x, cabeza_y = self.cuerpo[0]
        dx, dy = self.direccion
        nueva_cabeza = (
            (cabeza_x + dx * BLOQUE) % ANCHO,
            (cabeza_y + dy * BLOQUE) % ALTO
        )
        
        self.cuerpo.insert(0, nueva_cabeza)
        
        if self.crecimiento_pendiente > 0:
            self.crecimiento_pendiente -= 1
        else:
            if len(self.cuerpo) > self.largo:
                self.cuerpo.pop()
                
        if self.invencible and time.time() > self.tiempo_invencible:
            self.invencible = False
            
    def crecer(self, cantidad=1):
        self.crecimiento_pendiente += cantidad
        self.largo += cantidad
        
    def dibujar(self, superficie):
        for i, (x, y) in enumerate(self.cuerpo):
            intensidad = 200 - min(i * 10, 100)
            color = (0, intensidad, 0) if i > 0 else VERDE
            
            if self.invencible and i == 0:
                if int(time.time() * 10) % 2 == 0:
                    color = AZUL
                    
            pygame.draw.rect(superficie, color, 
                           (x + 1, y + 1, BLOQUE - 2, BLOQUE - 2))
            pygame.draw.rect(superficie, VERDE_OSCURO, 
                           (x + 1, y + 1, BLOQUE - 2, BLOQUE - 2), 1)
            
            if i == 0:
                dx, dy = self.direccion
                ojo_x = x + 5 if dx != 1 else x + BLOQUE - 10
                ojo_y = y + 5 if dy != 1 else y + BLOQUE - 10
                pygame.draw.circle(superficie, NEGRO, (ojo_x, ojo_y), 3)
                
                ojo_x = x + BLOQUE - 5 if dx != -1 else x + 10
                ojo_y = y + BLOQUE - 5 if dy != -1 else y + 10
                pygame.draw.circle(superficie, NEGRO, (ojo_x, ojo_y), 3)
                
    def colision_con_si_misma(self):
        return self.cuerpo[0] in self.cuerpo[1:]

class Juego:
    def __init__(self):
        self.serpiente = Serpiente()
        self.comida = Comida()
        self.estado = "menu"  # menu, jugando, pausa, game_over
        self.puntuacion_alta = cargar_puntuacion_alta()
        self.tiempo_inicio = None
        self.tiempo_juego = 0
        self.comidas_recolectadas = 0
        self.botones = []
        self.crear_botones()
        self.particulas = []
        
    def crear_botones(self):
        centro_x = ANCHO // 2
        self.botones = [
            Boton(centro_x - 100, 250, 200, 50, "JUGAR", AZUL, (50, 150, 255)),
            Boton(centro_x - 100, 320, 200, 50, "CONTROLES", VERDE, (50, 255, 50)),
            Boton(centro_x - 100, 390, 200, 50, "SALIR", ROJO, (255, 100, 100))
        ]
        
    def mostrar_menu(self):
        ventana.fill(NEGRO)
        
        for i in range(20):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            pygame.draw.circle(ventana, GRIS_CLARO, (x, y), 2)
        
        titulo = fuente_titulo.render("SNAKE PRO", True, VERDE)
        sombra = fuente_titulo.render("SNAKE PRO", True, GRIS_CLARO)
        ventana.blit(sombra, (ANCHO//2 - titulo.get_width()//2 + 3, 103))
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        subtitulo = fuente_pequena.render("🐍 El clásico juego mejorado", True, BLANCO)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 180))
        
        for boton in self.botones:
            boton.dibujar(ventana)
            
        if self.puntuacion_alta > 0:
            texto_puntuacion = fuente_pequena.render(
                f"Puntuación más alta: {self.puntuacion_alta}", True, AMARILLO)
            ventana.blit(texto_puntuacion, 
                        (ANCHO//2 - texto_puntuacion.get_width()//2, 470))
        
        for i in range(5):
            x = 100 + i * 30
            y = 500
            color = (0, 200 - i * 30, 0)
            pygame.draw.rect(ventana, color, (x, y, 25, 25))
            if i == 0:
                pygame.draw.circle(ventana, NEGRO, (x + 5, y + 5), 3)
                pygame.draw.circle(ventana, NEGRO, (x + 20, y + 5), 3)
        
    def mostrar_controles(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_grande.render("CONTROLES", True, AZUL)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        controles = [
            "FLECHAS: Mover la serpiente",
            "ESPACIO: Pausar/Reanudar",
            "P: Mostrar/Ocultar puntuación",
            "ESC: Volver al menú",
            "R: Reiniciar juego"
        ]
        
        for i, texto in enumerate(controles):
            texto_surf = fuente_normal.render(texto, True, BLANCO)
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, 150 + i * 60))
            
        comida_info = [
            "🍎 ROJA: +1 punto, crece 1",
            "⭐ AMARILLA: +3 puntos, crece 2",
            "💜 MORADA: +5 puntos, invencibilidad 3s"
        ]
        
        for i, texto in enumerate(comida_info):
            texto_surf = fuente_pequena.render(texto, True, BLANCO)
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, 400 + i * 40))
        
        boton_volver = Boton(ANCHO//2 - 100, 530, 200, 50, "VOLVER", VERDE, (50, 255, 50))
        boton_volver.dibujar(ventana)
        
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.estado = "menu"
            elif boton_volver.esta_presionado(evento):
                self.estado = "menu"
                
        return boton_volver
    
    def mostrar_hud(self):
        pygame.draw.rect(ventana, (20, 20, 20, 180), (0, 0, ANCHO, 40))
        
        texto_puntos = fuente_pequena.render(f"Puntos: {self.serpiente.puntuacion}", True, BLANCO)
        ventana.blit(texto_puntos, (20, 10))
        
        texto_nivel = fuente_pequena.render(f"Nivel: {self.serpiente.nivel}", True, AZUL)
        ventana.blit(texto_nivel, (ANCHO//2 - texto_nivel.get_width()//2, 10))
        
        if self.tiempo_inicio:
            self.tiempo_juego = int(time.time() - self.tiempo_inicio)
        minutos = self.tiempo_juego // 60
        segundos = self.tiempo_juego % 60
        texto_tiempo = fuente_pequena.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, BLANCO)
        ventana.blit(texto_tiempo, (ANCHO - texto_tiempo.get_width() - 20, 10))
        
        if self.serpiente.invencible:
            tiempo_restante = max(0, int(self.serpiente.tiempo_invencible - time.time()))
            texto_inv = fuente_pequena.render(f"INV: {tiempo_restante}s", True, MORADO)
            ventana.blit(texto_inv, (ANCHO - 150, ALTO - 30))
            
        texto_vel = fuente_pequena.render(f"Vel: {self.serpiente.velocidad}", True, VERDE)
        ventana.blit(texto_vel, (20, ALTO - 30))
        
    def mostrar_pantalla_pausa(self):
        superficie_pausa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_pausa.fill((0, 0, 0, 150))
        ventana.blit(superficie_pausa, (0, 0))
        
        texto_pausa = fuente_grande.render("PAUSA", True, AMARILLO)
        ventana.blit(texto_pausa, (ANCHO//2 - texto_pausa.get_width()//2, ALTO//2 - 50))
        
        texto_instruccion = fuente_pequena.render("Presiona ESPACIO para continuar", True, BLANCO)
        ventana.blit(texto_instruccion, 
                    (ANCHO//2 - texto_instruccion.get_width()//2, ALTO//2 + 20))
    
    def mostrar_pantalla_game_over(self):
        superficie_game_over = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_game_over.fill((0, 0, 0, 200))
        ventana.blit(superficie_game_over, (0, 0))
        
        texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
        ventana.blit(texto_game_over, (ANCHO//2 - texto_game_over.get_width()//2, 100))
        
        estadisticas = [
            f"Puntuación final: {self.serpiente.puntuacion}",
            f"Longitud máxima: {self.serpiente.largo}",
            f"Tiempo jugado: {self.tiempo_juego // 60}:{self.tiempo_juego % 60:02d}",
            f"Comidas recolectadas: {self.comidas_recolectadas}"
        ]
        
        for i, texto in enumerate(estadisticas):
            texto_surf = fuente_normal.render(texto, True, BLANCO)
            ventana.blit(texto_surf, (ANCHO//2 - texto_surf.get_width()//2, 200 + i * 50))
        
        if self.serpiente.puntuacion > self.puntuacion_alta:
            self.puntuacion_alta = self.serpiente.puntuacion
            guardar_puntuacion_alta(self.puntuacion_alta)
            texto_record = fuente_grande.render("¡NUEVO RÉCORD!", True, AMARILLO)
            ventana.blit(texto_record, (ANCHO//2 - texto_record.get_width()//2, 400))
        
        texto_opciones = fuente_normal.render("Presiona R para reiniciar o ESC para menú", True, VERDE)
        ventana.blit(texto_opciones, (ANCHO//2 - texto_opciones.get_width()//2, 500))
    
    def actualizar_nivel(self):
        nuevo_nivel = self.serpiente.puntuacion // 10 + 1
        if nuevo_nivel > self.serpiente.nivel:
            self.serpiente.nivel = nuevo_nivel
            self.serpiente.velocidad = min(20, 10 + self.serpiente.nivel)
            self.crear_efecto_cambio_nivel()
    
    def crear_efecto_cambio_nivel(self):
        for _ in range(20):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO)
            color = random.choice([AZUL, VERDE, AMARILLO, MORADO])
            self.particulas.append({
                'x': x,
                'y': y,
                'color': color,
                'size': random.randint(3, 8),
                'speed_x': random.uniform(-2, 2),
                'speed_y': random.uniform(-2, 2),
                'life': 30
            })
    
    def actualizar_particulas(self):
        for particula in self.particulas[:]:
            particula['x'] += particula['speed_x']
            particula['y'] += particula['speed_y']
            particula['life'] -= 1
            
            if particula['life'] <= 0:
                self.particulas.remove(particula)
            else:
                alpha = int(255 * (particula['life'] / 30))
                color = particula['color']
                pygame.draw.circle(ventana, color, 
                                 (int(particula['x']), int(particula['y'])), 
                                 particula['size'])
    
    def verificar_colision_comida(self):
        cabeza_x, cabeza_y = self.serpiente.cuerpo[0]
        comida_x, comida_y = self.comida.pos
        
        if cabeza_x == comida_x and cabeza_y == comida_y:
            if sonido_comida:
                sonido_comida.play()
                
            self.comidas_recolectadas += 1
            
            if self.comida.tipo == "normal":
                self.serpiente.puntuacion += 1
                self.serpiente.crecer(1)
            elif self.comida.tipo == "bonus":
                self.serpiente.puntuacion += 3
                self.serpiente.crecer(2)
            elif self.comida.tipo == "especial":
                self.serpiente.puntuacion += 5
                self.serpiente.crecer(1)
                self.serpiente.invencible = True
                self.serpiente.tiempo_invencible = time.time() + 3
            
            self.comida = Comida()
            
            while self.comida.pos in self.serpiente.cuerpo:
                self.comida = Comida()
            
            # Actualizar nivel
            self.actualizar_nivel()
            
            for _ in range(10):
                self.particulas.append({
                    'x': comida_x + BLOQUE//2,
                    'y': comida_y + BLOQUE//2,
                    'color': ROJO if self.comida.tipo == "normal" else 
                            AMARILLO if self.comida.tipo == "bonus" else MORADO,
                    'size': random.randint(2, 5),
                    'speed_x': random.uniform(-3, 3),
                    'speed_y': random.uniform(-3, 3),
                    'life': random.randint(20, 40)
                })
            
            return True
        return False
    
    def verificar_colision_paredes(self):
        cabeza_x, cabeza_y = self.serpiente.cuerpo[0]
        return False
    
    def verificar_colision_cuerpo(self):
        if self.serpiente.invencible:
            return False
        return self.serpiente.colision_con_si_misma()
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        mostrar_puntuacion = True
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.estado == "menu":
                    for boton in self.botones:
                        if boton.esta_presionado(evento):
                            if boton.texto == "JUGAR":
                                self.serpiente.reset()
                                self.tiempo_inicio = time.time()
                                self.tiempo_juego = 0
                                self.comidas_recolectadas = 0
                                self.estado = "jugando"
                            elif boton.texto == "CONTROLES":
                                self.estado = "controles"
                            elif boton.texto == "SALIR":
                                pygame.quit()
                                sys.exit()
                
                elif self.estado == "controles":
                    boton_volver = self.mostrar_controles()
                    if boton_volver.esta_presionado(evento):
                        self.estado = "menu"
                
                elif self.estado == "jugando":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            self.estado = "menu"
                        elif evento.key == pygame.K_SPACE:
                            self.estado = "pausa"
                        elif evento.key == pygame.K_p:
                            mostrar_puntuacion = not mostrar_puntuacion
                        elif evento.key == pygame.K_r:
                            self.serpiente.reset()
                            self.tiempo_inicio = time.time()
                            self.comidas_recolectadas = 0
                        elif evento.key == pygame.K_LEFT:
                            self.serpiente.nueva_direccion = IZQUIERDA
                        elif evento.key == pygame.K_RIGHT:
                            self.serpiente.nueva_direccion = DERECHA
                        elif evento.key == pygame.K_UP:
                            self.serpiente.nueva_direccion = ARRIBA
                        elif evento.key == pygame.K_DOWN:
                            self.serpiente.nueva_direccion = ABAJO
                
                elif self.estado == "pausa":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_SPACE:
                            self.estado = "jugando"
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = "menu"
                
                elif self.estado == "game_over":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            self.serpiente.reset()
                            self.tiempo_inicio = time.time()
                            self.comidas_recolectadas = 0
                            self.estado = "jugando"
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = "menu"
            
            if self.estado == "jugando":
                self.serpiente.mover()
                
                if self.verificar_colision_cuerpo():
                    if sonido_game_over:
                        sonido_game_over.play()
                    self.estado = "game_over"
                
                self.verificar_colision_comida()
                
                if self.tiempo_inicio:
                    self.tiempo_juego = int(time.time() - self.tiempo_inicio)
            
            ventana.fill(NEGRO)

            if self.estado == "menu":
                self.mostrar_menu()
            elif self.estado == "controles":
                self.mostrar_controles()
            elif self.estado == "jugando":
                self.comida.dibujar(ventana)
                self.serpiente.dibujar(ventana)
                self.actualizar_particulas()
                if mostrar_puntuacion:
                    self.mostrar_hud()
            elif self.estado == "pausa":
                self.comida.dibujar(ventana)
                self.serpiente.dibujar(ventana)
                self.mostrar_hud()
                self.mostrar_pantalla_pausa()
            elif self.estado == "game_over":
                self.comida.dibujar(ventana)
                self.serpiente.dibujar(ventana)
                self.mostrar_hud()
                self.mostrar_pantalla_game_over()
            
            # Actualizar pantalla
            pygame.display.flip()
            
            # Controlar velocidad
            if self.estado == "jugando":
                reloj.tick(self.serpiente.velocidad)
            else:
                reloj.tick(60)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()