import os

sourceDir = 'sims_maps'
i18nDir = 'i18n'

langDir = os.path.join(sourceDir, i18nDir)
tsFiles = os.listdir(langDir)

baseNames = [os.path.splitext(tsFile)[0] for tsFile in tsFiles if tsFile.endswith('.ts')]

for baseName in baseNames:
    tsFilePath = os.path.join(sourceDir, i18nDir, f'{baseName}.ts')
    qmFilePath = os.path.join(sourceDir, i18nDir, f'{baseName}.qm')
    cmd = f'lrelease {tsFilePath} {qmFilePath}'
    print(cmd)
    os.system(cmd)
