# CSA08 - Assignment 1: Payment Calculator for a Village Milk Co-operative

| | |
|---|---|
| Name | `<YOUR NAME>` |
| Register number | `<REGISTER NUMBER>` |
| Python version | 3.12 |
| Libraries | standard library only (see `requirements.txt`) |

Repository name to use on GitHub: `CSA08-<RegisterNumber>-Assignment1`
(rename this folder before pushing, and commit at least once per task folder).

## How to run (from inside each task folder)

| Task | Command | Result in one line |
|---|---|---|
| 01 | `python task01_data_model.py` | Data model table; 3-variable design needs 601 lines for 300 farmers vs 7 for a list |
| 02 | `python make_session.py`, `python task02_decimal.py`, `python task02_alternatives.py` | Interpreter session; Decimal total 33400.30 exact, float 33400.30000000061 |
| 03 | `python task03_constants.py` | One named-constant block; all three designs run at the same speed |
| 04 | `python task04_expressions.py` | Float step surprises; int() gives a wrong rate for fat 3.1 and 4.3 |
| 05 | `python task05_input.py < sample_input.txt` (or `--demo`) | Invalid text rejected, aligned table printed |
| 06 | `python task06_functions.py` | Functions, return vs print, scope errors, lambda/script timings |
| 07 | `python milkrate.py` then `python use_milkrate.py` | Expected table; import prints no table |
| 08 | `python task08_algorithm.py` | Hand trace total 917.50; running total uses O(1) memory |
| 09 | `python test_milkcalc.py` and `python milkcalc.py` | 22 tests pass; 5-entry hand total 2059.25 |
| 10 | `python task10_compare.py` | Float and Decimal totals differ by up to Rs 71.78 at 150,000 payments |
| 11 | `python task11_ratecard_loader.py` | JSON rate card loads in about 33 microseconds |
| 12 | `python test_milkrate_v2.py`, `python task12_evaluation.py` | 24 tests pass for both seasons and the bonus |

Tasks 10, 11 and 12 import `Task07/milkrate.py` and `Task09/milkcalc.py` using a relative path,
so keep the folder layout unchanged.

## Design decision
Original design: Decimal values, one block of named constants, payment rounded to the paisa
(half up), ten-day total = sum of rounded payments. Day-4 change: MODIFIED, not redesigned
(see Task 12 and the report).
