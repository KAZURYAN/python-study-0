# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['kadai1.py'],
             pathex=['/Users/kazunori1986/project/pythonpractice/study_five'],
             binaries=[],
             datas=[('/Users/kazunori1986/.pyenv/versions/3.8.1/lib/python3.8/site-packages/eel/eel.js', 'eel'), ('web', 'web')],
             hiddenimports=['bottle_websocket'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('item_master.csv','./csv/item_master.csv', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='kadai1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='kadai1.app',
             icon=None,
             bundle_identifier=None)
