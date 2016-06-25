# -*- mode: python -*-

block_cipher = None

datafiles = [
    ('data/0_default/*', 'data/0_default'),
    #('Puppet.icns', '.')
    ]

a = Analysis(['puppet.py'],
             pathex=['/Users/sakanomotonori/Scripts/mascot'],
             binaries=None,
             datas=datafiles,
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
          exclude_binaries=True,
          name='Puppet',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='puppet')
app = BUNDLE(coll,
             name='Puppet.app',
             icon='Puppet.icns',
             bundle_identifier=None,
             info_plist={
                'CFBundleShortVersionString': '1.0.0'
             })
