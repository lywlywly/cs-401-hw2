import json
import os
import infer
from flask import Flask, jsonify, request

app = Flask(__name__)
data_dir = os.environ.get("DATA_DIR", "/data")


@app.route("/api/recommend", methods=["POST"])
def hello_world():
    data = request.get_json()
    songs = data["songs"]
    recommendation = infer.run(songs)
    with open(os.path.join(data_dir, "ml/rule_info.json"), "r") as file:
        info = json.load(file)
    result = {
        "songs": list(recommendation),
        "version": "1.0",
        "model_date": info["date"],
        "dataset": info["file_name"],
    }
    return jsonify(result)
