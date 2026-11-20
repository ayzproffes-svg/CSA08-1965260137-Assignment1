"""milkcalc - payment calculator for the Ksheera Village Milk Producers' Co-operative.

All money and all readings are kept as decimal.Decimal, so every payment is exact
to the paisa.  Every rate and limit is a named constant defined ONCE, here.
"""
from collections import namedtuple
from decimal import Decimal, ROUND_HALF_UP

# ---- Rate card (change a rate here and nowhere else) ------------------------------
BASE_RATE = Decimal("30.00")       # Rs/litre at 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE = Decimal("0.40")   # Rs/litre per 0.1 % fat above/below standard
SNF_STEP_VALUE = Decimal("0.30")   # Rs/litre per 0.1 % SNF above/below standard
STD_FAT = Decimal("3.5")
STD_SNF = Decimal("8.5")
STEP = Decimal("0.1")              # size of one step, in percentage points

# ---- Validation limits (assumptions, see report Task 1) ---------------------------
FAT_MIN, FAT_MAX = Decimal("2.0"), Decimal("7.0")
SNF_MIN, SNF_MAX = Decimal("7.0"), Decimal("10.0")
MAX_LITRES_PER_ENTRY = Decimal("200")
SHIFTS = ("M", "E")                # morning / evening
PAISA = Decimal("0.01")

Entry = namedtuple("Entry", "farmer_id shift litres fat snf")


def money(value):
    """Round a Decimal to whole paise, halves going up (the usual cash rule)."""
    return Decimal(value).quantize(PAISA, rounding=ROUND_HALF_UP)


def parse_number(text, name):
    """Convert clerk's text to Decimal, or raise ValueError with a clear message.

    The text is checked with str methods BEFORE converting, so "8,5", "eight",
    "nan", "1e3" and non-ASCII digits are all rejected.  A leading sign is allowed
    so that a negative quantity gets a precise message later (range check).
    """
    cleaned = text.strip()
    body = cleaned[1:] if cleaned and cleaned[0] in "+-" else cleaned
    if not (body.isascii() and body.replace(".", "", 1).isdigit()):
        raise ValueError(f"{name}: '{text}' is not a number (digits and one '.' only)")
    return Decimal(cleaned)


def parse_entry(farmer_id, shift, litres_text, fat_text, snf_text):
    """Validate one raw entry (all text) and return an Entry of exact values."""
    farmer_id = farmer_id.strip().upper()
    if not (farmer_id.isascii() and farmer_id.isalnum()):
        raise ValueError(f"farmer ID: '{farmer_id}' must be letters/digits only")
    shift = shift.strip().upper()
    if shift not in SHIFTS:
        raise ValueError(f"shift: '{shift}' must be one of {SHIFTS}")
    litres = parse_number(litres_text, "litres")
    fat = parse_number(fat_text, "fat %")
    snf = parse_number(snf_text, "SNF %")
    if litres <= 0:
        raise ValueError(f"litres: {litres} must be greater than 0")
    if litres > MAX_LITRES_PER_ENTRY:
        raise ValueError(f"litres: {litres} exceeds {MAX_LITRES_PER_ENTRY} per entry")
    if not FAT_MIN <= fat <= FAT_MAX:
        raise ValueError(f"fat %: {fat} outside {FAT_MIN}-{FAT_MAX}")
    if not SNF_MIN <= snf <= SNF_MAX:
        raise ValueError(f"SNF %: {snf} outside {SNF_MIN}-{SNF_MAX}")
    return Entry(farmer_id, shift, litres, fat, snf)


def whole_steps(value, standard):
    """Number of 0.1 % steps between value and standard (nearest whole step)."""
    return ((Decimal(value) - standard) / STEP).quantize(Decimal("1"),
                                                        rounding=ROUND_HALF_UP)


def rate_per_litre(fat, snf):
    """Price per litre in Rs, exact to the paisa."""
    fat_steps = whole_steps(fat, STD_FAT)
    snf_steps = whole_steps(snf, STD_SNF)
    return money(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE)


def payout(litres, fat, snf):
    """Amount payable for one entry in Rs, exact to the paisa."""
    return money(Decimal(litres) * rate_per_litre(fat, snf))


def ten_day_total(entries):
    """Sum of the (already rounded) payments of one farmer's entries."""
    return sum((payout(e.litres, e.fat, e.snf) for e in entries), Decimal("0.00"))


def main():
    """Clerk's console: enter milk entries; blank farmer ID ends the session."""
    totals = {}
    print("Ksheera Co-operative - milk entry (blank farmer ID to finish)")
    print(f"{'ID':<6}{'Sh':<3}{'Litres':>8}{'Fat':>6}{'SNF':>6}{'Rate':>8}{'Amount':>10}")
    while True:
        farmer_id = input("Farmer ID : ")
        if not farmer_id.strip():
            break
        try:
            entry = parse_entry(farmer_id, input("Shift M/E : "), input("Litres    : "),
                                input("Fat %     : "), input("SNF %     : "))
        except ValueError as err:
            print(f"  REJECTED - {err}")
            continue
        rate, amount = rate_per_litre(entry.fat, entry.snf), payout(*entry[2:])
        totals.setdefault(entry.farmer_id, []).append(entry)
        print(f"{entry.farmer_id:<6}{entry.shift:<3}{entry.litres:>8}{entry.fat:>6}"
              f"{entry.snf:>6}{rate:>8.2f}{amount:>10.2f}")
    print("\nTen-day statement")
    for farmer_id, entries in totals.items():
        print(f"  {farmer_id:<6}{len(entries):>3} entries  Rs {ten_day_total(entries):>10.2f}")


if __name__ == "__main__":
    main()
