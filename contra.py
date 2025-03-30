from flask import Flask, render_template, request
import random
import string
import hashlib

app = Flask(__name__)

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    longitud = 12  # Más seguro con 12 caracteres
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def verificar_seguridad(contraseña):
    # 1. Verificar si la contraseña está vacía o demasiado corta
    if not contraseña:
        return "Contraseña vacía", "red"
    if len(contraseña) < 6:
        return "Muy corta. Agregue más caracteres", "fácil"
    
    # 2. Verificar si la contraseña es "Fácil"
    # Contraseñas fáciles: solo números, solo letras, solo minúsculas, etc.
    if (any(c.isdigit() for c in contraseña) and len(contraseña) < 8):
        return "Fácil. Agregue más caracteres", "fácil"
    
    # 3. Verificar si la contraseña es "Moderada"
    # Contraseñas moderadas: contiene al menos un número, una mayúscula y una minúscula, pero no tiene caracteres especiales
    if (any(c.isdigit() for c in contraseña) and 
        any(c.isupper() for c in contraseña) and 
        any(c.islower() for c in contraseña) and 
        len(contraseña) >= 8 and 
        not any(c in string.punctuation for c in contraseña)):
        return "Moderada. Agregue caracteres especiales", "moderada"
    
    # 4. Verificar si la contraseña es "Difícil"
    # Contraseñas difíciles: contiene mayúsculas, minúsculas, números, caracteres especiales y longitud > 11
    if (any(c.isdigit() for c in contraseña) and 
        any(c.isupper() for c in contraseña) and 
        any(c.islower() for c in contraseña) and 
        any(c in string.punctuation for c in contraseña) and 
        len(contraseña) > 11):
        return "Difícil. Muy segura", "difícil"
    
    # Si no cumple con ninguna de las anteriores, es "Fácil"
    return "Fácil. Agregue más caracteres", "fácil"

def hashear_contraseña(contraseña):
    if contraseña == None:
        return "Error: contraseña inexistente"
    return hashlib.sha256(contraseña.encode()).hexdigest()[:50]

@app.route('/', methods=['GET', 'POST'])
def index():
    contraseña = None
    hashed = None
    seguridad = ""
    color = ""
    
    if request.method == 'POST':
        if 'generar' in request.form:
            contraseña = generar_contraseña()
            seguridad, color = verificar_seguridad(contraseña)  
            hashed = None  
        elif 'hashear' in request.form:
            contraseña = request.form['contraseña']
            if not contraseña:
                hashed = "Error: contraseña inexistente"

            else:
                hashed = hashear_contraseña(contraseña)  # Hasheamos la contraseña ingresada
                seguridad, color = verificar_seguridad(contraseña)
    
    return render_template('contra.html', contraseña=contraseña, seguridad=seguridad, color=color, hashed=hashed)

if __name__ == "__main__":
    app.run(debug=True)
