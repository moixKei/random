import pygame
import random
import sys
import json
import os
from enum import Enum

pygame.init()
pygame.mixer.init()

ANCHO = 900
ALTO = 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🎮 Ahorcado Pro")

# Colores
NEGRO = (20, 20, 30)
BLANCO = (255, 255, 255)
ROJO = (220, 60, 80)
VERDE = (60, 180, 100)
AZUL = (30, 144, 255)
AMARILLO = (255, 215, 0)
NARANJA = (255, 165, 0)
MORADO = (147, 112, 219)
GRIS = (100, 100, 120)
GRIS_CLARO = (200, 200, 210)

try:
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_grande = pygame.font.Font(None, 48)
    fuente_normal = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 28)
    fuente_muy_pequena = pygame.font.Font(None, 22)
    fuente_mono = pygame.font.Font(None, 30)
except:
    fuente_titulo = pygame.font.SysFont('arial', 72, bold=True)
    fuente_grande = pygame.font.SysFont('arial', 48)
    fuente_normal = pygame.font.SysFont('arial', 36)
    fuente_pequena = pygame.font.SysFont('arial', 28)
    fuente_muy_pequena = pygame.font.SysFont('arial', 22)
    fuente_mono = pygame.font.SysFont('courier', 30)

try:
    sonido_click = pygame.mixer.Sound(buffer=bytes([128] * 300))
    sonido_letra_correcta = pygame.mixer.Sound(buffer=bytes([128] * 400))
    sonido_letra_incorrecta = pygame.mixer.Sound(buffer=bytes([128] * 200))
    sonido_ganar = pygame.mixer.Sound(buffer=bytes([128] * 600))
    sonido_perder = pygame.mixer.Sound(buffer=bytes([128] * 300))
    
    sonido_click.set_volume(0.3)
    sonido_letra_correcta.set_volume(0.4)
    sonido_letra_incorrecta.set_volume(0.4)
    sonido_ganar.set_volume(0.5)
    sonido_perder.set_volume(0.4)
except:
    sonido_click = sonido_letra_correcta = sonido_letra_incorrecta = sonido_ganar = sonido_perder = None

CATEGORIAS = {
    "PROGRAMACIÓN": [
        "PYTHON", "JAVASCRIPT", "PROGRAMACION", "ALGORITMO", "VARIABLE",
        "FUNCION", "OBJETO", "CLASE", "INTERFAZ", "HERENCIA",
        "POLIMORFISMO", "BASE_DATOS", "FRAMEWORK", "LIBRERIA", "COMPILADOR",
        "DEBUGGING", "GITHUB", "REPOSITORIO", "BACKEND", "FRONTEND"
    ],
    "ANIMALES": [
        "ELEFANTE", "JIRAFA", "CANGURO", "PINGUINO", "DELFIN",
        "MARIPOSA", "CAMELLO", "LEOPARDO", "TIBURON", "ARDILLA",
        "GUACAMAYA", "ORNITORRINCO", "HIPOPOTAMO", "RINOCERONTE", "CHIMPANCE"
    ],
    "PAÍSES": [
        "ESPAÑA", "MEXICO", "ARGENTINA", "COLOMBIA", "BRASIL",
        "FRANCIA", "ITALIA", "ALEMANIA", "JAPON", "AUSTRALIA",
        "CANADA", "RUSIA", "CHINA", "INDIA", "EGIPTO"
    ],
    "CIENCIA": [
        "BIOLOGIA", "QUIMICA", "FISICA", "ASTRONOMIA", "GEOLOGIA",
        "ECOLOGIA", "GENETICA", "NEUROCIENCIA", "MATEMATICAS", "ELECTRONICA"
    ],
    "DEPORTES": [
        "FUTBOL", "BALONCESTO", "TENIS", "NATACION", "ATLETISMO",
        "CICLISMO", "VOLEIBOL", "BEISBOL", "RUGBY", "BOXEO"
    ]
}

class Dificultad(Enum):
    FACIL = 1
    MEDIO = 2
    DIFICIL = 3

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.hover = False
        
    def dibujar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        color = self.color_hover if self.hover else self.color_normal
        
        # Dibujar botón con sombra
        pygame.draw.rect(superficie, (color[0]//2, color[1]//2, color[2]//2), 
                        self.rect.move(4, 4), border_radius=10)
        pygame.draw.rect(superficie, color, self.rect, border_radius=10)
        pygame.draw.rect(superficie, BLANCO, self.rect, 2, border_radius=10)
        
        # Dibujar texto
        texto_surf = fuente_normal.render(self.texto, True, BLANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def esta_presionado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.hover
        return False

class Tecla:
    def __init__(self, letra, x, y):
        self.letra = letra
        self.rect = pygame.Rect(x, y, 50, 50)
        self.presionada = False
        self.rect_correcta = False
        self.rect_incorrecta = False
        
    def dibujar(self, superficie):
        color = GRIS_CLARO
        
        if self.presionada:
            if self.rect_correcta:
                color = VERDE
            elif self.rect_incorrecta:
                color = ROJO
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            color = AZUL
        
        # Dibujar tecla
        pygame.draw.rect(superficie, color, self.rect, border_radius=8)
        pygame.draw.rect(superficie, BLANCO, self.rect, 2, border_radius=8)
        
        # Dibujar letra
        letra_surf = fuente_normal.render(self.letra, True, BLANCO if self.presionada else NEGRO)
        letra_rect = letra_surf.get_rect(center=self.rect.center)
        superficie.blit(letra_surf, letra_rect)
        
    def esta_presionada(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False

class Ahorcado:
    def __init__(self):
        self.palabra_secreta = ""
        self.palabra_mostrada = []
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.vidas = 6
        self.max_vidas = 6
        self.categoria_actual = "PROGRAMACIÓN"
        self.dificultad = Dificultad.MEDIO
        self.estado = "MENU"
        self.puntuacion = 0
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.racha_actual = 0
        self.mejor_racha = 0
        self.teclas = []
        self.botones = []
        self.pistas_disponibles = 3
        self.crear_teclado()
        self.crear_botones()
        self.cargar_estadisticas()
        
    def cargar_estadisticas(self):
        try:
            if os.path.exists("ahorcado_stats.json"):
                with open("ahorcado_stats.json", "r") as f:
                    stats = json.load(f)
                    self.puntuacion = stats.get("puntuacion", 0)
                    self.partidas_ganadas = stats.get("partidas_ganadas", 0)
                    self.partidas_perdidas = stats.get("partidas_perdidas", 0)
                    self.mejor_racha = stats.get("mejor_racha", 0)
        except:
            pass
    
    def guardar_estadisticas(self):
        try:
            stats = {
                "puntuacion": self.puntuacion,
                "partidas_ganadas": self.partidas_ganadas,
                "partidas_perdidas": self.partidas_perdidas,
                "mejor_racha": max(self.mejor_racha, self.racha_actual)
            }
            with open("ahorcado_stats.json", "w") as f:
                json.dump(stats, f, indent=2)
        except:
            pass
    
    def crear_teclado(self):
        self.teclas = []
        filas = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        for i, fila in enumerate(filas):
            for j, letra in enumerate(fila):
                x = ANCHO // 2 - (len(fila) * 55) // 2 + j * 55
                y = ALTO - 180 + i * 60
                self.teclas.append(Tecla(letra, x, y))
    
    def crear_botones(self):
        centro_x = ANCHO // 2
        
        self.botones_menu = [
            Boton(centro_x - 150, 200, 300, 60, "🎮 JUGAR", VERDE, (80, 220, 80)),
            Boton(centro_x - 150, 280, 300, 60, "⚙️ OPCIONES", AZUL, (70, 170, 255)),
            Boton(centro_x - 150, 360, 300, 60, "📊 ESTADÍSTICAS", AMARILLO, (255, 235, 80)),
            Boton(centro_x - 150, 440, 300, 60, "❓ CÓMO JUGAR", MORADO, (167, 132, 219)),
            Boton(centro_x - 150, 520, 300, 60, "❌ SALIR", ROJO, (255, 100, 100))
        ]
        
        self.botones_juego = [
            Boton(ANCHO - 180, 20, 160, 50, "💡 PISTA", MORADO, (167, 132, 219)),
            Boton(ANCHO - 180, 80, 160, 50, "🔄 REINICIAR", AZUL, (70, 170, 255)),
            Boton(ANCHO - 180, 140, 160, 50, "🏠 MENÚ", NARANJA, (255, 185, 50))
        ]
        
        self.botones_opciones = [
            Boton(centro_x - 200, 200, 400, 60, "", AZUL, (70, 170, 255)),  # Categoría
            Boton(centro_x - 200, 300, 400, 60, "", VERDE, (80, 220, 80)),   # Dificultad
            Boton(centro_x - 150, 500, 300, 60, "💾 GUARDAR", AMARILLO, (255, 235, 80)),
            Boton(centro_x - 150, 580, 300, 60, "🏠 MENÚ", MORADO, (167, 132, 219))
        ]
    
    def nueva_palabra(self):
        self.palabra_secreta = random.choice(CATEGORIAS[self.categoria_actual])
        self.palabra_mostrada = ["_" if c != "_" else " " for c in self.palabra_secreta]
        self.letras_adivinadas.clear()
        self.letras_incorrectas.clear()
        
        # Configurar vidas según dificultad
        if self.dificultad == Dificultad.FACIL:
            self.vidas = 8
            self.max_vidas = 8
            self.pistas_disponibles = 5
        elif self.dificultad == Dificultad.MEDIO:
            self.vidas = 6
            self.max_vidas = 6
            self.pistas_disponibles = 3
        else:
            self.vidas = 4
            self.max_vidas = 4
            self.pistas_disponibles = 1
        
        for tecla in self.teclas:
            tecla.presionada = False
            tecla.rect_correcta = False
            tecla.rect_incorrecta = False
    
    def adivinar_letra(self, letra):
        letra = letra.upper()
        
        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            return False
        
        for tecla in self.teclas:
            if tecla.letra == letra:
                tecla.presionada = True
        
        if letra in self.palabra_secreta:
            self.letras_adivinadas.add(letra)
            
            for i, char in enumerate(self.palabra_secreta):
                if char == letra:
                    self.palabra_mostrada[i] = letra
            
            for tecla in self.teclas:
                if tecla.letra == letra:
                    tecla.rect_correcta = True
            
            if sonido_letra_correcta:
                sonido_letra_correcta.play()
            
            self.puntuacion += 10
            
            if "_" not in "".join(self.palabra_mostrada):
                self.partidas_ganadas += 1
                self.racha_actual += 1
                self.mejor_racha = max(self.mejor_racha, self.racha_actual)
                self.puntuacion += 100 * self.vidas  # Bonus por vidas restantes
                
                if sonido_ganar:
                    sonido_ganar.play()
                
                self.guardar_estadisticas()
                return "GANAR"
            
            return True
        else:
            self.letras_incorrectas.add(letra)
            self.vidas -= 1
            
            for tecla in self.teclas:
                if tecla.letra == letra:
                    tecla.rect_incorrecta = True
            
            if sonido_letra_incorrecta:
                sonido_letra_incorrecta.play()
            
            if self.vidas <= 0:
                self.partidas_perdidas += 1
                self.racha_actual = 0
                
                self.palabra_mostrada = list(self.palabra_secreta)
                
                if sonido_perder:
                    sonido_perder.play()
                
                self.guardar_estadisticas()
                return "PERDER"
            
            return False
    
    def usar_pista(self):
        if self.pistas_disponibles <= 0:
            return False
        
        letras_faltantes = []
        for i, char in enumerate(self.palabra_secreta):
            if self.palabra_mostrada[i] == "_" and char not in self.letras_adivinadas:
                letras_faltantes.append((i, char))
        
        if not letras_faltantes:
            return False
        
        idx, letra = random.choice(letras_faltantes)
        self.palabra_mostrada[idx] = letra
        self.letras_adivinadas.add(letra)
        self.pistas_disponibles -= 1
        
        for tecla in self.teclas:
            if tecla.letra == letra:
                tecla.presionada = True
                tecla.rect_correcta = True
        
        if "_" not in "".join(self.palabra_mostrada):
            self.partidas_ganadas += 1
            self.racha_actual += 1
            self.mejor_racha = max(self.mejor_racha, self.racha_actual)
            self.puntuacion += 100 * self.vidas
            
            if sonido_ganar:
                sonido_ganar.play()
            
            self.guardar_estadisticas()
            return "GANAR"
        
        return True
    
    def dibujar_ahorcado(self):
        x_base = ANCHO // 4
        y_base = 150
        grosor = 4
        
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base - 50, y_base + 200), 
                        (x_base + 50, y_base + 200), grosor)
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base, y_base + 200), 
                        (x_base, y_base), grosor)
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base, y_base), 
                        (x_base + 100, y_base), grosor)
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base + 100, y_base), 
                        (x_base + 100, y_base + 30), grosor)
        
        if self.vidas < self.max_vidas:
            pygame.draw.circle(ventana, ROJO, (x_base + 100, y_base + 60), 30, 3)
        
        if self.vidas < self.max_vidas - 1:
            pygame.draw.line(ventana, ROJO, 
                           (x_base + 100, y_base + 90), 
                           (x_base + 100, y_base + 150), grosor)
        
        if self.vidas < self.max_vidas - 2:
            pygame.draw.line(ventana, ROJO, 
                           (x_base + 100, y_base + 100), 
                           (x_base + 70, y_base + 130), grosor)
        
        if self.vidas < self.max_vidas - 3:
            pygame.draw.line(ventana, ROJO, 
                           (x_base + 100, y_base + 100), 
                           (x_base + 130, y_base + 130), grosor)
        
        if self.vidas < self.max_vidas - 4:
            pygame.draw.line(ventana, ROJO, 
                           (x_base + 100, y_base + 150), 
                           (x_base + 70, y_base + 190), grosor)
        
        if self.vidas < self.max_vidas - 5:
            pygame.draw.line(ventana, ROJO, 
                           (x_base + 100, y_base + 150), 
                           (x_base + 130, y_base + 190), grosor)
        
        if self.vidas <= 0:
            # Ojos
            pygame.draw.circle(ventana, NEGRO, (x_base + 90, y_base + 55), 3)
            pygame.draw.circle(ventana, NEGRO, (x_base + 110, y_base + 55), 3)
            # Boca triste
            pygame.draw.arc(ventana, NEGRO, 
                          (x_base + 85, y_base + 65, 30, 20), 
                          3.14, 6.28, 2)
    
    def dibujar_menu(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("🎮 AHORCADO PRO", True, BLANCO)
        sombra = fuente_titulo.render("🎮 AHORCADO PRO", True, (50, 50, 70))
        ventana.blit(sombra, (ANCHO//2 - titulo.get_width()//2 + 3, 103))
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        subtitulo = fuente_pequena.render("Adivina la palabra antes de que se complete el ahorcado", 
                                         True, GRIS_CLARO)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 160))
        
        for boton in self.botones_menu:
            boton.dibujar(ventana)
        
        self.dibujar_ahorcado_decorativo()
    
    def dibujar_ahorcado_decorativo(self):
        x_base = ANCHO - 100
        y_base = 100
        
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base - 20, y_base + 80), 
                        (x_base + 20, y_base + 80), 2)
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base, y_base + 80), 
                        (x_base, y_base), 2)
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base, y_base), 
                        (x_base + 40, y_base), 2)
        pygame.draw.line(ventana, GRIS_CLARO, 
                        (x_base + 40, y_base), 
                        (x_base + 40, y_base + 10), 2)
        
        pygame.draw.circle(ventana, VERDE, (x_base + 40, y_base + 25), 15, 2)
        pygame.draw.line(ventana, VERDE, (x_base + 40, y_base + 40), 
                        (x_base + 40, y_base + 70), 2)
        pygame.draw.line(ventana, VERDE, (x_base + 40, y_base + 50), 
                        (x_base + 20, y_base + 65), 2)
        pygame.draw.line(ventana, VERDE, (x_base + 40, y_base + 50), 
                        (x_base + 60, y_base + 65), 2)
        pygame.draw.line(ventana, VERDE, (x_base + 40, y_base + 70), 
                        (x_base + 20, y_base + 90), 2)
        pygame.draw.line(ventana, VERDE, (x_base + 40, y_base + 70), 
                        (x_base + 60, y_base + 90), 2)
    
    def dibujar_juego(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_grande.render("AHORCADO", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 30))
        
        categoria_texto = fuente_pequena.render(f"Categoría: {self.categoria_actual}", 
                                               True, GRIS_CLARO)
        ventana.blit(categoria_texto, (20, 30))
        
        dificultad_texto = fuente_pequena.render(
            f"Dificultad: {self.dificultad.name.title()}", 
            True, GRIS_CLARO)
        ventana.blit(dificultad_texto, (20, 60))
        
        self.dibujar_ahorcado()
        
        palabra_texto = fuente_mono.render("  ".join(self.palabra_mostrada), True, BLANCO)
        ventana.blit(palabra_texto, (ANCHO//2 - palabra_texto.get_width()//2, 400))
        
        if self.letras_incorrectas:
            incorrectas_texto = fuente_pequena.render(
                f"Letras incorrectas: {' '.join(sorted(self.letras_incorrectas))}", 
                True, ROJO)
            ventana.blit(incorrectas_texto, (ANCHO//2 - incorrectas_texto.get_width()//2, 450))
        
        vidas_texto = fuente_normal.render(f"Vidas: {self.vidas}", True, VERDE)
        ventana.blit(vidas_texto, (ANCHO - 200, 100))
        
        pistas_texto = fuente_normal.render(f"Pistas: {self.pistas_disponibles}", True, MORADO)
        ventana.blit(pistas_texto, (ANCHO - 200, 140))
        
        puntuacion_texto = fuente_pequena.render(f"Puntuación: {self.puntuacion}", True, AMARILLO)
        ventana.blit(puntuacion_texto, (ANCHO - 200, 180))
        
        for tecla in self.teclas:
            tecla.dibujar(ventana)
        
        for boton in self.botones_juego:
            boton.dibujar(ventana)
        
        if self.vidas <= 0 or "_" not in "".join(self.palabra_mostrada):
            self.dibujar_resultado()
    
    def dibujar_resultado(self):
        superficie_resultado = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_resultado.fill((0, 0, 0, 180))
        ventana.blit(superficie_resultado, (0, 0))
        
        if self.vidas > 0:
            titulo = fuente_titulo.render("🎉 ¡GANASTE!", True, VERDE)
            mensaje = fuente_normal.render(f"Palabra: {self.palabra_secreta}", True, BLANCO)
            bonus = fuente_pequena.render(f"Bonus: +{100 * self.vidas} puntos por vidas restantes", 
                                         True, AMARILLO)
        else:
            titulo = fuente_titulo.render("💀 ¡PERDISTE!", True, ROJO)
            mensaje = fuente_normal.render(f"Palabra: {self.palabra_secreta}", True, BLANCO)
            bonus = fuente_pequena.render("Inténtalo de nuevo", True, AMARILLO)
        
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
        ventana.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 300))
        ventana.blit(bonus, (ANCHO//2 - bonus.get_width()//2, 350))
        
        opciones = fuente_normal.render("Presiona ESPACIO para nueva palabra o ESC para menú", 
                                       True, GRIS_CLARO)
        ventana.blit(opciones, (ANCHO//2 - opciones.get_width()//2, 450))
    
    def dibujar_opciones(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("⚙️ OPCIONES", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        categoria_btn = self.botones_opciones[0]
        categoria_btn.texto = f"Categoría: {self.categoria_actual}"
        categoria_btn.dibujar(ventana)
        
        dificultad_btn = self.botones_opciones[1]
        dificultad_btn.texto = f"Dificultad: {self.dificultad.name.title()}"
        dificultad_btn.dibujar(ventana)
        
        explicaciones = [
            "FÁCIL: 8 vidas, 5 pistas",
            "MEDIO: 6 vidas, 3 pistas",
            "DIFÍCIL: 4 vidas, 1 pista"
        ]
        
        for i, texto in enumerate(explicaciones):
            exp = fuente_pequena.render(texto, True, GRIS_CLARO)
            ventana.blit(exp, (ANCHO//2 - exp.get_width()//2, 380 + i * 30))

        for i in range(2, 4):
            self.botones_opciones[i].dibujar(ventana)
    
    def dibujar_estadisticas(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("📊 ESTADÍSTICAS", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        stats = [
            f"Puntuación total: {self.puntuacion}",
            f"Partidas ganadas: {self.partidas_ganadas}",
            f"Partidas perdidas: {self.partidas_perdidas}",
            f"Racha actual: {self.racha_actual}",
            f"Mejor racha: {self.mejor_racha}"
        ]
        
        if self.partidas_ganadas + self.partidas_perdidas > 0:
            porcentaje = (self.partidas_ganadas / (self.partidas_ganadas + self.partidas_perdidas)) * 100
            stats.append(f"Porcentaje de victorias: {porcentaje:.1f}%")
        
        for i, texto in enumerate(stats):
            stat = fuente_normal.render(texto, True, BLANCO)
            ventana.blit(stat, (ANCHO//2 - stat.get_width()//2, 150 + i * 50))
        
        boton_volver = Boton(ANCHO//2 - 100, ALTO - 100, 200, 50, 
                            "VOLVER AL MENÚ", AZUL, (70, 170, 255))
        boton_volver.dibujar(ventana)
        return boton_volver
    
    def dibujar_instrucciones(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("❓ CÓMO JUGAR", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        instrucciones = [
            "1. Selecciona una categoría y dificultad en OPCIONES",
            "2. Adivina las letras de la palabra secreta",
            "3. Cada letra incorrecta reduce tus vidas",
            "4. Usa pistas cuando estés atascado (tecla P)",
            "5. Gana puntos por letras correctas y vidas restantes",
            "",
            "CONTROLES:",
            "- Haz clic en las letras o usa el teclado",
            "- P: Usar pista",
            "- R: Reiniciar partida",
            "- ESC: Volver al menú",
            "- ESPACIO: Nueva palabra (tras ganar/perder)"
        ]
        
        for i, texto in enumerate(instrucciones):
            instruccion = fuente_pequena.render(texto, True, GRIS_CLARO)
            ventana.blit(instruccion, (ANCHO//2 - instruccion.get_width()//2, 150 + i * 35))
        
        boton_volver = Boton(ANCHO//2 - 100, ALTO - 100, 200, 50, 
                            "VOLVER AL MENÚ", AZUL, (70, 170, 255))
        boton_volver.dibujar(ventana)
        return boton_volver
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        boton_actual = None
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if evento.type == pygame.KEYDOWN:
                    if self.estado == "JUGANDO":
                        if evento.unicode.isalpha() and len(evento.unicode) == 1:
                            letra = evento.unicode.upper()
                            self.adivinar_letra(letra)
                        
                        elif evento.key == pygame.K_p:
                            self.usar_pista()
                        elif evento.key == pygame.K_r:
                            self.nueva_palabra()
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"
                        elif evento.key == pygame.K_SPACE:
                            if self.vidas <= 0 or "_" not in "".join(self.palabra_mostrada):
                                self.nueva_palabra()
                    
                    elif self.estado == "MENU":
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    
                    elif self.estado in ["OPCIONES", "ESTADISTICAS", "INSTRUCCIONES"]:
                        if evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"
                
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if sonido_click:
                        sonido_click.play()
                    
                    if self.estado == "MENU":
                        for i, boton in enumerate(self.botones_menu):
                            if boton.esta_presionado(evento):
                                if i == 0: 
                                    self.estado = "JUGANDO"
                                    self.nueva_palabra()
                                elif i == 1: 
                                    self.estado = "OPCIONES"
                                elif i == 2:
                                    self.estado = "ESTADISTICAS"
                                elif i == 3: 
                                    self.estado = "INSTRUCCIONES"
                                elif i == 4: 
                                    pygame.quit()
                                    sys.exit()
                    
                    elif self.estado == "JUGANDO":
                        for tecla in self.teclas:
                            if tecla.esta_presionada(evento):
                                self.adivinar_letra(tecla.letra)
                        
                        for boton in self.botones_juego:
                            if boton.esta_presionado(evento):
                                if boton.texto == "💡 PISTA":
                                    self.usar_pista()
                                elif boton.texto == "🔄 REINICIAR":
                                    self.nueva_palabra()
                                elif boton.texto == "🏠 MENÚ":
                                    self.estado = "MENU"
                    
                    elif self.estado == "OPCIONES":
                        for i, boton in enumerate(self.botones_opciones):
                            if boton.esta_presionado(evento):
                                if i == 0:  
                                    categorias = list(CATEGORIAS.keys())
                                    idx = categorias.index(self.categoria_actual)
                                    self.categoria_actual = categorias[(idx + 1) % len(categorias)]
                                elif i == 1: 
                                    dificultades = list(Dificultad)
                                    idx = dificultades.index(self.dificultad)
                                    self.dificultad = dificultades[(idx + 1) % len(dificultades)]
                                elif i == 2: 
                                    self.guardar_estadisticas()
                                elif i == 3:
                                    self.estado = "MENU"
                    
                    elif self.estado == "ESTADISTICAS":
                        if boton_actual and boton_actual.esta_presionado(evento):
                            self.estado = "MENU"
                    
                    elif self.estado == "INSTRUCCIONES":
                        if boton_actual and boton_actual.esta_presionado(evento):
                            self.estado = "MENU"
            
            if self.estado == "MENU":
                self.dibujar_menu()
            elif self.estado == "JUGANDO":
                self.dibujar_juego()
            elif self.estado == "OPCIONES":
                self.dibujar_opciones()
            elif self.estado == "ESTADISTICAS":
                boton_actual = self.dibujar_estadisticas()
            elif self.estado == "INSTRUCCIONES":
                boton_actual = self.dibujar_instrucciones()
            
            pygame.display.flip()
            reloj.tick(60)

if __name__ == "__main__":
    juego = Ahorcado()
    juego.ejecutar()