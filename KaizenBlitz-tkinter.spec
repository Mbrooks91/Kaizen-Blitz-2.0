# -*- mode: python ; coding: utf-8 -*-
# Single-file .exe build configuration for Windows 11 with tkinter

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect document generation libraries
reportlab_datas = collect_data_files('reportlab')
docx_datas = collect_data_files('docx')
ttkbootstrap_datas = collect_data_files('ttkbootstrap')

src_path = os.path.abspath('src')

a = Analysis(
    ['src/kaizen_blitz/main_tk.py'],
    pathex=[src_path],
    binaries=[],
    datas=[
        ('src', 'src'),
    ] + reportlab_datas + docx_datas + ttkbootstrap_datas,
    hiddenimports=[
        'pkg_resources',
        'sqlalchemy.sql.default_comparator',
        'ttkbootstrap',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'seaborn', 'numpy', 'pandas', 'scipy', 'PyQt6', 'PyQt5'],
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
