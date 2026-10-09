#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# --- DICCIONARIO DE TEMAS ---
TEMAS = {
    "oscuro": {
        "bg_ventana": "#1e1e1e",
        "bg_texto": "#2d2d2d",
        "fg_texto": "white",
        "menu_bg": "#2d2d2d",
        "menu_fg": "white",
        "insert": "white",
        "bg_status": "#111111",
        "fg_status": "#aaaaaa"
    },
    "claro": {
        "bg_ventana": "#f0f0f0",
        "bg_texto": "#ffffff",
        "fg_texto": "#333333",
        "menu_bg": "#ffffff",
        "menu_fg": "#333333",
        "insert": "#333333",
        "bg_status": "#e0e0e0",
        "fg_status": "#555555"
    },
    "hacker": {
        "bg_ventana": "#0d0208",
        "bg_texto": "#1a0005",
        "fg_texto": "#00ff66",
        "menu_bg": "#161b22",
        "menu_fg": "#00ff66",
        "insert": "#00ff66",
        "bg_status": "#050103",
        "fg_status": "#00aa44"
    }
}

tema_actual = "oscuro"
archivo_actual = None
tamanio_fuente = 12

def nuevo_archivo(event=None):
    global archivo_actual
    texto.delete("1.0", tk.END)
    archivo_actual = None
    ventana.title("Bloc de Notas - Sin título")
    actualizar_estado()

def abrir_archivo(event=None):
    global archivo_actual
    ruta = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if ruta:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            texto.delete("1.0", tk.END)
            texto.insert("1.0", contenido)
            archivo_actual = ruta
            ventana.title(f"Bloc de Notas - {ruta}")
            actualizar_estado()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

def guardar_archivo(event=None):
    global archivo_actual
    if archivo_actual:
        try:
            contenido = texto.get("1.0", tk.END)
            with open(archivo_actual, "w", encoding="utf-8") as f:
                f.write(contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
    else:
        guardar_como()

def guardar_como(event=None):
    global archivo_actual
    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if ruta:
        try:
            contenido = texto.get("1.0", tk.END)
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            archivo_actual = ruta
            ventana.title(f"Bloc de Notas - {ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def buscar_texto():
    palabra = simpledialog.askstring("Buscar", "Introduce el texto a buscar:")
    if palabra:
        # Eliminar marcas de búsquedas anteriores
        texto.tag_remove("coincidencia", "1.0", tk.END)
        matches = 0
        inicio = "1.0"
        while True:
            inicio = texto.search(palabra, inicio, stopindex=tk.END, nocase=True)
            if not inicio:
                break
            fin = f"{inicio}+{len(palabra)}c"
            texto.tag_add("coincidencia", inicio, fin)
            matches += 1
            inicio = fin
        
        # Estilo visual para la palabra encontrada
        texto.tag_config("coincidencia", background="yellow", foreground="black")
        messagebox.showinfo("Resultado", f"Se encontraron {matches} coincidencia(s)")

def cambiar_fuente(delta):
    global tamanio_fuente
    tamanio_fuente += delta
    if tamanio_fuente < 8: 
        tamanio_fuente = 8
    texto.config(font=("Courier", tamanio_fuente))

def actualizar_estado(event=None):
    contenido = texto.get("1.0", "end-1c")
    palabras = len(contenido.split()) if contenido.strip() else 0
    caracteres = len(contenido)
    lineas = texto.index("end-1c").split(".")[0]
    label_estado.config(text=f" Líneas: {lineas} | Palabras: {palabras} | Caracteres: {caracteres} ")

def aplicar_tema(nombre_tema):
    global tema_actual
    tema_actual = nombre_tema
    t = TEMAS[tema_actual]

    ventana.config(bg=t["bg_ventana"])
    barra_menu.config(bg=t["menu_bg"], fg=t["menu_fg"])
    menu_archivo.config(bg=t["menu_bg"], fg=t["menu_fg"])
    menu_editar.config(bg=t["menu_bg"], fg=t["menu_fg"])
    menu_ver.config(bg=t["menu_bg"], fg=t["menu_fg"])
    menu_temas.config(bg=t["menu_bg"], fg=t["menu_fg"])
    
    texto.config(
        bg=t["bg_texto"], 
        fg=t["fg_texto"], 
        insertbackground=t["insert"]
    )
    scroll.config(bg=t["bg_ventana"])
    label_estado.config(bg=t["bg_status"], fg=t["fg_status"])

# --- VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Bloc de Notas - Sin título")
ventana.geometry("650x450")
t = TEMAS[tema_actual]
ventana.config(bg=t["bg_ventana"])

# --- BARRA DE MENÚ ---
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Menú Archivo
menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Nuevo", command=nuevo_archivo, accelerator="Ctrl+N")
menu_archivo.add_command(label="Abrir...", command=abrir_archivo, accelerator="Ctrl+O")
menu_archivo.add_command(label="Guardar", command=guardar_archivo, accelerator="Ctrl+S")
menu_archivo.add_command(label="Guardar como...", command=guardar_como)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=ventana.quit)

# Menú Editar
menu_editar = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Editar", menu=menu_editar)
menu_editar.add_command(label="Buscar...", command=buscar_texto, accelerator="Ctrl+F")

# Menú Ver (Zoom y Temas)
menu_ver = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ver", menu=menu_ver)
menu_ver.add_command(label="Acercar fuente (+)", command=lambda: cambiar_fuente(2))
menu_ver.add_command(label="Alejar fuente (-)", command=lambda: cambiar_fuente(-2))

menu_temas = tk.Menu(menu_ver, tearoff=0)
menu_ver.add_cascade(label="Temas", menu=menu_temas)
menu_temas.add_command(label="Oscuro (Default)", command=lambda: aplicar_tema("oscuro"))
menu_temas.add_command(label="Claro", command=lambda: aplicar_tema("claro"))
menu_temas.add_command(label="Hacker (Neon)", command=lambda: aplicar_tema("hacker"))

# --- ATAJOS DE TECLADO RÁPIDOS ---
ventana.bind("<Control-n>", nuevo_archivo)
ventana.bind("<Control-o>", abrir_archivo)
ventana.bind("<Control-s>", guardar_archivo)

# --- ÁREA DE TEXTO Y SCROLLBAR ---
scroll = tk.Scrollbar(ventana)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

texto = tk.Text(
    ventana, 
    wrap=tk.WORD, 
    font=("Courier", tamanio_fuente), 
    bd=0, 
    highlightthickness=0,
    bg=t["bg_texto"], 
    fg=t["fg_texto"], 
    insertbackground=t["insert"],
    yscrollcommand=scroll.set
)
texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
scroll.config(command=texto.yview)

# Evento para actualizar el contador en tiempo real al escribir
texto.bind("<KeyRelease>", actualizar_estado)

# --- BARRA DE ESTADO INFERIOR ---
label_estado = tk.Label(ventana, text=" Líneas: 1 | Palabras: 0 | Caracteres: 0 ", anchor="w", bg=t["bg_status"], fg=t["fg_status"])
label_estado.pack(side=tk.BOTTOM, fill=tk.X)

ventana.mainloop()
