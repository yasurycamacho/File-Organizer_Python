import os # Manejo de archivos y directorios
import shutil  # Para mover archivos
import tkinter as tk # Interfaz gráfica
from tkinter import filedialog, messagebox
from tkinter import ttk # Barra de progreso
def organizar_archivos():
    # Abrir selector de carpeta
    ruta = filedialog.askdirectory(title="Select folder to organize")
    #Validar si el usuario no seleccionó nada
    if not ruta:
        estado_label.config(text="No folder selected.")
        return
    # Verificar que la ruta exista realmente
    if not os.path.isdir(ruta):
        messagebox.showerror("Error", "The selected path does not exist.")
        return
    # Desactivar botón mientras se ejecuta el proceso
    boton.config(state="disabled")
    estado_label.config(text="Organizing files...")
    ventana.update()

    contador = 0 # Contador de archivos movidos
    # Diccionario de categorías y sus extensiones
    categorias = {
    "Images": ["JPG", "JPEG", "PNG", "GIF"],
    "Videos": ["MP4", "AVI", "MKV"],
    "Documents": ["PDF", "DOCX", "DOC","XLSX","XLS", "TXT", "CSV","PPTX"]
    }
    # Normaliza nombres de carpetas (primera letra mayúscula)
    for nombre in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, nombre)

        if os.path.isdir(ruta_completa):
            nombre_correcto = nombre.capitalize()

            if nombre != nombre_correcto:
                nueva_ruta = os.path.join(ruta, nombre_correcto)
                # Evita sobrescribir carpetas existentes
                if not os.path.exists(nueva_ruta):
                    os.rename(ruta_completa, nueva_ruta)
    # Obtener solo archivos (no carpetas)
    archivos = [
    f for f in os.listdir(ruta)
    if os.path.isfile(os.path.join(ruta, f))
]
    # Procesar cada archivo
    barra["maximum"] = len(archivos)

    for elemento in archivos:
        ruta_completa = os.path.join(ruta, elemento)
        # Separar nombre y extensión
        nombre, extension = os.path.splitext(elemento)
        extension_limpia = extension.lstrip(".").upper()
        # Si no tiene extensión, clasificar como OTHER
        if extension_limpia == "":
            extension_limpia = "OTHER"

        tipo_principal = "Others"

        for categoria, extensiones in categorias.items():
            if extension_limpia in extensiones:
                tipo_principal = categoria
                break
        # Crear subcarpetas por extensión solo para documentos
        if tipo_principal == "Documents":
            carpeta_destino = os.path.join(ruta, tipo_principal, extension_limpia)
        else:
            carpeta_destino = os.path.join(ruta, tipo_principal)
        # Crear carpeta si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        destino_final = os.path.join(carpeta_destino, elemento)

    # Evita renombrar innecesario
        if os.path.exists(destino_final):
            if os.path.abspath(ruta_completa) != os.path.abspath(destino_final):
                contador_nombre = 1
                base, ext = os.path.splitext(elemento)
                # Generar nuevo nombre si ya existe
                while os.path.exists(destino_final):
                    nuevo_nombre = f"{base}_{contador_nombre}{ext}"
                    destino_final = os.path.join(carpeta_destino, nuevo_nombre)
                    contador_nombre += 1
            else:
                continue
        # Mover archivo a su destino
        shutil.move(ruta_completa, destino_final)
        # Actualizar contador y barra
        contador += 1
        barra["value"] += 1
        ventana.update_idletasks()
    # Mostrar resultado final
    if contador == 0:
        estado_label.config(text="No files to organize.")
        messagebox.showinfo("Information", "No files were found to move.")
    else:
        estado_label.config(text=f"{contador} files organized successfully.")
        messagebox.showinfo("Process Completed", f"{contador} files were moved successfully.")
    # Resetear barra y botón
    barra["value"] = 0
    boton.config(state="normal")
# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
ventana = tk.Tk()
ventana.title("Smart Folder Organizer")
ventana.configure(bg="#F4F4F8")
# Intentar cargar icono
try:
    ventana.iconbitmap("icono.ico")
except Exception as e:
    print("Icon could not be loaded:", e)
# Tamaño de ventana
ventana.geometry("450x300")
ventana.resizable(False, False)
# Tamaño de ventana
ancho = 450
alto = 300
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()
x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)
ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
# Título principal
titulo = tk.Label(
    ventana,
    text="Organize Your Files Automatically",
    font=("Segoe UI", 14, "bold"),
    bg="#F4F4F8",
    fg="#1C1C1C"
)
titulo.pack(pady=20)
# Descripción
descripcion = tk.Label(
    ventana,
    text="Sort your files into folders by extension.",
    font=("Segoe UI", 10),
    bg="#F4F4F8",
    fg="#1C1C1C"
)
descripcion.pack(pady=5)
# Botón principal
boton = tk.Button(
    ventana,
    text="Select Folder & Organize",
    font=("Segoe UI", 11, "bold"),
    bg="#7D3C98",
    fg="white",
    activebackground="#5B2C6F",
    relief="flat",
    padx=16,
    pady=8,
    cursor="hand2",
    command=organizar_archivos
)
boton.pack(pady=20)
# Barra de progreso
barra = ttk.Progressbar(
    ventana,
    orient="horizontal",
    length=300,
    mode="determinate"
)
barra.pack(pady=10)
# Estado del proceso
estado_label = tk.Label(
    ventana,
    text="Waiting for action...",
    font=("Segoe UI", 9),
    fg="gray",
    bg="#F4F4F8"
)
estado_label.pack(pady=10)
# Footer
footer = tk.Label(
    ventana,
    text="Smart Folder Organizer v1.0",
    font=("Segoe UI", 8),
    fg="gray",
    bg="#F4F4F8"
)

footer.pack(side="bottom", pady=5)
# Ejecutar app
ventana.mainloop()



