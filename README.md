# Playwright + Python – Installation and Running Tests

A step-by-step guide: from setting up your environment (macOS + Homebrew) to running tests and generating a report.

## Prerequisites

- macOS
- Terminal

## 1. Install Homebrew

If you don't have Homebrew yet, install it:

```bash
xcode-select --install
```

Then run the official install script:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, if you're on Apple Silicon (M1/M2/M3/M4), add Homebrew to your PATH (the install script will print the exact commands to run, typically):

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify it works:

```bash
brew --version
```

## 2. Install Python

Recommended version: **Python 3.12** (fully compatible with both Playwright and PyTorch).

```bash
brew install python@3.12
python3.12 --version
```

> Python 3.13 is also fully supported if you prefer the latest version.

## 3. Create a Virtual Environment

```bash
python3.12 -m venv .venv
source venv/bin/activate
```

Inside the activated environment, `python` and `python3` will always point to Python 3.12, regardless of your global PATH.

## 4. Install Playwright

```bash
pip install pytest-playwright
playwright install
```

By default, this downloads three browsers (Chromium, Firefox, WebKit) — roughly 300–400 MB total. To install just one, e.g. Chromium:

```bash
playwright install chromium
```

## 5. Running Tests

Basic run:

```bash
pytest
```

With a visible browser window (headed mode):

```bash
pytest --headed
```

With verbose output (shows each test's name and status instead of just dots):

```bash
pytest -v
```

### Running a Specific Test File

To run only the tests in one file:

```bash
pytest <test_file>.py
```

For example: `pytest test_login.py`

## 6. Test Reports

### HTML Report

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

- `--html=report.html` – generates an HTML report with the given filename
- `--self-contained-html` – bundles styles and assets into a single file, making the report easy to share and open on any machine

Open `report.html` in a browser to see results, durations, and any failures.

### Trace Viewer (step-by-step playback)

```bash
pytest --tracing on
```

Trace files are saved under the `test-results/` folder. Open the viewer with:

```bash
playwright show-trace test-results/test-name/trace.zip
```

Trace Viewer shows an interactive timeline with screenshots, the DOM, network activity, and console logs — very useful for debugging.