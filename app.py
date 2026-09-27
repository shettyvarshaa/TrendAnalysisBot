from flask import Flask, jsonify, render_template, request

from parser import parse_multi
from storage import load_data, save_data


app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api")
def get_data():
    return jsonify(load_data())


@app.post("/api")
def add_data():
    try:
        payload = request.get_json(silent=True) or {}
        new_items = parse_multi(payload.get("text", ""))
        data = load_data()

        for item in new_items:
            data = [record for record in data if record["date"] != item["date"]]
            data.append(item)

        save_data(data)
        return jsonify(data)
    except (TypeError, ValueError, KeyError) as error:
        return jsonify(error=str(error)), 400


@app.delete("/api")
def clear_data():
    save_data([])
    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
