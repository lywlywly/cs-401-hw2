import argparse
import json

import requests


def run(tracks, ip, port):
    payload = {"songs": tracks}
    json_payload = json.dumps(payload)

    url = f"http://{ip}:{port}/api/recommend"

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
    parser.add_argument("-H", "--host", required=True, help="Host IP address.")
    parser.add_argument("-p", "--port", required=True, help="Port number.")
    parser.add_argument("-i", "--input", required=True, nargs="+", help="Input tracks.")
    args = parser.parse_args()
    tracks = args.input
    ip = args.host
    port = args.port
    run(tracks, ip, port)


main() if __name__ == "__main__" else None
