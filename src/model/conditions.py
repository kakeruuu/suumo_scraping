from dataclasses import dataclass


@dataclass
class Conditions:
    region: str
    real_estate: str
    map: str
    way: str
    city_codes: list[int]
    other_condtions: list[dict[str | int]]
