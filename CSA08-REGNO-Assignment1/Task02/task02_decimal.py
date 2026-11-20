"""Task 2 - Complete the Code (TODO 1 completed)."""
from decimal import Decimal

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3

def total_float(items):
    total = 0.0
    for amount in items:
        total += float(amount)
    return total

def total_decimal(items):
    # TODO 1: Add the amounts exactly by creating a Decimal from each string, and
    # return the Decimal total
    total = Decimal("0")
    for amount in items:
        total += Decimal(amount)
    return total

def total_decimal_from_float(items):
    """The follow-up experiment: Decimal(float(amount)) instead of Decimal(amount)."""
    total = Decimal("0")
    for amount in items:
        total += Decimal(float(amount))
    return total

print("float :", total_float(payments))
print("Decimal:", total_decimal(payments))
print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

print("\n-- follow-up: Decimal(float(amount)) --")
print("Decimal(float(33.40)) =", Decimal(float("33.40")))
print("Decimal via float     :", total_decimal_from_float(payments))
print("rounded to paise      :", total_decimal_from_float(payments).quantize(Decimal("0.01")))
