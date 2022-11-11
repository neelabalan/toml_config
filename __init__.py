from pathlib import Path
from typing import Dict
from typing import Union

import toml
from pydantic import BaseModel


class _config:
    def __init__(self, obj: Dict):
        self.__dict = obj
        for key, value in obj.items():
            if isinstance(key, (list, tuple)):
                setattr(
                    self,
                    key,
                    [_config(x) if isinstance(x, dict) else x for x in value],
                )
            else:
                setattr(
                    self,
                    key,
                    _config(value) if isinstance(value, dict) else value,
                )

    def __dict__(self):
        return self.__dict


def __file_exists(path: Union[str, Path]):
    return (
        isinstance(path, str)
        and not Path(path).exists()
        or (isinstance(path, Path) and not path.exists())
    )


def load(path: Union[str, Path], model: BaseModel = None):
    obj = None
    if __file_exists(path):
        raise FileNotFoundError(f"Config file not found at {path}")
    with open(path, "r") as file:
        # Should raise toml.TomlDecodeError
        obj = toml.load(file)
    if not obj:
        raise ValueError("Config file is empty")
    if model and isinstance(model, BaseModel):
        # validate here
        model(**obj)
    return _config(obj)
