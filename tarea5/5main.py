from flask import Flask, render_template, request, redirect, url_for
import redis
import json

# Configuración de la base de datos Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)

@app.route('/')
def index():
    recetas = client.keys()
    return render_template('index.html', recetas=recetas)

@app.route('/receta/<nombre>')
def ver_receta(nombre):
    receta = client.hgetall(nombre)
    if receta:
        receta['ingredientes'] = json.loads(receta['ingredientes'])
        return render_template('receta.html', receta=receta)
    return 'Receta no encontrada', 404

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes'].split(',')
        pasos = request.form['pasos']
        
        receta = {
            "nombre": nombre,
            "ingredientes": json.dumps(ingredientes),
            "pasos": pasos
        }
        client.hset(nombre, mapping=receta)
        return redirect(url_for('index'))
    
    return render_template('agregar.html')

@app.route('/actualizar/<nombre>', methods=['GET', 'POST'])
def actualizar_receta(nombre):
    receta = client.hgetall(nombre)
    if not receta:
        return 'Receta no encontrada', 404
    
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevos_ingredientes = request.form['ingredientes'].split(',')
        nuevos_pasos = request.form['pasos']
        
        nueva_receta = {
            "nombre": nuevo_nombre,
            "ingredientes": json.dumps(nuevos_ingredientes),
            "pasos": nuevos_pasos
        }
        client.delete(nombre)  # Eliminar la antigua receta
        client.hset(nuevo_nombre, mapping=nueva_receta)  # Insertar la nueva receta
        return redirect(url_for('index'))
    
    receta['ingredientes'] = json.loads(receta['ingredientes'])
    return render_template('actualizar.html', receta=receta)

@app.route('/eliminar/<nombre>')
def eliminar_receta(nombre):
    client.delete(nombre)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
