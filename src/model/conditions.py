from dataclasses import dataclass


@dataclass
class Conditions:
    region: str
    real_estate: str
    map: str
    way: str
    main_conditions: list[int]
    other_conditions: list[dict[str | int]]
