from flask import Flask, jsonify, render_template, request

from parser import parse_multi
from storage import load_data, save_data
from summary_service import generate_summary


app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api")
def get_data():
    return jsonify(load_data())


@app.get("/api/summary")
def get_summary():
    return jsonify(summary=generate_summary(load_data()))


@app.post("/api")
def add_data():
    try:
        payload = request.get_json(silent=True) or {}
        new_items = parse_multi(payload.get("text", ""))
        data = load_data()

        existing_dates = {record["date"] for record in data}
        incoming_dates = [item["date"] for item in new_items]
        if any(date in existing_dates for date in incoming_dates) or len(incoming_dates) != len(set(incoming_dates)):
            return jsonify(
                error="Same date entry is present, edit it or remove and add again."
            ), 409

        for item in new_items:
            data.append(item)

        save_data(data)
        return jsonify(data)
    except (TypeError, ValueError, KeyError) as error:
        return jsonify(error=str(error)), 400


@app.put("/api/record/<path:date>")
def edit_data(date):
    try:
        payload = request.get_json(silent=True) or {}
        new_items = parse_multi(payload.get("text", ""))
        if len(new_items) != 1:
            raise ValueError("Please provide exactly one sales report when editing an entry.")

        data = load_data()
        if not any(record["date"] == date for record in data):
            return jsonify(error="The selected record no longer exists."), 404

        updated_item = new_items[0]
        if updated_item["date"] != date and any(
            record["date"] == updated_item["date"] for record in data
        ):
            return jsonify(
                error="Same date entry is present, edit it or remove and add again."
            ), 409

        data = [
            updated_item if record["date"] == date else record
            for record in data
        ]
        save_data(data)
        return jsonify(data)
    except (TypeError, ValueError, KeyError) as error:
        return jsonify(error=str(error)), 400


@app.delete("/api/record/<path:date>")
def delete_data(date):
    data = load_data()
    updated_data = [record for record in data if record["date"] != date]
    if len(updated_data) == len(data):
        return jsonify(error="The selected record no longer exists."), 404

    save_data(updated_data)
    return jsonify(updated_data)


@app.delete("/api")
def clear_data():
    save_data([])
    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
