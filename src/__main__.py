
from flask import Flask, render_template, request, redirect, url_for, flash
from database import SessionLocal, Transaccion
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Free IP geolocation API endpoint
GEOLOCATION_API_URL = "https://ipapi.co/json/"

def get_geolocation():
    try:
        response = requests.get(GEOLOCATION_API_URL)
        data = response.json()
        return data.get("latitude"), data.get("longitude")
    except Exception as e:
        print(f"Error getting geolocation: {e}")
        return None, None

# Rutas de la aplicación
@app.route('/')
def index():
    session = SessionLocal()
    transacciones = session.query(Transaccion).all()
    session.close()
    return render_template('index.html', transacciones=transacciones)

@app.route('/add', methods=['GET', 'POST'])
def add_transaccion():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        categoria = request.form['categoria']
        tipo = request.form['tipo']

        if not descripcion or not monto or not categoria or not tipo:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('add_transaccion'))

        try:
            monto = float(monto)
        except ValueError:
            flash('El monto debe ser un número')
            return redirect(url_for('add_transaccion'))

        latitude, longitude = get_geolocation()

        session = SessionLocal()
        nueva_transaccion = Transaccion(
            descripcion=descripcion,
            monto=monto,
            categoria=categoria,
            tipo=tipo,
            latitude=latitude,
            longitude=longitude
        )
        session.add(nueva_transaccion)
        session.commit()
        session.close()
        flash('Transacción agregada con éxito')
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == "__main__":
    app.run(debug=True)
