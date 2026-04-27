from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class UsdtRange:
    from_: float
    to: float | None        # exclusive upper bound; None = open-ended
    tip: float | None = None
    formula: str | None = None  # "floor10" → floor(amount / 10)


@dataclass
class DiceRule:
    id: str
    name: str
    symbol: str             # currency label for history ("C", "L", …)
    unit_size: float        # credits per 1 unit  (50.0 for Legión, 1.0 otherwise)
    min_credits: float      # minimum game amount in credits
    usdt_min: float         # minimum game amount in USDT
    usdt_table: list[UsdtRange] = field(default_factory=list)

    # ── tip helpers ───────────────────────────────────────────────────────────

    def tip_usdt(self, amount: float) -> float:
        for r in self.usdt_table:
            if r.from_ <= amount and (r.to is None or amount < r.to):
                if r.tip is not None:
                    return r.tip
                if r.formula == "floor10":
                    return float(int(amount // 10))
        return round(amount // 10.0, 2)

    def min_hint(self) -> str:
        if self.unit_size > 1.0:
            units = self.min_credits / self.unit_size
            return f"Mín: {self.min_credits:.0f}C  ({units:.0f}{self.symbol})  |  Mín USDT: {self.usdt_min}"
        return f"Mín: {self.min_credits:.0f}{self.symbol}  |  Mín USDT: {self.usdt_min}"

    def amount_label(self, amount: float) -> str:
        """Human-readable amount label for history entries."""
        if self.unit_size > 1.0:
            units = amount / self.unit_size
            return f"{amount:.0f}C ({units:.1f}{self.symbol})"
        return f"{amount} {self.symbol}"

    # ── serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "unit_size": self.unit_size,
            "min_credits": self.min_credits,
            "usdt_min": self.usdt_min,
            "usdt_table": [
                {
                    "from": r.from_,
                    "to": r.to,
                    "tip": r.tip,
                    "formula": r.formula,
                }
                for r in self.usdt_table
            ],
        }

    @classmethod
    def from_dict(cls, d: dict) -> DiceRule:
        return cls(
            id=d["id"],
            name=d["name"],
            symbol=d["symbol"],
            unit_size=float(d.get("unit_size", 1.0)),
            min_credits=float(d["min_credits"]),
            usdt_min=float(d["usdt_min"]),
            usdt_table=[
                UsdtRange(
                    from_=float(r["from"]),
                    to=float(r["to"]) if r.get("to") is not None else None,
                    tip=float(r["tip"]) if r.get("tip") is not None else None,
                    formula=r.get("formula"),
                )
                for r in d.get("usdt_table", [])
            ],
        )
