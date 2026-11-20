"""Task 3: named constants, dynamic typing, swapping, and the RATE_CARD dict alternative."""
import timeit

# ---- the single place where rates live (UPPER_CASE = "do not change") -------------------
BASE_RATE = 30.00          # Rs/litre at 3.5 % fat, 8.5 % SNF
FAT_STEP_VALUE = 0.40      # Rs per 0.1 % fat
SNF_STEP_VALUE = 0.30      # Rs per 0.1 % SNF
STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1
FAT_MIN, FAT_MAX = 2.0, 7.0

def rate(fat, snf):
    return round(BASE_RATE + round((fat - STD_FAT) / STEP) * FAT_STEP_VALUE
                 + round((snf - STD_SNF) / STEP) * SNF_STEP_VALUE, 2)

print("rate(4.2, 8.7) =", rate(4.2, 8.7))

# ---- no true constants: Python only trusts the convention ------------------------------
BASE_RATE = 99.0
print("after BASE_RATE = 99.0 (legal!):", rate(4.2, 8.7), "<- convention was broken, no error")
BASE_RATE = 30.00

# ---- dynamic typing ---------------------------------------------------------------------
x = 10
print("\nx =", x, type(x))
x = "ten"
print("x =", x, type(x))
try:
    print(x + 1)
except TypeError as err:
    print("TypeError:", err)

# ---- multiple assignment and swapping ---------------------------------------------------
fat, snf = 4.2, 8.7
print("\nbefore swap:", fat, snf)
fat, snf = snf, fat            # right side is evaluated first, as a tuple (8.7, 4.2)
print("after swap :", fat, snf)
a = b = c = 0
print("a = b = c = 0 ->", a, b, c)

# ---- alternatives: magic numbers vs dict ------------------------------------------------
def rate_magic(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)

RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}

def rate_dict(fat, snf):
    return round(RATE_CARD["base"] + round((fat - 3.5) / 0.1) * RATE_CARD["fat"]
                 + round((snf - 8.5) / 0.1) * RATE_CARD["snf"], 2)

assert rate(4.2, 8.7) == rate_magic(4.2, 8.7) == rate_dict(4.2, 8.7)
n = 300_000
print("\ntime for 300,000 rate calculations (seconds, best of 5):")
for name, fn in (("named constants", rate), ("magic numbers", rate_magic), ("RATE_CARD dict", rate_dict)):
    print(f"  {name:<16}{min(timeit.repeat(lambda: fn(4.2, 8.7), number=n, repeat=5)):8.3f}")
print("\nplaces to edit for a fat-step revision: magic numbers = k (every expression),")
print("named constant = 1 line, RATE_CARD dict = 1 line.")
