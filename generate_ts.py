import os
import subprocess

languages = ['nl']
sourceFiles = ['__init__.py', 'create_layout_dialog.ui', 'edit_layout_dialog.ui']

sourceDir = 'sims_maps'
i18nDir = 'i18n'

pathSourceFiles = [os.path.join(sourceDir, srcF) for srcF in sourceFiles]
sourceString = ' '.join(pathSourceFiles)
#print(sourceString)

for language in languages:
    destFile = os.path.join(sourceDir, i18nDir, 'sims_maps_{}.ts'.format(language))
    cmd = 'pylupdate5 -noobsolete {} -ts {}'.format(sourceString, destFile)
    print(cmd)
    os.system(cmd)
