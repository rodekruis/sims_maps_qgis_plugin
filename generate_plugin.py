import os
import argparse
import shutil

# defaults
outputDir = 'sims_maps_generated'

parser = argparse.ArgumentParser(description=u'Create plugin directory including dependency files from other repos.')
parser.add_argument(u'-d', default=outputDir, help=u'destination directory')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args)

repoDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.join(repoDir, u'sims_maps')
destDir = os.path.join(repoDir, args.d)

print(srcDir)
print(destDir)

# delete existing directory
shutil.rmtree(destDir, ignore_errors=True)

# create directory
os.makedirs(destDir)

# cp py, ui and svg root files
files = os.listdir(srcDir)
fileTypes = [u'.py', u'.ui', u'.svg']
for file in files:
    fn, ext = os.path.splitext(file)
    if ext in fileTypes:
        print(file)
        shutil.copy2(os.path.join(srcDir, file), destDir)

# copy metadata TODO: auto update version
shutil.copy2(os.path.join(srcDir, u'metadata.txt'), destDir)

# copy data dir
shutil.copytree(os.path.join(srcDir, u'data'), os.path.join(destDir, u'data'))
