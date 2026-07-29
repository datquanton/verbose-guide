# PyInstaller spec — build with:  pyinstaller mastrade_morning_report.spec --clean --noconfirm
#
# This reproduces the same shape as the shipped mastrade_morning_report.exe:
# a single-file, console-mode Windows binary with a bundled CPython interpreter.

a = Analysis(
    ["src/mastrade_morning_report.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    # The shipped exe carried beautifulsoup4/soupsieve/cryptography it never imports,
    # because they happened to be installed in the build venv. Excluding the ones we
    # can safely drop keeps the binary smaller.
    excludes=[
        "bs4",
        "soupsieve",
        "tkinter",
        "unittest",
        "pydoc_data",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="mastrade_morning_report",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=True,          # console app — matches the original (PE32+ console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon="assets/app.ico",       # optional
    # version="version_info.txt",  # optional Windows version resource
)
