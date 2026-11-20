"""Tests for milkrate_v2.py - run with:  python test_milkrate_v2.py"""
from datetime import date
from decimal import Decimal as D
import milkrate_v2 as v2

# (label, month, litres, fat, snf, expected rate, expected amount) - worked by hand
RATE_CASES = [
    ("standard, 1-dec readings",     11, "10",  "3.5",  "8.5",  "30.00", "300.00"),
    ("summer, standard milk",         5, "10",  "3.5",  "8.5",  "32.00", "320.00"),
    ("summer, 1-dec, above",          4, "8.5", "4.2",  "8.7",  "35.75", "303.88"),
    ("standard, 1-dec, above",       12, "8.5", "4.2",  "8.7",  "33.40", "283.90"),
    ("standard, 2-dec (4.25/8.63)",   3, "10",  "4.25", "8.63", "33.39", "333.90"),
    ("summer, 2-dec (4.25/8.63)",     4, "10",  "4.25", "8.63", "35.77", "357.70"),
    ("standard, 2-dec, below",        7, "10",  "3.14", "8.37", "28.17", "281.70"),
    ("summer, 2-dec, below",          6, "10",  "3.14", "8.37", "29.99", "299.90"),
    ("summer lowest boundary",        4, "20",  "2.00", "7.00", "20.75", "415.00"),
    ("standard highest boundary",     1, "15.5","7.00", "10.00","48.50", "751.75"),
]
# boundary of the season: (date, expected card name)
SEASON_CASES = [(date(2026, 3, 31), "standard"), (date(2026, 4, 1), "Apr-Jun"),
                (date(2026, 6, 30), "Apr-Jun"), (date(2026, 7, 1), "standard")]


def twenty(day, last_litres, fat="3.5", snf="8.5"):
    """19 shifts of 25 L plus one shift of last_litres (so period litres vary)."""
    return ([v2.Reading(day, D("25"), D(fat), D(snf))] * 19
            + [v2.Reading(day, D(last_litres), D(fat), D(snf))])


# (label, readings, litres, milk amount, bonus, total) - worked by hand
PERIOD_CASES = [
    ("summer, exactly 500 L",   twenty(date(2026, 6, 5), "25"),
     "500", "16000.00", "0.00", "16000.00"),
    ("summer, 499.9 L",         twenty(date(2026, 6, 5), "24.9"),
     "499.9", "15996.80", "0.00", "15996.80"),
    ("summer, 500.1 L",         twenty(date(2026, 6, 5), "25.1"),
     "500.1", "16003.20", "250.05", "16253.25"),
    ("standard, 500.1 L",       twenty(date(2026, 11, 5), "25.1"),
     "500.1", "15003.00", "250.05", "15253.05"),
    ("standard, exactly 500 L", twenty(date(2026, 11, 5), "25"),
     "500", "15000.00", "0.00", "15000.00"),
    ("period crossing 31 Mar/1 Apr",
     [v2.Reading(date(2026, 3, 31), D("300"), D("3.5"), D("8.5")),
      v2.Reading(date(2026, 4, 1), D("300"), D("3.5"), D("8.5"))],
     "600", "18600.00", "300.00", "18900.00"),
]


def run_tests():
    rows = []
    for label, month, l, f, s, exp_rate, exp_pay in RATE_CASES:
        card = v2.rate_card_for(month)
        fat, snf = v2.read_analyser(f, s)
        rate, pay = v2.rate_per_litre(fat, snf, card), v2.payout(l, fat, snf, card)
        assert (rate, pay) == (D(exp_rate), D(exp_pay)), (label, rate, pay)
        rows.append((label, f"m{month} {l}L {f}/{s}", f"{exp_rate}/{exp_pay}",
                     f"{rate}/{pay}", "PASS"))
    for d, name in SEASON_CASES:
        got = v2.rate_card_for(d.month).name
        assert got == name, (d, got)
        rows.append((f"season of {d}", str(d), name, got, "PASS"))
    for label, readings, litres, milk, bonus, total in PERIOD_CASES:
        r = v2.ten_day_total(readings)
        assert (r.litres, r.milk_amount, r.bonus, r.total) == (
            D(litres), D(milk), D(bonus), D(total)), (label, r)
        rows.append((label, f"{r.litres} L", f"{bonus}/{total}",
                     f"{r.bonus}/{r.total}", "PASS"))
    for fat, snf in (("1.99", "8.5"), ("7.01", "8.5"), ("3.5", "6.99"), ("3.5", "10.01")):
        try:
            v2.read_analyser(fat, snf)
        except ValueError as err:
            rows.append(("invalid reading", f"{fat}/{snf}", "ValueError", str(err)[:30], "PASS"))
        else:
            raise AssertionError((fat, snf))
    return rows


if __name__ == "__main__":
    rows = run_tests()
    print(f"{'Test case':<31}{'Input':<20}{'Expected':<21}{'Actual':<31}Result")
    for r in rows:
        print(f"{r[0]:<31}{r[1]:<20}{r[2]:<21}{r[3]:<31}{r[4]}")
    print(f"\nAll {len(rows)} tests passed.")
