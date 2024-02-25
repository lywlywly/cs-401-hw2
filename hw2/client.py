import argparse
import json

import requests
import logging
import time
import os

log_filename = 'log.log'
if os.path.exists(log_filename):
    os.remove(log_filename)

logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def run(tracks, ip, port, continuous):
    if continuous:
        while True:
            _run(tracks, ip, port)
            time.sleep(0.1)
    else:
        _run(tracks, ip, port)

def _run(tracks, ip, port):
    payload = {"songs": tracks}
    json_payload = json.dumps(payload)

    url = f"http://{ip}:{port}/api/recommend"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json_payload, headers=headers)
    logging.info(f"Response: {response}")
    try:
        response_json = json.loads(response.text)
        print(f"Code version: {response_json['version']}")
        logging.info(f"Code version: {response_json['version']}")
        print(f"Model time: {response_json['model_date']}")
        logging.info(f"Model time: {response_json['model_date']}")
        print(f"Dataset: {response_json['dataset']}")
        logging.info(f"Dataset: {response_json['dataset']}")
        print(f"Recommended songs: {response_json['songs']}")
        logging.info(f"Recommended songs: {response_json['songs']}")
    except:
        logging.info(f"Failed to parse response json")

def main():
    parser = argparse.ArgumentParser(description="Playlist recommendation.")
    parser.add_argument("-H", "--host", required=True, help="Host IP address.")
    parser.add_argument("-p", "--port", required=True, help="Port number.")
    parser.add_argument("-i", "--input", required=True, nargs="+", help="Input tracks.")
    parser.add_argument("-c", "--continuous", action='store_true', default=False, help="Continuous send requests, save result in `log.log`.")
    args = parser.parse_args()
    tracks = args.input
    ip = args.host
    port = args.port
    continuous = args.continuous
    run(tracks, ip, port, continuous)


main() if __name__ == "__main__" else None
