import tkinter as tk

def validar_entrada(caracter):
    if caracter.isdigit() or caracter in "+-*/.=C":
        return True
    return False

# Función para actualizar la pantalla
def actualizar_pantalla(caracter):
    if validar_entrada(caracter):
        pantalla.insert(tk.END, caracter)

def borrar():
    pantalla.delete(0, tk.END)

def calcular():
    try:
        resultado = eval(pantalla.get())  
        pantalla.delete(0, tk.END)
        pantalla.insert(tk.END, resultado)  # Insertamos el resultado en la pantalla
    except Exception as e:
        pantalla.delete(0, tk.END)
        pantalla.insert(tk.END, "Error")  # Si hay error, mostramos "Error"

ventana = tk.Tk()
ventana.title("Calculadora")
ventana.configure(bg="#FADADD")
 
vcmd = ventana.register(validar_entrada)
pantalla = tk.Entry(ventana, width=20, font=("Times New Roman", 20), bd=15, relief="sunken", justify="right", bg="#ECF0F1", fg="black")
pantalla.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

boton_config = {
    "width": 7, "height": 3, "font": ("Times New Roman", 12, "bold"), "bg": "#FF1493", "fg": "black",
    "bd": 5, "relief": "raised"
}

# Botones de la calculadora
botones = [
    '1', '2', '3', '-',
    '4', '5', '6', '*',
    '7', '8', '9', '/',
    '0', '.', '=', '+'
]

fila = 1
columna = 0
for boton in botones:
    if boton == "=":
        tk.Button(ventana, text="=", command=calcular, **boton_config).grid(row=fila, column=columna, padx=5, pady=5)
    else:
        tk.Button(ventana, text=boton, command=lambda c=boton: actualizar_pantalla(c), **boton_config).grid(row=fila, column=columna, padx=5, pady=5)
    
    columna += 1
    if columna > 3:
        columna = 0
        fila += 1

tk.Button(ventana, text="C", command=borrar, **boton_config).grid(row=fila, column=0, padx=5, pady=5)

ventana.mainloop()
