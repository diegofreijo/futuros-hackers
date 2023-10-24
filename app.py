from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/idor", strict_slashes=False)
@app.route("/idor/<int:cat>")
def idor(cat:int = None) -> str:
    match cat:
        case 0:
            image = "/ihfoabsdibiblsdidlbqeirugrq.jpg"
        case 1 | 2 | 3:
            image = f"{cat}.jpg"
        case _:
            image = None
    return render_template("idor.html", image=image, cat=cat)


@app.route("/csv", methods=(['GET']))
def csv_get():
    return render_template("csv.html", saldo=100)

@app.route("/csv", methods=(['POST']))
def csv_post():
    importe = int(request.form['importe'])
    return render_template("csv.html", saldo=(100-importe))
