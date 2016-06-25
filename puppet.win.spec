# -*- mode: python -*-

block_cipher = None

data_files = [('data/0_default/*', 'data/0_default'),
              ('Puppet.ico', '.')]

bin_files = [ ('msvcrt/msvcp140.dll','.'),
              ('msvcrt/vcruntime140.dll','.')]

a = Analysis(['puppet.py'],
             pathex=['C:\\Users\\Administrator\\Desktop\\Puppet\\source'],
             binaries=bin_files,
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Puppet',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='Puppet.ico',
          version='version')
