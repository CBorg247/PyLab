from flask import Flask, render_template, request
import base64

app = Flask(__name__)

def cifrar_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            mayuscula = char.isupper()
            char = chr(((ord(char.lower()) - 97 + desplazamiento) % 26) + 97)
            if mayuscula:
                char = char.upper()
        resultado += char
    return resultado

def descifrar_cesar(texto, desplazamiento):
    return cifrar_cesar(texto, -desplazamiento)

def cifrar_base64(texto):
    return base64.b64encode(texto.encode()).decode()

def decodificar_base64(texto):
    try:
        return base64.b64decode(texto).decode()
    except Exception:
        return "Error: No se pudo decodificar el texto en Base64."

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""
    error = ""

    if request.method == "POST":
        accion = request.form.get("accion", "")
        texto = request.form.get("texto", "").strip()
        metodo = request.form.get("metodo", "")
        desplazamiento = request.form.get("desplazamiento", "0")

        if not texto:
            error = "Error: Debes ingresar un texto."
        elif len(texto) > 150:
            error = "Error: El texto no puede superar los 150 caracteres."
        else:
            if metodo == "cesar":
                try:
                    desplazamiento = int(desplazamiento)
                    if desplazamiento < 1:
                        error = "Error: El desplazamiento debe ser mayor que 0."
                    else:
                        if accion == "cifrar":
                            resultado = cifrar_cesar(texto, desplazamiento)
                        elif accion == "descifrar":
                            resultado = descifrar_cesar(texto, desplazamiento)
                        else:
                            error = "Error: Acción no válida."
                except ValueError:
                    error = "Error: El desplazamiento debe ser un número."

            elif metodo == "base64":
                if accion == "cifrar":
                    resultado = cifrar_base64(texto)
                elif accion == "descifrar":
                    resultado = decodificar_base64(texto)
                else:
                    error = "Error: Acción no válida."

            else:
                error = "Error: Método no válido."

    return render_template("Descifrador_pantalla.html", resultado=resultado, error=error)

if __name__ == "__main__":
    app.run(debug=True)