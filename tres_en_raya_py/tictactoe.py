import pygame
import sys
import random
import time
import json
import os
from enum import Enum

pygame.init()
pygame.mixer.init()

ANCHO = 900
ALTO = 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🎮 Tres en Raya Pro")

# Colores
NEGRO = (20, 20, 30)
BLANCO = (255, 255, 255)
AZUL = (30, 144, 255)
ROJO = (255, 50, 100)
VERDE = (50, 205, 50)
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
except:
    fuente_titulo = pygame.font.SysFont('arial', 72, bold=True)
    fuente_grande = pygame.font.SysFont('arial', 48)
    fuente_normal = pygame.font.SysFont('arial', 36)
    fuente_pequena = pygame.font.SysFont('arial', 28)
    fuente_muy_pequena = pygame.font.SysFont('arial', 22)

try:
    sonido_click = pygame.mixer.Sound(buffer=bytes([128] * 500))
    sonido_ganar = pygame.mixer.Sound(buffer=bytes([128] * 1000))
    sonido_empatar = pygame.mixer.Sound(buffer=bytes([128] * 800))
    sonido_click.set_volume(0.3)
    sonido_ganar.set_volume(0.5)
    sonido_empatar.set_volume(0.4)
except:
    sonido_click = sonido_ganar = sonido_empatar = None

TAM_CELDA = 150
MARGEN = 50
TABLERO_X = (ANCHO - 3 * TAM_CELDA) // 2
TABLERO_Y = 200

class ModoJuego(Enum):
    VS_HUMANO = 1
    VS_IA_FACIL = 2
    VS_IA_MEDIO = 3
    VS_IA_DIFICIL = 4

class Jugador:
    def __init__(self, simbolo, nombre, color):
        self.simbolo = simbolo
        self.nombre = nombre
        self.color = color
        self.puntuacion = 0
        self.ganadas = 0
        self.empatadas = 0
        self.perdidas = 0

class Tablero:
    def __init__(self):
        self.celdas = [" " for _ in range(9)]
        self.movimientos = []
        
    def reset(self):
        self.celdas = [" " for _ in range(9)]
        self.movimientos = []
        
    def hacer_movimiento(self, posicion, jugador):
        if self.celdas[posicion] == " ":
            self.celdas[posicion] = jugador.simbolo
            self.movimientos.append((posicion, jugador.simbolo))
            return True
        return False
    
    def deshacer_movimiento(self):
        if self.movimientos:
            posicion, _ = self.movimientos.pop()
            self.celdas[posicion] = " "
            return True
        return False
    
    def obtener_movimientos_validos(self):
        return [i for i, celda in enumerate(self.celdas) if celda == " "]
    
    def hay_ganador(self):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)              # Diagonales
        ]
        
        for a, b, c in combinaciones:
            if (self.celdas[a] == self.celdas[b] == self.celdas[c] != " "):
                return self.celdas[a], (a, b, c)
        return None, None
    
    def tablero_lleno(self):
        return " " not in self.celdas
    
    def obtener_linea_ganadora(self):
        _, linea = self.hay_ganador()
        return linea

class IA:
    def __init__(self, simbolo, dificultad):
        self.simbolo = simbolo
        self.dificultad = dificultad
        self.oponente = "X" if simbolo == "O" else "O"
        
    def obtener_movimiento(self, tablero):
        movimientos_validos = tablero.obtener_movimientos_validos()
        
        if not movimientos_validos:
            return None
            
        if self.dificultad == "FACIL":
            return self.movimiento_facil(movimientos_validos)
        elif self.dificultad == "MEDIO":
            return self.movimiento_medio(tablero, movimientos_validos)
        else:  # DIFICIL
            return self.movimiento_dificil(tablero)
    
    def movimiento_facil(self, movimientos_validos):
        return random.choice(movimientos_validos)
    
    def movimiento_medio(self, tablero, movimientos_validos):
        if 4 in movimientos_validos:
            return 4
            
        esquinas = [0, 2, 6, 8]
        esquinas_disponibles = [e for e in esquinas if e in movimientos_validos]
        if esquinas_disponibles:
            return random.choice(esquinas_disponibles)
            
        return random.choice(movimientos_validos)
    
    def movimiento_dificil(self, tablero):
        mejor_movimiento = -1
        mejor_valor = -float('inf')
        
        for movimiento in tablero.obtener_movimientos_validos():
            tablero.hacer_movimiento(movimiento, Jugador(self.simbolo, "IA", AZUL))
            valor = self.minimax(tablero, False)
            tablero.deshacer_movimiento()
            
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
                
        return mejor_movimiento
    
    def minimax(self, tablero, es_maximizando, profundidad=0, alpha=-float('inf'), beta=float('inf')):
        ganador, _ = tablero.hay_ganador()
        
        if ganador == self.simbolo:
            return 10 - profundidad
        elif ganador == self.oponente:
            return profundidad - 10
        elif tablero.tablero_lleno():
            return 0
            
        if es_maximizando:
            max_eval = -float('inf')
            for movimiento in tablero.obtener_movimientos_validos():
                tablero.hacer_movimiento(movimiento, Jugador(self.simbolo, "IA", AZUL))
                evaluacion = self.minimax(tablero, False, profundidad + 1, alpha, beta)
                tablero.deshacer_movimiento()
                max_eval = max(max_eval, evaluacion)
                alpha = max(alpha, evaluacion)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for movimiento in tablero.obtener_movimientos_validos():
                tablero.hacer_movimiento(movimiento, Jugador(self.oponente, "Humano", ROJO))
                evaluacion = self.minimax(tablero, True, profundidad + 1, alpha, beta)
                tablero.deshacer_movimiento()
                min_eval = min(min_eval, evaluacion)
                beta = min(beta, evaluacion)
                if beta <= alpha:
                    break
            return min_eval

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
        
        pygame.draw.rect(superficie, (color[0]//2, color[1]//2, color[2]//2), 
                        self.rect.move(4, 4), border_radius=10)
        pygame.draw.rect(superficie, color, self.rect, border_radius=10)
        pygame.draw.rect(superficie, BLANCO, self.rect, 2, border_radius=10)
        
        texto_surf = fuente_normal.render(self.texto, True, BLANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def esta_presionado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.hover
        return False

class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.jugador_x = Jugador("X", "Jugador X", ROJO)
        self.jugador_o = Jugador("O", "Jugador O", AZUL)
        self.jugador_actual = self.jugador_x
        self.modo_juego = ModoJuego.VS_HUMANO
        self.estado = "MENU"
        self.linea_ganadora = None
        self.animacion_actual = None
        self.tiempo_animacion = 0
        self.historial = []
        self.puntuacion_alta = self.cargar_puntuacion_alta()
        self.botones = []
        self.crear_botones()
        
    def cargar_puntuacion_alta(self):
        try:
            if os.path.exists("tres_raya_stats.json"):
                with open("tres_raya_stats.json", "r") as f:
                    return json.load(f).get("puntuacion_alta", 0)
        except:
            pass
        return 0
    
    def guardar_estadisticas(self):
        try:
            stats = {
                "puntuacion_alta": max(self.puntuacion_alta, 
                                      max(self.jugador_x.puntuacion, self.jugador_o.puntuacion)),
                "partidas_jugadas": len(self.historial),
                "fecha_ultima_partida": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open("tres_raya_stats.json", "w") as f:
                json.dump(stats, f, indent=2)
        except:
            pass
    
    def crear_botones(self):
        centro_x = ANCHO // 2
        
        self.botones_menu = [
            Boton(centro_x - 150, 200, 300, 60, "👥 VS HUMANO", AZUL, (70, 170, 255)),
            Boton(centro_x - 150, 280, 300, 60, "🤖 VS IA (Fácil)", VERDE, (80, 220, 80)),
            Boton(centro_x - 150, 360, 300, 60, "🤖 VS IA (Medio)", AMARILLO, (255, 235, 80)),
            Boton(centro_x - 150, 440, 300, 60, "🤖 VS IA (Difícil)", NARANJA, (255, 185, 50)),
            Boton(centro_x - 150, 520, 300, 60, "📊 ESTADÍSTICAS", MORADO, (167, 132, 219)),
            Boton(centro_x - 150, 600, 300, 60, "❌ SALIR", ROJO, (255, 100, 100))
        ]
        
        self.botones_juego = [
            Boton(ANCHO - 180, 20, 160, 50, "↻ REINICIAR", VERDE, (80, 220, 80)),
            Boton(ANCHO - 180, 80, 160, 50, "🏠 MENÚ", AZUL, (70, 170, 255)),
            Boton(ANCHO - 180, 140, 160, 50, "↶ DESHACER", NARANJA, (255, 185, 50))
        ]
        
        self.botones_resultado = [
            Boton(centro_x - 150, 500, 300, 60, "🔄 NUEVA PARTIDA", VERDE, (80, 220, 80)),
            Boton(centro_x - 150, 580, 300, 60, "🏠 MENÚ PRINCIPAL", AZUL, (70, 170, 255))
        ]
    
    def reset_juego(self):
        self.tablero.reset()
        self.jugador_actual = self.jugador_x
        self.linea_ganadora = None
        self.animacion_actual = None
        self.tiempo_animacion = 0
    
    def cambiar_jugador(self):
        self.jugador_actual = self.jugador_o if self.jugador_actual == self.jugador_x else self.jugador_x
    
    def hacer_movimiento(self, posicion):
        if self.tablero.hacer_movimiento(posicion, self.jugador_actual):
            if sonido_click:
                sonido_click.play()
            
            ganador, linea = self.tablero.hay_ganador()
            if ganador:
                self.linea_ganadora = linea
                jugador_ganador = self.jugador_x if ganador == "X" else self.jugador_o
                jugador_ganador.ganadas += 1
                jugador_ganador.puntuacion += 10
                
                if self.modo_juego == ModoJuego.VS_HUMANO:
                    jugador_perdedor = self.jugador_o if ganador == "X" else self.jugador_x
                    jugador_perdedor.perdidas += 1
                
                self.animacion_actual = "ganar"
                self.tiempo_animacion = time.time()
                
                if sonido_ganar:
                    sonido_ganar.play()
                    
                self.historial.append({
                    "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ganador": jugador_ganador.nombre,
                    "movimientos": len(self.tablero.movimientos),
                    "modo": self.modo_juego.name
                })
                self.guardar_estadisticas()
                
                return True
                
            elif self.tablero.tablero_lleno():
                self.jugador_x.empatadas += 1
                self.jugador_o.empatadas += 1
                self.jugador_x.puntuacion += 5
                self.jugador_o.puntuacion += 5
                
                self.animacion_actual = "empatar"
                self.tiempo_animacion = time.time()
                
                if sonido_empatar:
                    sonido_empatar.play()
                    
                self.historial.append({
                    "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ganador": "Empate",
                    "movimientos": 9,
                    "modo": self.modo_juego.name
                })
                self.guardar_estadisticas()
                
                return True
            
            self.cambiar_jugador()
            
            if ((self.modo_juego != ModoJuego.VS_HUMANO) and 
                self.jugador_actual.simbolo == "O" and 
                not self.tablero.tablero_lleno() and 
                self.tablero.hay_ganador()[0] is None):
                self.ejecutar_movimiento_ia()
                
        return False
    
    def ejecutar_movimiento_ia(self):
        dificultad = {
            ModoJuego.VS_IA_FACIL: "FACIL",
            ModoJuego.VS_IA_MEDIO: "MEDIO",
            ModoJuego.VS_IA_DIFICIL: "DIFICIL"
        }[self.modo_juego]
        
        ia = IA("O", dificultad)
        movimiento = ia.obtener_movimiento(self.tablero)
        
        if movimiento is not None:
            pygame.time.delay(500)  
            self.hacer_movimiento(movimiento)
    
    def dibujar_tablero(self):
        pygame.draw.rect(ventana, (40, 40, 50), 
                        (TABLERO_X - 10, TABLERO_Y - 10, 
                         3 * TAM_CELDA + 20, 3 * TAM_CELDA + 20), border_radius=15)
        
        for i in range(1, 3):
            pygame.draw.line(ventana, GRIS_CLARO,
                           (TABLERO_X + i * TAM_CELDA, TABLERO_Y),
                           (TABLERO_X + i * TAM_CELDA, TABLERO_Y + 3 * TAM_CELDA), 4)
            pygame.draw.line(ventana, GRIS_CLARO,
                           (TABLERO_X, TABLERO_Y + i * TAM_CELDA),
                           (TABLERO_X + 3 * TAM_CELDA, TABLERO_Y + i * TAM_CELDA), 4)
        
        for i in range(9):
            fila = i // 3
            columna = i % 3
            x = TABLERO_X + columna * TAM_CELDA + TAM_CELDA // 2
            y = TABLERO_Y + fila * TAM_CELDA + TAM_CELDA // 2
            
            if self.tablero.celdas[i] == "X":
                self.dibujar_x(x, y, self.jugador_x.color)
            elif self.tablero.celdas[i] == "O":
                self.dibujar_o(x, y, self.jugador_o.color)
        
        if self.linea_ganadora:
            self.dibujar_linea_ganadora()
    
    def dibujar_x(self, x, y, color):
        tam = TAM_CELDA // 2 - 20
        grosor = 8
        
        progreso = min(1.0, (time.time() - self.tiempo_animacion) * 2) if self.animacion_actual else 1.0
        
        pygame.draw.line(ventana, color,
                        (x - tam, y - tam),
                        (x - tam + 2 * tam * progreso, y - tam + 2 * tam * progreso),
                        grosor)
        
        pygame.draw.line(ventana, color,
                        (x + tam, y - tam),
                        (x + tam - 2 * tam * progreso, y - tam + 2 * tam * progreso),
                        grosor)
    
    def dibujar_o(self, x, y, color):
        radio = TAM_CELDA // 2 - 20
        grosor = 8
        
        progreso = min(1.0, (time.time() - self.tiempo_animacion) * 2) if self.animacion_actual else 1.0
        
        puntos = []
        for angulo in range(int(360 * progreso)):
            rad = angulo * 3.14159 / 180
            px = x + int(radio * pygame.math.Vector2(1, 0).rotate(angulo)[0])
            py = y + int(radio * pygame.math.Vector2(1, 0).rotate(angulo)[1])
            puntos.append((px, py))
        
        if len(puntos) > 1:
            pygame.draw.lines(ventana, color, False, puntos, grosor)
    
    def dibujar_linea_ganadora(self):
        if not self.linea_ganadora:
            return
            
        puntos = []
        for pos in self.linea_ganadora:
            fila = pos // 3
            columna = pos % 3
            x = TABLERO_X + columna * TAM_CELDA + TAM_CELDA // 2
            y = TABLERO_Y + fila * TAM_CELDA + TAM_CELDA // 2
            puntos.append((x, y))
        
        progreso = min(1.0, (time.time() - self.tiempo_animacion) * 1.5)
        
        if progreso < 1.0:
            dx = puntos[2][0] - puntos[0][0]
            dy = puntos[2][1] - puntos[0][1]
            x_intermedio = puntos[0][0] + dx * progreso
            y_intermedio = puntos[0][1] + dy * progreso
            puntos_animados = [puntos[0], (x_intermedio, y_intermedio)]
            pygame.draw.lines(ventana, AMARILLO, False, puntos_animados, 6)
        else:
            pygame.draw.lines(ventana, AMARILLO, False, puntos, 6)
            pygame.draw.lines(ventana, BLANCO, False, puntos, 2)
    
    def dibujar_menu(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("🎮 TRES EN RAYA PRO", True, BLANCO)
        sombra = fuente_titulo.render("🎮 TRES EN RAYA PRO", True, (50, 50, 70))
        ventana.blit(sombra, (ANCHO//2 - titulo.get_width()//2 + 3, 103))
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        subtitulo = fuente_pequena.render("Selecciona un modo de juego", True, GRIS_CLARO)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 160))
        
        for boton in self.botones_menu:
            boton.dibujar(ventana)
        
        self.dibujar_tablero_decorativo()
    
    def dibujar_tablero_decorativo(self):
        tam_mini = 60
        margen_mini = 20
        x_mini = ANCHO - tam_mini * 3 - margen_mini
        y_mini = margen_mini
        
        for i in range(1, 3):
            pygame.draw.line(ventana, GRIS_CLARO,
                           (x_mini + i * tam_mini, y_mini),
                           (x_mini + i * tam_mini, y_mini + 3 * tam_mini), 2)
            pygame.draw.line(ventana, GRIS_CLARO,
                           (x_mini, y_mini + i * tam_mini),
                           (x_mini + 3 * tam_mini, y_mini + i * tam_mini), 2)
        
        for i in range(3):
            for j in range(3):
                x = x_mini + j * tam_mini + tam_mini // 2
                y = y_mini + i * tam_mini + tam_mini // 2
                
                if (i + j) % 2 == 0:
                    tam = tam_mini // 3
                    pygame.draw.line(ventana, ROJO, (x - tam, y - tam), (x + tam, y + tam), 4)
                    pygame.draw.line(ventana, ROJO, (x + tam, y - tam), (x - tam, y + tam), 4)
                else:
                    radio = tam_mini // 3
                    pygame.draw.circle(ventana, AZUL, (x, y), radio, 4)
    
    def dibujar_juego(self):
        ventana.fill(NEGRO)
        
        titulo_texto = "TRES EN RAYA"
        if self.modo_juego != ModoJuego.VS_HUMANO:
            titulo_texto += f" - VS IA"
        
        titulo = fuente_grande.render(titulo_texto, True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 30))
        
        self.dibujar_info_jugadores()
        
        self.dibujar_tablero()
        
        for boton in self.botones_juego:
            boton.dibujar(ventana)
        
        turno_texto = f"Turno: {self.jugador_actual.nombre}"
        if self.modo_juego != ModoJuego.VS_HUMANO and self.jugador_actual.simbolo == "O":
            turno_texto = "Turno: IA pensando..."
        
        turno = fuente_normal.render(turno_texto, True, self.jugador_actual.color)
        ventana.blit(turno, (ANCHO//2 - turno.get_width()//2, 150))
        
        movimientos = fuente_pequena.render(f"Movimientos: {len(self.tablero.movimientos)}", True, GRIS_CLARO)
        ventana.blit(movimientos, (TABLERO_X, TABLERO_Y + 3 * TAM_CELDA + 20))
    
    def dibujar_info_jugadores(self):
        pygame.draw.rect(ventana, (30, 30, 40), (20, 20, 200, 100), border_radius=10)
        pygame.draw.rect(ventana, self.jugador_actual.color if self.jugador_actual.simbolo == "X" else GRIS, 
                        (20, 20, 200, 100), 2, border_radius=10)
        
        x_nombre = fuente_pequena.render(self.jugador_x.nombre, True, BLANCO)
        x_puntos = fuente_pequena.render(f"Puntos: {self.jugador_x.puntuacion}", True, self.jugador_x.color)
        x_estad = fuente_muy_pequena.render(f"G: {self.jugador_x.ganadas} E: {self.jugador_x.empatadas} P: {self.jugador_x.perdidas}", 
                                           True, GRIS_CLARO)
        
        ventana.blit(x_nombre, (30, 30))
        ventana.blit(x_puntos, (30, 55))
        ventana.blit(x_estad, (30, 80))
        
        pygame.draw.rect(ventana, (30, 30, 40), (ANCHO - 220, 20, 200, 100), border_radius=10)
        pygame.draw.rect(ventana, self.jugador_actual.color if self.jugador_actual.simbolo == "O" else GRIS, 
                        (ANCHO - 220, 20, 200, 100), 2, border_radius=10)
        
        o_nombre = fuente_pequena.render(self.jugador_o.nombre, True, BLANCO)
        o_puntos = fuente_pequena.render(f"Puntos: {self.jugador_o.puntuacion}", True, self.jugador_o.color)
        o_estad = fuente_muy_pequena.render(f"G: {self.jugador_o.ganadas} E: {self.jugador_o.empatadas} P: {self.jugador_o.perdidas}", 
                                           True, GRIS_CLARO)
        
        ventana.blit(o_nombre, (ANCHO - 210, 30))
        ventana.blit(o_puntos, (ANCHO - 210, 55))
        ventana.blit(o_estad, (ANCHO - 210, 80))
    
    def dibujar_resultado(self):
        ventana.fill(NEGRO)
        
        ganador, _ = self.tablero.hay_ganador()
        
        if ganador:
            jugador = self.jugador_x if ganador == "X" else self.jugador_o
            titulo = fuente_titulo.render(f"🎉 ¡{jugador.nombre} GANA!", True, jugador.color)
            mensaje = fuente_normal.render("¡Felicidades!", True, BLANCO)
        else:
            titulo = fuente_titulo.render("🤝 ¡EMPATE!", True, AMARILLO)
            mensaje = fuente_normal.render("Nadie gana, nadie pierde", True, BLANCO)
        
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        ventana.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 180))
        
        self.dibujar_tablero()
        
        stats_y = TABLERO_Y + 3 * TAM_CELDA + 50
        stats = [
            f"Movimientos totales: {len(self.tablero.movimientos)}",
            f"Duración: {len(self.historial)} partidas jugadas",
            f"Puntuación más alta: {self.puntuacion_alta}"
        ]
        
        for i, texto in enumerate(stats):
            stat_texto = fuente_pequena.render(texto, True, GRIS_CLARO)
            ventana.blit(stat_texto, (ANCHO//2 - stat_texto.get_width()//2, stats_y + i * 30))
        
        for boton in self.botones_resultado:
            boton.dibujar(ventana)
    
    def dibujar_estadisticas(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("📊 ESTADÍSTICAS", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        stats_generales = [
            f"Partidas jugadas: {len(self.historial)}",
            f"Puntuación más alta: {self.puntuacion_alta}",
            f"Jugador X - Puntos: {self.jugador_x.puntuacion}",
            f"Jugador O - Puntos: {self.jugador_o.puntuacion}"
        ]
        
        for i, texto in enumerate(stats_generales):
            stat = fuente_normal.render(texto, True, BLANCO)
            ventana.blit(stat, (ANCHO//2 - stat.get_width()//2, 150 + i * 50))
        
        if self.historial:
            titulo_historial = fuente_grande.render("Historial Reciente:", True, GRIS_CLARO)
            ventana.blit(titulo_historial, (ANCHO//2 - titulo_historial.get_width()//2, 350))
            
            for i, partida in enumerate(self.historial[-5:]):  # Últimas 5 partidas
                texto = f"{partida['fecha']} - {partida['ganador']} ({partida['movimientos']} movimientos)"
                hist = fuente_muy_pequena.render(texto, True, GRIS_CLARO)
                ventana.blit(hist, (ANCHO//2 - hist.get_width()//2, 400 + i * 30))
        
        boton_volver = Boton(ANCHO//2 - 100, ALTO - 100, 200, 50, "VOLVER AL MENÚ", AZUL, (70, 170, 255))
        boton_volver.dibujar(ventana)
        return boton_volver
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        boton_estadisticas = None
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Manejo de estados
                if self.estado == "MENU":
                    for i, boton in enumerate(self.botones_menu):
                        if boton.esta_presionado(evento):
                            if i == 0:  # VS HUMANO
                                self.modo_juego = ModoJuego.VS_HUMANO
                                self.jugador_o.nombre = "Jugador O"
                                self.reset_juego()
                                self.estado = "JUGANDO"
                            elif i == 1:  # VS IA Fácil
                                self.modo_juego = ModoJuego.VS_IA_FACIL
                                self.jugador_o.nombre = "IA (Fácil)"
                                self.reset_juego()
                                self.estado = "JUGANDO"
                            elif i == 2:  # VS IA Medio
                                self.modo_juego = ModoJuego.VS_IA_MEDIO
                                self.jugador_o.nombre = "IA (Medio)"
                                self.reset_juego()
                                self.estado = "JUGANDO"
                            elif i == 3:  # VS IA Difícil
                                self.modo_juego = ModoJuego.VS_IA_DIFICIL
                                self.jugador_o.nombre = "IA (Difícil)"
                                self.reset_juego()
                                self.estado = "JUGANDO"
                            elif i == 4:  # Estadísticas
                                self.estado = "ESTADISTICAS"
                            elif i == 5:  # Salir
                                pygame.quit()
                                sys.exit()
                
                elif self.estado == "JUGANDO":
                    for boton in self.botones_juego:
                        if boton.esta_presionado(evento):
                            if boton.texto == "↻ REINICIAR":
                                self.reset_juego()
                            elif boton.texto == "🏠 MENÚ":
                                self.estado = "MENU"
                            elif boton.texto == "↶ DESHACER":
                                if self.tablero.deshacer_movimiento():
                                    self.cambiar_jugador()
                    
                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        mouse_x, mouse_y = evento.pos
                        if (TABLERO_X <= mouse_x < TABLERO_X + 3 * TAM_CELDA and
                            TABLERO_Y <= mouse_y < TABLERO_Y + 3 * TAM_CELDA):
                            
                            columna = (mouse_x - TABLERO_X) // TAM_CELDA
                            fila = (mouse_y - TABLERO_Y) // TAM_CELDA
                            posicion = fila * 3 + columna
                            
                            if (self.modo_juego == ModoJuego.VS_HUMANO or 
                                (self.modo_juego != ModoJuego.VS_HUMANO and self.jugador_actual.simbolo == "X")):
                                
                                self.hacer_movimiento(posicion)
                
                elif self.estado == "RESULTADO":
                    for boton in self.botones_resultado:
                        if boton.esta_presionado(evento):
                            if boton.texto == "🔄 NUEVA PARTIDA":
                                self.reset_juego()
                                self.estado = "JUGANDO"
                            elif boton.texto == "🏠 MENÚ PRINCIPAL":
                                self.estado = "MENU"
                
                elif self.estado == "ESTADISTICAS":
                    if boton_estadisticas and boton_estadisticas.esta_presionado(evento):
                        self.estado = "MENU"
                    elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        self.estado = "MENU"
            
            if self.estado == "MENU":
                self.dibujar_menu()
            elif self.estado == "JUGANDO":
                self.dibujar_juego()
                
                ganador, _ = self.tablero.hay_ganador()
                if ganador or self.tablero.tablero_lleno():
                    if time.time() - self.tiempo_animacion > 2.0:
                        self.estado = "RESULTADO"
                        
            elif self.estado == "RESULTADO":
                self.dibujar_resultado()
            elif self.estado == "ESTADISTICAS":
                boton_estadisticas = self.dibujar_estadisticas()
            
            pygame.display.flip()
            reloj.tick(60)

if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()