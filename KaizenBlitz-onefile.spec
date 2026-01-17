# -*- mode: python ; coding: utf-8 -*-
# Single-file .exe build configuration for Windows 11
import os
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files, collect_submodules

block_cipher = None

# Collect PyQt6 dependencies
pyqt6_binaries = collect_dynamic_libs('PyQt6')
pyqt6_datas = collect_data_files('PyQt6')
pyqt6_hiddenimports = collect_submodules('PyQt6')

# Collect document generation libraries
reportlab_datas = collect_data_files('reportlab')
docx_datas = collect_data_files('docx')

src_path = os.path.abspath('src')

a = Analysis(
    ['run.py'],
    pathex=[src_path],
    binaries=pyqt6_binaries,
    datas=[
        ('src', 'src'),
    ] + pyqt6_datas + reportlab_datas + docx_datas,
    hiddenimports=[
        'pkgutil',
        'pkg_resources',
        'win32timezone',
        'win32api',
        'pywintypes',
        'sqlalchemy.sql.default_comparator',
    ] + pyqt6_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'seaborn', 'tkinter', 'numpy', 'pandas', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KaizenBlitz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    uac_admin=False,
)
