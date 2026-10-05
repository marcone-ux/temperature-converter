# Temperature Converter

A small Python web app that converts temperatures between **Celsius**, **Fahrenheit** and **Kelvin**. It runs on a local XAMPP (Apache) server as a CGI script, and it also works as a text menu in the terminal.

## Features

- Interactive menu bar: choose the scale you have, type a value, and see the other two scales.
- The menu is shown again after every conversion, until the user clicks **Exit**.
- Accepts decimal points and commas (`36.6` or `36,6`).
- Rejects text and values below absolute zero, with a clear error message.
- A mercury bar shows where the result sits between -50 °C and 150 °C.
- Terminal mode: the same conversions in a numbered menu (`0 - Exit`).

## Project requirements and where they are met

| Requirement | Where in `conversor.py` |
|---|---|
| One function for each temperature system | `celsius()`, `fahrenheit()` and `kelvin()` |
| Repetition structures | `for` loops build the menu bar and the result rows; a `while True` loop runs the terminal menu |
| Menu stays until the user decides to leave | The page re-renders the menu after each conversion; only the **Exit** button shows the goodbye page. In the terminal, the loop stops only on option `0` |

## Files

```
marcone2b/
├── conversor.py   # the whole app (conversions, web page, terminal menu)
├── .htaccess      # tells Apache to run .py files as CGI scripts
└── README.md
```

## Requirements

- Windows with [XAMPP](https://www.apachefriends.org/) (Apache)
- Python 3.7 or newer, installed from [python.org](https://www.python.org/downloads/)

> **Warning:** the Microsoft Store version of Python (path containing `WindowsApps`) usually does not work with Apache. Use the python.org installer instead. You can choose "Install for current user only" if you don't have administrator rights.

## Installation

1. Copy the project folder to `C:\xampp\htdocs\`, for example `C:\xampp\htdocs\marcone2b\`. `conversor.py` and `.htaccess` must be directly inside that folder.
2. Make sure the hidden-style file is named exactly `.htaccess` (not `.htaccess.txt`). In Windows Explorer, turn on **View > Show > File name extensions** to check.
3. Find your Python path: open cmd and run `where python` (or `py -0p`).
4. Edit **line 1** of `conversor.py` so it points to that path. It must start with `#!` and use forward slashes:

   ```python
   #!C:/Users/YourName/AppData/Local/Programs/Python/Python313/python.exe
   ```

5. Open the XAMPP Control Panel and start **Apache**.
6. Open `http://localhost/marcone2b/` in your browser.

## Usage

**In the browser**

1. Pick the scale you are converting from (Celsius, Fahrenheit or Kelvin).
2. Type the value.
3. Click **Convert** to see the other two scales. Repeat as many times as you like.
4. Click **Exit** to close the converter. **Start again** brings the menu back.

**In the terminal**

```
cd C:\xampp\htdocs\marcone2b
python conversor.py
```

Type `1`, `2` or `3` to choose the scale, enter a value, and repeat. Type `0` to quit.

## Formulas

| From | To Celsius | To Fahrenheit | To Kelvin |
|---|---|---|---|
| Celsius (C) | | F = C × 9/5 + 32 | K = C + 273.15 |
| Fahrenheit (F) | C = (F − 32) × 5/9 | | K = (F − 32) × 5/9 + 273.15 |
| Kelvin (K) | C = K − 273.15 | F = (K − 273.15) × 9/5 + 32 | |

Lowest valid values (absolute zero): -273.15 °C, -459.67 °F, 0 K.

## Troubleshooting

If the browser shows **Internal Server Error (500)**, open the XAMPP Control Panel, click **Logs** next to Apache, open `error.log`, and read the last lines:

| Message in `error.log` | Cause and fix |
|---|---|
| `don't know how to spawn child process` or `cannot find the file specified` | Line 1 of `conversor.py` has a wrong Python path, is missing `#!`, or uses backslashes. Fix it as shown in Installation step 4. |
| `Options ExecCGI is off in this directory` | `.htaccess` is not being applied. Check its name, and make sure `httpd.conf` has `AllowOverride All` for the `htdocs` directory. Restart Apache. |
| `Options not allowed here` | Same as above: set `AllowOverride All` in `httpd.conf` and restart Apache. |
| `Premature end of script headers` | The script started but crashed. Run `python conversor.py` in cmd to see the Python error. |

After any change, restart Apache (**Stop**, then **Start**) and reload the page.
