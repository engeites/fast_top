from abc import ABC
from .loaders import FileLoader, APILoader


class LoaderFactory(ABC):
    def get_loader(self):
        "returns a loader"
        pass


class FileLoaderFactory(LoaderFactory):
    def get_loader(self):
        return FileLoader()

    def __repr__(self):
        return "FileLoader"


class APILoaderFactory(LoaderFactory):
    def get_loader(self):
        return APILoader()

    def __repr__(self):
        return "APILoader"
