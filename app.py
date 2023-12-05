from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Importa la configuración desde el archivo config.py

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Usuario(db.Model):
    dni = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100))
    telefono = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    detalles_adicionales = db.Column(db.String(200))
    usuario_activo = db.Column(db.String(10), default='activo', nullable=False)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/usuarios')
def index():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/nuevo_usuario', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        try:
            dni = request.form['dni']
            nombre = request.form['nombre']
            correo = request.form['correo']
            telefono = request.form['telefono']
            edad = request.form['edad']
            genero = request.form['genero']
            plan = request.form['plan']
            detalles = request.form['detalles']
            usuario_activo = request.form['usuario_activo']

            nuevo_usuario = Usuario(
                dni=dni,
                nombre=nombre,
                correo_electronico=correo,
                telefono=telefono,
                edad=edad,
                genero=genero,
                plan=plan,
                detalles_adicionales=detalles,
                usuario_activo=usuario_activo
            )

            db.session.add(nuevo_usuario)
            db.session.commit()

            flash('Usuario creado exitosamente.')
            return redirect(url_for('usuarios'))

        except IntegrityError as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e):
                flash('Error: El DNI ya está en uso. Por favor, elija otro.')
            else:
                flash('Error al crear el usuario. Por favor, inténtelo nuevamente.')
            return redirect(url_for('nuevo_usuario'))

    return render_template('nuevo_usuario.html')

@app.route('/editar_usuario/<int:dni>', methods=['GET', 'POST'])
def editar_usuario(dni):
    usuario = Usuario.query.get(dni)

    if request.method == 'POST':
        # Actualiza los datos del usuario
        usuario.nombre = request.form['nombre']
        usuario.correo_electronico = request.form['correo']
        usuario.telefono = request.form['telefono']
        usuario.edad = request.form['edad']
        usuario.genero = request.form['genero']
        usuario.plan = request.form['plan']
        usuario.detalles_adicionales = request.form['detalles']
        usuario.usuario_activo = request.form['usuario_activo']

        # Guarda los cambios en la base de datos
        db.session.commit()

        return redirect(url_for('usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:dni>')
def eliminar_usuario(dni):
    usuario = Usuario.query.get(dni)

    # Elimina el usuario de la base de datos
    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for('usuarios'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)