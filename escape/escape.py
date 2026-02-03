import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from PIL import Image, ImageTk
import time

class EscapeRoom:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("🚀 Escape Room Pro - La Fuga del Laboratorio")
        self.ventana.geometry("1200x800")
        self.ventana.configure(bg="#1a1a2e")
        
        # Datos del juego mejorados
        self.habitaciones = {
            "laboratorio": {
                "nombre": "🧪 Laboratorio de Experimentos",
                "descripcion": "Un laboratorio abandonado lleno de equipos científicos. Hay un olor químico en el aire.",
                "imagen": "🔬",
                "salidas": {"este": "oficina", "sur": "archivos"},
                "objetos": ["llave_roja", "nota_rasgada"],
                "puzzle": None,
                "examinar": {
                    "mesa": "Una mesa con tubos de ensayo y un microscopio. Uno de los tubos contiene un líquido brillante.",
                    "computadora": "La pantalla muestra: 'Sistema bloqueado. Requiere clave de acceso.'",
                    "pizarra": "En la pizarra hay ecuaciones químicas y la frase: 'La verdad está en los números'"
                }
            },
            "oficina": {
                "nombre": "📁 Oficina del Director",
                "descripcion": "Una oficina elegante con muebles de madera y una gran ventana.",
                "imagen": "💼",
                "salidas": {"oeste": "laboratorio", "norte": "sala_servidores"},
                "objetos": ["libro_codigos", "linterna"],
                "puzzle": "caja_fuerte",
                "examinar": {
                    "escritorio": "Un escritorio organizado con documentos. Un cajón está cerrado con llave.",
                    "caja_fuerte": "Una caja fuerte con combinación. Tiene 3 ruedas numéricas (0-9).",
                    "estanteria": "Libros sobre física cuántica y criptografía."
                }
            },
            "archivos": {
                "nombre": "🗄️ Sala de Archivos",
                "descripcion": "Estanterías llenas de cajas polvorientas. El aire huele a papel viejo.",
                "imagen": "📚",
                "salidas": {"norte": "laboratorio", "este": "pasillo_oscuro"},
                "objetos": ["disco_duro", "cable_usb"],
                "puzzle": None,
                "examinar": {
                    "caja_verde": "Contiene documentos sobre experimentos fallidos.",
                    "caja_roja": "Está cerrada con un candado de 4 dígitos.",
                    "archivador": "Carpetas etiquetadas con fechas: '2023', '2024', 'Proyecto X'"
                }
            },
            "pasillo_oscuro": {
                "nombre": "🚨 Pasillo de Emergencia",
                "descripcion": "Un pasillo oscuro con luces parpadeantes. Escuchas un zumbido eléctrico.",
                "imagen": "⚠️",
                "salidas": {"oeste": "archivos", "norte": "sala_control"},
                "objetos": ["botiquin"],
                "puzzle": "panel_electrico",
                "examinar": {
                    "panel_electrico": "Un panel con 6 interruptores. Algunos están en ON, otros en OFF.",
                    "extintor": "El extintor está vacío. Alguien lo usó recientemente.",
                    "alarma": "La luz de la alarma parpadea en rojo. Parece desactivada."
                }
            },
            "sala_servidores": {
                "nombre": "💻 Sala de Servidores",
                "descripcion": "Una sala fría llena de servidores parpadeantes. El zumbido es ensordecedor.",
                "imagen": "🖥️",
                "salidas": {"sur": "oficina", "este": "sala_control"},
                "objetos": ["tarjeta_magnética"],
                "puzzle": "terminal",
                "examinar": {
                    "terminal": "Una terminal con pantalla táctil. Muestra: 'Acceso: Nivel 2 requerido'",
                    "servidor_principal": "Luces verdes y rojas parpadean secuencialmente.",
                    "router": "Un router con luces que parpadean en un patrón específico."
                }
            },
            "sala_control": {
                "nombre": "🎮 Sala de Control Principal",
                "descripcion": "Una sala circular con pantallas gigantes y una consola central.",
                "imagen": "🎛️",
                "salidas": {"sur": "pasillo_oscuro", "oeste": "sala_servidores"},
                "objetos": [],
                "puzzle": "puerta_salida",
                "examinar": {
                    "consola": "La consola tiene botones etiquetados: 'Emergencia', 'Liberar', 'Auto-Destrucción'",
                    "pantallas": "Muestran diferentes áreas del complejo. Una está en blanco.",
                    "puerta_salida": "Una puerta blindada con un escáner biométrico y un teclado numérico."
                }
            }
        }
        
        # Variables del juego
        self.ubicacion_actual = "laboratorio"
        self.inventario = []
        self.juego_activo = True
        self.tiempo_inicio = time.time()
        self.tiempo_limite = 1800  # 30 minutos en segundos
        self.pistas_usadas = 0
        self.objetos_combinados = []
        self.codigos_descubiertos = []
        self.puzzles_resueltos = []
        
        # Soluciones de puzzles
        self.soluciones = {
            "caja_fuerte": "723",  # Basado en pistas del laboratorio
            "panel_electrico": [1, 0, 1, 0, 1, 0],  # Patrón binario
            "terminal": "nivel2",  # Encontrado en libro_codigos
            "puerta_salida": "1945"  # Fecha en documentos
        }
        
        self.cargar_partida()
        self.crear_interfaz()
        self.actualizar_interfaz()
        
        # Iniciar temporizador
        self.iniciar_temporizador()
    
    def cargar_partida(self):
        """Cargar partida guardada si existe"""
        try:
            if os.path.exists("escape_room_save.json"):
                with open("escape_room_save.json", "r") as f:
                    datos = json.load(f)
                    self.ubicacion_actual = datos.get("ubicacion", "laboratorio")
                    self.inventario = datos.get("inventario", [])
                    self.pistas_usadas = datos.get("pistas_usadas", 0)
                    self.puzzles_resueltos = datos.get("puzzles_resueltos", [])
                    self.codigos_descubiertos = datos.get("codigos_descubiertos", [])
        except:
            pass
    
    def guardar_partida(self):
        """Guardar estado del juego"""
        try:
            datos = {
                "ubicacion": self.ubicacion_actual,
                "inventario": self.inventario,
                "pistas_usadas": self.pistas_usadas,
                "puzzles_resueltos": self.puzzles_resueltos,
                "codigos_descubiertos": self.codigos_descubiertos
            }
            with open("escape_room_save.json", "w") as f:
                json.dump(datos, f, indent=2)
        except:
            pass
    
    def crear_interfaz(self):
        # Configurar estilo
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Frame principal con paneles
        main_frame = tk.Frame(self.ventana, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (habitación y acciones)
        left_panel = tk.Frame(main_frame, bg="#16213e", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Panel derecho (información e inventario)
        right_panel = tk.Frame(main_frame, bg="#0f3460", width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # ===== PANEL IZQUIERDO =====
        
        # Encabezado de habitación
        self.habitacion_header = tk.Label(
            left_panel,
            text="",
            font=("Consolas", 20, "bold"),
            fg="#e94560",
            bg="#16213e"
        )
        self.habitacion_header.pack(pady=(10, 5), padx=10)
        
        # Icono de habitación
        self.habitacion_icon = tk.Label(
            left_panel,
            text="",
            font=("Segoe UI Emoji", 50),
            bg="#16213e"
        )
        self.habitacion_icon.pack(pady=(0, 10))
        
        # Área de descripción
        desc_frame = tk.Frame(left_panel, bg="#16213e")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            desc_frame,
            text="Descripción:",
            font=("Arial", 12, "bold"),
            fg="#4cc9f0",
            bg="#16213e"
        ).pack(anchor=tk.W)
        
        self.descripcion_text = scrolledtext.ScrolledText(
            desc_frame,
            height=6,
            width=50,
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white",
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=2
        )
        self.descripcion_text.pack(fill=tk.X, pady=(5, 0))
        
        # Elementos examinables
        exam_frame = tk.Frame(left_panel, bg="#16213e")
        exam_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(
            exam_frame,
            text="Elementos:",
            font=("Arial", 12, "bold"),
            fg="#4cc9f0",
            bg="#16213e"
        ).pack(anchor=tk.W)
        
        self.examinar_frame = tk.Frame(exam_frame, bg="#16213e")
        self.examinar_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Entrada de comandos
        cmd_frame = tk.Frame(left_panel, bg="#16213e")
        cmd_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            cmd_frame,
            text="Comando:",
            font=("Arial", 12, "bold"),
            fg="#4cc9f0",
            bg="#16213e"
        ).pack(anchor=tk.W)
        
        # Frame para entrada y botones
        input_frame = tk.Frame(cmd_frame, bg="#16213e")
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.entrada_comando = ttk.Entry(
            input_frame,
            font=("Arial", 12),
            width=30
        )
        self.entrada_comando.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entrada_comando.bind("<Return>", lambda e: self.procesar_comando())
        
        btn_ejecutar = tk.Button(
            input_frame,
            text="Ejecutar",
            font=("Arial", 11, "bold"),
            bg="#e94560",
            fg="white",
            relief=tk.RAISED,
            bd=2,
            command=self.procesar_comando
        )
        btn_ejecutar.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botones de comandos rápidos
        quick_buttons_frame = tk.Frame(left_panel, bg="#16213e")
        quick_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        comandos_rapidos = ["Mirar", "Norte", "Sur", "Este", "Oeste", "Inventario", "Examinar"]
        for cmd in comandos_rapidos:
            btn = tk.Button(
                quick_buttons_frame,
                text=cmd,
                font=("Arial", 10),
                bg="#4361ee",
                fg="white",
                width=8,
                relief=tk.RAISED,
                command=lambda c=cmd.lower(): self.boton_rapido(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # ===== PANEL DERECHO =====
        
        # Título del panel
        tk.Label(
            right_panel,
            text="📊 PANEL DE CONTROL",
            font=("Consolas", 16, "bold"),
            fg="#e94560",
            bg="#0f3460"
        ).pack(pady=(10, 20))
        
        # Temporizador
        self.temporizador_label = tk.Label(
            right_panel,
            text="Tiempo: 30:00",
            font=("Consolas", 14, "bold"),
            fg="#4cc9f0",
            bg="#0f3460"
        )
        self.temporizador_label.pack(pady=(0, 10))
        
        # Progreso
        self.progreso_label = tk.Label(
            right_panel,
            text="Progreso: 0%",
            font=("Consolas", 12),
            fg="#f72585",
            bg="#0f3460"
        )
        self.progreso_label.pack(pady=(0, 20))
        
        # Inventario
        inv_frame = tk.Frame(right_panel, bg="#0f3460")
        inv_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            inv_frame,
            text="🎒 INVENTARIO",
            font=("Arial", 14, "bold"),
            fg="#4cc9f0",
            bg="#0f3460"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.inventario_listbox = tk.Listbox(
            inv_frame,
            height=10,
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="white",
            selectbackground="#4361ee",
            relief=tk.FLAT,
            bd=2
        )
        self.inventario_listbox.pack(fill=tk.X)
        
        # Botones de inventario
        inv_buttons_frame = tk.Frame(inv_frame, bg="#0f3460")
        inv_buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        btn_usar = tk.Button(
            inv_buttons_frame,
            text="Usar",
            font=("Arial", 10),
            bg="#4361ee",
            fg="white",
            command=self.usar_objeto_seleccionado
        )
        btn_usar.pack(side=tk.LEFT, expand=True, padx=2)
        
        btn_examinar_inv = tk.Button(
            inv_buttons_frame,
            text="Examinar",
            font=("Arial", 10),
            bg="#4361ee",
            fg="white",
            command=self.examinar_objeto_seleccionado
        )
        btn_examinar_inv.pack(side=tk.LEFT, expand=True, padx=2)
        
        # Pistas
        pistas_frame = tk.Frame(right_panel, bg="#0f3460")
        pistas_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        tk.Label(
            pistas_frame,
            text="💡 PISTAS",
            font=("Arial", 14, "bold"),
            fg="#4cc9f0",
            bg="#0f3460"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.pista_text = tk.Text(
            pistas_frame,
            height=8,
            width=30,
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#f72585",
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=2
        )
        self.pista_text.pack(fill=tk.X)
        self.pista_text.insert(tk.END, "Usa 'pedir pista' cuando estés atascado.")
        self.pista_text.config(state=tk.DISABLED)
        
        btn_pista = tk.Button(
            pistas_frame,
            text="Pedir Pista",
            font=("Arial", 11, "bold"),
            bg="#f72585",
            fg="white",
            command=self.pedir_pista
        )
        btn_pista.pack(pady=(5, 0))
        
        # Botones de acción
        action_frame = tk.Frame(right_panel, bg="#0f3460")
        action_frame.pack(fill=tk.X, padx=10, pady=20)
        
        btn_guardar = tk.Button(
            action_frame,
            text="💾 Guardar",
            font=("Arial", 11),
            bg="#2a9d8f",
            fg="white",
            command=self.guardar_partida
        )
        btn_guardar.pack(fill=tk.X, pady=2)
        
        btn_cargar = tk.Button(
            action_frame,
            text="📂 Cargar",
            font=("Arial", 11),
            bg="#2a9d8f",
            fg="white",
            command=self.cargar_y_actualizar
        )
        btn_cargar.pack(fill=tk.X, pady=2)
        
        btn_reiniciar = tk.Button(
            action_frame,
            text="🔄 Reiniciar",
            font=("Arial", 11),
            bg="#e76f51",
            fg="white",
            command=self.reiniciar_juego
        )
        btn_reiniciar.pack(fill=tk.X, pady=2)
        
        btn_salir = tk.Button(
            action_frame,
            text="🚪 Salir",
            font=("Arial", 11),
            bg="#e63946",
            fg="white",
            command=self.salir_juego
        )
        btn_salir.pack(fill=tk.X, pady=2)
    
    def actualizar_interfaz(self):
        """Actualizar toda la interfaz con la información actual"""
        hab = self.habitaciones[self.ubicacion_actual]
        
        # Actualizar header e icono
        self.habitacion_header.config(text=hab["nombre"])
        self.habitacion_icon.config(text=hab["imagen"])
        
        # Actualizar descripción
        self.descripcion_text.delete(1.0, tk.END)
        self.descripcion_text.insert(tk.END, hab["descripcion"])
        
        # Mostrar objetos en la habitación
        if hab["objetos"]:
            objetos_text = f"\n\nObjetos visibles: {', '.join(hab['objetos'])}"
            self.descripcion_text.insert(tk.END, objetos_text)
        
        # Actualizar elementos examinables
        for widget in self.examinar_frame.winfo_children():
            widget.destroy()
        
        for elemento in hab["examinar"]:
            btn = tk.Button(
                self.examinar_frame,
                text=f"🔍 {elemento.capitalize()}",
                font=("Arial", 10),
                bg="#4361ee",
                fg="white",
                relief=tk.RAISED,
                command=lambda e=elemento: self.examinar_elemento(e)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Actualizar inventario
        self.inventario_listbox.delete(0, tk.END)
        for obj in self.inventario:
            self.inventario_listbox.insert(tk.END, f"• {obj.replace('_', ' ').title()}")
        
        # Actualizar progreso
        progreso = (len(self.puzzles_resueltos) / len(self.soluciones)) * 100
        self.progreso_label.config(text=f"Progreso: {progreso:.0f}%")
    
    def iniciar_temporizador(self):
        """Iniciar el temporizador del juego"""
        self.actualizar_temporizador()
    
    def actualizar_temporizador(self):
        """Actualizar el temporizador"""
        if not self.juego_activo:
            return
        
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        tiempo_restante = max(0, self.tiempo_limite - tiempo_transcurrido)
        
        minutos = int(tiempo_restante // 60)
        segundos = int(tiempo_restante % 60)
        
        # Cambiar color según tiempo restante
        color = "#4cc9f0" if tiempo_restante > 600 else "#f1c40f" if tiempo_restante > 300 else "#e74c3c"
        
        self.temporizador_label.config(
            text=f"Tiempo: {minutos:02d}:{segundos:02d}",
            fg=color
        )
        
        # Verificar si se acabó el tiempo
        if tiempo_restante <= 0:
            self.juego_terminado("⏰ ¡Se acabó el tiempo! La alarma se activó y no pudiste escapar.")
        else:
            self.ventana.after(1000, self.actualizar_temporizador)
    
    def boton_rapido(self, comando):
        """Manejar botones de comandos rápidos"""
        self.entrada_comando.delete(0, tk.END)
        self.entrada_comando.insert(0, comando)
        self.procesar_comando()
    
    def procesar_comando(self):
        """Procesar el comando ingresado"""
        comando = self.entrada_comando.get().lower().strip()
        self.entrada_comando.delete(0, tk.END)
        
        if not comando:
            return
        
        # Comandos básicos
        if comando == "mirar":
            self.actualizar_interfaz()
        
        elif comando in ["norte", "sur", "este", "oeste"]:
            self.mover(comando)
        
        elif comando == "inventario":
            self.mostrar_inventario_detallado()
        
        elif comando == "examinar":
            self.mostrar_pista("Escribe 'examinar [elemento]' o haz clic en los botones de elementos.")
        
        elif comando.startswith("examinar "):
            elemento = comando[9:].strip()
            self.examinar_elemento(elemento)
        
        elif comando.startswith("coger "):
            objeto = comando[5:].strip()
            self.coger_objeto(objeto)
        
        elif comando.startswith("usar "):
            partes = comando[5:].split(" en ", 1)
            if len(partes) == 2:
                objeto, destino = partes[0].strip(), partes[1].strip()
                self.usar_objeto(objeto, destino)
            else:
                self.mostrar_pista("Formato: usar [objeto] en [destino]")
        
        elif comando == "pedir pista":
            self.pedir_pista()
        
        elif comando.startswith("combinar "):
            partes = comando[9:].split(" con ", 1)
            if len(partes) == 2:
                obj1, obj2 = partes[0].strip(), partes[1].strip()
                self.combinar_objetos(obj1, obj2)
            else:
                self.mostrar_pista("Formato: combinar [objeto1] con [objeto2]")
        
        elif comando == "guardar":
            self.guardar_partida()
            self.mostrar_pista("✅ Partida guardada exitosamente.")
        
        elif comando == "cargar":
            self.cargar_y_actualizar()
        
        elif comando == "reiniciar":
            self.reiniciar_juego()
        
        elif comando == "salir":
            self.salir_juego()
        
        elif comando == "ayuda":
            self.mostrar_ayuda()
        
        else:
            self.mostrar_pista(f"Comando no reconocido: '{comando}'. Escribe 'ayuda' para ver comandos disponibles.")
    
    def mover(self, direccion):
        """Mover a otra habitación"""
        hab_actual = self.habitaciones[self.ubicacion_actual]
        
        if direccion in hab_actual["salidas"]:
            # Verificar si hay puerta cerrada
            if self.ubicacion_actual == "laboratorio" and direccion == "este":
                if "llave_roja" not in self.inventario:
                    self.mostrar_pista("La puerta está cerrada. Necesitas una llave.")
                    return
            
            self.ubicacion_actual = hab_actual["salidas"][direccion]
            self.actualizar_interfaz()
            self.mostrar_pista(f"Te has movido hacia el {direccion}.")
        else:
            self.mostrar_pista("No puedes ir en esa dirección.")
    
    def coger_objeto(self, objeto):
        """Coger un objeto de la habitación"""
        hab = self.habitaciones[self.ubicacion_actual]
        objeto_id = objeto.replace(" ", "_")
        
        if objeto_id in hab["objetos"]:
            self.inventario.append(objeto_id)
            hab["objetos"].remove(objeto_id)
            self.actualizar_interfaz()
            self.mostrar_pista(f"Has cogido: {objeto.replace('_', ' ').title()}")
            
            # Efecto especial para objetos importantes
            if objeto_id in ["llave_roja", "tarjeta_magnética", "disco_duro"]:
                self.mostrar_pista("✨ ¡Este objeto parece importante!")
        else:
            self.mostrar_pista(f"No hay '{objeto}' aquí.")
    
    def usar_objeto(self, objeto, destino):
        """Usar un objeto del inventario"""
        objeto_id = objeto.replace(" ", "_")
        
        if objeto_id not in self.inventario:
            self.mostrar_pista(f"No tienes '{objeto}' en tu inventario.")
            return
        
        # Usar llave roja en laboratorio
        if objeto_id == "llave_roja" and self.ubicacion_actual == "laboratorio":
            self.mostrar_pista("Usas la llave roja para abrir la puerta hacia el este.")
            # La puerta ya está abierta lógicamente
        
        # Usar llave roja en cajón
        elif objeto_id == "llave_roja" and destino == "cajón" and self.ubicacion_actual == "oficina":
            self.mostrar_pista("Abres el cajón del escritorio. Encuentras un código: '723'")
            self.codigos_descubiertos.append("723")
        
        # Usar linterna en pasillo oscuro
        elif objeto_id == "linterna" and self.ubicacion_actual == "pasillo_oscuro":
            self.mostrar_pista("La linterna revela un patrón en el panel eléctrico: ON-OFF-ON-OFF-ON-OFF")
            self.codigos_descubiertos.append("101010")
        
        # Usar cable usb con disco duro
        elif objeto_id == "cable_usb" and destino == "disco_duro":
            if "disco_duro" in self.inventario:
                self.mostrar_pista("Conectas el disco duro. Contiene información sobre el código de salida: '1945'")
                self.codigos_descubiertos.append("1945")
                self.objetos_combinados.append(("cable_usb", "disco_duro"))
            else:
                self.mostrar_pista("Necesitas el disco duro para usar el cable USB.")
        
        # Usar tarjeta magnética en terminal
        elif objeto_id == "tarjeta_magnética" and destino == "terminal" and self.ubicacion_actual == "sala_servidores":
            self.mostrar_pista("Desbloqueas la terminal. Requiere contraseña: 'nivel2'")
        
        else:
            self.mostrar_pista(f"No puedes usar '{objeto}' en '{destino}' aquí.")
    
    def usar_objeto_seleccionado(self):
        """Usar el objeto seleccionado en el inventario"""
        seleccion = self.inventario_listbox.curselection()
        if seleccion:
            objeto = self.inventario[seleccion[0]]
            self.entrada_comando.delete(0, tk.END)
            self.entrada_comando.insert(0, f"usar {objeto.replace('_', ' ')} en ")
            self.entrada_comando.focus()
            self.entrada_comando.icursor(tk.END)
    
    def examinar_objeto_seleccionado(self):
        """Examinar el objeto seleccionado en el inventario"""
        seleccion = self.inventario_listbox.curselection()
        if seleccion:
            objeto = self.inventario[seleccion[0]]
            self.examinar_objeto_inventario(objeto)
    
    def examinar_elemento(self, elemento):
        """Examinar un elemento de la habitación"""
        hab = self.habitaciones[self.ubicacion_actual]
        
        if elemento in hab["examinar"]:
            descripcion = hab["examinar"][elemento]
            self.mostrar_pista(f"🔍 {elemento.capitalize()}: {descripcion}")
            
            # Revelar códigos especiales
            if elemento == "computadora" and self.ubicacion_actual == "laboratorio":
                self.mostrar_pista("💡 Pista: Revisa la pizarra para encontrar pistas numéricas.")
            
            elif elemento == "caja_fuerte" and self.ubicacion_actual == "oficina":
                self.mostrar_pista("🔒 La caja fuerte requiere un código de 3 dígitos. Busca pistas en el laboratorio.")
            
            elif elemento == "panel_electrico" and self.ubicacion_actual == "pasillo_oscuro":
                self.mostrar_pista("⚡ Necesitas ver el patrón correcto. ¿Tienes una linterna?")
            
            elif elemento == "terminal" and self.ubicacion_actual == "sala_servidores":
                self.mostrar_pista("💻 Necesitas una tarjeta de acceso y la contraseña correcta.")
            
            elif elemento == "puerta_salida" and self.ubicacion_actual == "sala_control":
                self.mostrar_pista("🚪 Para abrir la puerta necesitas:\n1. El código numérico\n2. Resolver todos los puzzles")
        else:
            self.mostrar_pista(f"No hay '{elemento}' para examinar aquí.")
    
    def examinar_objeto_inventario(self, objeto):
        """Examinar un objeto del inventario"""
        descripciones = {
            "llave_roja": "Una llave metálica roja oxidada. Tiene el símbolo de un átomo grabado.",
            "nota_rasgada": "Fragmento de papel: '...las 3 primeras ecuaciones suman 7, 2, 3...'",
            "libro_codigos": "Libro de criptografía. Una página marcada dice: 'Acceso Nivel 2: contraseña básica'",
            "linterna": "Una linterna potente. Las baterías están medio gastadas.",
            "disco_duro": "Disco duro externo. Parece contener datos importantes.",
            "cable_usb": "Cable USB. Podría servir para conectar dispositivos.",
            "botiquin": "Botiquín de primeros auxilios. Contiene vendas y analgésicos.",
            "tarjeta_magnética": "Tarjeta de acceso nivel 1. Funciona en algunos sistemas."
        }
        
        if objeto in descripciones:
            self.mostrar_pista(f"📦 {objeto.replace('_', ' ').title()}: {descripciones[objeto]}")
        else:
            self.mostrar_pista(f"📦 {objeto.replace('_', ' ').title()}: Un objeto misterioso.")
    
    def combinar_objetos(self, obj1, obj2):
        """Combinar dos objetos del inventario"""
        obj1_id = obj1.replace(" ", "_")
        obj2_id = obj2.replace(" ", "_")
        
        if obj1_id not in self.inventario or obj2_id not in self.inventario:
            self.mostrar_pista("Necesitas ambos objetos en tu inventario.")
            return
        
        # Combinaciones posibles
        combinaciones = {
            ("disco_duro", "cable_usb"): ("disco_accesible", "Has conectado el disco duro. Ahora puedes acceder a su contenido."),
            ("linterna", "botiquin"): ("kit_supervivencia", "Has creado un kit de supervivencia básico.")
        }
        
        for (o1, o2), (resultado, mensaje) in combinaciones.items():
            if (obj1_id == o1 and obj2_id == o2) or (obj1_id == o2 and obj2_id == o1):
                if resultado not in self.inventario:
                    self.inventario.remove(obj1_id)
                    self.inventario.remove(obj2_id)
                    self.inventario.append(resultado)
                    self.objetos_combinados.append((obj1_id, obj2_id))
                    self.mostrar_pista(f"✨ {mensaje}")
                    self.actualizar_interfaz()
                    return
        
        self.mostrar_pista("Esos objetos no se pueden combinar.")
    
    def pedir_pista(self):
        """Dar una pista al jugador"""
        self.pistas_usadas += 1
        hab = self.habitaciones[self.ubicacion_actual]
        
        pistas = {
            "laboratorio": [
                "Mira la pizarra para encontrar pistas numéricas.",
                "La computadora bloqueada podría necesitar información de otros lugares.",
                "Revisa todos los objetos en la habitación cuidadosamente."
            ],
            "oficina": [
                "La caja fuerte requiere un código de 3 dígitos.",
                "Busca en el libro de códigos pistas sobre contraseñas.",
                "El escritorio podría esconder algo importante."
            ],
            "archivos": [
                "Algunas cajas contienen información valiosa.",
                "Los documentos viejos a veces tienen códigos escondidos.",
                "Revisa todas las cajas meticulosamente."
            ],
            "pasillo_oscuro": [
                "El panel eléctrico sigue un patrón binario.",
                "Necesitas ver bien para identificar el patrón correcto.",
                "Los interruptores deben estar en una secuencia específica."
            ],
            "sala_servidores": [
                "La terminal necesita una tarjeta de acceso y contraseña.",
                "Observa el patrón de luces de los servidores.",
                "La información del router podría ser útil."
            ],
            "sala_control": [
                "La puerta de salida requiere resolver todos los puzzles.",
                "Reúne todos los códigos que has encontrado.",
                "La consola central controla todo el sistema."
            ]
        }
        
        pista = random.choice(pistas.get(self.ubicacion_actual, ["Sigue explorando y examinando todo."]))
        self.mostrar_pista(f"💡 Pista #{self.pistas_usadas}: {pista}")
    
    def resolver_puzzle(self, puzzle, solucion):
        """Resolver un puzzle"""
        if puzzle in self.puzzles_resueltos:
            self.mostrar_pista("Este puzzle ya está resuelto.")
            return False
        
        if puzzle == "caja_fuerte" and self.ubicacion_actual == "oficina":
            respuesta = self.pedir_input("Introduce el código de 3 dígitos:")
            if respuesta == solucion:
                self.puzzles_resueltos.append("caja_fuerte")
                self.mostrar_pista("✅ ¡Caja fuerte abierta! Encuentras un documento importante.")
                self.habitaciones["oficina"]["objetos"].append("documento_secreto")
                return True
            else:
                self.mostrar_pista("❌ Código incorrecto.")
                return False
        
        elif puzzle == "panel_electrico" and self.ubicacion_actual == "pasillo_oscuro":
            self.mostrar_pista("💡 El patrón correcto es: ON-OFF-ON-OFF-ON-OFF")
            self.puzzles_resueltos.append("panel_electrico")
            self.mostrar_pista("✅ ¡Luz restaurada! El pasillo ahora está iluminado.")
            return True
        
        elif puzzle == "terminal" and self.ubicacion_actual == "sala_servidores":
            if "tarjeta_magnética" not in self.inventario:
                self.mostrar_pista("❌ Necesitas una tarjeta de acceso.")
                return False
            
            respuesta = self.pedir_input("Introduce la contraseña para el Nivel 2:")
            if respuesta.lower() == solucion:
                self.puzzles_resueltos.append("terminal")
                self.mostrar_pista("✅ ¡Terminal desbloqueada! Obtienes acceso al sistema principal.")
                self.habitaciones["sala_servidores"]["objetos"].append("manual_sistema")
                return True
            else:
                self.mostrar_pista("❌ Contraseña incorrecta.")
                return False
        
        elif puzzle == "puerta_salida" and self.ubicacion_actual == "sala_control":
            # Verificar que todos los puzzles estén resueltos
            if len(self.puzzles_resueltos) < len(self.soluciones) - 1:
                self.mostrar_pista("❌ Necesitas resolver todos los puzzles primero.")
                return False
            
            respuesta = self.pedir_input("Introduce el código final de 4 dígitos:")
            if respuesta == solucion:
                self.puzzles_resueltos.append("puerta_salida")
                self.juego_ganado()
                return True
            else:
                self.mostrar_pista("❌ Código incorrecto.")
                return False
        
        return False
    
    def pedir_input(self, mensaje):
        """Pedir input al jugador con una ventana emergente"""
        ventana_input = tk.Toplevel(self.ventana)
        ventana_input.title("Ingresar código")
        ventana_input.geometry("300x150")
        ventana_input.configure(bg="#1a1a2e")
        ventana_input.transient(self.ventana)
        ventana_input.grab_set()
        
        tk.Label(
            ventana_input,
            text=mensaje,
            font=("Arial", 12),
            fg="white",
            bg="#1a1a2e"
        ).pack(pady=20)
        
        entrada = ttk.Entry(ventana_input, font=("Arial", 14), width=10)
        entrada.pack(pady=10)
        entrada.focus()
        
        resultado = {"valor": None}
        
        def aceptar():
            resultado["valor"] = entrada.get()
            ventana_input.destroy()
        
        btn_aceptar = tk.Button(
            ventana_input,
            text="Aceptar",
            font=("Arial", 11),
            bg="#4361ee",
            fg="white",
            command=aceptar
        )
        btn_aceptar.pack(pady=10)
        
        self.ventana.wait_window(ventana_input)
        return resultado["valor"]
    
    def mostrar_pista(self, mensaje):
        """Mostrar un mensaje en el área de pistas"""
        self.pista_text.config(state=tk.NORMAL)
        self.pista_text.delete(1.0, tk.END)
        self.pista_text.insert(tk.END, mensaje)
        self.pista_text.config(state=tk.DISABLED)
    
    def mostrar_inventario_detallado(self):
        """Mostrar inventario detallado"""
        if self.inventario:
            items = "\n".join([f"• {obj.replace('_', ' ').title()}" for obj in self.inventario])
            self.mostrar_pista(f"🎒 INVENTARIO ({len(self.inventario)} objetos):\n\n{items}")
        else:
            self.mostrar_pista("🎒 Tu inventario está vacío.")
    
    def mostrar_ayuda(self):
        """Mostrar ayuda de comandos"""
        ayuda = """
        🎮 COMANDOS DISPONIBLES:
        
        MOVIMIENTO:
        - norte, sur, este, oeste: Moverse
        - mirar: Ver la habitación actual
        
        INTERACCIÓN:
        - coger [objeto]: Tomar un objeto
        - usar [objeto] en [destino]: Usar objeto
        - examinar [elemento]: Examinar algo
        - combinar [objeto1] con [objeto2]: Combinar objetos
        
        INFORMACIÓN:
        - inventario: Ver objetos que llevas
        - pedir pista: Obtener una pista
        - ayuda: Mostrar esta ayuda
        
        SISTEMA:
        - guardar: Guardar partida
        - cargar: Cargar partida
        - reiniciar: Reiniciar juego
        - salir: Salir del juego
        
        💡 CONSEJOS:
        - Examina TODO cuidadosamente
        - Combina objetos cuando sea posible
        - Toma nota de los códigos que encuentres
        - Usa pistas si estás atascado
        """
        self.mostrar_pista(ayuda)
    
    def cargar_y_actualizar(self):
        """Cargar partida y actualizar interfaz"""
        self.cargar_partida()
        self.actualizar_interfaz()
        self.mostrar_pista("✅ Partida cargada exitosamente.")
    
    def reiniciar_juego(self):
        """Reiniciar el juego"""
        respuesta = messagebox.askyesno("Reiniciar", "¿Estás seguro de que quieres reiniciar? Se perderá el progreso actual.")
        if respuesta:
            # Restaurar valores iniciales
            self.ubicacion_actual = "laboratorio"
            self.inventario = []
            self.juego_activo = True
            self.tiempo_inicio = time.time()
            self.pistas_usadas = 0
            self.objetos_combinados = []
            self.codigos_descubiertos = []
            self.puzzles_resueltos = []
            
            # Restaurar habitaciones
            self.habitaciones = {
                "laboratorio": {
                    "nombre": "🧪 Laboratorio de Experimentos",
                    "descripcion": "Un laboratorio abandonado lleno de equipos científicos. Hay un olor químico en el aire.",
                    "imagen": "🔬",
                    "salidas": {"este": "oficina", "sur": "archivos"},
                    "objetos": ["llave_roja", "nota_rasgada"],
                    "puzzle": None,
                    "examinar": {
                        "mesa": "Una mesa con tubos de ensayo y un microscopio. Uno de los tubos contiene un líquido brillante.",
                        "computadora": "La pantalla muestra: 'Sistema bloqueado. Requiere clave de acceso.'",
                        "pizarra": "En la pizarra hay ecuaciones químicas y la frase: 'La verdad está en los números'"
                    }
                },
                # ... (resto de habitaciones)
            }
            
            self.actualizar_interfaz()
            self.mostrar_pista("🔄 Juego reiniciado. ¡Buena suerte!")
    
    def juego_ganado(self):
        """Mostrar mensaje de victoria"""
        self.juego_activo = False
        tiempo_total = time.time() - self.tiempo_inicio
        minutos = int(tiempo_total // 60)
        segundos = int(tiempo_total % 60)
        
        mensaje = f"""
        🎉 ¡ESCAPE EXITOSO! 🎉
        
        Has escapado del laboratorio en {minutos} minutos y {segundos} segundos.
        
        ESTADÍSTICAS:
        • Pistas usadas: {self.pistas_usadas}
        • Puzzles resueltos: {len(self.puzzles_resueltos)}/{len(self.soluciones)}
        • Objetos recolectados: {len(self.inventario)}
        • Combinaciones creadas: {len(self.objetos_combinados)}
        
        ¡Felicidades! Has demostrado ser un maestro del escape.
        """
        
        messagebox.showinfo("¡Victoria!", mensaje)
        self.ventana.destroy()
    
    def juego_terminado(self, motivo):
        """Mostrar mensaje de derrota"""
        self.juego_activo = False
        mensaje = f"""
        💀 JUEGO TERMINADO 💀
        
        {motivo}
        
        ESTADÍSTICAS:
        • Progreso: {(len(self.puzzles_resueltos) / len(self.soluciones)) * 100:.0f}%
        • Pistas usadas: {self.pistas_usadas}
        • Objetos recolectados: {len(self.inventario)}
        • Tiempo jugado: {int((time.time() - self.tiempo_inicio) / 60)} minutos
        
        ¿Quieres intentarlo de nuevo?
        """
        
        respuesta = messagebox.askyesno("Game Over", mensaje)
        if respuesta:
            self.reiniciar_juego()
        else:
            self.ventana.destroy()
    
    def salir_juego(self):
        """Salir del juego"""
        respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir? Se guardará tu progreso.")
        if respuesta:
            self.guardar_partida()
            self.ventana.destroy()
    
    def iniciar(self):
        """Iniciar el juego"""
        self.ventana.mainloop()

# Ejecutar el juego
if __name__ == "__main__":
    juego = EscapeRoom()
    juego.iniciar()