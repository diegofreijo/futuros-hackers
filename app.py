import base64
import sqlite3
from flask import Flask, make_response, redirect, request, url_for
from flask import render_template
from flask import g

app = Flask(__name__)


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
        nombre = "pepe"
        resp = make_response(render_template('cf.html', nombre=nombre, logueado=True))

        nombre64 = base64.b64encode(nombre.encode())
        resp.set_cookie('nombre', nombre64.decode())

        return resp
    else:
        if 'nombre' in request.cookies:
            nombre64 = request.cookies.get('nombre')
            print(nombre64)
            nombre = base64.b64decode(nombre64).decode()
        else:
            nombre = None
        logueado = nombre is not None
        return render_template("cf.html", nombre=nombre, logueado=logueado)

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
        print(dbname)
        if dbname and dbname[0] and dbname[0][0] == nombre:
            print(dbname[0][0])
            message = f"Bienvenido {dbname[0][0]}"
        else:
            message = "Usuario o contraseña incorrecta"
        return render_template("sqli.html", message=message)
    else:
        return render_template("sqli.html", )

###################################################

@app.route("/rxss")
def rxss():
    archivo = request.args.get('archivo')
    if not archivo:
        return redirect(url_for('rxss', archivo='password.txt'))
    return render_template("rxss.html", archivo=archivo)
