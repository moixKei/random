import pygame
import sys
import time
import random
import json
import os

# Inicializar Pygame
pygame.init()
pygame.font.init()

# Configuración de la pantalla
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🎮 Quiz Interactivo")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
PURPLE = (147, 112, 219)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)

# Fuentes
TITLE_FONT = pygame.font.Font(None, 60)
QUESTION_FONT = pygame.font.Font(None, 40)
OPTION_FONT = pygame.font.Font(None, 35)
SCORE_FONT = pygame.font.Font(None, 50)
SMALL_FONT = pygame.font.Font(None, 30)

# Clase para botones
class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=(70, 130, 180)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.clicked = False
        
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        
        # Cambiar color si el mouse está encima
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
            
        # Dibujar botón
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=15)
        
        # Dibujar texto
        text_surf = OPTION_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
        return self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

# Base de datos de preguntas
preguntas = {
    "general": [
        {
            "pregunta": "¿Cuál es la capital de Francia?",
            "opciones": ["Madrid", "París", "Roma", "Berlín"],
            "respuesta": 1,
            "explicacion": "París es la capital y ciudad más poblada de Francia."
        },
        {
            "pregunta": "¿Qué lenguaje se usa principalmente para desarrollo web frontend?",
            "opciones": ["Python", "C++", "JavaScript", "Java"],
            "respuesta": 2,
            "explicacion": "JavaScript es el lenguaje de programación más usado para desarrollo web frontend."
        },
        {
            "pregunta": "¿Cuál es el río más largo del mundo?",
            "opciones": ["Amazonas", "Nilo", "Yangtsé", "Misisipi"],
            "respuesta": 0,
            "explicacion": "El río Amazonas es el más largo del mundo con aproximadamente 7,062 km."
        },
        {
            "pregunta": "¿En qué año llegó el hombre a la Luna?",
            "opciones": ["1965", "1969", "1972", "1975"],
            "respuesta": 1,
            "explicacion": "El Apolo 11 aterrizó en la Luna el 20 de julio de 1969."
        },
        {
            "pregunta": "¿Cuál es el animal más rápido del mundo?",
            "opciones": ["León", "Guepardo", "Águila", "Leopardo"],
            "respuesta": 1,
            "explicacion": "El guepardo puede alcanzar velocidades de 100-120 km/h."
        }
    ],
    "matematicas": [
        {
            "pregunta": "¿Cuánto es 8 × 7?",
            "opciones": ["54", "56", "64", "49"],
            "respuesta": 1,
            "explicacion": "8 multiplicado por 7 es igual a 56."
        },
        {
            "pregunta": "¿Cuál es el resultado de 15 ÷ 3?",
            "opciones": ["3", "5", "6", "4"],
            "respuesta": 1,
            "explicacion": "15 dividido entre 3 es igual a 5."
        },
        {
            "pregunta": "¿Cuánto es 12²?",
            "opciones": ["144", "121", "132", "169"],
            "respuesta": 0,
            "explicacion": "12 al cuadrado (12 × 12) es igual a 144."
        },
        {
            "pregunta": "¿Cuál es la raíz cuadrada de 64?",
            "opciones": ["6", "7", "8", "9"],
            "respuesta": 2,
            "explicacion": "La raíz cuadrada de 64 es 8 (8 × 8 = 64)."
        }
    ],
    "ciencias": [
        {
            "pregunta": "¿Cuál es el símbolo químico del oro?",
            "opciones": ["Go", "Au", "Ag", "Gd"],
            "respuesta": 1,
            "explicacion": "Au es el símbolo químico del oro (del latín 'aurum')."
        },
        {
            "pregunta": "¿Qué planeta es conocido como el planeta rojo?",
            "opciones": ["Venus", "Marte", "Júpiter", "Saturno"],
            "respuesta": 1,
            "explicacion": "Marte es conocido como el planeta rojo debido al óxido de hierro en su superficie."
        }
    ]
}

class QuizGame:
    def __init__(self):
        self.categoria_actual = "general"
        self.preguntas = preguntas[self.categoria_actual].copy()
        random.shuffle(self.preguntas)
        self.pregunta_actual = 0
        self.puntaje = 0
        self.tiempo_inicio = 0
        self.tiempo_limite = 10
        self.estado = "inicio"  # inicio, jugando, resultado
        self.respuesta_seleccionada = None
        self.mostrar_explicacion = False
        self.botones_opciones = []
        self.mejor_puntaje = self.cargar_mejor_puntaje()
        self.crear_botones()
        
    def cargar_mejor_puntaje(self):
        try:
            if os.path.exists("mejor_puntaje.json"):
                with open("mejor_puntaje.json", "r") as f:
                    data = json.load(f)
                    return data.get(self.categoria_actual, 0)
        except:
            pass
        return 0
    
    def guardar_mejor_puntaje(self):
        try:
            data = {}
            if os.path.exists("mejor_puntaje.json"):
                with open("mejor_puntaje.json", "r") as f:
                    data = json.load(f)
            data[self.categoria_actual] = max(self.mejor_puntaje, self.puntaje)
            with open("mejor_puntaje.json", "w") as f:
                json.dump(data, f)
        except:
            pass
    
    def crear_botones(self):
        # Botones de opciones
        self.botones_opciones = []
        for i in range(4):
            btn = Button(150, 350 + i * 80, 600, 60, "")
            self.botones_opciones.append(btn)
        
        # Botón de siguiente
        self.btn_siguiente = Button(350, 550, 200, 60, "Siguiente", GREEN)
        self.btn_reiniciar = Button(300, 550, 300, 60, "Jugar de Nuevo", BLUE)
        self.btn_cambiar_categoria = Button(300, 620, 300, 60, "Cambiar Categoría", PURPLE)
        
        # Botones de categoría en pantalla de inicio
        self.btn_cat_general = Button(100, 300, 200, 60, "General", BLUE)
        self.btn_cat_matematicas = Button(350, 300, 200, 60, "Matemáticas", GREEN)
        self.btn_cat_ciencias = Button(600, 300, 200, 60, "Ciencias", PURPLE)
        
    def cambiar_categoria(self, categoria):
        self.categoria_actual = categoria
        self.preguntas = preguntas[categoria].copy()
        random.shuffle(self.preguntas)
        self.mejor_puntaje = self.cargar_mejor_puntaje()
        self.reiniciar_juego()
        
    def reiniciar_juego(self):
        self.pregunta_actual = 0
        self.puntaje = 0
        self.estado = "jugando"
        self.respuesta_seleccionada = None
        self.mostrar_explicacion = False
        self.tiempo_inicio = time.time()
        
    def dibujar_pantalla_inicio(self):
        # Fondo
        SCREEN.fill(DARK_BLUE)
        
        # Título
        titulo = TITLE_FONT.render("🎮 QUIZ INTERACTIVO", True, YELLOW)
        SCREEN.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 50))
        
        # Instrucciones
        instrucciones = [
            "¡Bienvenido al Quiz Interactivo!",
            "Tienes 10 segundos para responder cada pregunta.",
            "Selecciona una categoría para comenzar:"
        ]
        
        for i, texto in enumerate(instrucciones):
            texto_surf = SMALL_FONT.render(texto, True, WHITE)
            SCREEN.blit(texto_surf, (SCREEN_WIDTH//2 - texto_surf.get_width()//2, 150 + i*40))
        
        # Dibujar botones de categoría
        if self.btn_cat_general.draw(SCREEN):
            categoria_texto = SMALL_FONT.render("General - Conocimiento básico", True, LIGHT_BLUE)
            SCREEN.blit(categoria_texto, (SCREEN_WIDTH//2 - categoria_texto.get_width()//2, 370))
            
        if self.btn_cat_matematicas.draw(SCREEN):
            categoria_texto = SMALL_FONT.render("Matemáticas - Cálculos y números", True, LIGHT_BLUE)
            SCREEN.blit(categoria_texto, (SCREEN_WIDTH//2 - categoria_texto.get_width()//2, 370))
            
        if self.btn_cat_ciencias.draw(SCREEN):
            categoria_texto = SMALL_FONT.render("Ciencias - Naturaleza y química", True, LIGHT_BLUE)
            SCREEN.blit(categoria_texto, (SCREEN_WIDTH//2 - categoria_texto.get_width()//2, 370))
        
        # Mejor puntuación
        mejor_puntaje_texto = SMALL_FONT.render(
            f"Mejor puntuación ({self.categoria_actual}): {self.mejor_puntaje}/{len(preguntas[self.categoria_actual])}",
            True, YELLOW
        )
        SCREEN.blit(mejor_puntaje_texto, (SCREEN_WIDTH//2 - mejor_puntaje_texto.get_width()//2, 450))
        
        # Instrucción para comenzar
        comenzar_texto = SMALL_FONT.render(
            "Haz clic en una categoría para comenzar", 
            True, WHITE
        )
        SCREEN.blit(comenzar_texto, (SCREEN_WIDTH//2 - comenzar_texto.get_width()//2, 520))
    
    def dibujar_pantalla_juego(self):
        # Fondo
        SCREEN.fill(DARK_BLUE)
        
        # Barra de progreso
        pygame.draw.rect(SCREEN, GRAY, (50, 20, 800, 20), border_radius=10)
        progreso = (self.pregunta_actual / len(self.preguntas)) * 800
        pygame.draw.rect(SCREEN, BLUE, (50, 20, progreso, 20), border_radius=10)
        
        # Mostrar progreso
        progreso_texto = SMALL_FONT.render(
            f"Pregunta {self.pregunta_actual + 1} de {len(self.preguntas)}", 
            True, WHITE
        )
        SCREEN.blit(progreso_texto, (SCREEN_WIDTH//2 - progreso_texto.get_width()//2, 50))
        
        # Puntuación actual
        puntuacion_texto = SCORE_FONT.render(f"Puntos: {self.puntaje}", True, YELLOW)
        SCREEN.blit(puntuacion_texto, (700, 80))
        
        # Temporizador
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)
        
        # Cambiar color del temporizador según el tiempo restante
        color_tiempo = GREEN if tiempo_restante > 5 else YELLOW if tiempo_restante > 2 else RED
        
        tiempo_texto = QUESTION_FONT.render(f"Tiempo: {tiempo_restante:.1f}s", True, color_tiempo)
        SCREEN.blit(tiempo_texto, (100, 80))
        
        # Dibujar barra de tiempo
        pygame.draw.rect(SCREEN, GRAY, (100, 120, 200, 15), border_radius=7)
        barra_tiempo = (tiempo_restante / self.tiempo_limite) * 200
        pygame.draw.rect(SCREEN, color_tiempo, (100, 120, barra_tiempo, 15), border_radius=7)
        
        # Pregunta actual
        pregunta_actual = self.preguntas[self.pregunta_actual]
        pregunta_texto = QUESTION_FONT.render(pregunta_actual["pregunta"], True, WHITE)
        
        # Ajustar pregunta si es muy larga
        if pregunta_texto.get_width() > 800:
            # Dividir pregunta en líneas
            palabras = pregunta_actual["pregunta"].split()
            lineas = []
            linea_actual = ""
            for palabra in palabras:
                prueba_linea = f"{linea_actual} {palabra}".strip()
                if SMALL_FONT.size(prueba_linea)[0] < 800:
                    linea_actual = prueba_linea
                else:
                    lineas.append(linea_actual)
                    linea_actual = palabra
            lineas.append(linea_actual)
            
            # Dibujar cada línea
            for i, linea in enumerate(lineas):
                linea_surf = SMALL_FONT.render(linea, True, WHITE)
                SCREEN.blit(linea_surf, (SCREEN_WIDTH//2 - linea_surf.get_width()//2, 180 + i*35))
        else:
            SCREEN.blit(pregunta_texto, (SCREEN_WIDTH//2 - pregunta_texto.get_width()//2, 180))
        
        # Opciones
        for i, opcion in enumerate(pregunta_actual["opciones"]):
            # Determinar color del botón
            color_boton = BLUE
            
            if self.respuesta_seleccionada is not None:
                if i == pregunta_actual["respuesta"]:
                    color_boton = GREEN  # Respuesta correcta
                elif i == self.respuesta_seleccionada and i != pregunta_actual["respuesta"]:
                    color_boton = RED  # Respuesta incorrecta del usuario
            
            # Crear y dibujar botón con el color apropiado
            btn = Button(150, 280 + i * 80, 600, 60, f"{chr(65+i)}) {opcion}", color_boton)
            self.botones_opciones[i] = btn
            
            if btn.draw(SCREEN):
                # Solo permitir seleccionar si no se ha respondido
                if self.respuesta_seleccionada is None:
                    self.respuesta_seleccionada = i
                    self.tiempo_inicio = time.time()  # Reiniciar tiempo para la explicación
                    
                    # Verificar respuesta
                    if i == pregunta_actual["respuesta"]:
                        self.puntaje += 1
        
        # Si se ha seleccionado una respuesta, mostrar explicación
        if self.respuesta_seleccionada is not None:
            self.mostrar_explicacion = True
            
            # Dibujar cuadro de explicación
            pygame.draw.rect(SCREEN, (30, 30, 60), (100, 600, 700, 80), border_radius=10)
            pygame.draw.rect(SCREEN, BLUE, (100, 600, 700, 80), 2, border_radius=10)
            
            explicacion = pregunta_actual["explicacion"]
            explicacion_texto = SMALL_FONT.render(f"💡 {explicacion}", True, LIGHT_BLUE)
            
            # Ajustar explicación si es muy larga
            if explicacion_texto.get_width() > 680:
                palabras = explicacion.split()
                lineas = []
                linea_actual = ""
                for palabra in palabras:
                    prueba_linea = f"{linea_actual} {palabra}".strip()
                    if SMALL_FONT.size(prueba_linea)[0] < 680:
                        linea_actual = prueba_linea
                    else:
                        lineas.append(linea_actual)
                        linea_actual = palabra
                lineas.append(linea_actual)
                
                for i, linea in enumerate(lineas):
                    linea_surf = SMALL_FONT.render(linea, True, LIGHT_BLUE)
                    SCREEN.blit(linea_surf, (110, 610 + i*25))
            else:
                SCREEN.blit(explicacion_texto, (110, 625))
            
            # Botón siguiente
            if self.btn_siguiente.draw(SCREEN):
                self.siguiente_pregunta()
        
        # Verificar si se acabó el tiempo
        if tiempo_restante <= 0 and self.respuesta_seleccionada is None:
            self.respuesta_seleccionada = -1  # Marcar como tiempo agotado
            self.mostrar_explicacion = True
            
            # Mostrar mensaje de tiempo agotado
            tiempo_texto = QUESTION_FONT.render("⏰ ¡Tiempo agotado!", True, RED)
            SCREEN.blit(tiempo_texto, (SCREEN_WIDTH//2 - tiempo_texto.get_width()//2, 600))
            
            # Botón siguiente
            if self.btn_siguiente.draw(SCREEN):
                self.siguiente_pregunta()
    
    def siguiente_pregunta(self):
        self.pregunta_actual += 1
        self.respuesta_seleccionada = None
        self.mostrar_explicacion = False
        self.tiempo_inicio = time.time()
        
        if self.pregunta_actual >= len(self.preguntas):
            self.estado = "resultado"
            if self.puntaje > self.mejor_puntaje:
                self.mejor_puntaje = self.puntaje
                self.guardar_mejor_puntaje()
    
    def dibujar_pantalla_resultado(self):
        # Fondo
        SCREEN.fill(DARK_BLUE)
        
        # Título de resultados
        resultado_texto = TITLE_FONT.render("🏁 RESULTADOS", True, YELLOW)
        SCREEN.blit(resultado_texto, (SCREEN_WIDTH//2 - resultado_texto.get_width()//2, 50))
        
        # Puntuación
        puntuacion_final = SCORE_FONT.render(
            f"Puntuación Final: {self.puntaje}/{len(self.preguntas)}", 
            True, WHITE
        )
        SCREEN.blit(puntuacion_final, (SCREEN_WIDTH//2 - puntuacion_final.get_width()//2, 150))
        
        # Porcentaje
        porcentaje = (self.puntaje / len(self.preguntas)) * 100
        porcentaje_texto = QUESTION_FONT.render(f"{porcentaje:.1f}% de aciertos", True, LIGHT_BLUE)
        SCREEN.blit(porcentaje_texto, (SCREEN_WIDTH//2 - porcentaje_texto.get_width()//2, 210))
        
        # Mejor puntuación
        mejor_texto = SMALL_FONT.render(
            f"Mejor puntuación en {self.categoria_actual}: {self.mejor_puntaje}/{len(self.preguntas)}",
            True, YELLOW
        )
        SCREEN.blit(mejor_texto, (SCREEN_WIDTH//2 - mejor_texto.get_width()//2, 260))
        
        # Mensaje según puntuación
        mensajes = [
            (100, "🏆 ¡PERFECTO! ¡Eres un genio!", GREEN),
            (80, "🎯 ¡Excelente! Sabes mucho", GREEN),
            (60, "👍 Buen trabajo, sigue así", YELLOW),
            (40, "💪 No está mal, puedes mejorar", YELLOW),
            (0, "📚 Sigue practicando, ¡tú puedes!", RED)
        ]
        
        mensaje_final = ""
        color_mensaje = WHITE
        for limite, mensaje, color in mensajes:
            if porcentaje >= limite:
                mensaje_final = mensaje
                color_mensaje = color
                break
        
        mensaje_texto = QUESTION_FONT.render(mensaje_final, True, color_mensaje)
        SCREEN.blit(mensaje_texto, (SCREEN_WIDTH//2 - mensaje_texto.get_width()//2, 320))
        
        # Detalles de las respuestas
        detalles_y = 380
        detalles_texto = SMALL_FONT.render("Resumen de respuestas:", True, WHITE)
        SCREEN.blit(detalles_texto, (SCREEN_WIDTH//2 - detalles_texto.get_width()//2, detalles_y))
        
        # Botones
        if self.btn_reiniciar.draw(SCREEN):
            self.reiniciar_juego()
            
        if self.btn_cambiar_categoria.draw(SCREEN):
            self.estado = "inicio"
    
    def manejar_eventos(self, event):
        if self.estado == "inicio":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_cat_general.rect.collidepoint(event.pos):
                    self.cambiar_categoria("general")
                elif self.btn_cat_matematicas.rect.collidepoint(event.pos):
                    self.cambiar_categoria("matematicas")
                elif self.btn_cat_ciencias.rect.collidepoint(event.pos):
                    self.cambiar_categoria("ciencias")
                    
        elif self.estado == "jugando":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clics en botones de opciones
                for i, btn in enumerate(self.botones_opciones):
                    if btn.rect.collidepoint(event.pos) and self.respuesta_seleccionada is None:
                        self.respuesta_seleccionada = i
                        self.tiempo_inicio = time.time()
                        
                        # Verificar respuesta
                        if i == self.preguntas[self.pregunta_actual]["respuesta"]:
                            self.puntaje += 1
                
                # Verificar botón siguiente
                if self.btn_siguiente.rect.collidepoint(event.pos) and self.respuesta_seleccionada is not None:
                    self.siguiente_pregunta()
                    
        elif self.estado == "resultado":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_reiniciar.rect.collidepoint(event.pos):
                    self.reiniciar_juego()
                elif self.btn_cambiar_categoria.rect.collidepoint(event.pos):
                    self.estado = "inicio"
    
    def dibujar(self):
        if self.estado == "inicio":
            self.dibujar_pantalla_inicio()
        elif self.estado == "jugando":
            self.dibujar_pantalla_juego()
        elif self.estado == "resultado":
            self.dibujar_pantalla_resultado()
        
        # Actualizar pantalla
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = QuizGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game.estado == "jugando" and game.respuesta_seleccionada is None:
                    # Permitir respuesta con teclas 1-4
                    if event.key == pygame.K_1 or event.key == pygame.K_a:
                        game.respuesta_seleccionada = 0
                    elif event.key == pygame.K_2 or event.key == pygame.K_b:
                        game.respuesta_seleccionada = 1
                    elif event.key == pygame.K_3 or event.key == pygame.K_c:
                        game.respuesta_seleccionada = 2
                    elif event.key == pygame.K_4 or event.key == pygame.K_d:
                        game.respuesta_seleccionada = 3
                    
                    # Verificar respuesta si se seleccionó
                    if game.respuesta_seleccionada is not None:
                        if game.respuesta_seleccionada == game.preguntas[game.pregunta_actual]["respuesta"]:
                            game.puntaje += 1
            
            game.manejar_eventos(event)
        
        # Actualizar lógica del juego
        if game.estado == "jugando" and game.respuesta_seleccionada is None:
            # Verificar tiempo límite
            tiempo_transcurrido = time.time() - game.tiempo_inicio
            if tiempo_transcurrido > game.tiempo_limite:
                game.respuesta_seleccionada = -1  # Tiempo agotado
        
        # Dibujar todo
        game.dibujar()
        
        # Controlar FPS
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()