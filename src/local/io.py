from os.path import join, abspath, dirname
from dataclasses import dataclass
from contextlib import contextmanager
from pathlib import PurePath
import json
from typing import Any

@dataclass(frozen=True, init=False)
class ProjectFolders:
    root = PurePath(abspath(join(dirname(__file__), "..", "..")))
    config = root.joinpath("config")
    templates = root.joinpath("templates")

@contextmanager
def access_db():
    path = ProjectFolders.root.joinpath("db.json")
    with open(path, "rb") as file:
        content = json.load(file)
    yield content
    with open(path, "w") as file:
        json.dump(content, file)

def raw_access_db() -> dict[str, Any]:
    with open(ProjectFolders.root.joinpath("db.json")) as file:
        return json.load(file)
    
def get_secrets() -> dict[str, Any]:
    with open(ProjectFolders.config.joinpath("secrets.json")) as file:
        return json.load(file)
