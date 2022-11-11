import datetime
from typing import Any
from typing import Dict
from typing import List

import pytest
from pydantic import BaseModel

import toml_config


class FirstStep(BaseModel):
    a: int
    b: int


class MiscTypes(BaseModel):
    test_list: List[int]
    test_dict: Dict
    test_date: datetime.date


class Config(BaseModel):
    first_step: FirstStep
    second_step: Any
    misc_types: MiscTypes


@pytest.fixture
def conf():
    return toml_config.load("tests/test_conf.toml")


def test_no_file_case():
    with pytest.raises(FileNotFoundError):
        toml_config.load("does_not_exists.toml")


def test_file_exists(conf):
    assert conf


def test_empty_config():
    with pytest.raises(ValueError):
        toml_config.load("tests/empty.toml")


def test_attributes(conf):
    assert conf.first_step.a == 1
    assert conf.second_step.d == 4
    assert isinstance(conf.misc_types.test_list, list)
    assert isinstance(conf.misc_types.test_date, datetime.date)
    assert conf.misc_types.test_dict.key == "value"


def test_validation():
    assert toml_config.load("tests/test_conf.toml", model=Config)
