# How `mastrade_morning_report.exe` was built

Short answer: **it's a Python script frozen into a single Windows executable with
[PyInstaller](https://pyinstaller.org/).** There is no compiled C, no C#, no Go. The `.exe`
is a small launcher stub with a whole CPython 3.13 interpreter, the standard library,
and the third-party packages stapled onto the end of it.

That's why it's 17.5 MB for what is, underneath, ~430 lines of Python.

This directory contains the recovered source, a reproducible build, and an offline test rig.

---

## 1. What the binary actually is

Running `file` on it gives the first clue:

```
PE32+ executable (console) x86-64, for MS Windows, 7 sections
```

`console`, not `windowed` — it prints to a terminal and expects command-line flags.
Strings inside it confirm the packer:

```
PyInstaller's PKG archive ...  _MEIPASS  ...  python313.dll  ...  PYZ.pyz
```

`_MEIPASS` is the giveaway. A PyInstaller one-file exe, at startup, unpacks its payload
into a temp directory, points `sys._MEIPASS` at it, and runs the bundled interpreter.

### Anatomy

A one-file PyInstaller exe is four things concatenated:

| Part | What it is |
|---|---|
| Bootloader | A native C stub — the only genuinely compiled part. Unpacks and launches. |
| `PYZ.pyz` | A zlib archive of every pure-Python module (508 of them here). |
| Binary deps | `python313.dll`, `libssl-3.dll`, `libcrypto-3.dll`, `_ssl.pyd`, `lxml`, … |
| TOC + cookie | A table of contents and a magic footer (`MEI\014\013\012\013\016`) so the stub can find everything. |

### What was bundled

| Package | Why it's there |
|---|---|
| `requests`, `urllib3`, `certifi`, `idna`, `charset_normalizer` | HTTP client — imported directly |
| `python-docx` (`docx`) + `lxml` | Word output — imported directly |
| `cryptography`, `socks` | Dragged in by urllib3's optional TLS/SOCKS backends |
| `bs4`, `soupsieve` | **Not imported by the script at all** — they just happened to be installed in the build venv |

That last row is worth internalising: PyInstaller bundles what it *finds*, and a messy
virtualenv silently inflates your binary. Build from a clean venv with only what you import.

### What it does

A Vietnamese-language morning market report generator. It hits the MAStrade API
(`https://mastrade.masvn.com`), pulls VN-INDEX data, and writes a formatted `.docx`:

1. `/api/v1/market/{symbol}/quote` — index level, change, volume, traded value
2. `/api/v2/vs/detailIndex` — P/E, P/B, market cap, foreign buy/sell totals
3. `/api/v2/vs/stockInfluence` — top 5 stocks pushing the index up and down
4. `/api/v2/vs/foreignHistory` — net foreign flow
5. `/api/v1/market/top` — top foreign net buy/sell names

Then it writes each run to `data/snapshots/*.json`, and on the next run compares against
the most recent snapshot *from a previous day* to produce the "DoD" percentages.
That's the whole persistence layer — no database.

One quirk worth noting: those endpoints take a `?query=` parameter holding a
GraphQL-ish string that the script builds by hand with `json.dumps` per argument:

```python
def build_mastrade_query(name, query, fields):
    args = ",".join(f"{key}:{json.dumps(value, ensure_ascii=False)}" for key, value in query.items())
    return f"query{{{name}({args}){{{','.join(fields)}}}}}"
    # -> query{vsDetailIndex(fetchCount:1,symbol:"VN-INDEX"){PE,PB}}
```

---

## 2. Build it yourself

### Layout

```
mastrade-morning-report/
├── src/mastrade_morning_report.py   # the program
├── requirements.txt
├── mastrade_morning_report.spec     # PyInstaller build recipe
├── build.ps1                        # Windows build
├── build.sh                         # Linux/macOS build
└── tools/mock_mastrade_server.py    # offline API stub for testing
```

### Run it as a plain script first

Always get this working before you freeze anything — debugging a frozen binary is
much worse than debugging a script.

```bash
python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python src/mastrade_morning_report.py --help
```

### Freeze it

```powershell
# Windows -> mastrade_morning_report.exe
powershell -ExecutionPolicy Bypass -File build.ps1
```

```bash
# Linux/macOS -> a native binary for THAT platform (see the cross-compile note below)
./build.sh
```

Both drive the same one-liner:

```
pyinstaller mastrade_morning_report.spec --clean --noconfirm
```

Without a spec file you'd write it as flags — this is the minimal form:

```
pyinstaller --onefile --console src/mastrade_morning_report.py
```

`--onefile` is what produces a single self-contained exe instead of a `dist/` folder full
of DLLs. The spec file is just that command frozen into a file so it stays reproducible;
generate one from flags with `pyi-makespec`, then edit it.

### Test without hitting the live API

```bash
python tools/mock_mastrade_server.py 8765 &
./dist/mastrade_morning_report --base-url http://127.0.0.1:8765 --output out.docx
```

The mock encodes the response shape of every endpoint, so it also serves as a written
record of the API contract.

---

## 3. Things that will bite you

**PyInstaller cannot cross-compile.** Building on Linux gives you a Linux ELF binary,
full stop. There is no `--target-platform`. To produce a `.exe` you need Windows — a VM,
a Windows box, or a CI runner. `.github/workflows/build-windows-exe.yml` in this repo does
the last one: it builds on `windows-latest` and uploads the exe as an artifact, which is
usually the least painful option if you don't run Windows day to day.

**Antivirus false positives.** The PyInstaller bootloader pattern — a stub that unpacks
an encrypted-looking blob and executes it — is exactly what packed malware looks like.
Expect SmartScreen warnings and occasional AV quarantines. Mitigations, in order of
effectiveness: code-sign the binary with a real certificate; prefer `--onedir` over
`--onefile`; avoid UPX compression (`upx=False`, as set in the spec here).

**Size.** 17.5 MB is mostly interpreter and DLLs, and you can't get rid of those. What you
*can* control is dependency creep — this spec's `excludes` list drops `bs4`, `soupsieve`,
`tkinter`, and `unittest`. Building from a clean venv matters more than any flag.

**Relative paths.** The script writes to `output/` and `data/snapshots/` relative to the
*current working directory*, not the exe's location. Double-clicking from Explorer can put
files somewhere surprising. If you want paths relative to the binary, use
`sys._MEIPASS` for bundled read-only data and `Path(sys.executable).parent` for output.

**Fonts.** The document asks for `Noto Sans`. Word substitutes silently if it's missing,
which can mangle Vietnamese diacritics on a machine that doesn't have it installed.
Fonts are a property of the machine opening the `.docx`, not something the exe bundles.

**Startup latency.** One-file builds unpack to a temp dir on every launch — expect a
1–3 second delay before anything happens. `--onedir` starts much faster and is the better
choice for anything interactive.

---

## 4. Inspecting a PyInstaller exe

The same technique that recovered this source works on any PyInstaller binary — useful
when you've lost the source to something you shipped.

1. **Confirm the packer.** `strings the.exe | grep -i "MEIPASS\|pyinstaller\|python3"` — the
   `python3XX.dll` name also tells you the exact Python version, which you'll need next.
2. **Extract the archive.** Find the `MEI\014\013\012\013\016` cookie near EOF, read the
   TOC, zlib-decompress each entry. [`pyinstxtractor`](https://github.com/extremecoders-re/pyinstxtractor)
   automates this.
3. **Recover the source.** Entries typed `s` are entry-point scripts, stored as marshalled
   code objects. With a matching Python (3.13 here), `marshal.loads()` then `dis.dis()`
   gives you full bytecode. [Decompyle++](https://github.com/zrax/pycdc) can often go
   straight to source, though its 3.13 support is incomplete — the source in `src/` was
   reconstructed from the disassembly instead.

Note what this implies about shipping Python as an exe: **it is packaging, not protection.**
Anything embedded in the binary — API keys, tokens, endpoints — is trivially recoverable.
The source in this directory compiles to bytecode byte-identical to the shipped exe, line
numbers included, which is a fair demonstration of how little is actually hidden.

---

## 5. Alternatives to PyInstaller

| Tool | Trade-off |
|---|---|
| **PyInstaller** | Most widely used, best docs. What was used here. |
| **Nuitka** | Compiles to real C. Faster, harder to reverse, notably slower builds. |
| **cx_Freeze** | Simpler, but no true one-file mode on Windows. |
| **Briefcase** | Proper installers (MSI/DMG) rather than a bare exe. Best for GUI apps. |
| **`uv` / pipx** | If your users have Python, don't freeze at all — ship a wheel. Vastly less pain. |

For an internal tool run by a handful of colleagues on Windows without Python,
PyInstaller `--onefile` is the right call, and it's what the original author picked.
