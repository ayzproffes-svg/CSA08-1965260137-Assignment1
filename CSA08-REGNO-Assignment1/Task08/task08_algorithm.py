"""Task 8: algorithm planned as pseudocode first, then written, traced and measured.

PSEUDOCODE (written before the Python):

ALGORITHM TenDayPayment
START
  SET total TO 0.00
  INPUT number of entries
  FOR each entry IN the ten-day entries
    INPUT farmer_id, shift, litres, fat, snf
    IF entry is valid THEN
      SET rate TO base rate + fat steps * fat value + snf steps * snf value
      SET amount TO litres * rate, rounded to paise
      SET total TO total + amount
      OUTPUT shift, litres, rate, amount
    ELSE
      OUTPUT "invalid entry", reason
    ENDIF
  ENDFOR
  OUTPUT total
END

ALGORITHM ValidateEntry
START
  IF litres is not a number OR fat is not a number OR snf is not a number THEN
    entry is invalid
  ELSE
    IF litres <= 0 OR litres > 200 THEN entry is invalid
    ELSE
      IF fat < 2.0 OR fat > 7.0 THEN entry is invalid
      ELSE
        IF snf < 7.0 OR snf > 10.0 THEN entry is invalid
        ELSE entry is valid
        ENDIF
      ENDIF
    ENDIF
  ENDIF
END
"""
import sys
import time
import tracemalloc
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Task09"))
import milkcalc as mc

# ---- hand trace of the pseudocode for three entries ---------------------------------------
RAW = [("K001", "M", "10", "3.5", "8.5"),
       ("K001", "E", "8.5", "4.2", "8.7"),
       ("K001", "M", "12", "3.1", "8.3")]
print("TRACE        litres  fat  snf | fat steps snf steps  rate    amount    total")
total = Decimal("0.00")
for raw in RAW:
    e = mc.parse_entry(*raw)
    fs, ss = mc.whole_steps(e.fat, mc.STD_FAT), mc.whole_steps(e.snf, mc.STD_SNF)
    rate, amount = mc.rate_per_litre(e.fat, e.snf), mc.payout(e.litres, e.fat, e.snf)
    total += amount
    print(f"entry {e.shift:<6}{e.litres:>7}{e.fat:>5}{e.snf:>5} |{fs:>9}{ss:>10}{rate:>7}{amount:>10}{total:>10}")
print("expected total by hand: 300.00 + 283.90 + 333.60 =", Decimal("917.50"), "->", total)


# ---- two solutions: store every entry, or keep a running total ----------------------------
def make_entries(n):
    """Generator of n valid entries (no list is built)."""
    for i in range(n):
        yield mc.Entry("K001", "M", Decimal(10 + i % 7), Decimal("3.5") + Decimal(i % 5) / 10,
                       Decimal("8.5"))


def total_stored(n):
    entries = list(make_entries(n))                  # O(n) space
    return mc.ten_day_total(entries)


def total_running(n):
    total = Decimal("0.00")                          # O(1) space
    for e in make_entries(n):
        total += mc.payout(e.litres, e.fat, e.snf)
    return total


print("\n   n   | stored: time(s) peak memory(KB) | running: time(s) peak memory(KB) | equal")
for n in (300, 6000, 150_000):
    row = []
    for fn in (total_stored, total_running):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = fn(n)
        elapsed = time.perf_counter() - t0
        peak = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()
        row.append((elapsed, peak, result))
    print(f"{n:>7}|{row[0][0]:>14.3f}{row[0][1]:>16.0f} |{row[1][0]:>15.3f}{row[1][1]:>17.0f} | {row[0][2] == row[1][2]}")
