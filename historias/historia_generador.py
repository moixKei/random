import pygame
import random
import sys
import json
import os
from enum import Enum

pygame.init()
pygame.mixer.init()

ANCHO = 1000
ALTO = 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Generador de Historias Creativo")

NEGRO = (20, 20, 30)
BLANCO = (255, 255, 255)
AZUL = (30, 144, 255)
VERDE = (60, 180, 100)
ROJO = (220, 60, 80)
AMARILLO = (255, 215, 0)
NARANJA = (255, 165, 0)
MORADO = (147, 112, 219)
GRIS = (100, 100, 120)
GRIS_CLARO = (200, 200, 210)
AZUL_CLARO = (173, 216, 230)
VERDE_CLARO = (144, 238, 144)

try:
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_grande = pygame.font.Font(None, 48)
    fuente_normal = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 28)
    fuente_muy_pequena = pygame.font.Font(None, 22)
    fuente_historia = pygame.font.Font(None, 32)
except:
    fuente_titulo = pygame.font.SysFont('arial', 72, bold=True)
    fuente_grande = pygame.font.SysFont('arial', 48)
    fuente_normal = pygame.font.SysFont('arial', 36)
    fuente_pequena = pygame.font.SysFont('arial', 28)
    fuente_muy_pequena = pygame.font.SysFont('arial', 22)
    fuente_historia = pygame.font.SysFont('arial', 32)

try:
    sonido_click = pygame.mixer.Sound(buffer=bytes([128] * 400))
    sonido_historia = pygame.mixer.Sound(buffer=bytes([128] * 600))
    sonido_guardar = pygame.mixer.Sound(buffer=bytes([128] * 500))
    
    sonido_click.set_volume(0.3)
    sonido_historia.set_volume(0.4)
    sonido_guardar.set_volume(0.4)
except:
    sonido_click = sonido_historia = sonido_guardar = None

ELEMENTOS_HISTORIAS = {
    "PERSONAJES": {
        "FANTASÍA": [
            "un dragón anciano sabio", "una princesa guerrera", "un mago olvidadizo", 
            "un elfo curioso", "un hada traviesa", "un guerrero legendario",
            "un unicornio mágico", "un duende bromista", "un gigante amable",
            "una sirena cantante", "un fénix renaciente", "un licántropo solitario"
        ],
        "CIENCIA FICCIÓN": [
            "un androide sensible", "un piloto espacial", "un científico loco",
            "un alienígena pacifista", "un hacker rebelde", "un cazarrecompensas interestelar",
            "un explorador dimensional", "un robot doméstico", "un mutante con poderes",
            "un viajero en el tiempo", "un clon confundido", "un cyborg rebelde"
        ],
        "AVENTURA": [
            "un pirata buscador de tesoros", "un explorador intrépido", "un detective astuto",
            "un arqueólogo aventurero", "un montañista valiente", "un periodista investigador",
            "un ladrón de guante blanco", "un espía misterioso", "un superviviente experimentado",
            "un cazador de reliquias", "un fotógrafo viajero", "un mercenario solitario"
        ],
        "HISTÓRICO": [
            "un caballero medieval", "una reina poderosa", "un inventor renacentista",
            "un filósofo griego", "un samurái honorable", "un vikingo explorador",
            "un revolucionario idealista", "un artista bohemio", "un sabio oriental",
            "un noble intrigante", "un campesino valiente", "un monje erudito"
        ]
    },
    "LUGARES": {
        "MISTERIOSOS": [
            "en un bosque encantado donde los árboles susurran secretos",
            "en una ciudad subterránea olvidada por el tiempo",
            "en un castillo flotante entre las nubes",
            "en una biblioteca infinita con libros vivientes",
            "en un jardín donde las flores cantan al amanecer",
            "en una isla que aparece solo en los sueños",
            "en un mercado mágico que solo abre a medianoche",
            "en un desierto de cristales que reflejan el futuro",
            "en una cueva con pinturas que cobran vida",
            "en un laberinto que cambia con cada decisión"
        ],
        "FUTURISTAS": [
            "en una megaciudad de neón y hologramas",
            "en una colonia en Marte con cúpulas de biósfera",
            "en una estación espacial en órbita alrededor de Júpiter",
            "en el ciberespacio, navegando por ríos de datos",
            "en una fábrica automatizada dirigida por IA",
            "en un mundo virtual de realidad aumentada",
            "en una nave generacional rumbo a Alpha Centauri",
            "en una base científica en las profundidades oceánicas",
            "en una ciudad flotante en los cielos de Venus",
            "en una realidad paralela con leyes físicas diferentes"
        ],
        "EXÓTICOS": [
            "en las ruinas de una civilización perdida en la selva",
            "en un templo antiguo custodiado por estatuas vivientes",
            "en un oasis oculto en el corazón del desierto",
            "en un volcán inactivo con cristales luminosos",
            "en las catacumbas bajo una ciudad antigua",
            "en un valle prohibido donde el tiempo se detiene",
            "en un pantano habitado por criaturas ancestrales",
            "en un acantilado con vista a un mar de estrellas",
            "en una gruta de hielo con esculturas naturales",
            "en un puente entre dos mundos en el crepúsculo"
        ],
        "COTIDIANOS": [
            "en una cafetería acogedora durante una tormenta",
            "en un parque abandonado al atardecer",
            "en una librería de segunda mano llena de secretos",
            "en un apartamento pequeño con vista a la ciudad",
            "en una estación de tren en una noche lluviosa",
            "en un museo vacío después del horario de cierre",
            "en un mercado callejero lleno de colores y aromas",
            "en una biblioteca universitaria durante la noche",
            "en un puente viejo sobre un río tranquilo",
            "en una azotea con vista a los rascacielos"
        ]
    },
    "ACCIONES": {
        "DRAMÁTICAS": [
            "descubrió un secreto que cambiaría el curso de la historia",
            "luchó contra su propio destino escrito en las estrellas",
            "encontró algo que no debería haber encontrado jamás",
            "tomó una decisión que dividió su alma en dos",
            "vio algo que nadie más podía ver ni creer",
            "perdió lo más preciado para ganar algo invaluable",
            "rompió las reglas del universo por amor",
            "enfrentó su mayor miedo solo para descubrir otro aún mayor",
            "traicionó a alguien para salvar a muchos",
            "sacrificó todo por una verdad incómoda"
        ],
        "AVENTURERAS": [
            "descubrió un mapa que conducía a lo imposible",
            "desenterró un artefacto de poder inimaginable",
            "siguió una pista que lo llevó más allá de la realidad",
            "sobrevivió a algo que nadie había sobrevivido antes",
            "encontró una puerta a un mundo que no debería existir",
            "descifró un código que revelaba una conspiración milenaria",
            "persiguió una leyenda que resultó ser cierta",
            "encontró una criatura que se creía extinta",
            "descubrió una ciudad perdida bajo sus pies",
            "siguió un rastro de migas de pan cósmicas"
        ],
        "MISTERIOSAS": [
            "recibió una carta de alguien que había muerto años atrás",
            "vio su propio reflejo haciendo cosas diferentes",
            "encontró un diario que predecía su futuro exacto",
            "oyó una voz que solo él podía escuchar",
            "soñó con eventos que comenzaron a suceder en la realidad",
            "descubrió que era alguien más en una vida pasada",
            "encontró un objeto que solo funcionaba para él",
            "vio sombras moviéndose contra las leyes de la física",
            "oyó una música que nadie más podía percibir",
            "encontró una puerta en su casa que no recordaba"
        ],
        "INSPIRADORAS": [
            "aprendió que la verdadera magia está en los pequeños actos",
            "descubrió que su mayor debilidad era su mayor fortaleza",
            "encontró la belleza en lo imperfecto y caótico",
            "enseñó algo valioso a quien menos lo esperaba",
            "creó algo hermoso a partir de fragmentos rotos",
            "encontró la paz en medio del caos absoluto",
            "descubrió que el viaje era más importante que el destino",
            "aprendió a bailar bajo la lluvia de problemas",
            "encontró la luz en la oscuridad más profunda",
            "descubrió que el amor era la fuerza más poderosa"
        ]
    },
    "CONFLICTOS": {
        "INTERNOS": [
            "mientras lidiaba con el peso de un secreto inconfesable",
            "aunque su corazón le decía una cosa y su mente otra",
            "mientras luchaba contra sus propios demonios interiores",
            "a pesar del miedo que paralizaba su alma",
            "mientras intentaba encontrar su verdadero propósito",
            "aunque dudaba de todo lo que alguna vez creyó cierto",
            "mientras buscaba redimirse de un pasado oscuro",
            "a pesar de sentirse perdido en su propio camino",
            "mientras enfrentaba la soledad más absoluta",
            "aunque sabía que cada elección tenía un precio"
        ],
        "EXTERNOS": [
            "mientras una fuerza oscura amenazaba con destruirlo todo",
            "aunque todo el mundo estaba en su contra",
            "mientras una maldición antigua despertaba de su sueño",
            "a pesar de las leyes que prohibían su búsqueda",
            "mientras el tiempo se agotaba inexorablemente",
            "aunque las probabilidades de éxito eran mínimas",
            "mientras una guerra inminente se cernía sobre el horizonte",
            "a pesar de las trampas y engaños en cada esquina",
            "mientras la naturaleza misma se rebelaba contra él",
            "aunque cada paso era más peligroso que el anterior"
        ],
        "SOCIALES": [
            "mientras navegaba por intrigas políticas mortales",
            "aunque su propia familia lo había desterrado",
            "mientras la sociedad lo rechazaba por ser diferente",
            "a pesar de los prejuicios y las falsas acusaciones",
            "mientras intentaba unir a facciones enemigas",
            "aunque todos creían que estaba loco o perdido",
            "mientras luchaba por justicia en un mundo corrupto",
            "a pesar de las tradiciones que lo ataban al pasado",
            "mientras buscaba aceptación en un mundo hostil",
            "aunque el sistema estaba diseñado para que fracasara"
        ],
        "SOBRENATURALES": [
            "mientras las leyes de la realidad comenzaban a deshilacharse",
            "aunque criaturas de pesadilla emergían de las sombras",
            "mientras el velo entre mundos se hacía más delgado",
            "a pesar de las profecías que predecían su fracaso",
            "mientras la magia antigua despertaba de su letargo",
            "aunque los dioses jugaban con su destino como un tablero",
            "mientras los muertos comenzaban a caminar entre los vivos",
            "a pesar de los portales que se abrían a dimensiones extrañas",
            "mientras los elementos se descontrolaban sin explicación",
            "aunque su propia existencia comenzaba a desvanecerse"
        ]
    },
    "DESENLACES": {
        "FELICES": [
            "y finalmente encontró la paz que tanto anhelaba.",
            "descubriendo que el amor verdadero era la respuesta.",
            "y comprendió que el viaje valía más que el destino.",
            "hallando su lugar en el vasto universo.",
            "y vivió para contar la leyenda con una sonrisa.",
            "encontrando que la felicidad estaba en las pequeñas cosas.",
            "y su historia inspiró a generaciones futuras.",
            "descubriendo que tenía el poder dentro de sí mismo.",
            "y el mundo fue un lugar mejor gracias a su acción.",
            "encontrando que la verdadera riqueza era la amistad."
        ],
        "TRÁGICOS": [
            "pero el precio a pagar fue demasiado alto.",
            "y se perdió en la eternidad que había creado.",
            "descubriendo que algunas verdades es mejor no conocerlas.",
            "y quedó atrapado en el ciclo que intentó romper.",
            "pero la victoria tuvo un sabor amargo y solitario.",
            "y su sacrificio fue olvidado por aquellos que salvó.",
            "descubriendo que había llegado demasiado tarde.",
            "y el remordimiento sería su compañero eterno.",
            "pero algunas heridas nunca sanan completamente.",
            "y aprendió que no todos los héroes tienen final feliz."
        ],
        "AMBIGUOS": [
            "y nunca supo si había hecho lo correcto.",
            "dejando más preguntas que respuestas en su camino.",
            "y la historia continuó, con o sin él.",
            "descubriendo que cada fin es solo un nuevo comienzo.",
            "y el misterio permaneció, esperando al próximo buscador.",
            "dejando un legado que sería interpretado de mil maneras.",
            "y la verdad quedó oculta en las sombras de la duda.",
            "descubriendo que algunas batallas nunca terminan.",
            "y el eco de sus acciones resonó en el vacío.",
            "dejando que el tiempo decidiera su lugar en la historia."
        ],
        "SORPRESIVOS": [
            "pero resultó que todo era parte de un plan mayor.",
            "descubriendo que era el villano de otra historia.",
            "y se dio cuenta de que había estado soñando todo el tiempo.",
            "pero la realidad era mucho más extraña de lo imaginado.",
            "descubriendo que el verdadero tesoro eran los amigos hechos.",
            "y todo volvió a empezar desde el principio.",
            "pero nadie creyó su increíble historia.",
            "descubriendo que tenía el poder de reescribir su destino.",
            "y el giro final dejó a todos sin aliento.",
            "pero el mayor misterio aún estaba por resolverse."
        ]
    }
}

class Genero(Enum):
    FANTASIA = 1
    CIENCIA_FICCION = 2
    AVENTURA = 3
    MISTERIO = 4
    DRAMA = 5

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
        
        texto_surf = fuente_pequena.render(self.texto, True, BLANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def esta_presionado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.hover
        return False

class ElementoSelector:
    def __init__(self, x, y, ancho, alto, titulo, elementos, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.titulo = titulo
        self.elementos = elementos
        self.color = color
        self.elemento_seleccionado = None
        self.scroll_y = 0
        self.max_scroll = 0
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, (30, 30, 40), self.rect, border_radius=10)
        pygame.draw.rect(superficie, self.color, self.rect, 2, border_radius=10)
        
        titulo_surf = fuente_pequena.render(self.titulo, True, self.color)
        superficie.blit(titulo_surf, (self.rect.x + 10, self.rect.y + 10))
        
        area_elementos = pygame.Rect(self.rect.x + 10, self.rect.y + 40, 
                                   self.rect.width - 20, self.rect.height - 50)
        pygame.draw.rect(superficie, (40, 40, 50), area_elementos, border_radius=5)
        
        clip_rect = pygame.Rect(area_elementos)
        superficie.set_clip(clip_rect)
        
        y_pos = area_elementos.y + 10 - self.scroll_y
        for i, elemento in enumerate(self.elementos):
            elemento_rect = pygame.Rect(area_elementos.x + 5, y_pos, 
                                      area_elementos.width - 10, 40)
            
            color_elemento = VERDE_CLARO if elemento == self.elemento_seleccionado else AZUL_CLARO
            
            mouse_pos = pygame.mouse.get_pos()
            if elemento_rect.collidepoint(mouse_pos):
                color_elemento = (color_elemento[0] + 20, 
                                color_elemento[1] + 20, 
                                color_elemento[2] + 20)
            
            pygame.draw.rect(superficie, color_elemento, elemento_rect, border_radius=5)
            pygame.draw.rect(superficie, self.color, elemento_rect, 1, border_radius=5)
            
            texto = elemento
            if len(texto) > 40:
                texto = texto[:37] + "..."
            
            elemento_surf = fuente_muy_pequena.render(texto, True, NEGRO)
            superficie.blit(elemento_surf, (elemento_rect.x + 10, elemento_rect.y + 12))
            
            y_pos += 45
        
        self.max_scroll = max(0, y_pos - area_elementos.height + 20)
        superficie.set_clip(None)
        
        if self.max_scroll > 0:
            scroll_ratio = self.scroll_y / self.max_scroll
            barra_altura = area_elementos.height * (area_elementos.height / (y_pos - area_elementos.y))
            barra_y = area_elementos.y + scroll_ratio * (area_elementos.height - barra_altura)
            
            pygame.draw.rect(superficie, GRIS, 
                           (area_elementos.right - 5, barra_y, 5, barra_altura), 
                           border_radius=2)
    
    def manejar_evento(self, evento):
        area_elementos = pygame.Rect(self.rect.x + 10, self.rect.y + 40, 
                                   self.rect.width - 20, self.rect.height - 50)
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: 
                y_pos = area_elementos.y + 10 - self.scroll_y
                for elemento in self.elementos:
                    elemento_rect = pygame.Rect(area_elementos.x + 5, y_pos, 
                                              area_elementos.width - 10, 40)
                    
                    if elemento_rect.collidepoint(evento.pos):
                        self.elemento_seleccionado = elemento
                        if sonido_click:
                            sonido_click.play()
                        return True
                    
                    y_pos += 45
            
            elif evento.button == 4:  
                self.scroll_y = max(0, self.scroll_y - 20)
                return True
            elif evento.button == 5:
                self.scroll_y = min(self.max_scroll, self.scroll_y + 20)
                return True
        
        return False

class GeneradorHistorias:
    def __init__(self):
        self.estado = "MENU"
        self.historia_actual = ""
        self.historias_guardadas = []
        self.genero_actual = Genero.FANTASIA
        self.longitud = "MEDIA" 
        self.tema_actual = None
        
        # Selectores de elementos
        self.selectores = []
        self.crear_selectores()
        
        self.botones = []
        self.crear_botones()
        
        self.cargar_historias()
    
    def crear_selectores(self):
        x_pos = 50
        y_pos = 150
        ancho = 250
        alto = 300
        
        categorias = [
            ("PERSONAJE", "PERSONAJES"),
            ("LUGAR", "LUGARES"),
            ("ACCIÓN", "ACCIONES"),
            ("CONFLICTO", "CONFLICTOS"),
            ("DESENLACE", "DESENLACES")
        ]
        
        colores = [AZUL, VERDE, NARANJA, MORADO, ROJO]
        
        self.selectores = []
        for i, (titulo, clave) in enumerate(categorias):
            elementos = self.obtener_elementos_por_genero(clave)
            
            selector = ElementoSelector(x_pos, y_pos, ancho, alto, 
                                       titulo, elementos, colores[i])
            self.selectores.append(selector)
            x_pos += ancho + 20
    
    def obtener_elementos_por_genero(self, categoria):
        if categoria == "PERSONAJES":
            clave_genero = {
                Genero.FANTASIA: "FANTASÍA",
                Genero.CIENCIA_FICCION: "CIENCIA FICCIÓN",
                Genero.AVENTURA: "AVENTURA",
                Genero.MISTERIO: "AVENTURA", 
                Genero.DRAMA: "HISTÓRICO"
            }
            subcategoria = clave_genero[self.genero_actual]
            return ELEMENTOS_HISTORIAS[categoria][subcategoria]
        
        elif categoria == "LUGARES":
            subcategorias = ["MISTERIOSOS", "FUTURISTAS", "EXÓTICOS", "COTIDIANOS"]
            todos_lugares = []
            for sub in subcategorias:
                todos_lugares.extend(ELEMENTOS_HISTORIAS[categoria][sub][:3])
            return todos_lugares
        
        elif categoria == "ACCIONES":
            subcategorias = ["DRAMÁTICAS", "AVENTURERAS", "MISTERIOSAS", "INSPIRADORAS"]
            todas_acciones = []
            for sub in subcategorias:
                todas_acciones.extend(ELEMENTOS_HISTORIAS[categoria][sub][:3])
            return todas_acciones
        
        elif categoria == "CONFLICTOS":
            subcategorias = ["INTERNOS", "EXTERNOS", "SOCIALES", "SOBRENATURALES"]
            todos_conflictos = []
            for sub in subcategorias:
                todos_conflictos.extend(ELEMENTOS_HISTORIAS[categoria][sub][:3])
            return todos_conflictos
        
        elif categoria == "DESENLACES":
            subcategorias = ["FELICES", "TRÁGICOS", "AMBIGUOS", "SORPRESIVOS"]
            todos_desenlaces = []
            for sub in subcategorias:
                todos_desenlaces.extend(ELEMENTOS_HISTORIAS[categoria][sub][:3])
            return todos_desenlaces
        
        return []
    
    def crear_botones(self):
        centro_x = ANCHO // 2
        
        self.botones_menu = [
            Boton(centro_x - 150, 200, 300, 60, "GENERAR HISTORIA", VERDE, (80, 220, 80)),
            Boton(centro_x - 150, 280, 300, 60, "BIBLIOTECA", AZUL, (70, 170, 255)),
            Boton(centro_x - 150, 360, 300, 60, "CONFIGURACIÓN", AMARILLO, (255, 235, 80)),
            Boton(centro_x - 150, 440, 300, 60, "AYUDA", MORADO, (167, 132, 219)),
            Boton(centro_x - 150, 520, 300, 60, "SALIR", ROJO, (255, 100, 100))
        ]
        
        self.botones_generacion = [
            Boton(50, ALTO - 80, 200, 50, "🎲 ALEATORIO", AZUL, (70, 170, 255)),
            Boton(ANCHO - 250, ALTO - 80, 200, 50, "💾 GUARDAR", VERDE, (80, 220, 80)),
            Boton(ANCHO - 250, ALTO - 140, 200, 50, "🏠 MENÚ", MORADO, (167, 132, 219)),
            Boton(ANCHO // 2 - 100, ALTO - 80, 200, 50, "🔄 REGENERAR", NARANJA, (255, 185, 50))
        ]
    
    def cargar_historias(self):
        try:
            if os.path.exists("historias_guardadas.json"):
                with open("historias_guardadas.json", "r", encoding='utf-8') as f:
                    self.historias_guardadas = json.load(f)
        except:
            self.historias_guardadas = []
    
    def guardar_historia(self, historia, titulo=""):
        if not titulo:
            titulo = f"Historia {len(self.historias_guardadas) + 1}"
        
        historia_data = {
            "titulo": titulo,
            "texto": historia,
            "fecha": pygame.time.get_ticks() // 1000,
            "genero": self.genero_actual.name,
            "longitud": self.longitud
        }
        
        self.historias_guardadas.append(historia_data)
        
        try:
            with open("historias_guardadas.json", "w", encoding='utf-8') as f:
                json.dump(self.historias_guardadas, f, ensure_ascii=False, indent=2)
        except:
            pass
        
        if sonido_guardar:
            sonido_guardar.play()
    
    def generar_historia(self, aleatorio=False):
        elementos = {}
        
        if aleatorio:
            for selector in self.selectores:
                if selector.elementos:
                    selector.elemento_seleccionado = random.choice(selector.elementos)
                    elementos[selector.titulo.lower()] = selector.elemento_seleccionado
        else:
            for selector in self.selectores:
                if selector.elemento_seleccionado:
                    elementos[selector.titulo.lower()] = selector.elemento_seleccionado
                elif selector.elementos:
                    selector.elemento_seleccionado = random.choice(selector.elementos)
                    elementos[selector.titulo.lower()] = selector.elemento_seleccionado
        
        if self.longitud == "CORTA":
            historia = f"{elementos.get('personaje', 'Alguien')} {elementos.get('lugar', 'en algún lugar')} {elementos.get('acción', 'hizo algo')}."
        
        elif self.longitud == "MEDIA":
            historia = f"{elementos.get('personaje', 'Alguien')} {elementos.get('lugar', 'en algún lugar')} {elementos.get('acción', 'hizo algo')}, {elementos.get('conflicto', 'aunque enfrentó dificultades')} {elementos.get('desenlace', 'y así terminó la historia')}"
        
        else: 
            historia_parts = [
                f"Érase una vez {elementos.get('personaje', 'un personaje')}.",
                f"Este ser se encontraba {elementos.get('lugar', 'en un lugar misterioso')},",
                f"cuando de repente {elementos.get('acción', 'sucedió algo extraordinario')}.",
                f"Sin embargo, {elementos.get('conflicto', 'un gran obstáculo apareció en su camino')},",
                f"y después de mucho esfuerzo, {elementos.get('desenlace', 'la historia llegó a su conclusión')}"
            ]
            historia = " ".join(historia_parts)
        
        self.historia_actual = historia
        
        if sonido_historia:
            sonido_historia.play()
        
        return historia
    
    def dibujar_menu(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("📚 GENERADOR DE HISTORIAS", True, BLANCO)
        sombra = fuente_titulo.render("📚 GENERADOR DE HISTORIAS", True, (50, 50, 70))
        ventana.blit(sombra, (ANCHO//2 - titulo.get_width()//2 + 3, 103))
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        subtitulo = fuente_pequena.render("Crea historias increíbles con elementos aleatorios", 
                                         True, GRIS_CLARO)
        ventana.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 160))
        
        # Dibujar botones
        for boton in self.botones_menu:
            boton.dibujar(ventana)
        
        self.dibujar_ejemplo_decorativo()
    
    def dibujar_ejemplo_decorativo(self):
        ejemplo = "Un valiente explorador en una jungla perdida descubrió las ruinas de una civilización olvidada..."
        
        ejemplo_rect = pygame.Rect(100, ALTO - 120, ANCHO - 200, 80)
        pygame.draw.rect(ventana, (30, 30, 40), ejemplo_rect, border_radius=10)
        pygame.draw.rect(ventana, AZUL, ejemplo_rect, 2, border_radius=10)
        
        ejemplo_surf = fuente_muy_pequena.render(ejemplo, True, GRIS_CLARO)
        ventana.blit(ejemplo_surf, (ejemplo_rect.x + 10, ejemplo_rect.y + 10))
    
    def dibujar_generacion(self):
        ventana.fill(NEGRO)
        
        # Título
        titulo = fuente_grande.render("GENERAR HISTORIA", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 30))
        
        config_texto = fuente_pequena.render(
            f"Género: {self.genero_actual.name.title()} | Longitud: {self.longitud}", 
            True, GRIS_CLARO)
        ventana.blit(config_texto, (ANCHO//2 - config_texto.get_width()//2, 80))
        
        for selector in self.selectores:
            selector.dibujar(ventana)
        
        if self.historia_actual:
            self.dibujar_historia_generada()
        
        for boton in self.botones_generacion:
            boton.dibujar(ventana)
    
    def dibujar_historia_generada(self):
        historia_rect = pygame.Rect(50, 470, ANCHO - 100, 150)
        pygame.draw.rect(ventana, (30, 30, 40), historia_rect, border_radius=10)
        pygame.draw.rect(ventana, VERDE, historia_rect, 2, border_radius=10)
        
        titulo_area = fuente_pequena.render("HISTORIA GENERADA:", True, VERDE)
        ventana.blit(titulo_area, (historia_rect.x + 10, historia_rect.y - 25))
        
        palabras = self.historia_actual.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            prueba_linea = f"{linea_actual} {palabra}".strip()
            if fuente_historia.size(prueba_linea)[0] < historia_rect.width - 20:
                linea_actual = prueba_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        
        if linea_actual:
            lineas.append(linea_actual)
        
        for i, linea in enumerate(lineas):
            linea_surf = fuente_historia.render(linea, True, BLANCO)
            ventana.blit(linea_surf, (historia_rect.x + 10, historia_rect.y + 10 + i * 35))
    
    def dibujar_biblioteca(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("BIBLIOTECA", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        if not self.historias_guardadas:
            mensaje = fuente_normal.render("No hay historias guardadas aún.", True, GRIS_CLARO)
            ventana.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 200))
            
            instruccion = fuente_pequena.render("Genera y guarda historias para verlas aquí.", 
                                               True, GRIS_CLARO)
            ventana.blit(instruccion, (ANCHO//2 - instruccion.get_width()//2, 250))
        else:
            historia_area = pygame.Rect(50, 120, ANCHO - 100, ALTO - 200)
            pygame.draw.rect(ventana, (30, 30, 40), historia_area, border_radius=10)
            pygame.draw.rect(ventana, AZUL, historia_area, 2, border_radius=10)
            
            y_pos = historia_area.y + 10
            for i, historia in enumerate(self.historias_guardadas[-10:]):  # Últimas 10
                hist_rect = pygame.Rect(historia_area.x + 10, y_pos, 
                                      historia_area.width - 20, 80)
                pygame.draw.rect(ventana, (40, 40, 50), hist_rect, border_radius=5)
                pygame.draw.rect(ventana, GRIS_CLARO, hist_rect, 1, border_radius=5)
                
                titulo_hist = fuente_pequena.render(
                    f"{historia['titulo']} ({historia['genero'].title()})", 
                    True, AZUL)
                ventana.blit(titulo_hist, (hist_rect.x + 10, hist_rect.y + 10))
                
                fragmento = historia['texto'][:80] + "..." if len(historia['texto']) > 80 else historia['texto']
                texto_hist = fuente_muy_pequena.render(fragmento, True, GRIS_CLARO)
                ventana.blit(texto_hist, (hist_rect.x + 10, hist_rect.y + 35))
                
                y_pos += 90
        
        boton_volver = Boton(ANCHO//2 - 100, ALTO - 80, 200, 50, 
                            "VOLVER AL MENÚ", AZUL, (70, 170, 255))
        boton_volver.dibujar(ventana)
        return boton_volver
    
    def dibujar_configuracion(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("⚙️ CONFIGURACIÓN", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        centro_x = ANCHO // 2
        
        genero_texto = fuente_normal.render("Seleccionar Género:", True, BLANCO)
        ventana.blit(genero_texto, (centro_x - genero_texto.get_width()//2, 150))
        
        generos = ["FANTASÍA", "CIENCIA FICCIÓN", "AVENTURA", "MISTERIO", "DRAMA"]
        genero_actual_texto = fuente_grande.render(
            generos[self.genero_actual.value - 1], True, AZUL)
        ventana.blit(genero_actual_texto, (centro_x - genero_actual_texto.get_width()//2, 200))
        
        longitud_texto = fuente_normal.render("Longitud de la Historia:", True, BLANCO)
        ventana.blit(longitud_texto, (centro_x - longitud_texto.get_width()//2, 300))
        
        longitud_actual_texto = fuente_grande.render(self.longitud, True, VERDE)
        ventana.blit(longitud_actual_texto, (centro_x - longitud_actual_texto.get_width()//2, 350))
        
        explicaciones = [
            "CORTA: Personaje + Lugar + Acción",
            "MEDIA: Incluye conflicto y desenlace",
            "LARGA: Historia completa con detalles"
        ]
        
        for i, texto in enumerate(explicaciones):
            exp = fuente_pequena.render(texto, True, GRIS_CLARO)
            ventana.blit(exp, (centro_x - exp.get_width()//2, 400 + i * 30))
        
        boton_cambiar_genero = Boton(centro_x - 150, 500, 300, 50, 
                                    "CAMBIAR GÉNERO", AZUL, (70, 170, 255))
        boton_cambiar_longitud = Boton(centro_x - 150, 560, 300, 50, 
                                      "CAMBIAR LONGITUD", VERDE, (80, 220, 80))
        boton_volver = Boton(centro_x - 150, 620, 300, 50, 
                            "VOLVER AL MENÚ", MORADO, (167, 132, 219))
        
        boton_cambiar_genero.dibujar(ventana)
        boton_cambiar_longitud.dibujar(ventana)
        boton_volver.dibujar(ventana)
        
        return boton_cambiar_genero, boton_cambiar_longitud, boton_volver
    
    def dibujar_ayuda(self):
        ventana.fill(NEGRO)
        
        titulo = fuente_titulo.render("❓ AYUDA", True, BLANCO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        
        instrucciones = [
            "CÓMO USAR EL GENERADOR:",
            "1. Selecciona elementos de cada categoría o déjalos al azar",
            "2. Elige un género y longitud en CONFIGURACIÓN",
            "3. Presiona GENERAR para crear tu historia",
            "4. Puedes regenerar o guardar las historias que te gusten",
            "",
            "CATEGORÍAS:",
            "• PERSONAJE: Quién protagoniza la historia",
            "• LUGAR: Dónde sucede la acción",
            "• ACCIÓN: Qué evento desencadena la trama",
            "• CONFLICTO: Qué obstáculos debe superar",
            "• DESENLACE: Cómo termina la historia",
            "",
            "CONTROLES:",
            "- Haz clic en los elementos para seleccionarlos",
            "- Usa la rueda del mouse para desplazarte",
            "- ESC: Volver al menú desde cualquier pantalla"
        ]
        
        for i, texto in enumerate(instrucciones):
            instruccion = fuente_pequena.render(texto, True, GRIS_CLARO)
            ventana.blit(instruccion, (ANCHO//2 - instruccion.get_width()//2, 120 + i * 30))
        
        boton_volver = Boton(ANCHO//2 - 100, ALTO - 80, 200, 50, 
                            "VOLVER AL MENÚ", AZUL, (70, 170, 255))
        boton_volver.dibujar(ventana)
        return boton_volver
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        botones_actuales = []
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado != "MENU":
                            self.estado = "MENU"
                        else:
                            pygame.quit()
                            sys.exit()
                
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if sonido_click:
                        sonido_click.play()
                    
                    if self.estado == "MENU":
                        for i, boton in enumerate(self.botones_menu):
                            if boton.esta_presionado(evento):
                                if i == 0: 
                                    self.estado = "GENERACION"
                                    self.crear_selectores() 
                                elif i == 1: 
                                    self.estado = "BIBLIOTECA"
                                elif i == 2: 
                                    self.estado = "CONFIGURACION"
                                elif i == 3: 
                                    self.estado = "AYUDA"
                                elif i == 4: 
                                    pygame.quit()
                                    sys.exit()
                    
                    elif self.estado == "GENERACION":
                        for selector in self.selectores:
                            selector.manejar_evento(evento)
                        
                        for boton in self.botones_generacion:
                            if boton.esta_presionado(evento):
                                if boton.texto == "🎲 ALEATORIO":
                                    self.generar_historia(aleatorio=True)
                                elif boton.texto == "💾 GUARDAR":
                                    # Mostrar diálogo simple para título
                                    self.guardar_historia(self.historia_actual)
                                elif boton.texto == "🏠 MENÚ":
                                    self.estado = "MENU"
                                elif boton.texto == "🔄 REGENERAR":
                                    self.generar_historia()
                    
                    elif self.estado == "BIBLIOTECA":
                        if botones_actuales and botones_actuales[0].esta_presionado(evento):
                            self.estado = "MENU"
                    
                    elif self.estado == "CONFIGURACION":
                        if len(botones_actuales) >= 3:
                            if botones_actuales[0].esta_presionado(evento): 
                                generos = list(Genero)
                                idx = generos.index(self.genero_actual)
                                self.genero_actual = generos[(idx + 1) % len(generos)]
                            elif botones_actuales[1].esta_presionado(evento): 
                                longitudes = ["CORTA", "MEDIA", "LARGA"]
                                idx = longitudes.index(self.longitud)
                                self.longitud = longitudes[(idx + 1) % len(longitudes)]
                            elif botones_actuales[2].esta_presionado(evento): 
                                self.estado = "MENU"
                    
                    elif self.estado == "AYUDA":
                        if botones_actuales and botones_actuales[0].esta_presionado(evento):
                            self.estado = "MENU"
                
                if self.estado == "GENERACION" and evento.type == pygame.MOUSEBUTTONDOWN:
                    for selector in self.selectores:
                        selector.manejar_evento(evento)
            
            if self.estado == "MENU":
                self.dibujar_menu()
                botones_actuales = []
            
            elif self.estado == "GENERACION":
                self.dibujar_generacion()
                botones_actuales = []
            
            elif self.estado == "BIBLIOTECA":
                botones_actuales = [self.dibujar_biblioteca()]
            
            elif self.estado == "CONFIGURACION":
                botones_actuales = list(self.dibujar_configuracion())
            
            elif self.estado == "AYUDA":
                botones_actuales = [self.dibujar_ayuda()]
            
            pygame.display.flip()
            reloj.tick(60)

if __name__ == "__main__":
    generador = GeneradorHistorias()
    generador.ejecutar()