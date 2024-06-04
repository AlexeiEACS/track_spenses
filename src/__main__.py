from flask import Flask, render_template, request, redirect, url_for, flash
from database import SessionLocal, Transaccion

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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

        session = SessionLocal()
        nueva_transaccion = Transaccion(
            descripcion=descripcion,
            monto=monto,
            categoria=categoria,
            tipo=tipo
        )
        session.add(nueva_transaccion)
        session.commit()
        session.close()
        flash('Transacción agregada con éxito')
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == "__main__":
    app.run(debug=True)