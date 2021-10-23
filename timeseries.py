#!/usr/bin/env python3

from datetime import timedelta
import gzip
import msgpack
from sortedcontainers import SortedList
import time


class TimePoint(object):
    def __init__(self, time: float):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"({self.time})"


class DataPoint(TimePoint):
    def __init__(self, data: dict):
        data.setdefault('time', time.time())
        super().__init__(data.get('time'))
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"({self.time} => {self.data})"


class TimeSeries(object):
    def __init__(self, max_size=10_000):
        self.max_size = max_size
        self.series = SortedList()

    def add(self, data={}):
        if len(self.series) >= self.max_size:
            self.series.pop(0)
        self.series.add(DataPoint(data))

    def select(self, start: TimePoint=None, end: TimePoint=None):
        start = TimePoint(start) if start else None
        end = TimePoint(end) if end else None
        return [x.data for x in self.series.irange(start, end)]

    def expire(self, max_age: timedelta):
        epoch_age = time.time() - max_age.total_seconds()
        while self.series and self.series[0].time < epoch_age:
            self.series.pop(0)

    def __repr__(self):
        return repr(self.series)

    def __len__(self):
        return len(self.series)

    def load(self, filename: str):
        with gzip.open(filename, 'rb') as f:
            msg = msgpack.Unpacker(f)
            self.max_size = msg.unpack()
            self._unpack_series(msg)

    def _unpack_series(self, msg: msgpack.Unpacker):
        self.series = SortedList()
        for _ in range(msg.read_array_header()):
            self.series.add(DataPoint(self._unpack_datapoint(msg)))

    def _unpack_datapoint(self, msg: msgpack.Unpacker):
        return {msg.unpack(): msg.unpack() for _ in range(msg.read_map_header())}

    def save(self, filename: str):
        with gzip.open(filename, 'wb') as f:
            f.write(msgpack.packb(self.max_size))
            f.write(msgpack.packb([p.data for p in self.series]))
