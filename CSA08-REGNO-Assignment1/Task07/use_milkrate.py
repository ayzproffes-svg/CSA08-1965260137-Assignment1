"""Second script: imports milkrate and calls payout() (Task 7)."""
import os
import sys
import time

t0 = time.perf_counter()
import milkrate                       # style 1: whole module, use milkrate.name
first_import = time.perf_counter() - t0

import milkrate as mr                 # style 2: alias for the same module object
from milkrate import payout           # style 3: one name copied into this namespace

t0 = time.perf_counter()
import milkrate                       # repeat import: only a sys.modules lookup
repeat_import = time.perf_counter() - t0

print("Importing milkrate printed no rate table: the __main__ guard stayed False.")
print("payout(8.5, 4.2, 8.7) via milkrate.payout :", milkrate.payout(8.5, 4.2, 8.7))
print("payout(8.5, 4.2, 8.7) via mr.payout       :", mr.payout(8.5, 4.2, 8.7))
print("payout(8.5, 4.2, 8.7) via payout          :", payout(8.5, 4.2, 8.7))
print("milkrate is mr                            :", milkrate is mr)
print("milkrate.__name__                         :", milkrate.__name__)
print("'milkrate' in sys.modules                 :", "milkrate" in sys.modules)
print("module file                               :", os.path.basename(milkrate.__file__))
print("sys.path[0] (script folder searched first):", sys.path[0])
print(f"first import {first_import*1e6:8.1f} us   repeat import {repeat_import*1e6:6.2f} us")
