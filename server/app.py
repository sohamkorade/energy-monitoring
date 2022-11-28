from flask import Flask, request, render_template, send_file, make_response
import backend
from random import choice, randint
import json

app = Flask(__name__)

saved = False
queue = []

try:
    with open("queue.json", "r") as f:
        queue = json.load(f)
except:
    pass


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
    token = request.cookies.get("token")
    resp = make_response(send_file("index.html"))
    if token is not None:
        resp.delete_cookie("token")
    return resp


@app.route("/data", methods=["GET"])
def data():
    data, chart = backend.get_sensor_data(saved)
    # chart = {"Humidity": [[randint(70, 80) for i in range(5)],
    #                       ["21:01", "21:01", "21:01", "21:01", "21:02"]],
    #          "Rain": [[randint(0, 4095) for i in range(5)], [
    #              "21:01", "21:01", "21:01", "21:01", "21:02"]],
    #          "Temperature": [[randint(28, 29) for i in range(5)],
    #                          ["21:01", "21:01", "21:01", "21:01", "21:02"]]}
    clean_data(data, chart)
    return {"data": data, "chart": chart}


def clean_data(data, chart):
    pass


@app.route("/joinqueue", methods=["GET"])
def joinqueue():
    token = request.cookies.get("token")
    if token is None:
        token = "T" + str(len(queue) + 1 if queue else 1)
        queue.append({"token": token, "time": 0})
        with open("queue.json", "w") as f:
            json.dump(queue, f)
        resp = make_response({"status": "added to queue"})
        resp.set_cookie("token", token)
        return resp
    else:
        for i in queue:
            if i["token"] == token:
                return {"status": "already in queue"}
    return {"status": "error"}


@app.route("/leavequeue", methods=["GET"])
def leavequeue():
    token = request.cookies.get("token")
    resp = make_response({})
    for i in queue:
        if i["token"] == token:
            queue.remove(i)
            resp = make_response({"status": "removed from queue"})
    with open("queue.json", "w") as f:
        json.dump(queue, f)
    resp.delete_cookie("token")
    return resp


@app.route("/queue", methods=["GET"])
def getqueue():
    return {"token": request.cookies.get("token"), "queue": queue}


@app.route("/old", methods=["GET"])
def oldpage():
    return send_file("old.html")


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    # app.run(host="0.0.0.0")
    from waitress import serve
    serve(app)
