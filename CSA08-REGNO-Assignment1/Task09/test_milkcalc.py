"""Tests for milkcalc.py - run with:  python test_milkcalc.py"""
from decimal import Decimal as D
import milkcalc as mc

# (label, litres, fat, snf, expected rate, expected amount)  - all worked out by hand
RATE_CASES = [
    ("standard milk",               "10",    "3.5", "8.5",  "30.00", "300.00"),
    ("fat above, snf above",        "8.5",   "4.2", "8.7",  "33.40", "283.90"),
    ("fat below, snf below",        "12",    "3.1", "8.3",  "27.80", "333.60"),
    ("fat above, snf below",        "10",    "4.0", "8.0",  "30.50", "305.00"),
    ("fat below, snf above",        "10",    "3.0", "9.0",  "29.50", "295.00"),
    ("lowest fat & snf (boundary)", "20",    "2.0", "7.0",  "19.50", "390.00"),
    ("highest fat & snf (boundary)","15.5",  "7.0", "10.0", "48.50", "751.75"),
    ("standard fat, high snf",      "10",    "3.5", "9.1",  "31.80", "318.00"),
    ("two-decimal litres",          "12.25", "3.5", "8.5",  "30.00", "367.50"),
    ("half-paisa tie rounds up",    "0.25",  "3.5", "8.4",  "29.70", "7.43"),
]
# (label, farmer, shift, litres, fat, snf)
INVALID_CASES = [
    ("text as litres",        "K001", "M", "eight", "3.5", "8.5"),
    ("comma decimal",         "K001", "M", "10",    "3,5", "8.5"),
    ("negative quantity",     "K001", "M", "-5",    "3.5", "8.5"),
    ("zero quantity",         "K001", "M", "0",     "3.5", "8.5"),
    ("fat below 2.0",         "K001", "M", "10",    "1.9", "8.5"),
    ("fat above 7.0",         "K001", "M", "10",    "7.1", "8.5"),
    ("snf out of range",      "K001", "M", "10",    "3.5", "10.1"),
    ("blank litres",          "K001", "M", "  ",    "3.5", "8.5"),
    ("'nan' sneaks past float","K001", "M", "nan",  "3.5", "8.5"),
    ("bad shift",             "K001", "N", "10",    "3.5", "8.5"),
    ("litres over limit",     "K001", "M", "250",   "3.5", "8.5"),
]
FIVE = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3"),
        ("20", "2.0", "7.0"), ("15.5", "7.0", "10.0")]
FIVE_HAND_TOTAL = D("2059.25")      # 300.00+283.90+333.60+390.00+751.75


def run_tests():
    rows = []
    for label, l, f, s, exp_rate, exp_pay in RATE_CASES:
        e = mc.parse_entry("K001", "M", l, f, s)
        rate, pay = mc.rate_per_litre(e.fat, e.snf), mc.payout(e.litres, e.fat, e.snf)
        assert rate == D(exp_rate), (label, rate)
        assert pay == D(exp_pay), (label, pay)
        rows.append((label, f"{l} L {f}/{s}", f"{exp_rate} / {exp_pay}",
                     f"{rate} / {pay}", "PASS"))
    for label, *raw in INVALID_CASES:
        try:
            mc.parse_entry(*raw)
        except ValueError as err:
            rows.append((label, "/".join(raw[2:]), "ValueError", str(err)[:34], "PASS"))
        else:
            raise AssertionError(f"'{label}' should have been rejected")
    entries = [mc.parse_entry("K001", "M", *t) for t in FIVE]
    total = mc.ten_day_total(entries)
    assert total == FIVE_HAND_TOTAL, total
    rows.append(("5-entry hand total", "5 entries", str(FIVE_HAND_TOTAL), str(total), "PASS"))
    return rows


if __name__ == "__main__":
    rows = run_tests()
    print(f"{'Test case':<31}{'Input':<20}{'Expected':<18}{'Actual':<36}Result")
    for r in rows:
        print(f"{r[0]:<31}{r[1]:<20}{r[2]:<18}{r[3]:<36}{r[4]}")
    print(f"\nAll {len(rows)} tests passed.")
