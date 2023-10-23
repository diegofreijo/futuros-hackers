from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/idor")
@app.route("/idor/<int:id>")
def idor(id:int = None):
    match id:
        case 0:
            image = "/ihfoabsdibiblsdidlbqeirugrq.jpg"
        case 1 | 2 | 3:
            image = f"{id}.jpg"
        case _:
            image = None
            
    return render_template("idor.html", image=image)
