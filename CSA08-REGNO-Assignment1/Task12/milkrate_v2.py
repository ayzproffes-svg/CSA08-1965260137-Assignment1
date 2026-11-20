"""milkrate_v2 - seasonal rate cards, two-decimal analyser readings, 10-day bonus.

Decision: the original design is MODIFIED, not redesigned.
  retained : Decimal types, money() rounding rule, parse_number()/validation,
             payout() = litres x rate rounded to paise
  modified : the three rate constants become one RateCard per season, the step count
             is exact (pro-rata) instead of rounded, ten_day_total() adds the bonus
  new      : rate_card_for(), bonus()
"""
import sys
from collections import namedtuple
from datetime import date          # noqa: F401  (readings carry a datetime.date)
from decimal import Decimal
from pathlib import Path

# milkcalc.py lives in the Task09 folder of this repository
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Task09"))
from milkcalc import (money, parse_number, STD_FAT, STD_SNF, STEP,       # noqa: E402
                      FAT_MIN, FAT_MAX, SNF_MIN, SNF_MAX)

RateCard = namedtuple("RateCard", "name base fat_step snf_step")

# ---- Seasonal rate cards: the ONLY place rates are written ---------------------------
STANDARD_CARD = RateCard("standard", Decimal("30.00"), Decimal("0.40"), Decimal("0.30"))
SUMMER_CARD = RateCard("Apr-Jun", Decimal("32.00"), Decimal("0.45"), Decimal("0.30"))
SUMMER_MONTHS = (4, 5, 6)

# ---- Bonus rule ------------------------------------------------------------------
BONUS_THRESHOLD_LITRES = Decimal("500")   # strictly MORE than this earns the bonus
BONUS_PER_LITRE = Decimal("0.50")         # paid on ALL litres of the ten-day period

Reading = namedtuple("Reading", "day litres fat snf")          # one shift's entry
Summary = namedtuple("Summary", "litres milk_amount bonus total")


def rate_card_for(month):
    """Return the rate card in force for a calendar month (1-12)."""
    return SUMMER_CARD if month in SUMMER_MONTHS else STANDARD_CARD


def steps(value, standard):
    """Exact number of 0.1 % steps from the standard (not rounded: 4.25 -> 7.5)."""
    return (Decimal(value) - standard) / STEP


def rate_per_litre(fat, snf, card=STANDARD_CARD):
    """Price per litre for the given card, rounded to paise (same rule as before)."""
    return money(card.base + steps(fat, STD_FAT) * card.fat_step
                 + steps(snf, STD_SNF) * card.snf_step)


def payout(litres, fat, snf, card=STANDARD_CARD):
    """Amount payable for one entry, rounded to paise."""
    return money(Decimal(litres) * rate_per_litre(fat, snf, card))


def bonus(total_litres):
    """Bonus for a ten-day period: 0.50/litre on all litres if litres > 500."""
    if Decimal(total_litres) > BONUS_THRESHOLD_LITRES:
        return money(Decimal(total_litres) * BONUS_PER_LITRE)
    return Decimal("0.00")


def check_reading(fat, snf):
    """Raise ValueError if an analyser reading is outside the allowed range."""
    if not FAT_MIN <= fat <= FAT_MAX:
        raise ValueError(f"fat % {fat} outside {FAT_MIN}-{FAT_MAX}")
    if not SNF_MIN <= snf <= SNF_MAX:
        raise ValueError(f"SNF % {snf} outside {SNF_MIN}-{SNF_MAX}")


def ten_day_total(readings):
    """Summarise one farmer's ten-day period.

    Each reading is paid with the rate card of ITS OWN date, so a period that
    crosses 31 March / 1 April or 30 June / 1 July is handled correctly; the bonus
    depends on the litres of the whole period.
    """
    litres = Decimal("0")
    milk = Decimal("0.00")
    for r in readings:
        check_reading(Decimal(r.fat), Decimal(r.snf))
        milk += payout(r.litres, r.fat, r.snf, rate_card_for(r.day.month))
        litres += Decimal(r.litres)
    extra = bonus(litres)
    return Summary(litres, milk, extra, milk + extra)


def read_analyser(text_fat, text_snf):
    """Parse the analyser's two-decimal text (e.g. '4.25', '8.63') into Decimals."""
    fat, snf = parse_number(text_fat, "fat %"), parse_number(text_snf, "SNF %")
    check_reading(fat, snf)
    return fat, snf


if __name__ == "__main__":
    fat, snf = read_analyser("4.25", "8.63")
    for month in (3, 4):
        card = rate_card_for(month)
        print(f"month {month}: card {card.name:<8} rate {rate_per_litre(fat, snf, card)}"
              f"  pay for 10 L {payout('10', fat, snf, card)}")
