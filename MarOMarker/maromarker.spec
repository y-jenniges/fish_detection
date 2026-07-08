# PyInstaller spec for MarOMarker. Build with:
#   pyinstaller maromarker.spec
#
# PyInstaller cannot cross compile, so run this on each target OS:
# Windows produces a .exe, macOS a .app bundle, Linux an executable folder.
import os
import sys
from PyInstaller.utils.hooks import collect_all

# MSVC runtime DLLs. The versions PyInstaller collects from the wheels are
# older than what TensorFlow needs, and mixing versions gives a "DLL
# initialization routine failed" error at startup. Force the current system
# copies instead.
MSVC_DLLS = ("msvcp140.dll", "msvcp140_1.dll", "msvcp140_2.dll",
             "vcruntime140.dll", "vcruntime140_1.dll", "concrt140.dll")

block_cipher = None

# collect data files, binaries and hidden imports of the heavy dependencies
# that PyInstaller does not fully pick up on its own
datas = [("src/maromarker/config.json", "maromarker")]
binaries = []
hiddenimports = []
for package in ("tensorflow", "cv2", "skimage", "scipy", "sklearn"):
    try:
        pkg_datas, pkg_binaries, pkg_hidden = collect_all(package)
        datas += pkg_datas
        binaries += pkg_binaries
        hiddenimports += pkg_hidden
    except Exception:
        pass

icon = "src/maromarker/logos/fish.ico" if sys.platform == "win32" else None

a = Analysis(
    ["src/maromarker/__main__.py"],
    pathex=["src"],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "sphinx"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# on Windows, replace any collected MSVC runtime DLLs with the current system
# ones so TensorFlow's native libraries load against a consistent runtime
if sys.platform == "win32":
    system32 = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"),
                            "System32")
    a.binaries = [b for b in a.binaries
                  if os.path.basename(b[0]).lower() not in MSVC_DLLS]
    for dll in MSVC_DLLS:
        src = os.path.join(system32, dll)
        if os.path.exists(src):
            a.binaries.append((dll, src, "BINARY"))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MarOMarker",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="MarOMarker",
)
