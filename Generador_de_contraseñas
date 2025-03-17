import tkinter as tk
import random
import string

def actualizar_pantalla(caracter):
    pantalla.insert(tk.END, caracter)

def borrar():
    pantalla.delete(0, tk.END)

# Función para generar la contraseña
def generar_contrasena():
    print("Ejecutando generar_contrasena()")

    caracteres = ""
    if mayus_var.get():
        caracteres += string.ascii_uppercase
    if minus_var.get():
        caracteres += string.ascii_lowercase
    if numeros_var.get():
        caracteres += string.digits
    if especiales_var.get():
        caracteres += string.punctuation
    print("Mayúsculas:", mayus_var.get(), "Minúsculas:", minus_var.get(), "Números:", numeros_var.get(), "Especiales:", especiales_var.get())

    if longitud < 6 or longitud > 10:
        longitud = int(longitud_var.get())
        
        print("Longitud ingresada:", longitud_var.get())
        
    else:
        resultado_var.set("Error: Longitud inválida")
        return
        
        if caracteres:
            contraseña = "".join(random.choice(caracteres) for _ in range(longitud))
            print("Contraseña generada:", contraseña)
            resultado_var.set(contraseña)
            pantalla.delete(0, tk.END)
            pantalla.insert(tk.END, str(contraseña))


        else:
            resultado_var.set("Seleccione al menos un tipo")

    except ValueError:
        resultado_var.set("Error: Ingrese un número válido")

def on_enter(boton):
    boton.config(bg="#FF69B4")

def on_leave(boton):
    boton.config(bg="#FADADD")

# Crear ventana
pantalla = tk.Tk()
pantalla.title("Generador de Contraseñas")
pantalla.configure(bg="#D0F0C0")  # Fondo verde claro
pantalla.geometry("300x350")

# Variables
mayus_var = tk.BooleanVar()
minus_var = tk.BooleanVar()
numeros_var = tk.BooleanVar()
especiales_var = tk.BooleanVar()
longitud_var = tk.StringVar(value="10")  # Longitud por defecto
resultado_var = tk.StringVar()

# Estilo de los botones
btn_style = {"bg":"#FF69B4", "font": ("Times New Roman", 14, "bold"), "padx": 10, "pady": 5}

# Elementos de la interfaz
tk.Label(pantalla, text="Seleccione los tipos de caracteres:", bg="#D0F0C0").grid(row=0, column=0, padx=10, pady=10, sticky="w")

tk.Checkbutton(pantalla, text="Mayúsculas", variable=mayus_var, bg="#D0F0C0").grid(row=1, column=0, padx=10, sticky="w")
tk.Checkbutton(pantalla, text="Minúsculas", variable=minus_var, bg="#D0F0C0").grid(row=2, column=0, padx=10, sticky="w")
tk.Checkbutton(pantalla, text="Números", variable=numeros_var, bg="#D0F0C0").grid(row=3, column=0, padx=10, sticky="w")
tk.Checkbutton(pantalla, text="Caracteres especiales", variable=especiales_var, bg="#D0F0C0").grid(row=4, column=0, padx=10, sticky="w")

tk.Label(pantalla, text="Longitud de la contraseña (6-10):", bg="#D0F0C0").grid(row=5, column=0, padx=10, pady=10, sticky="w")
tk.Entry(pantalla, textvariable=longitud_var, width=5).grid(row=6, column=0, padx=10, pady=5)

tk.Button(pantalla, text="Generar Contraseña", command = generar_contrasena, **btn_style).grid(row=7, column=0, padx=10, pady=10)

tk.Label(pantalla, text="Contraseña generada:", bg="#D0F0C0").grid(row=8, column=0, padx=10, pady=10, sticky="w")
pantalla_display = tk.Entry(pantalla, textvariable=resultado_var, state="readonly", width=20)
pantalla_display.grid(row=9, column=0, padx=10, pady=5)


# Iniciar aplicación
pantalla.mainloop()

# Iniciar la interfaz
pantalla.mainloop()
