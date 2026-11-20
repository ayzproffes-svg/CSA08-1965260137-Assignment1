"""Task 1: the data the program stores, and the 'three variables per farmer' alternative."""
import sys
import time

# ---- 1. data model: every value, its type and its role --------------------------------
MODEL = [
    # name,            python type,    kind,      why
    ("farmer_id",      "str",          "input",   "identifier, e.g. 'K017'; never added up"),
    ("shift",          "str",          "input",   "'M' or 'E'; a label, not a number"),
    ("litres",         "Decimal",      "input",   "fractional quantity, e.g. 8.5 L"),
    ("fat",            "Decimal",      "input",   "fractional percentage"),
    ("snf",            "Decimal",      "input",   "fractional percentage"),
    ("rate_per_litre", "Decimal",      "output",  "money: must be exact to the paisa"),
    ("amount",         "Decimal",      "output",  "money, rounded to paise"),
    ("ten_day_total",  "Decimal",      "output",  "money, sum of rounded amounts"),
    ("fat_steps",      "int-valued",   "derived", "whole number of 0.1 % steps (can be negative)"),
    ("entry count",    "int",          "derived", "whole number, e.g. 20 shifts in ten days"),
    ("BASE_RATE ...",  "Decimal",      "constant", "never change during a run"),
]
print(f"{'name':<16}{'type':<12}{'kind':<10}reason")
for row in MODEL:
    print(f"{row[0]:<16}{row[1]:<12}{row[2]:<10}{row[3]}")

# ---- 2. alternative: litres1, fat1, snf1, litres2 ... instead of one tuple per entry ----
def three_variable_program(n):
    """Return the source code a clerk would have to write for n farmers."""
    lines = [f"litres{i}, fat{i}, snf{i} = {10 + i % 5}, 3.5, 8.5" for i in range(1, n + 1)]
    lines.append("total = 0.0")
    lines += [f"total += litres{i} * (30.0 + round((fat{i}-3.5)/0.1)*0.4 + "
              f"round((snf{i}-8.5)/0.1)*0.3)" for i in range(1, n + 1)]
    return "\n".join(lines)


def list_program(n):
    """Same job with one tuple per entry in a list: the code length does not depend on n."""
    entries = [(10 + i % 5, 3.5, 8.5) for i in range(1, n + 1)]
    total = 0.0
    for litres, fat, snf in entries:
        total += litres * (30.0 + round((fat - 3.5) / 0.1) * 0.4
                           + round((snf - 8.5) / 0.1) * 0.3)
    return total


print("\nn      3-variable: lines of code   names   run time(ms) | list design: lines  run time(ms)")
for n in (300, 1000, 3000):
    source = three_variable_program(n)
    namespace = {}
    t0 = time.perf_counter()
    exec(compile(source, "<generated>", "exec"), namespace)
    t_vars = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    total = list_program(n)
    t_list = (time.perf_counter() - t0) * 1000
    assert abs(namespace["total"] - total) < 1e-6
    names = sum(1 for k in namespace if k.startswith(("litres", "fat", "snf")))
    print(f"{n:<7}{source.count(chr(10)) + 1:>22}{names:>10}{t_vars:>15.2f} | {7:>17}{t_list:>14.2f}")
print("\nFor 150,000 farmers the three-variable source would need about 450,000 names and")
print("300,000 lines of hand-written code; the list/tuple design is still 7 lines.")
