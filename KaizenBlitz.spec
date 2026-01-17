# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# Collect all PyQt6 data and binaries
pyqt6_datas = collect_data_files('PyQt6')
pyqt6_binaries = collect_dynamic_libs('PyQt6')
pyqt6_hiddenimports = collect_submodules('PyQt6')

# Collect other package data
reportlab_datas = collect_data_files('reportlab')
docx_datas = collect_data_files('docx')

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=pyqt6_binaries,
    datas=[
        ('src', 'src'),
    ] + pyqt6_datas + reportlab_datas + docx_datas,
    hiddenimports=[
        'pkgutil',
        'pkg_resources',
        'PyQt6.sip',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'sqlalchemy.sql.default_comparator',
    ] + pyqt6_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KaizenBlitz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
