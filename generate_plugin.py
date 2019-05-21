import os
import argparse
import shutil
import csv

def findNsInfo(filename):
    nsName = None
    nsCountry = None
    nsCode = None

    with open(os.path.join(nsDir, filename), encoding='utf-8', mode='r') as mdFile:
        for line in mdFile:
            line = line.strip()
            #print(line)
            if len(line) > 0 and line[0] == '#':
                nsName = line.replace('#', '').strip()
                break
                #print(nsName)

    with open(os.path.join(nsDir, filename), encoding='utf-8', mode='r') as mdFile:
        for line in mdFile:
            line = line.strip()
            #print(line)
            if ' - ' in line:
                nsName = line.replace('#', '').strip()
                parts = line.split(' - ')
                #print(parts)
                nsCountry = parts[0].strip()
                nsCode = parts[1].strip()
                #print(nsName, nsCountry, nsCode)
                break

    return (nsName, nsCountry, nsCode)


parser = argparse.ArgumentParser(description='Create plugin directory including dependency files from other repos.')
parser.add_argument('-d', default='sims_maps_generated', help='destination directory')

args = parser.parse_args()
print(args)

repoDir = os.path.dirname(os.path.abspath(__file__))
srcDir = os.path.join(repoDir, 'sims_maps')
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
fileTypes = ['.py', '.ui', '.svg']
for file in files:
    fn, ext = os.path.splitext(file)
    if ext in fileTypes:
        print(file)
        shutil.copy2(os.path.join(srcDir, file), destDir)

# copy metadata TODO: auto update version
shutil.copy2(os.path.join(srcDir, 'metadata.txt'), destDir)

# copy data dir
destDataDir = os.path.join(destDir, 'data')
shutil.copytree(os.path.join(srcDir, 'data'), destDataDir)

# copy logos from local clone of git@github.com:IFRCGo/logos.git
#print('- logos -')
logosSrcDir = os.path.join(gitDir, 'logos')
print(logosSrcDir)
logosDestDir = os.path.join(destDataDir, 'logos')
os.makedirs(logosDestDir)

csvFileName = os.path.join(logosDestDir, 'logos.csv')
csvFile = open(csvFileName, encoding='utf-8', mode='w', newline='')
csvWriter = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC, quotechar='"')

csvWriter.writerow(['code', 'country', 'society', 'logo'])

nsLogosSrcDir = os.path.join(logosSrcDir, 'national-societies')
for file in os.listdir(nsLogosSrcDir):
    if os.path.isdir(os.path.join(nsLogosSrcDir, file)):
        #print(file)
        # find svg
        nsSvgFiles = []
        nsDir = os.path.join(nsLogosSrcDir, file)
        for filename in os.listdir(nsDir):
            fn, ext = os.path.splitext(filename)
            if ext.lower() == '.svg':
                #print('  ::  ', filename)
                nsSvgFiles.append(filename)
            #if ext.lower() == '.eps':
            #    pass
            if filename == 'README.md':
                (nsName, nsCountry, nsCode) = findNsInfo(filename)


        if  nsName is not None and \
            nsCountry is not None and \
            nsCode is not None:
            for nsSvgFile in nsSvgFiles:
                srcFile = os.path.join(nsDir, nsSvgFile)
                #print(srcFile)
                shutil.copy2(srcFile, logosDestDir)
                csvWriter.writerow([nsCode, nsCountry, nsName, nsSvgFile])
csvFile.close()

# copy icons from local clone of git@github.com:IFRC-Icons.git

# OCHA 2012
iconsSrcDir = os.path.join(gitDir, 'IFRC-Icons', 'OCHA_Icons', 'qgis_versions', 'svg')
iconsDestDir = os.path.join(destDataDir, 'SIMS-Icons', 'OCHA_2012')
os.makedirs(iconsDestDir)

files = os.listdir(iconsSrcDir)
fileTypes = ['.svg']
for file in files:
    fn, ext = os.path.splitext(file)
    if ext in fileTypes:
        shutil.copy2(os.path.join(iconsSrcDir, file), iconsDestDir)

# OCHA 2018
iconsSrcDir = os.path.join(gitDir, 'IFRC-Icons', 'OCHA_Icons_2018', 'qgis_versions', 'svg')
iconsDestDir = os.path.join(destDataDir, 'SIMS-Icons', 'OCHA_2018')
os.makedirs(iconsDestDir)

files = os.listdir(iconsSrcDir)
fileTypes = ['.svg']
for file in files:
    fn, ext = os.path.splitext(file)
    if ext in fileTypes:
        shutil.copy2(os.path.join(iconsSrcDir, file), iconsDestDir)
