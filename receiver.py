from flask import Flask, render_template, request,jsonify
from flask_cors import CORS, cross_origin
from uuid import uuid4
from numpy import random

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.secret_key = str(uuid4())

class Connection:
    def __init__(self,color,name) -> None:
        self.name=name
        self.color=color
        self.id = str(uuid4())
        
    def __repr__(self):
        return f"<Connection {self.name=} {self.color=} {self.id=}>"

connected = []
logs = []

@app.route("/")
@cross_origin()
def index():
    
    return render_template('index.html')

@app.route("/start")
@cross_origin()
def start():
    name = request.args.get('name')
    conn = Connection(list(random.choice(range(256), size=3)),name=name)
    connected.append(conn)
    return render_template('btn.html',connid=conn.id,name=conn.name,r=conn.color[0],g=conn.color[1],b=conn.color[2])

@app.route("/vote")
@cross_origin()
def vote():
    connid = request.args.get('connid')
    for i in connected:
        if i.id == connid:
            print(i.name)
            logs.append(i.name)
            break
    return jsonify(success=True)

@app.route('/get_logs')
@cross_origin()
def get_log():
    return jsonify(logs[::-1][:25])

@app.route('/clear')
@cross_origin()
def clear():
    global logs
    logs=[]
    return jsonify(success=True)


@app.route('/clearconn')
@cross_origin()
def clearconn():
    global connected
    connected=[]
    return jsonify(success=True)

@app.route("/logs")
@cross_origin()
def log():
    return render_template('logs.html') 


if __name__ == "__main__":
    app.run(debug=True)