import base64
import sqlite3
from flask import Flask, make_response, redirect, request, url_for
from flask import render_template
from flask import g
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",)


@app.route("/idor", strict_slashes=False)
@app.route("/idor/<int:cat>")
def idor(cat:int = None):
    match cat:
        case 0:
            image = "/ihfoabsdibiblsdidlbqeirugrq.jpg"
        case 1 | 2 | 3:
            image = f"{cat}.jpg"
        case _:
            image = None
    return render_template("idor.html", image=image, cat=cat)


@app.route("/csv", methods=(['GET', 'POST']))
def csv():
    saldo = 100
    if request.method == 'POST':
        importe = int(request.form['importe'])
        saldo -= importe
    return render_template("csv.html", saldo=saldo)


@app.route("/cf", methods=(['GET', 'POST']))
def cf():
    if request.method == 'POST':
        nombre = request.form['name']
        password = request.form['pass']
        
        if nombre == "pepe" and password == "passresegura":
            resp = make_response(respuesta_usuario_logueado(nombre))
            nombre64 = base64.b64encode(nombre.encode())
            resp.set_cookie('nombre', nombre64.decode())
            return resp
        else:
            mensaje = "Usuario o contraseña incorrectos"
            return make_response(render_template('cf.html', logueado=False, mensaje=mensaje))
    else:
        if 'nombre' in request.cookies:
            nombre64 = request.cookies.get('nombre')
            nombre = base64.b64decode(nombre64).decode()
            return respuesta_usuario_logueado(nombre)
        else:
            return render_template("cf.html", logueado=False)

def respuesta_usuario_logueado(nombre):
    data = None
    if nombre == "pepe":
        data = "Aca va la informacion personal de pepe"
    elif nombre == "admin":
        data = "Aca va la informacion personal de admin. Como es admin, podria llegar a ver la informacion de todos los demas usuarios"
    else:
        data = "ERROR: No encontre informacion de este usuario"
    return render_template("cf.html", nombre=nombre, logueado=True, data=data)


###################################################

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.teardown_appcontext
def close_connection(_exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/sqli", methods=(['GET', 'POST']))
def sqli():
    if request.method == 'POST':
        nombre = request.form['name']
        password = request.form['pass']
        dbname = query_db(f"SELECT Nombre FROM Usuarios WHERE Nombre = '{nombre}' AND Pass = '{password}';")
        # print(dbname)
        if dbname and dbname[0] and dbname[0][0] == nombre:
            # print(dbname[0][0])
            message = f"Bienvenido {dbname[0][0]}"
        else:
            message = "Usuario o contraseña incorrecta"
        return render_template("sqli.html", message=message)
    else:
        return render_template("sqli.html", )

###################################################

@app.route("/rxss")
def rxss():
    usuario = request.args.get('usuario')
    if not usuario:
        return redirect(url_for('rxss', usuario='Cosme Fulanito'))
    return render_template("rxss.html", usuario=usuario)

@app.route("/ci")
def ci():
    archivo = request.args.get('archivo')
    cmd = None
    output = None
    if archivo:
        if archivo.startswith("publico"):
            cmd = f"cat {archivo}"
            proc = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="static")
            o, e = proc.communicate()
            output = o.decode("ascii") + e.decode("ascii")
        else:
            cmd = "(nada)"
            output = "ERROR: El nombre del archivo debe comenzar con 'publico'"
    return render_template("ci.html", archivo=archivo, cmd=cmd, output=output)
