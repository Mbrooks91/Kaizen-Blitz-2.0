# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None

# Collect all PyQt6 data and binaries
pyqt6_datas = collect_data_files('PyQt6')
pyqt6_binaries = collect_dynamic_libs('PyQt6')
pyqt6_hiddenimports = collect_submodules('PyQt6')

# Collect other package data  
reportlab_datas = collect_data_files('reportlab')
docx_datas = collect_data_files('docx')

# Add Windows platform plugins explicitly
added_files = [
    ('src', 'src'),
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=pyqt6_binaries,
    datas=added_files + pyqt6_datas + reportlab_datas + docx_datas,
    hiddenimports=[
        'pkgutil',
        'pkg_resources',
        'PyQt6.sip',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'sqlalchemy.sql.default_comparator',
        'win32timezone',
    ] + pyqt6_hiddenimports,
    hookspath=[],
    hooksconfig={
        'PyQt6': {
            'plugins': ['platforms', 'styles']
        }
    },
    runtime_hooks=[],
    excludes=['matplotlib', 'seaborn', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries
seen = set()
unique_binaries = []
for item in a.binaries:
    if item[0] not in seen:
        seen.add(item[0])
        unique_binaries.append(item)
a.binaries = unique_binaries

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='KaizenBlitz',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version=None,
    uac_admin=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='KaizenBlitz',
)
