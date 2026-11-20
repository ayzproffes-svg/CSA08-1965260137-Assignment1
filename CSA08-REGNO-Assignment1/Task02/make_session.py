"""Runs the lines below in a real interactive console and prints them with >>> prompts.
Run:  python make_session.py   (or type the same lines yourself in `python`)."""
import code, contextlib, io, sys

LINES = [
    "type(10)", "type(10.0)", 'type("10")', "type(True)", "type([10, 8.5])",
    "isinstance(True, int), True + True",
    "7/2", "7//2", "7%2", "-7//2", "-7%2", "type(10/2)",
    "0.1 + 0.2", "0.1 + 0.2 == 0.3", "round(0.1 + 0.2, 2) == 0.3",
    "(0.1).hex()", "0.1 * 3", "1.1 + 2.2",
    "from decimal import Decimal",
    'Decimal("0.1") + Decimal("0.2") == Decimal("0.3")',
    "Decimal(0.1)", 'Decimal(str(0.1))',
    "sum([33.40] * 1000)", 'sum([Decimal("33.40")] * 1000)',
    "round(2.675, 2)", 'Decimal("2.675").quantize(Decimal("0.01"))',
]
console = code.InteractiveConsole()
for line in LINES:
    print(">>> " + line)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        console.push(line)
    print(buf.getvalue(), end="")
