"""Task 12 B/D: evaluate the ORIGINAL design on two-decimal analyser readings."""
import sys, time
from decimal import Decimal as D
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "Task07")); sys.path.insert(0, str(root / "Task09"))
import milkrate            # original float module (Task 7)
import milkcalc            # original Decimal module (Task 9)
import milkrate_v2 as v2

print("1) Step count of the ORIGINAL float code, fat readings with two decimals")
print(f"{'fat':>6}  {'(fat-3.5)/0.1':>22}  {'round()':>8}  {'exact (v2)':>10}")
for fat in ("4.15", "4.20", "4.25", "4.30", "4.35", "4.45"):
    raw = (float(fat) - 3.5) / 0.1
    print(f"{fat:>6}  {raw!r:>22}  {round(raw):>8}  {(D(fat)-D('3.5'))/D('0.1'):>10}")

print("\n2) Rate for fat 4.25 / SNF 8.63 (standard card) in each design")
print("  original float module   :", milkrate.rate_per_litre(4.25, 8.63))
print("  original Decimal module :", milkcalc.rate_per_litre(D("4.25"), D("8.63")))
print("  v2 (exact steps)        :", v2.rate_per_litre(D("4.25"), D("8.63")))

print("\n3) Same fat step bucket for different readings (original design)")
for fat in ("4.20", "4.25", "4.34"):
    print(f"  fat {fat}: original Decimal rate {milkcalc.rate_per_litre(D(fat), D('8.5'))}"
          f"   v2 rate {v2.rate_per_litre(D(fat), D('8.5'))}")

print("\n4) Original constants cannot express the seasons: summer needs base 32.00, fat step 0.45")
print("  milkcalc has one BASE_RATE / FAT_STEP_VALUE ->", milkcalc.BASE_RATE, milkcalc.FAT_STEP_VALUE)
print("  v2 cards:", v2.STANDARD_CARD, v2.SUMMER_CARD, sep="\n    ")

print("\n5) Cost of the change: time per payout, 200,000 calls")
fat, snf, litres = D("4.25"), D("8.63"), D("10")
for name, fn in (("milkcalc.payout (1 card, rounded steps)", lambda: milkcalc.payout(litres, fat, snf)),
                 ("v2.payout (card + exact steps)", lambda: v2.payout(litres, fat, snf, v2.SUMMER_CARD))):
    t0 = time.perf_counter()
    for _ in range(200_000):
        fn()
    print(f"  {name:<42} {(time.perf_counter()-t0)/200_000*1e6:6.2f} us per call")
