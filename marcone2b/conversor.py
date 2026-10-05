#!C:\Users\ALUNOS\AppData\Local\Microsoft\WindowsApps\python.exe
# -*- coding: utf-8 -*-
# ^ Line 1 must point to YOUR python.exe (run `where python` in cmd to find it).
"""Temperature converter: Celsius, Fahrenheit and Kelvin.

Runs as a CGI page under XAMPP (Apache) and, if started from a terminal
(`python conversor.py`), as a text menu that loops until you choose Exit.
"""
import html
import math
import os
import sys
from urllib.parse import parse_qs


# ---------------------------------------------------------------- conversions
# Requirement 1: one function for each temperature system.
# Each one takes a value in its own scale and returns the other two scales.

def celsius(value):
    return {"Fahrenheit": value * 9 / 5 + 32, "Kelvin": value + 273.15}


def fahrenheit(value):
    c = (value - 32) * 5 / 9
    return {"Celsius": c, "Kelvin": c + 273.15}


def kelvin(value):
    c = value - 273.15
    return {"Celsius": c, "Fahrenheit": c * 9 / 5 + 32}


# Menu definition: "minimum" is absolute zero expressed in each scale.
SYSTEMS = {
    "1": {"name": "Celsius", "symbol": "°C", "convert": celsius, "minimum": -273.15},
    "2": {"name": "Fahrenheit", "symbol": "°F", "convert": fahrenheit, "minimum": -459.67},
    "3": {"name": "Kelvin", "symbol": "K", "convert": kelvin, "minimum": 0.0},
}
SYMBOLS = {}
for _system in SYSTEMS.values():  # repetition structure: build a name -> symbol lookup
    SYMBOLS[_system["name"]] = _system["symbol"]


def read_value(text):
    """Accepts '36.6' or '36,6'. Raises ValueError for anything else."""
    number = float(text.strip().replace(",", "."))
    if not math.isfinite(number):
        raise ValueError("not a finite number")
    return number


def run_conversion(option, text):
    """Returns (error_message, result). Exactly one of them is None."""
    system = SYSTEMS.get(option)
    if system is None:
        return "Pick a scale from the menu.", None
    try:
        value = read_value(text)
    except ValueError:
        return "Enter a number, like 36.6 or -40.", None
    if value < system["minimum"]:
        return (f"{value:g} {system['symbol']} is below absolute zero. "
                f"The lowest possible value is {system['minimum']:g} {system['symbol']}."), None
    return None, {"system": system, "value": value, "converted": system["convert"](value)}


# ------------------------------------------------------------------ web (CGI)
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Temperature converter</title>
<style>
:root{--paper:#eef3f6;--ink:#12263a;--muted:#566b7e;--glass:#c9d6df;--mercury:#d6402b;--white:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:1rem/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:34rem;margin:0 auto;padding:2.5rem 1.25rem 3rem}
h1{font:600 2rem/1.15 Georgia,"Iowan Old Style",serif;margin:0 0 .35rem}
.lead{color:var(--muted);margin:0 0 1.75rem}
.bar{display:flex;border:2px solid var(--ink);border-radius:999px;overflow:hidden;background:var(--white)}
.seg{flex:1;margin:0}
.seg input{position:absolute;opacity:0}
.seg span{display:block;text-align:center;padding:.7rem .5rem;cursor:pointer;font-weight:600}
.seg small{display:block;font-weight:400;color:var(--muted)}
.seg input:checked+span{background:var(--ink);color:var(--white)}
.seg input:checked+span small{color:var(--glass)}
.seg input:focus-visible+span{outline:3px solid var(--mercury);outline-offset:-3px}
label.field{display:block;margin:1.25rem 0 .35rem;font-weight:600}
input[type=text]{width:100%;padding:.75rem .9rem;font:inherit;border:2px solid var(--ink);border-radius:.6rem;background:var(--white)}
input[type=text]:focus-visible,button:focus-visible,a.btn:focus-visible{outline:3px solid var(--mercury);outline-offset:2px}
.actions{display:flex;gap:.75rem;margin-top:1rem}
button,a.btn{font:inherit;font-weight:600;padding:.7rem 1.25rem;border-radius:.6rem;border:2px solid var(--ink);cursor:pointer;text-decoration:none;display:inline-block}
button.go{background:var(--mercury);border-color:var(--mercury);color:var(--white)}
button.exit,a.btn{background:transparent;color:var(--ink)}
.error{margin-top:1.25rem;padding:.8rem 1rem;border-left:4px solid var(--mercury);background:var(--white)}
.result{margin-top:2rem;padding-top:1.5rem;border-top:2px solid var(--glass)}
.result h2{font:600 1rem/1.3 system-ui,sans-serif;color:var(--muted);margin:0 0 .75rem}
.result ul{list-style:none;margin:0;padding:0;display:grid;gap:.5rem}
.result li{display:flex;align-items:baseline;gap:.5rem}
.n{font:600 2.25rem/1.1 Georgia,serif}
.u{font-weight:600}
.l{color:var(--muted);margin-left:auto}
.thermo{margin-top:1.5rem}
.track{height:.9rem;border-radius:999px;background:var(--glass);overflow:hidden}
.fill{height:100%;background:var(--mercury);border-radius:999px}
.scale{display:flex;justify-content:space-between;color:var(--muted);font-size:.85rem;margin-top:.3rem}
</style>
</head>
<body><main>
{{body}}
</main></body>
</html>"""


def menu_html(selected, value):
    # Repetition structure: one segment of the menu bar per temperature system.
    segments = ""
    for key, system in SYSTEMS.items():
        checked = " checked" if key == selected else ""
        segments += (f'<label class="seg"><input type="radio" name="option" value="{key}"{checked}>'
                     f'<span>{system["name"]}<small>{system["symbol"]}</small></span></label>')
    return f"""
<h1>Temperature converter</h1>
<p class="lead">Choose the scale you have, type a value, and see the other two.</p>
<form method="post" action="">
  <div class="bar" role="radiogroup" aria-label="Convert from">{segments}</div>
  <label class="field" for="value">Value</label>
  <input type="text" id="value" name="value" inputmode="decimal" autocomplete="off"
         value="{html.escape(value)}" placeholder="e.g. 36.6" autofocus>
  <div class="actions">
    <button class="go" type="submit" name="action" value="convert">Convert</button>
    <button class="exit" type="submit" name="action" value="exit" formnovalidate>Exit</button>
  </div>
</form>"""


def result_html(result):
    system, value, converted = result["system"], result["value"], result["converted"]
    rows = ""
    for name, number in converted.items():  # repetition structure: one row per target scale
        rows += (f'<li><span class="n">{number:.2f}</span><span class="u">{SYMBOLS[name]}</span>'
                 f'<span class="l">{name}</span></li>')
    celsius_value = value if system["name"] == "Celsius" else converted["Celsius"]
    percent = max(0, min(100, (celsius_value + 50) / 200 * 100))
    return f"""
<section class="result" aria-live="polite">
  <h2>{value:g} {system["symbol"]} ({system["name"]}) is</h2>
  <ul>{rows}</ul>
  <div class="thermo">
    <div class="track"><div class="fill" style="width:{percent:.1f}%"></div></div>
    <div class="scale"><span>-50 °C</span><span>150 °C</span></div>
  </div>
</section>"""


def goodbye_html():
    return """
<h1>Goodbye!</h1>
<p class="lead">The converter is closed. Come back whenever you need it.</p>
<a class="btn" href="?">Start again</a>"""


def send(body):
    sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
    sys.stdout.write(TEMPLATE.replace("{{body}}", body))


def web():
    sys.stdout.reconfigure(encoding="utf-8")
    form = {}
    if os.environ.get("REQUEST_METHOD") == "POST":
        length = int(os.environ.get("CONTENT_LENGTH") or 0)
        form = parse_qs(sys.stdin.buffer.read(length).decode("utf-8"))

    def field(name):
        return form.get(name, [""])[0]

    action = field("action")
    if action == "exit":                      # requirement 3: the user decides to leave
        send(goodbye_html())
        return

    option = field("option") or "1"
    value = field("value")
    body = menu_html(option, value)           # the menu is shown on every page until Exit
    if action == "convert":
        error, result = run_conversion(option, value)
        if error:
            body += f'<div class="error" role="alert">{html.escape(error)}</div>'
        else:
            body += result_html(result)
    send(body)


# -------------------------------------------------------------------- terminal
def terminal():
    while True:                               # requirement 3: loops until option 0
        print("\n=== Temperature converter ===")
        for key, system in SYSTEMS.items():
            print(f"{key} - from {system['name']} ({system['symbol']})")
        print("0 - Exit")
        option = input("Choose: ").strip()
        if option == "0":
            print("Goodbye!")
            break
        if option not in SYSTEMS:
            print("Invalid option.")
            continue
        error, result = run_conversion(option, input("Value: "))
        if error:
            print(error)
            continue
        for name, number in result["converted"].items():
            print(f"  {number:.2f} {SYMBOLS[name]} ({name})")


if __name__ == "__main__":
    if os.environ.get("GATEWAY_INTERFACE"):   # started by Apache
        web()
    else:                                     # started from cmd/PowerShell
        terminal()
