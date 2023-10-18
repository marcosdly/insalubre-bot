from os.path import join, abspath, dirname
from dataclasses import dataclass
from contextlib import contextmanager
import json
from typing import Any

@dataclass(frozen=True, init=False)
class ProjectFolders:
    root = abspath(join(dirname(__file__), "..", ".."))
    config = join(root, "config")
    templates = join(root, "templates")

@contextmanager
def access_db():
    path = join(ProjectFolders.root, "db.json")
    with open(path, "rb") as file:
        content = json.load(file)
    yield content
    with open(path, "w") as file:
        json.dump(content, file)

def raw_access_db() -> dict[str, Any]:
    with open(join(ProjectFolders.root, "db.json"), "rb") as file:
        return json.load(file)
    
def get_secrets() -> dict[str, Any]:
    with open(join(ProjectFolders.config, "secrets.json")) as file:
        return json.load(file)