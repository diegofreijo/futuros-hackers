import base64
from flask import Flask, make_response, request
from flask import render_template

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
