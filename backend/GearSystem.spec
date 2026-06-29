# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

backend_dir = Path.cwd()
frontend_dist = backend_dir / 'frontend_dist'

# 注意：数据文件现在会在运行时动态创建，不需要打包
datas = []
if frontend_dist.exists():
    datas.append((str(frontend_dist), 'frontend_dist'))

hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'starlette',
    'scipy',
    'numpy',
    'pydantic',
    'pydantic_settings',
    'app',
    'app.api',
    'app.schemas',
    'app.services',
    'app.data',
]

excludes = [
    'tkinter',
    'matplotlib',
    'pandas',
    'IPython',
    'jupyter',
    'notebook',
    'pytest',
    'unittest',
]

a = Analysis(
    ['desktop_app.py'],
    pathex=[str(backend_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
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
    name='GearSystem',
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
)
