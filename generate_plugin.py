import os
import argparse
import shutil
import csv

parser = argparse.ArgumentParser(description=u'Create plugin directory including dependency files from other repos.')
parser.add_argument(u'-d', default=u'sims_maps_generated', help=u'destination directory')

args = parser.parse_args()
print(args)

repoDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.join(repoDir, u'sims_maps')
destDir = os.path.join(repoDir, args.d)
gitDir = os.path.dirname(repoDir)

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
destDataDir = os.path.join(destDir, u'data')
shutil.copytree(os.path.join(srcDir, u'data'), destDataDir)

# copy logos from local clone of git@github.com:IFRCGo/logos.git
#print('- logos -')
logosSrcDir = os.path.join(gitDir, u'logos')
#print(logosSrcDir)
logosDestDir = os.path.join(destDataDir, 'logos')
os.makedirs(logosDestDir)

csvFileName = os.path.join(logosDestDir, u'logos.csv')
csvFile = open(csvFileName, encoding=u'utf-8', mode=u'w', newline=u'')
csvWriter = csv.writer(csvFile, delimiter=u';', quoting=csv.QUOTE_NONNUMERIC, quotechar=u'"')

csvWriter.writerow([u'code', u'country', u'society', u'logo'])

nsLogosSrcDir = os.path.join(logosSrcDir, u'national-societies')
for file in os.listdir(nsLogosSrcDir):
    if os.path.isdir(os.path.join(nsLogosSrcDir, file)):
        #print(file)
        # find svg
        nsSvgFiles = []
        nsName = None
        nsCountry = None
        nsCode = None
        nsDir = os.path.join(nsLogosSrcDir, file)
        for filename in os.listdir(nsDir):
            fn, ext = os.path.splitext(filename)
            if ext.lower() == u'.svg':
                #print('  ::  ', filename)
                nsSvgFiles.append(filename)
            #if ext.lower() == u'.eps':
            #    pass
            if filename == u'README.md':
                mdFile = open(os.path.join(nsDir, filename), encoding=u'utf-8', mode=u'r')
                line = mdFile.readline().strip()
                #print(line)
                nsName = line.replace(u'#', u'').strip()
                #print(nsName)

                line = mdFile.readline().strip()
                mdFile.close()
                #print(line)
                parts = line.split(' - ')
                #print(parts)
                nsCountry = parts[0]
                try:
                    nsCode = parts[1]
                    #print(nsName, nsCountry, nsCode)
                except Exception:
                    pass
                    print(u'Error in parsing README.md for {0}'.format(nsCountry))
        if  nsName is not None and \
            nsCountry is not None and \
            nsCode is not None:
            for nsSvgFile in nsSvgFiles:
                srcFile = os.path.join(nsDir, nsSvgFile)
                #print(srcFile)
                shutil.copy2(srcFile, logosDestDir)
                csvWriter.writerow([nsCode, nsCountry, nsName, nsSvgFile])
csvFile.close()
