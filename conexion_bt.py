import asyncio
import tkinter as tk
from tkinter import messagebox
from bleak import BleakScanner, BleakClient

class BluetoothApp:
    def __init__(self, master):
        self.master = master
        master.title("Conexión BLE con Bleak")
        master.geometry("450x400")

        self.devices = []

        self.search_button = tk.Button(master, text="Buscar dispositivos", command=self.buscar_dispositivos)
        self.search_button.pack(pady=10)

        self.device_listbox = tk.Listbox(master, width=60)
        self.device_listbox.pack(pady=10)

        self.connect_button = tk.Button(master, text="Conectar", command=self.conectar)
        self.connect_button.pack(pady=10)

        self.status_label = tk.Label(master, text="Estado: Esperando", fg="blue")
        self.status_label.pack(pady=10)

        self.client = None

    def buscar_dispositivos(self):
        self.device_listbox.delete(0, tk.END)
        self.status_label.config(text="Buscando dispositivos BLE...")

        async def scan():
            self.devices = await BleakScanner.discover(timeout=5.0)
            for i, d in enumerate(self.devices):
                self.device_listbox.insert(tk.END, f"{d.name or 'Desconocido'} - {d.address}")
            self.status_label.config(text="Dispositivos encontrados")

        asyncio.run(scan())

    def conectar(self):
        seleccion = self.device_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccioná un dispositivo para conectar.")
            return

        dispositivo = self.devices[seleccion[0]]
        address = dispositivo.address

        async def connect_to_device():
            try:
                self.client = BleakClient(address)
                await self.client.connect()
                if self.client.is_connected:
                    self.status_label.config(text=f"Conectado a {dispositivo.name}")
                    messagebox.showinfo("Éxito", f"Conectado a {dispositivo.name or address}")
                else:
                    self.status_label.config(text="Fallo en la conexión")
            except Exception as e:
                self.status_label.config(text="Error en la conexión")
                messagebox.showerror("Error", str(e))

        asyncio.run(connect_to_device())

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()
