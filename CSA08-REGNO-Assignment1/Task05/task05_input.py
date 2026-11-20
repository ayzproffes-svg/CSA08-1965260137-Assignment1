"""Task 5: reading the clerk's entries, validating text, converting, formatting."""
import sys
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Task07"))
import milkrate                        # float rate card from Task 7


def is_number_text(text):
    """Approach A (check first): True if text is digits with at most one '.'."""
    cleaned = text.strip()
    return cleaned.isascii() and cleaned.replace(".", "", 1).isdigit()


def read_float_checked(prompt, low, high):
    """Ask until the clerk types a number in [low, high]; uses is_number_text()."""
    while True:
        text = input(prompt)
        if not sys.stdin.isatty():      # echo typed text when input is piped (transcripts)
            print(text)
        if not is_number_text(text):
            print(f"  '{text}' is not a number - type digits and a '.' (e.g. 8.5)")
            continue
        value = float(text)
        if not low <= value <= high:
            print(f"  {value} is outside {low}-{high}")
            continue
        return value


def to_float_or_none(text):
    """Approach B (just try): float() inside try/except ValueError."""
    try:
        return float(text)
    except ValueError:
        return None


def demo_inputs():
    print("input text    isnumber?  try/except result")
    for text in ("8.5", " 8.5 ", "8,5", "eight", "", "-3", "nan", "1e1", "1_0", "٣"):
        print(f"{text!r:<14}{str(is_number_text(text)):<11}{to_float_or_none(text)!r}")
    n = 200_000
    t_a = timeit.timeit(lambda: is_number_text("8.5") and float("8.5"), number=n)
    t_b = timeit.timeit(lambda: to_float_or_none("8.5"), number=n)
    t_a_bad = timeit.timeit(lambda: is_number_text("eight"), number=n)
    t_b_bad = timeit.timeit(lambda: to_float_or_none("eight"), number=n)
    print(f"\nper entry (microseconds)   valid '8.5'   invalid 'eight'")
    print(f"  A: check then convert   {t_a / n * 1e6:10.3f}   {t_a_bad / n * 1e6:12.3f}")
    print(f"  B: try/except           {t_b / n * 1e6:10.3f}   {t_b_bad / n * 1e6:12.3f}")


def entry_session():
    """Interactive entry of three shifts, with an aligned table at the end."""
    rows = []
    for shift in ("M", "E", "M"):
        litres = read_float_checked(f"Litres ({shift}) : ", 0.1, 200)
        fat = read_float_checked("Fat %       : ", 2.0, 7.0)
        snf = read_float_checked("SNF %       : ", 7.0, 10.0)
        rows.append((shift, litres, fat, snf))
    print(f"\n{'Sh':<3}{'Litres':>8}{'Fat':>6}{'SNF':>6}{'Rate':>8}{'Amount':>10}")
    total = 0.0
    for shift, litres, fat, snf in rows:
        rate = milkrate.rate_per_litre(fat, snf)
        amount = milkrate.payout(litres, fat, snf)
        total += amount
        print(f"{shift:<3}{litres:8.1f}{fat:6.1f}{snf:6.1f}{rate:8.2f}{amount:10.2f}")
    print(f"{'Total':<29}{total:10.2f}")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo_inputs()
    else:
        entry_session()
