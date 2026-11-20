"""Task 2 alternative: integer paise, or float + round() after every addition."""
import sys
import time
from decimal import Decimal

payments = ["33.40"] * 1000 + ["0.10"] * 3


def to_paise(text):
    """'33.40' -> 3340 using only str and int operations (no float involved)."""
    rupees, _, paise = text.partition(".")
    return int(rupees) * 100 + int((paise + "00")[:2])


def total_paise(items):
    total = 0
    for amount in items:
        total += to_paise(amount)
    return total            # int paise; divide by 100 only for display


def total_float_rounded(items):
    total = 0.0
    for amount in items:
        total = round(total + float(amount), 2)
    return total


def total_decimal(items):
    total = Decimal("0")
    for amount in items:
        total += Decimal(amount)
    return total


exact = Decimal("33400.30")
p = total_paise(payments)
print("integer paise       :", p, "->", f"{p // 100}.{p % 100:02d}", " exact:", Decimal(p) / 100 == exact)
print("float + round/step  :", total_float_rounded(payments), " exact:", Decimal(str(total_float_rounded(payments))) == exact)
print("Decimal             :", total_decimal(payments), " exact:", total_decimal(payments) == exact)
print("plain float         :", sum(float(a) for a in payments), " exact: False")

print("\nmemory per value (sys.getsizeof, bytes):")
print("  float   :", sys.getsizeof(33.4))
print("  int     :", sys.getsizeof(3340))
print("  Decimal :", sys.getsizeof(Decimal("33.40")))

print("\ntime per addition (best of 5, 1,000,000 additions):")
N = 1_000_000
def bench(label, step, start):
    best = 1e9
    for _ in range(5):
        t = start
        t0 = time.perf_counter()
        for _ in range(N):
            t = step(t)
        best = min(best, time.perf_counter() - t0)
    print(f"  {label:<26}{best / N * 1e9:8.1f} ns")

f, i, d, dn = 33.4, 3340, Decimal("33.40"), Decimal("0")
bench("float +=", lambda t: t + f, 0.0)
bench("float + round(,2)", lambda t: round(t + f, 2), 0.0)
bench("int paise +=", lambda t: t + i, 0)
bench("Decimal +=", lambda t: t + d, dn)

print("\ncorrectness for n payments of Rs 0.10 (exact total = n/10):")
for n in (300, 6000, 150000):
    s = 0.0
    for _ in range(n):
        s += 0.10
    r = 0.0
    for _ in range(n):
        r = round(r + 0.10, 2)
    print(f"  n={n:<7} float sum {s!r:<22} float+round {r!r:<10} int paise {n * 10 / 100!r:<10}")
