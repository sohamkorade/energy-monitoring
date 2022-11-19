from flask import Flask, request, render_template, send_file
import backend
from random import choice, randint

app = Flask(__name__)

saved = False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
    return send_file("index.html")


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


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    app.run(host="0.0.0.0")
