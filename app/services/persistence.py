import json
import os

from app.constants import AUTOSAVE_FILE
from app.models.game_state import GameState


class PersistenceService:
    def __init__(self, filepath: str = AUTOSAVE_FILE) -> None:
        self._filepath = filepath

    def load(self) -> GameState:
        if not os.path.exists(self._filepath):
            return GameState()
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return GameState(
                balance_z0=data.get("z0", 0.0),
                balance_z1=data.get("z1", 0.0),
                balance_z2=data.get("z2", 0.0),
                name_z0=data.get("name_z0", "Inter"),
                name_z1=data.get("name_z1", "Jugador 1"),
                name_z2=data.get("name_z2", "Jugador 2"),
                currency=data.get("currency", "COP"),
                history=data.get("history", []),
            )
        except (json.JSONDecodeError, KeyError, OSError):
            return GameState()

    def save(self, state: GameState) -> None:
        try:
            data = {
                "z0": state.balance_z0,
                "z1": state.balance_z1,
                "z2": state.balance_z2,
                "name_z0": state.name_z0,
                "name_z1": state.name_z1,
                "name_z2": state.name_z2,
                "currency": state.currency,
                "history": state.history,
            }
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass
