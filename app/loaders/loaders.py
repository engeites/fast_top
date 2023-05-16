import datetime
import json
from abc import ABC

import requests

ENDPOINT = config.ENDPOINT
HEADERS: Config.HEADERS


class Loader(ABC):
    def load_data(self, day: str = None):
        pass

    def __repr__(self):
        pass


class APILoader(Loader):
    def load_data(self, day: str = None):
        response = self.make_request(day)
        return response.json()

    @staticmethod
    def make_request(day: str = None):
        if not day:
            return requests.get(ENDPOINT, headers=HEADERS)
        params = {'day': day}
        return requests.get(ENDPOINT, headers=HEADERS, params=params)


class FileLoader(Loader):
    def load_data(self, day: str = None):
        data = self.open_file(filename=day)
        if not data:
            return None
        return data

    @staticmethod
    def open_file(filename: str) -> json:
        try:
            with open(f"app/logs/{filename}", 'r', encoding='utf-8') as fout:
                data = json.load(fout)
                return data
        except FileNotFoundError:
            print(f"File {filename} not found")
            return None