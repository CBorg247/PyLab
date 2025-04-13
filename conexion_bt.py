import bluetooth
import tkinter as tk
from tkinter import messagebox

class BluetoothApp:
    def __init__(self, master):
        self.master = master
        master.title("Conexión Bluetooth")
        master.geometry("400x400")

        self.devices = []

        self.search_button = tk.Button(master, text="Buscar dispositivos", command=self.buscar_dispositivos)
        self.search_button.pack(pady=10)

        self.device_listbox = tk.Listbox(master, width=50)
        self.device_listbox.pack(pady=10)

        self.connect_button = tk.Button(master, text="Conectar", command=self.conectar)
        self.connect_button.pack(pady=10)

        self.status_label = tk.Label(master, text="Estado: Esperando", fg="blue")
        self.status_label.pack(pady=10)

        self.sock = None

    def buscar_dispositivos(self):
        self.status_label.config(text="Buscando dispositivos...")
        self.device_listbox.delete(0, tk.END)
        self.devices = bluetooth.discover_devices(duration=8, lookup_names=True)

        if not self.devices:
            self.status_label.config(text="No se encontraron dispositivos")
            return

        for addr, name in self.devices:
            self.device_listbox.insert(tk.END, f"{name} - {addr}")
        self.status_label.config(text="Dispositivos encontrados")

    def conectar(self):
        seleccion = self.device_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccioná un dispositivo para conectar.")
            return

        nombre_dispositivo, mac = self.devices[seleccion[0]]

        port = 1  # RFCOMM normalmente usa el puerto 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        try:
            self.sock.connect((mac, port))
            self.status_label.config(text=f"Conectado a {nombre_dispositivo}")
            messagebox.showinfo("Éxito", f"Conectado a {nombre_dispositivo}")
        except Exception as e:
            self.status_label.config(text="Error en la conexión")
            messagebox.showerror("Error", f"No se pudo conectar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()
