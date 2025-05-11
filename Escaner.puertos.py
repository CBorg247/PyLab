import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, simpledialog, filedialog
import subprocess
import re
import socket
import threading
from datetime import datetime

puerto_buttons = []

# ---------- Funciones de validación ----------
def validar_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

def validar_rango(rango):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$"
    return re.match(pattern, rango) is not None

# ---------- Escaneo con nmap ----------
def ejecutar_nmap(ip):
    comando = ["nmap", "-Pn", "-sS", "-sV", "-p-", "--min-rate", "100", "--max-retries", "3", ip]
    try:
        resultado = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
        return resultado
    except subprocess.CalledProcessError as e:
        return f"[ERROR]\n{e.output}"

def escanear_manual(ip, rango_puertos, resultado_text, label_estado):
    resultado_text.config(state="normal")
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"Escaneando puertos manualmente en {ip}...\n")
    resultado_text.config(state="disabled")

    def tarea():
        abiertos = []
        for puerto in rango_puertos:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip, puerto)) == 0:
                    abiertos.append(puerto)

        resultado_text.config(state="normal")
        resultado_text.insert(tk.END, f"Puertos abiertos: {abiertos}\n")
        resultado_text.config(state="disabled")
        label_estado.config(text="✅ Escaneo manual completado.")

    threading.Thread(target=tarea).start()

# ---------- Conexión manual a puerto ----------
def conectar_puerto(ip, puerto):
    resultado = ejecutar_nmap(ip)
    puertos = re.findall(r"^(\d+)/tcp\s+open", resultado, re.MULTILINE)

    if puertos:
        for widget in frame_socket.winfo_children():
            widget.destroy()

        ttk.Label(frame_socket, text="Puertos abiertos detectados. Seleccione uno para conectar:").pack(pady=5)
        for puerto in puertos:
            boton = ttk.Button(frame_socket, text=f"Conectar al puerto {puerto}",
                                   command=lambda p=puerto: conectar_socket(ip, int(p)))
            boton.pack(pady=2)

        btn_desconectar = ttk.Button(frame_socket, text="Desconectar", command=desconectar_socket)
        btn_desconectar.pack(pady=10)

def conectar_socket(ip, puerto):
    global conexion_socket
    try:
        conexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexion_socket.settimeout(5)
        conexion_socket.connect((ip, puerto))
        messagebox.showinfo("Conexión", f"Conectado exitosamente a {ip}:{puerto}")
    except Exception as e:
        messagebox.showerror("Error de conexión", str(e))

def desconectar_socket():
    global conexion_socket
    if conexion_socket:
        conexion_socket.close()
        conexion_socket = None
        messagebox.showinfo("Desconectado", "Conexión cerrada exitosamente")


threads = []

# ---------- Exportación de resultados ----------

def mostrar_resultado(resultado, resultado_text, label_estado):
    resultado_text.config(state="normal")
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, resultado)
    resultado_text.config(state="disabled")
    label_estado.config(text="✅ Escaneo con Nmap completado.")

def exportar_resultados():
    contenido = resultado_text.get("1.0", tk.END)
    if not contenido.strip():
        messagebox.showwarning("Exportación", "No hay resultados para exportar.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
    if filename:
        with open(filename, "w") as f:
            f.write(contenido)
        messagebox.showinfo("Exportado", f"Resultados guardados en {filename}")

# ---------- Limpieza y cambio de modo ----------
def limpiar_campos():
    global puerto_buttons 
    entry_ip.delete(0, tk.END)
    entry_rango.delete(0, tk.END)
    resultado_text.delete("1.0", tk.END)
    label_estado.config(text="")
    for btn in puerto_buttons:
        btn.destroy()
    puerto_buttons.clear()

def manejar_cambio_opcion():
    limpiar_campos()

# ---------- Escaneo ----------
def escanear():
    tipo = tipo_escaneo.get()
    ip = entry_ip.get().strip()

    if not validar_ip(ip):
        messagebox.showerror("Error", "Verifique la dirección IP.")
        return

    label_estado.config(text="🔎 Escaneando...")
    resultado_text.delete("1.0", tk.END)

    if tipo == "nmap":
        def tarea():
            resultado = ejecutar_nmap(ip)
            resultado_text.config(state="normal")
            resultado_text.delete("1.0", tk.END)
            resultado_text.insert("1.0", resultado)
            resultado_text.config(state="disabled")
            label_estado.config(text="✅ Escaneo completado.")

         # Buscar puertos abiertos e insertar botones
            abiertos = re.findall(r"(\d+)/tcp\s+open", resultado)
            if abiertos:
                label_resultado_extra = tk.Label(frame_puertos, text="Puertos abiertos:", bg="#f0f0f0", fg="black")
                label_resultado_extra.pack()
            for puerto in abiertos:
                btn = tk.Button(frame_puertos, text=f"Conectar al puerto {puerto}", command=lambda p=puerto: conectar_puerto(ip, p), bg="black", fg="white")
                btn.pack(pady=2)
                puerto_buttons.append(btn)

        threading.Thread(target=tarea).start()

    elif tipo == "manual":
        rango_str = entry_rango.get().strip()
        try:
            if rango_str:
                inicio, fin = map(int, rango_str.split('-'))
                rango_puertos = range(inicio, fin + 1)
            else:
                rango_puertos = range(1, 100)
        except:
            messagebox.showerror("Error", "Rango inválido. Use el formato 20-80.")
            return
        threading.Thread(target=lambda: escanear_manual(ip, rango_puertos, resultado_text, label_estado)).start()


# ---------- Interfaz ----------
ventana = tk.Tk()
ventana.title("Escáner de Red")
ventana.geometry("500x300")
ventana.configure(bg="white")

tipo_escaneo = tk.StringVar()
tipo_escaneo.set("nmap")

frame_seleccion = tk.Frame(ventana, bg="white")
tk.Label(frame_seleccion, text="Tipo de escaneo:", bg="white", fg="black").pack(anchor="w")
tk.Radiobutton(frame_seleccion, text="Puertos simples con Nmap", variable=tipo_escaneo, value="nmap", command=manejar_cambio_opcion, bg="white", fg="black", selectcolor="gray").pack(anchor="w")
tk.Radiobutton(frame_seleccion, text="Puertos simples manual", variable=tipo_escaneo, value="manual", command=manejar_cambio_opcion, bg="white", fg="black", selectcolor="gray").pack(anchor="w")
frame_seleccion.pack(padx=10, pady=10, fill="x")

frame_inputs = tk.Frame(ventana, bg="white")
tk.Label(frame_inputs, text="Dirección IP:", bg="white", fg="black").grid(row=0, column=0, sticky="e")
entry_ip = tk.Entry(frame_inputs, bg="white", fg="black", insertbackground="black")
entry_ip.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="(opcional) Rango:", bg="white", fg="gray").grid(row=1, column=0, sticky="e")
entry_rango = tk.Entry(frame_inputs, bg="white", fg="black", insertbackground="black")
entry_rango.grid(row=1, column=1, padx=5)
frame_inputs.pack(padx=10, pady=5, fill="x")

frame_botones = tk.Frame(ventana, bg="white")
boton_escanear = tk.Button(frame_botones, text="Escanear", command=escanear, bg="black", fg="white")
boton_escanear.pack(side="left", padx=5)

boton_exportar = tk.Button(frame_botones, text="Exportar resultados", command=exportar_resultados, bg="gray", fg="white")
boton_exportar.pack(side="left", padx=5)

frame_botones.pack(pady=10)

label_estado = tk.Label(ventana, text="", fg="blue", bg="white")
label_estado.pack()

frame_texto = tk.Frame(ventana, bg="white")
scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side="right", fill="y")

resultado_text = tk.Text(frame_texto, height=10, width=80, bg="black", fg="white", insertbackground="white", yscrollcommand=scrollbar.set)
resultado_text.pack(side="left", fill="both", expand=True)
resultado_text.config(state="normal")
resultado_text.config(state="disabled")


scrollbar.config(command=resultado_text.yview)
frame_texto.pack(padx=10, pady=5, fill="both", expand=True)


frame_puertos = tk.Frame(ventana, bg="white")
frame_puertos.pack(padx=10, pady=5)

frame_socket = tk.Frame(ventana, bg="white")
frame_socket.pack(padx=10, pady=5)

ventana.mainloop()
