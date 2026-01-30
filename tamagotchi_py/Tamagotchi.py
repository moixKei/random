import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from PIL import Image, ImageTk
import os

class TamagotchiAbsurdo:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("🐣 Tamagotchi Absurdo")
        self.ventana.geometry("500x600")
        self.ventana.configure(bg="#FFE6E6")
        
        # Estados de la criatura
        self.estado = {
            "hambre": 50,
            "energia": 50,
            "felicidad": 50,
            "salud": 100,
            "locura": 0  # ¡Nuevo! Nivel de locura
        }
        
        # Criaturas absurdas disponibles
        self.criaturas = [
            {"nombre": "Globito", "emoji": "🎈", "desc": "Un ser que flota y habla en rimas"},
            {"nombre": "Calcetín", "emoji": "🧦", "desc": "Un calcetín parlante con sueños"},
            {"nombre": "Quesito", "emoji": "🧀", "desc": "Un queso que cree ser filósofo"},
            {"nombre": "Nubecita", "emoji": "☁️", "desc": "Una nube con crisis existencial"},
            {"nombre": "Planta", "emoji": "🌵", "desc": "Un cactus bailarín de salsa"}
        ]
        
        self.criatura_actual = random.choice(self.criaturas)
        
        # Mensajes absurdos por categoría
        self.mensajes = {
            "hambre": [
                "¡Tengo hambre de estrellas fugaces! 🌠",
                "¿Tienes algo de luz de luna? 🌙",
                "Mi estómago suena como un theremín 🎵",
                "¡Quiero comer arcoíris! 🌈",
                "Huele a ideas fritas por aquí... 🤔"
            ],
            "energia": [
                "¡Necesito recargar con abrazos! 🤗",
                "Mi batería está hecha de sueños 💭",
                "Zzz... estoy soñando con ecuaciones ✨",
                "¡Un poco de polvo de hadas, por favor! 🧚",
                "Mis pestañas están haciendo yoga 🧘"
            ],
            "felicidad": [
                "¡Hoy me siento como un unicornio! 🦄",
                "Mi corazón hace palomitas de maíz 🍿",
                "¡La felicidad huele a galletas recién hechas! 🍪",
                "Estoy bailando con mi sombra 💃",
                "¡Mis pensamientos son de algodón de azúcar! 🍡"
            ],
            "locura": [
                "¡Acabo de tener una conversación con un tomate! 🍅",
                "Creo que mis ideas están tejiendo un suéter 🧶",
                "¡Los números me hacen cosquillas! 🔢",
                "Mi cerebro acaba de hacer un backflip 🤸",
                "¡Las palabras tienen sabor a vainilla! 🍨"
            ]
        }
        
        # Inventario absurdo
        self.inventario = {
            "galletas de nube": 3,
            "abrazos mágicos": 5,
            "chistes malos": 2,
            "suspiros de dragón": 1,
            "polvo de estrellas": 0
        }
        
        # Eventos aleatorios
        self.eventos = [
            "¡Tu criatura aprendió a tejer! 🧶",
            "¡Encontró un sombrero mágico! 🎩",
            "¡Acaba de inventar un nuevo baile! 💃",
            "¡Habla en código morse con las luciérnagas! ✨",
            "¡Se puso a contar ovejas al revés! 🐑"
        ]
        
        self.tiempo_inicio = time.time()
        self.evento_activo = False
        
        self.crear_interfaz()
        self.iniciar_juego()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg="#FFE6E6")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 1. ENCABEZADO
        header_frame = tk.Frame(main_frame, bg="#FFB6C1", relief=tk.RAISED, bd=4)
        header_frame.pack(fill=tk.X, pady=10)
        
        self.label_titulo = tk.Label(
            header_frame,
            text=f"{self.criatura_actual['emoji']} {self.criatura_actual['nombre']}",
            font=("Comic Sans MS", 24, "bold"),
            fg="#8B0000",
            bg="#FFB6C1",
            pady=10
        )
        self.label_titulo.pack()
        
        self.label_desc = tk.Label(
            header_frame,
            text=self.criatura_actual['desc'],
            font=("Comic Sans MS", 12, "italic"),
            fg="#8B0000",
            bg="#FFB6C1"
        )
        self.label_desc.pack(pady=5)
        
        # 2. PANEL DE ESTADO
        estado_frame = tk.Frame(main_frame, bg="#FFD700", relief=tk.GROOVE, bd=3)
        estado_frame.pack(fill=tk.X, pady=10)
        
        # Barras de progreso para cada estado
        self.barras_estado = {}
        
        for i, (key, valor) in enumerate(self.estado.items()):
            frame_estado = tk.Frame(estado_frame, bg="#FFD700")
            frame_estado.pack(fill=tk.X, padx=10, pady=5)
            
            # Etiqueta
            label_key = tk.Label(
                frame_estado,
                text=key.upper() + ":",
                font=("Comic Sans MS", 12, "bold"),
                fg="#8B4513",
                bg="#FFD700",
                width=12,
                anchor="w"
            )
            label_key.pack(side=tk.LEFT)
            
            # Barra de progreso
            progress_bar = ttk.Progressbar(
                frame_estado,
                length=200,
                mode='determinate',
                maximum=100
            )
            progress_bar['value'] = valor
            progress_bar.pack(side=tk.LEFT, padx=5)
            
            # Valor numérico
            label_valor = tk.Label(
                frame_estado,
                text=str(valor),
                font=("Comic Sans MS", 12),
                fg="#8B4513",
                bg="#FFD700",
                width=4
            )
            label_valor.pack(side=tk.LEFT)
            
            self.barras_estado[key] = (progress_bar, label_valor)
        
        # 3. PANEL DE MENSAJES
        self.mensaje_frame = tk.Frame(main_frame, bg="#E6FFE6", relief=tk.SUNKEN, bd=2)
        self.mensaje_frame.pack(fill=tk.X, pady=10)
        
        self.label_mensaje = tk.Label(
            self.mensaje_frame,
            text="¡Hola! Soy tu nueva criatura absurda 😜",
            font=("Comic Sans MS", 14),
            fg="#006400",
            bg="#E6FFE6",
            wraplength=400,
            pady=10,
            padx=10
        )
        self.label_mensaje.pack()
        
        # 4. PANEL DE ACCIONES
        acciones_frame = tk.Frame(main_frame, bg="#E6F2FF", relief=tk.RAISED, bd=3)
        acciones_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            acciones_frame,
            text="🎭 ACCIONES ABSURDAS 🎭",
            font=("Comic Sans MS", 16, "bold"),
            fg="#00008B",
            bg="#E6F2FF",
            pady=5
        ).pack()
        
        # Botones de acciones
        acciones = [
            ("🍔 Alimentar", self.alimentar, "#FFA07A"),
            ("🛌 Dormir", self.dormir, "#87CEEB"),
            ("🎮 Jugar", self.jugar, "#98FB98"),
            ("🎨 Arte", self.crear_arte, "#DDA0DD"),
            ("📚 Filosofar", self.filosofar, "#F0E68C")
        ]
        
        for texto, comando, color in acciones:
            btn = tk.Button(
                acciones_frame,
                text=texto,
                font=("Comic Sans MS", 12, "bold"),
                bg=color,
                fg="black",
                relief=tk.RAISED,
                bd=3,
                padx=10,
                pady=8,
                command=comando,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        
        # 5. PANEL DE INVENTARIO
        inventario_frame = tk.Frame(main_frame, bg="#FFF0F5", relief=tk.GROOVE, bd=2)
        inventario_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            inventario_frame,
            text="🎒 INVENTARIO MÁGICO 🎒",
            font=("Comic Sans MS", 14, "bold"),
            fg="#8B008B",
            bg="#FFF0F5",
            pady=5
        ).pack()
        
        self.inventario_labels = {}
        inventario_inner = tk.Frame(inventario_frame, bg="#FFF0F5")
        inventario_inner.pack(pady=5)
        
        for i, (item, cantidad) in enumerate(self.inventario.items()):
            if i % 2 == 0:
                frame = tk.Frame(inventario_inner, bg="#FFF0F5")
                frame.pack(fill=tk.X, pady=2)
            
            label = tk.Label(
                frame,
                text=f"{item.title()}: {cantidad}",
                font=("Comic Sans MS", 10),
                fg="#8B008B",
                bg="#FFF0F5",
                padx=10
            )
            label.pack(side=tk.LEFT, padx=5)
            self.inventario_labels[item] = label
        
        # 6. BOTONES ESPECIALES
        especial_frame = tk.Frame(main_frame, bg="#FFE6E6")
        especial_frame.pack(fill=tk.X, pady=10)
        
        btn_especiales = [
            ("✨ Evento Aleatorio", self.evento_aleatorio),
            ("🔁 Nueva Criatura", self.nueva_criatura),
            ("💾 Guardar", self.guardar_juego),
            ("❓ Ayuda", self.mostrar_ayuda)
        ]
        
        for texto, comando in btn_especiales:
            btn = tk.Button(
                especial_frame,
                text=texto,
                font=("Comic Sans MS", 10),
                bg="#D8BFD8",
                fg="black",
                relief=tk.RIDGE,
                bd=2,
                padx=5,
                pady=3,
                command=comando
            )
            btn.pack(side=tk.LEFT, padx=3, expand=True)
        
        # 7. CONTADOR DE TIEMPO
        self.tiempo_frame = tk.Frame(main_frame, bg="#FFE6E6")
        self.tiempo_frame.pack(pady=5)
        
        self.label_tiempo = tk.Label(
            self.tiempo_frame,
            text="Tiempo jugado: 00:00",
            font=("Comic Sans MS", 10),
            fg="#696969",
            bg="#FFE6E6"
        )
        self.label_tiempo.pack()
    
    def actualizar_estado(self):
        """Actualiza los estados de forma aleatoria"""
        for key in self.estado:
            if key != "salud":  # La salud se calcula diferente
                cambio = random.randint(-5, 5)
                self.estado[key] = max(0, min(100, self.estado[key] + cambio))
        
        # Calcular salud basada en otros estados
        self.estado["salud"] = int((self.estado["hambre"] + self.estado["energia"] + self.estado["felicidad"]) / 3)
        
        # Actualizar barras
        for key, (barra, label) in self.barras_estado.items():
            valor = self.estado[key]
            barra['value'] = valor
            label.config(text=str(valor))
            
            # Cambiar color según nivel
            if valor < 30:
                barra['style'] = 'red.Horizontal.TProgressbar'
            elif valor < 70:
                barra['style'] = 'yellow.Horizontal.TProgressbar'
            else:
                barra['style'] = 'green.Horizontal.TProgressbar'
        
        # Verificar si la criatura está "demasiado loca"
        if self.estado["locura"] > 80:
            self.mostrar_mensaje("¡Estoy demasiado loco! Mis ideas están escapando! 🤪", "locura")
    
    def mostrar_mensaje(self, mensaje=None, categoria=None):
        """Muestra un mensaje absurdo"""
        if not mensaje:
            if categoria and categoria in self.mensajes:
                mensaje = random.choice(self.mensajes[categoria])
            else:
                # Mensaje general absurdo
                mensajes_generales = [
                    f"¡{self.criatura_actual['nombre']} está pensando en tejer un suéter para la luna! 🌙",
                    f"¿Sabías que {self.criatura_actual['nombre']} cree que las nubes son algodón de azúcar gigante? ☁️",
                    f"¡{self.criatura_actual['emoji']} {self.criatura_actual['nombre']} acaba de inventar un nuevo idioma! 🗣️",
                    f"{self.criatura_actual['nombre']} está teniendo una conversación seria con un espejo... 🪞",
                    f"¡{self.criatura_actual['emoji']} Creo que mis pensamientos tienen color rosa hoy! 💖"
                ]
                mensaje = random.choice(mensajes_generales)
        
        self.label_mensaje.config(text=mensaje)
        
        # Efecto visual (cambiar color de fondo)
        colores = ["#E6FFE6", "#FFE6E6", "#E6E6FF", "#FFFFE6"]
        self.mensaje_frame.config(bg=random.choice(colores))
        self.label_mensaje.config(bg=self.mensaje_frame.cget("bg"))
    
    def alimentar(self):
        """Alimentar a la criatura absurda"""
        if self.inventario["galletas de nube"] > 0:
            self.estado["hambre"] = min(100, self.estado["hambre"] + 20)
            self.estado["locura"] = min(100, self.estado["locura"] + 10)
            self.inventario["galletas de nube"] -= 1
            self.inventario_labels["galletas de nube"].config(
                text=f"Galletas De Nube: {self.inventario['galletas de nube']}"
            )
            self.mostrar_mensaje("¡Ñam ñam! Esas galletas de nube saben a sueños húmedos ☁️🍪", "hambre")
        else:
            self.mostrar_mensaje("¡No tengo galletas de nube! ¿Y si comemos ideas fritas? 🤔")
        
        self.actualizar_estado()
        self.verificar_estado()
    
    def dormir(self):
        """La criatura duerme (de forma absurda)"""
        if self.inventario["abrazos mágicos"] > 0:
            self.estado["energia"] = min(100, self.estado["energia"] + 25)
            self.inventario["abrazos mágicos"] -= 1
            self.inventario_labels["abrazos mágicos"].config(
                text=f"Abrazos Mágicos: {self.inventario['abrazos mágicos']}"
            )
            self.mostrar_mensaje("Zzz... Estoy soñando con ovejas que bailan flamenco 🐑💃", "energia")
        else:
            self.mostrar_mensaje("¡Necesito un abrazo mágico para dormir! 🥱")
        
        self.actualizar_estado()
        self.verificar_estado()
    
    def jugar(self):
        """Jugar con la criatura"""
        self.estado["felicidad"] = min(100, self.estado["felicidad"] + 15)
        self.estado["energia"] = max(0, self.estado["energia"] - 10)
        self.estado["locura"] = min(100, self.estado["locura"] + 5)
        
        # Posible ganar item
        if random.random() < 0.3:  # 30% de probabilidad
            self.inventario["polvo de estrellas"] += 1
            self.inventario_labels["polvo de estrellas"].config(
                text=f"Polvo De Estrellas: {self.inventario['polvo de estrellas']}"
            )
            self.mostrar_mensaje("¡Encontré polvo de estrellas mientras jugaba! ✨")
        else:
            self.mostrar_mensaje("¡Qué divertido! Acabo de inventar un juego nuevo 🎲", "felicidad")
        
        self.actualizar_estado()
        self.verificar_estado()
    
    def crear_arte(self):
        """La criatura crea arte absurdo"""
        self.estado["felicidad"] = min(100, self.estado["felicidad"] + 10)
        self.estado["locura"] = min(100, self.estado["locura"] + 15)
        
        obras_arte = [
            "Un retrato de la luna sonriente 🌙😊",
            "Una escultura hecha de suspiros 🗿",
            "Una canción para las plantas cantantes 🎶🌱",
            "Un poema escrito con jugo de arcoíris 📜🌈",
            "Un baile interpretando el viento 💨💃"
        ]
        
        self.mostrar_mensaje(f"¡Creé {random.choice(obras_arte)}! 🎨")
        self.actualizar_estado()
        self.verificar_estado()
    
    def filosofar(self):
        """La criatura filosofa absurdamente"""
        self.estado["locura"] = min(100, self.estado["locura"] + 20)
        
        preguntas_filosoficas = [
            "¿Si un árbol cae en un bosque y nadie lo oye, hace yoga? 🧘",
            "¿Los espejos sueñan con reflejar otros espejos? 🪞",
            "¿Qué sonó primero: el huevo o la gallina filosofal? 🥚🐔",
            "¿Si camino hacia atrás, voy hacia el futuro? ⏮️",
            "¿Las nubes piensan en ovejas cuando duermen? ☁️🐑"
        ]
        
        self.mostrar_mensaje(f"Pregunta profunda: {random.choice(preguntas_filosoficas)}", "locura")
        self.actualizar_estado()
        self.verificar_estado()
    
    def evento_aleatorio(self):
        """Ocurre un evento aleatorio absurdo"""
        if not self.evento_activo:
            self.evento_activo = True
            evento = random.choice(self.eventos)
            
            # Efectos del evento
            for key in self.estado:
                if key != "salud":
                    self.estado[key] = max(0, min(100, self.estado[key] + random.randint(-10, 10)))
            
            # Posible recompensa
            if random.random() < 0.5:
                item = random.choice(list(self.inventario.keys()))
                self.inventario[item] += 1
                self.inventario_labels[item].config(
                    text=f"{item.title()}: {self.inventario[item]}"
                )
                evento += f" ¡Y ganó {item.replace('_', ' ')}!"
            
            self.mostrar_mensaje(f"¡EVENTO ESPECIAL! {evento}")
            self.actualizar_estado()
            
            # Resetear evento después de 5 segundos
            self.ventana.after(5000, lambda: setattr(self, 'evento_activo', False))
    
    def nueva_criatura(self):
        """Cambia a una nueva criatura absurda"""
        self.criatura_actual = random.choice(self.criaturas)
        self.label_titulo.config(
            text=f"{self.criatura_actual['emoji']} {self.criatura_actual['nombre']}"
        )
        self.label_desc.config(text=self.criatura_actual['desc'])
        
        # Resetear algunos estados
        self.estado["locura"] = 0
        
        self.mostrar_mensaje(
            f"¡Hola! Soy {self.criatura_actual['nombre']}. {self.criatura_actual['desc']} 😄"
        )
        self.actualizar_estado()
    
    def verificar_estado(self):
        """Verifica el estado general de la criatura"""
        if self.estado["hambre"] < 20:
            self.mostrar_mensaje("¡Tengo hambre de ideas abstractas! 🍽️")
        elif self.estado["energia"] < 20:
            self.mostrar_mensaje("Mis párpados están haciendo yoga... 😴")
        elif self.estado["felicidad"] < 20:
            self.mostrar_mensaje("Mi corazón necesita abrazos de nube... ☁️🤗")
        
        # Verificar si "murió" (se volvió demasiado loco)
        if self.estado["locura"] >= 100:
            respuesta = messagebox.askyesno(
                "¡Crisis Existencial!",
                f"{self.criatura_actual['nombre']} se volvió demasiado loco y decidió viajar a otra dimensión. \n\n¿Quieres adoptar una nueva criatura?"
            )
            if respuesta:
                self.nueva_criatura()
                self.estado["locura"] = 0
            else:
                self.ventana.destroy()
    
    def actualizar_tiempo(self):
        """Actualiza el contador de tiempo"""
        tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60
        self.label_tiempo.config(text=f"Tiempo jugado: {minutos:02d}:{segundos:02d}")
        
        # Cada 30 segundos, actualizar estado automáticamente
        if tiempo_transcurrido % 30 == 0:
            self.actualizar_estado()
            self.mostrar_mensaje()
        
        # Programar próxima actualización
        self.ventana.after(1000, self.actualizar_tiempo)
    
    def guardar_juego(self):
        """Guarda el juego (simulado)"""
        try:
            datos = {
                "criatura": self.criatura_actual,
                "estado": self.estado,
                "inventario": self.inventario,
                "tiempo_jugado": int(time.time() - self.tiempo_inicio)
            }
            
            # Simular guardado
            self.mostrar_mensaje("¡Juego guardado en la nube de algodón de azúcar! ☁️💾")
            
        except:
            self.mostrar_mensaje("¡Ups! El guardado se perdió en una grieta dimensional 🕳️")
    
    def mostrar_ayuda(self):
        """Muestra ayuda absurda"""
        ayuda_texto = """
        🎮 CÓMO JUGAR CON TU CRIATURA ABSURDA:
        
        • ALIMENTAR 🍔: Dale galletas de nube
        • DORMIR 🛌: Recarga con abrazos mágicos  
        • JUGAR 🎮: Aumenta felicidad, puede dar recompensas
        • ARTE 🎨: Tu criatura crea obras maestras absurdas
        • FILOSOFAR 📚: Preguntas profundas (y locas)
        
        🎯 OBJETIVO:
        Mantén a tu criatura feliz sin volverla demasiado loca.
        ¡Cuidado con la locura! Puede viajar a otra dimensión.
        
        ✨ TIP: Usa los eventos aleatorios para sorpresas divertidas!
        """
        
        messagebox.showinfo("❓ Ayuda Absurda", ayuda_texto)
    
    def iniciar_juego(self):
        """Inicia el juego"""
        # Configurar estilos de barras
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("green.Horizontal.TProgressbar",
                       background='#4CAF50',
                       troughcolor='#C8E6C9')
        
        style.configure("yellow.Horizontal.TProgressbar",
                       background='#FFEB3B',
                       troughcolor='#FFF9C4')
        
        style.configure("red.Horizontal.TProgressbar",
                       background='#F44336',
                       troughcolor='#FFCDD2')
        
        # Iniciar actualizaciones
        self.actualizar_tiempo()
        
        # Mostrar mensaje de bienvenida
        self.mostrar_mensaje(
            f"¡Hola! Soy {self.criatura_actual['nombre']}, {self.criatura_actual['desc'].lower()} "
            f"¿Listo para una aventura absurda? {self.criatura_actual['emoji']}"
        )
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana.mainloop()

# Ejecutar el juego
if __name__ == "__main__":
    juego = TamagotchiAbsurdo()
    juego.ejecutar()