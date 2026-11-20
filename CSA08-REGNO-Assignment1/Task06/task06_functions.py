"""Task 6: the calculation divided into functions, plus scope and alternatives."""
import timeit

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30


def rate_per_litre(fat, snf):
    """Return the price per litre (Rs, 2 decimals) for the given fat % and SNF %.

    Parameters: fat, snf - percentages as floats.  Reads the module constants but
    never changes them.
    """
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the amount payable (Rs, 2 decimals) for one entry. Does not print."""
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(entries):
    """Return the total payable for a list of (litres, fat, snf) tuples."""
    total = 0.0
    for litres, fat, snf in entries:
        total = round(total + payout(litres, fat, snf), 2)
    return total


def show_payment(litres, fat, snf):
    """Print one line (side effect) and return None - contrast with payout()."""
    print(f"{litres:6} L  Rs {payout(litres, fat, snf):8.2f}")


# ---- return vs print ---------------------------------------------------------------------
entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
result = show_payment(*entries[1])
print("show_payment returned:", result)
print("payout returned      :", payout(*entries[1]))
print("ten_day_total        :", ten_day_total(entries))

# ---- local vs global ---------------------------------------------------------------------
def wrong_revision():
    BASE_RATE = 99.0            # creates a LOCAL name; the global is untouched
    return BASE_RATE

def broken_revision():
    BASE_RATE = BASE_RATE + 1   # reads the name before it is assigned locally
    return BASE_RATE

print("\nwrong_revision() ->", wrong_revision(), "| global BASE_RATE still", BASE_RATE)
try:
    broken_revision()
except UnboundLocalError as err:
    print("UnboundLocalError:", err)

# ---- alternatives: lambda, and one long script ------------------------------------------
rate_lambda = lambda fat, snf: round(BASE_RATE + round((fat - 3.5) / 0.1) * FAT_STEP_VALUE
                                     + round((snf - 8.5) / 0.1) * SNF_STEP_VALUE, 2)
payout_lambda = lambda litres, fat, snf: round(litres * rate_lambda(fat, snf), 2)
print("\nlambda payout(8.5, 4.2, 8.7) =", payout_lambda(8.5, 4.2, 8.7))

N = 150_000
data = [(10 + i % 7, 3.0 + (i % 40) / 10, 7.5 + (i % 20) / 10) for i in range(N)]

def with_functions():
    return ten_day_total(data)

def one_long_script():
    total = 0.0
    for litres, fat, snf in data:
        fat_steps = round((fat - 3.5) / 0.1)
        snf_steps = round((snf - 8.5) / 0.1)
        rate = round(30.0 + fat_steps * 0.40 + snf_steps * 0.30, 2)
        total = round(total + round(litres * rate, 2), 2)
    return total

def with_lambdas():
    total = 0.0
    for litres, fat, snf in data:
        total = round(total + payout_lambda(litres, fat, snf), 2)
    return total

assert with_functions() == one_long_script() == with_lambdas()
print(f"\ntime for {N:,} entries (best of 3, seconds):")
for name, fn in (("functions", with_functions), ("one long script", one_long_script),
                 ("lambdas", with_lambdas)):
    print(f"  {name:<16}{min(timeit.repeat(fn, number=1, repeat=3)):7.3f}")
print("\nrate formula copies: functions 1, lambdas 1, one long script = 1 per place it is needed")
