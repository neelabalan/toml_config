from __future__ import annotations
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Any

import toml

M = TypeVar("M")


class config:
    def __init__(self, toml_config: Dict[str, Any]):
        self.toml_config = toml_config

    def __getattr__(self, attr: str) -> str | int | float | config:
        if attr not in self.toml_config:
            raise AttributeError(f"Attribute {attr} not found in config")
        value = self.toml_config[attr]
        if isinstance(value, dict):
            return config(value)
        return value

    def __getitem__(self, key: str) -> str | int | float | config:
        if key not in self.toml_config:
            raise KeyError(f"Key {key} not found in config")
        value = self.toml_config[key]
        if isinstance(value, dict):
            return config(self.toml_config[key])
        return value

    def __repr__(self):
        return f"config({self.toml_config})"

    def __str__(self):
        return str(self.toml_config)

    def validate(self, model: Type[M]):
        """Pydantic model to be passed for validation"""
        return model(**self.toml_config)


def load(config_file_path: str) -> config | None:
    with open(config_file_path, "r") as f:
        toml_config = toml.load(f)
    return config(toml_config)
