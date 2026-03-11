from dataclasses import dataclass, field


@dataclass
class GameState:
    balance_z0: float = 0.0
    balance_z1: float = 0.0
    balance_z2: float = 0.0
    name_z0: str = "Inter"
    name_z1: str = "Jugador 1"
    name_z2: str = "Jugador 2"
    currency: str = "COP"
    history: list[str] = field(default_factory=list)
