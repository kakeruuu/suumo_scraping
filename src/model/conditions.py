from dataclasses import dataclass, field


@dataclass
class Conditions:
    region: str = ""
    real_estate: str = "賃貸物件"
    prefecture: str = ""
    way: str = "エリア"
    main_conditions: list[int] = field(default_factory=list)
    other_conditions: dict[str | list[str | int]] = field(default_factory=dict)
