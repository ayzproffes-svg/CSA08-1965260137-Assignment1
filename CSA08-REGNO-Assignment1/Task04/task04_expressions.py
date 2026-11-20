"""Task 4: expressions, surprises, and int()/floor() alternatives."""
import math
import timeit

print("-- surprising results --")
print("(4.2 - 3.5) / 0.1        =", (4.2 - 3.5) / 0.1)
print("round((4.2 - 3.5) / 0.1) =", round((4.2 - 3.5) / 0.1))
print("(3.1 - 3.5) / 0.1        =", (3.1 - 3.5) / 0.1)
print("-2 ** 2                  =", -2 ** 2, "   (** binds tighter than unary minus)")
print("(-2) ** 2                =", (-2) ** 2)
print("2 ** 3 ** 2              =", 2 ** 3 ** 2, "  (** is right-associative: 2 ** 9)")
print("2 ** -1                  =", 2 ** -1)
print("10 - 4 - 3               =", 10 - 4 - 3, "   (- is left-associative)")
print("round(2.5), round(3.5)   =", round(2.5), round(3.5), "  (halves go to the EVEN number)")
print("round(0.5), round(1.5)   =", round(0.5), round(1.5))
print("8.5 * 33.4               =", 8.5 * 33.4)
print("0.1 * 3 == 0.3           =", 0.1 * 3 == 0.3)

print("\n-- round() vs int() vs math.floor() for negative values --")
for v in (-2.7, -2.5, -2.2, 2.7):
    print(f"value {v:5}: round {round(v):3}  int {int(v):3}  floor {math.floor(v):3}")

print("\n-- comparison chaining and Boolean operators --")
fat = 4.2
print("2.0 <= fat <= 7.0        =", 2.0 <= fat <= 7.0)
print("2.0 <= 8.0 <= 7.0        =", 2.0 <= 8.0 <= 7.0)
print("not (fat < 2.0 or fat > 7.0) =", not (fat < 2.0 or fat > 7.0))
print("1 < 2 < 3 == 3           =", 1 < 2 < 3 == 3)
print("True + True * 3          =", True + True * 3)

print("\n-- alternative: steps with int() or floor() instead of round() --")
BASE, FATV, SNFV = 30.0, 0.40, 0.30
def rate_with(step_fn, fat, snf=8.5):
    return round(BASE + step_fn((fat - 3.5) / 0.1) * FATV + step_fn((snf - 8.5) / 0.1) * SNFV, 2)
print(f"{'fat':>5}{'raw steps':>22}{'round':>8}{'int':>6}{'floor':>7} | rate: round    int  floor")
for fat in (4.2, 3.1, 4.3):
    raw = (fat - 3.5) / 0.1
    print(f"{fat:>5}{raw!r:>22}{round(raw):>8}{int(raw):>6}{math.floor(raw):>7} |"
          f"       {rate_with(round, fat):>6} {rate_with(int, fat):>6} {rate_with(math.floor, fat):>6}")
print("\ntime of one step calculation (1,000,000 calls, seconds):")
for name, fn in (("round", round), ("int", int), ("math.floor", math.floor)):
    print(f"  {name:<11}{timeit.timeit(lambda: fn(7.000000000000001), number=1_000_000):7.3f}")
