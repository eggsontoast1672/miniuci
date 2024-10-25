import dataclasses
import json
from typing import Any

from chess.engine import Limit

JSONValue = Any


@dataclasses.dataclass
class Config:
    engine: str
    limit: Limit


def parse_config_json(json: JSONValue) -> Config:
    match json["limit"]["kind"]:
        case "depth":
            limit = Limit(depth=json["limit"]["value"])
        case "time":
            limit = Limit(time=json["limit"]["value"])
        case _:
            assert False
    return Config(json["engine"], limit)


def get_config() -> Config:
    with open("settings.json", "r") as settings:
        config = json.load(settings)
        return parse_config_json(config)
