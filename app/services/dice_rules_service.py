import json
from pathlib import Path

from app.models.dice_rule import DiceRule, UsdtRange

_PATH = Path("dice_rules.json")

# ── default rules (written to disk on first run) ──────────────────────────────

DEFAULT_RULES: list[DiceRule] = [
    DiceRule(
        id="estandar",
        name="Estándar",
        symbol="C",
        unit_size=1.0,
        min_credits=5.0,
        usdt_min=1.0,
        usdt_table=[
            UsdtRange(from_=1.0,  to=10.0, tip=0.5),
            UsdtRange(from_=10.0, to=None, formula="floor10"),
        ],
    ),
    DiceRule(
        id="cafe",
        name="Café",
        symbol="C",
        unit_size=1.0,
        min_credits=20.0,
        usdt_min=1.0,
        usdt_table=[
            UsdtRange(from_=1.0,  to=6.0,  tip=0.5),
            UsdtRange(from_=6.0,  to=20.0, tip=1.0),
            UsdtRange(from_=20.0, to=None, formula="floor10"),
        ],
    ),
    DiceRule(
        id="legion",
        name="Legión",
        symbol="L",
        unit_size=50.0,
        min_credits=50.0,
        usdt_min=2.0,
        usdt_table=[
            UsdtRange(from_=2.0,  to=10.0, tip=0.5),
            UsdtRange(from_=10.0, to=None, formula="floor10"),
        ],
    ),
]


def load() -> list[DiceRule]:
    if not _PATH.exists():
        save(DEFAULT_RULES)
        return list(DEFAULT_RULES)
    try:
        with open(_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        rules = [DiceRule.from_dict(d) for d in data]
        return rules if rules else list(DEFAULT_RULES)
    except Exception:
        return list(DEFAULT_RULES)


def save(rules: list[DiceRule]) -> None:
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in rules], f, indent=2, ensure_ascii=False)


def find_by_id(rules: list[DiceRule], rule_id: str) -> DiceRule:
    for r in rules:
        if r.id == rule_id:
            return r
    return rules[0]
