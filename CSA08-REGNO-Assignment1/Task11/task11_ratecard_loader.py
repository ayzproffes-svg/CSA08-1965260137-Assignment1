"""Task 11 alternative: read the rate card from ratecard.json when the program starts."""
import json
import sys
import time
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "Task09"))
import milkcalc as mc


def load_rate_card(path):
    """Read the JSON rate card; values are strings so they become exact Decimals."""
    with open(path, encoding="utf-8") as handle:
        raw = json.load(handle)
    card = {key: Decimal(value) for key, value in raw.items()}
    for key in ("base_rate", "fat_step_value", "snf_step_value"):
        if card[key] <= 0:
            raise ValueError(f"rate card: {key} must be positive, got {card[key]}")
    return card


def rate_per_litre(fat, snf, card):
    fat_steps = mc.whole_steps(fat, card["std_fat"])
    snf_steps = mc.whole_steps(snf, card["std_snf"])
    return mc.money(card["base_rate"] + fat_steps * card["fat_step_value"]
                    + snf_steps * card["snf_step_value"])


if __name__ == "__main__":
    runs = 2000
    t0 = time.perf_counter()
    for _ in range(runs):
        card = load_rate_card(HERE / "ratecard.json")
    per_load = (time.perf_counter() - t0) / runs
    print("card loaded:", {k: str(v) for k, v in card.items()})
    print(f"start-up cost to read the file: {per_load * 1e6:.1f} microseconds (mean of {runs})")
    print("file size on disk:", (HERE / "ratecard.json").stat().st_size, "bytes;",
          "size in memory (dict + 5 Decimals):",
          sys.getsizeof(card) + sum(sys.getsizeof(v) for v in card.values()), "bytes")
    f, s = Decimal("4.2"), Decimal("8.7")
    print("rate from file :", rate_per_litre(f, s, card))
    print("rate from module:", mc.rate_per_litre(f, s))
    assert rate_per_litre(f, s, card) == mc.rate_per_litre(f, s)
    # a revision = edit ONE line of the text file, no code change, no redistribution of .py files
    revised = dict(card, fat_step_value=Decimal("0.45"))
    print("after editing fat_step_value to 0.45 in the file: rate(4.2, 8.7) =",
          rate_per_litre(f, s, revised))
    try:
        load_rate_card(HERE / "missing.json")
    except FileNotFoundError as err:
        print("missing file ->", type(err).__name__, "(program must stop with a clear message)")
