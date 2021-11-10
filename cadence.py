#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
import requests
import sys
import time
from timeseries import TimeSeries


class MetricsClient(object):
    def __init__(self, host, max_size=10_000):
        self.host = host
        self.max_size = max_size
        self.backlog = []

    def get_all(self):
        url = os.path.join(self.host, f"metrics")
        response = requests.get(url)
        return (response.json)

    def get(self, name: str):
        url = os.path.join(self.host, f"metric/{name}")
        response = requests.get(url)
        return (response.json)

    def post(self, name: str, data: dict):
        data.setdefault('time', time.time())
        self.backlog.append((name, data))

        error = False
        for _ in range(len(self.backlog)):
            (_name, _data) = self.backlog.pop(0)

            try:
                self._post(_name, _data)
            except e:
                error = True
                self.backlog.append((_name, _data))

        if error:
            print(f"Failed to post (backlog={len(self.backlog)})")

    def _post(self, name, data):
        url = os.path.join(self.host, f"metric/{name}")
        response = requests.post(url, json=data)
        response.raise_for_status()


class MetricsServer(object):
    def __init__(self):
        pass


def main():
    app = Flask(__name__)
    metrics = {}

    @app.route("/status")
    def status():
        return ("OK", 200)

    @app.route("/metrics")
    def get_metrics():
        return (jsonify(list(metrics.keys())), 200)

    @app.route("/metric/<name>", methods=["GET"])
    def get_metric(name: str):
        if name in metrics:
            start = request.args.get('start', default=None, type=float)
            end = request.args.get('end', default=None, type=float)
            return jsonify(metrics[name].select(start, end))
        else:
            return ("Metric not found", 404)

    @app.route("/metric/<name>", methods=["POST"])
    def post_metric(name: str):
        if name not in metrics:
            metrics[name] = TimeSeries()
        metrics[name].add(request.get_json(force=True))
        return ("OK", 201)

    app.run(host="0.0.0.0")


if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
