"""Task 10: float vs Decimal totals, timings, rounding policy, and the rate-table alternative."""
import random
import sys
import time
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "Task07")); sys.path.insert(0, str(root / "Task09"))
import milkrate            # float design (Task 7)
import milkcalc as mc      # Decimal design (Task 9)

SIZES = (300, 6000, 150_000)


def make_entries(n, seed=2026):
    """n random entries as TEXT (litres 2 decimals, fat/snf 1 decimal), as typed by clerks."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        l, f, s = rnd.randint(100, 6000), rnd.randint(20, 70), rnd.randint(70, 100)
        out.append((f"{l // 100}.{l % 100:02d}", f"{f // 10}.{f % 10}", f"{s // 10}.{s % 10}"))
    return out


def timed(fn, *args):
    t0 = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - t0


def float_naive(entries):          # float, nothing rounded until the end
    total = 0.0
    for l, f, s in entries:
        total += float(l) * (30.0 + round((float(f) - 3.5) / 0.1) * 0.4
                             + round((float(s) - 8.5) / 0.1) * 0.3)
    return total


def float_rounded(entries):        # float design of Task 7: round each payment, add as float
    total = 0.0
    for l, f, s in entries:
        total += milkrate.payout(float(l), float(f), float(s))
    return total


def decimal_each(entries):         # Decimal design: round each payment (ROUND_HALF_UP), add exactly
    total = Decimal("0.00")
    for l, f, s in entries:
        total += mc.payout(Decimal(l), Decimal(f), Decimal(s))
    return total


def decimal_total_only(entries):   # Decimal, exact amounts, round ONLY the final total
    total = Decimal("0")
    for l, f, s in entries:
        d_f, d_s = Decimal(f), Decimal(s)
        total += Decimal(l) * mc.rate_per_litre(d_f, d_s)
    return mc.money(total)


print("1) TOTALS (Rs) - bank amount = sum of payments each rounded to the paisa (Decimal)")
print(f"{'n':>8} {'float naive':>20} {'float, each rounded':>20} {'Decimal each (BANK)':>20} {'Decimal total only':>19}")
results = {}
for n in SIZES:
    e = make_entries(n)
    results[n] = (e, float_naive(e), float_rounded(e), decimal_each(e), decimal_total_only(e))
    _, a, b, c, d = results[n]
    print(f"{n:>8} {a:>20.6f} {b:>20.6f} {c:>20} {d:>19}")

print("\n2) DIFFERENCE from the bank amount (Rs)")
print(f"{'n':>8} {'float naive':>16} {'float each-rounded':>20} {'Decimal total-only':>20} {'payments that differ':>22}")
for n in SIZES:
    e, a, b, c, d = results[n]
    diff_payments = sum(
        1 for l, f, s in e
        if Decimal(str(milkrate.payout(float(l), float(f), float(s)))) != mc.payout(Decimal(l), Decimal(f), Decimal(s)))
    print(f"{n:>8} {Decimal(a) - c:>16.6f} {Decimal(b) - c:>20.6f} {d - c:>20} {diff_payments:>22}")

print("\n3) TIME (seconds, time.perf_counter, includes text -> number conversion)")
print(f"{'n':>8} {'float naive':>13} {'float rounded':>14} {'Decimal each':>13} {'Decimal/float':>14}")
for n in SIZES:
    e = results[n][0]
    _, t1 = timed(float_naive, e); _, t2 = timed(float_rounded, e); _, t3 = timed(decimal_each, e)
    print(f"{n:>8} {t1:>13.4f} {t2:>14.4f} {t3:>13.4f} {t3 / t2:>13.1f}x")

print("\n4) ALTERNATIVE - rate table: compute each (fat, snf) rate once, then look it up")
print(f"{'n':>8} {'k pairs':>8} {'recalc (s)':>11} {'table (s)':>10} {'speed-up':>9} {'table bytes':>12}")
for n in SIZES:
    e = results[n][0]
    parsed = [(Decimal(l), Decimal(f), Decimal(s)) for l, f, s in e]
    t0 = time.perf_counter()
    total1 = Decimal("0.00")
    for l, f, s in parsed:
        total1 += mc.money(l * mc.rate_per_litre(f, s))
    t_recalc = time.perf_counter() - t0
    t0 = time.perf_counter()
    table, total2 = {}, Decimal("0.00")
    for l, f, s in parsed:
        key = (f, s)
        rate = table.get(key)
        if rate is None:
            rate = table[key] = mc.rate_per_litre(f, s)
        total2 += mc.money(l * rate)
    t_table = time.perf_counter() - t0
    assert total1 == total2 == results[n][3]
    size = sys.getsizeof(table) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in table.items())
    print(f"{n:>8} {len(table):>8} {t_recalc:>11.4f} {t_table:>10.4f} {t_recalc / t_table:>8.1f}x {size:>12}")
print("(k can never exceed 51 fat values x 31 SNF values = 1,581 pairs for 1-decimal readings)")

print("\n5) WHERE DOES THE DIFFERENCE COME FROM?  Decimal with ROUND_HALF_EVEN (what float round() does on ties)")
from decimal import ROUND_HALF_EVEN
print(f"{'n':>8} {'Decimal half-even':>19} {'float each-rounded':>19} {'half-even - float':>18} {'half-up - half-even':>20}")
for n in SIZES:
    e, a, b, bank, d = results[n]
    total = Decimal("0.00")
    for l, f, s in e:
        rate = mc.rate_per_litre(Decimal(f), Decimal(s))
        total += (Decimal(l) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    print(f"{n:>8} {total:>19} {b:>19.6f} {total - Decimal(str(round(b, 2))):>18} {bank - total:>20}")
