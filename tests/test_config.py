import pytest
import toml
import toml_config
from pathlib import Path
from pydantic import BaseModel


class TestConfig:
    @classmethod
    def setup_class(cls):
        cls.cfg_path = "tests/test_conf.toml"
        cls.data = {"server": {"host": "127.0.0.1", "port": 8080}}
        with open("tests/test_conf.toml", "w") as file:
            toml.dump(cls.data, file)
        cls.cfg = toml_config.load(cls.cfg_path)

    @classmethod
    def teardown_class(cls):
        Path(cls.cfg_path).unlink()

    def test_valid_attribute_access(self):
        assert self.cfg.server.host == self.data["server"]["host"]
        assert self.cfg.server.port == self.data["server"]["port"]

    def test_invalid_attribute_access(self):
        with pytest.raises(AttributeError):
            self.cfg.key3

    def test_valid_item_access(self):
        assert self.cfg.server["host"] == self.data["server"]["host"]
        assert self.cfg.server["port"] == self.data["server"]["port"]

    def test_invalid_item_access(self):
        with pytest.raises(KeyError):
            self.cfg["key3"]

    def test_repr(self):
        assert (
            repr(self.cfg) == "config({'server': {'host': '127.0.0.1', 'port': 8080}})"
        )

    def test_validate(self):
        class Server(BaseModel):
            host: str
            port: int

        class Config(BaseModel):
            server: Server

        assert self.cfg.validate(Config)
