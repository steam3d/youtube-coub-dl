# -*- mode: python -*-

block_cipher = None


a = Analysis(['easydownloader.py'],
             pathex=['D:\\EasyDownloader'],
             binaries=[],
             datas=[ ('wffmpeg/','wffmpeg'),
              ('wintray.png','.'),
              ('wintraydl.png','.'),
              ('wintray.ico','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          icon = 'app.ico',
          exclude_binaries=True,
          name='easydownloader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='easydownloader')
