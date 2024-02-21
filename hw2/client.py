import argparse
import json

import requests


def run(tracks):
    payload = {"songs": tracks}
    json_payload = json.dumps(payload)

    url = "http://127.0.0.1:52002/api/recommend"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json_payload, headers=headers)

    response_json = json.loads(response.text)
    print(f"Code version: {response_json['version']}")
    print(f"Model time: {response_json['model_date']}")
    print(f"Recommended songs: {response_json['songs']}")

def main():
    parser = argparse.ArgumentParser(description="Playlist recommendation.")
    parser.add_argument("-i", "--input", required=True, nargs="+", help="Input tracks.")
    args = parser.parse_args()
    tracks = args.input
    run(tracks)


main() if __name__ == "__main__" else None
