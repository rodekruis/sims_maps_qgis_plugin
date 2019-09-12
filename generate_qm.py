import os
import subprocess

sourceDir = 'sims_maps'
i18nDir = 'i18n'

langDir = os.path.join(sourceDir, i18nDir)
tsFiles = os.listdir(langDir)

baseNames = [os.path.splitext(tsFile)[0] for tsFile in tsFiles if tsFile.endswith('.ts')]

for baseName in baseNames:
    tsFile = '{}.ts'.format(baseName)
    qmFile = '{}.qm'.format(baseName)
    cmd = 'lrelease {} {}'.format(
        os.path.join(sourceDir, i18nDir, tsFile),
        os.path.join(sourceDir, i18nDir, qmFile)
    )
    print(cmd)
    os.system(cmd)
