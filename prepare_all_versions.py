#!/usr/bin/python3 -uBdOO

import os
import glob


packages_directory = '/home/nikow/git/df_packs_collector/'
print("Main package directory %s" % packages_directory)

print("Gathering packages...")
branches = {
    'legacy': (
        [
            name for name
            in glob.glob(packages_directory + 'df_2*.zip')
            if '_s.zip' not in name
        ] + [
            packages_directory + 'df_31_01.zip',
            packages_directory + 'df_31_02.zip',
            packages_directory + 'df_31_03.zip'
        ] +
        glob.glob(packages_directory + '*legacy.zip')
    ),
    'legacy_small': [
        name for name in
        glob.glob(packages_directory + '*_s.zip')
        if 'win' not in name
    ],
    'mac': (
        glob.glob(packages_directory + '*osx.tar.bz2') +
        glob.glob(packages_directory + '*m.zip')
    ),
    'windows': glob.glob(packages_directory + '*win.zip'),
    'windows_small': glob.glob(packages_directory + '*win_s.zip'),
    'linux': glob.glob(packages_directory + '*linux.tar.bz2')
}

print("Sorting and counting packages...")
package_counter = 0
for x in branches.keys():
    print("Sorting packages for branch %s..." % x)
    branches[x] = list(
        set(branches[x])  # make sure it's unique
    )
    branches[x].sort()
    package_counter += len(branches[x])

print("Found %d packages." % package_counter)

for branch_name in sorted(branches.keys()):
    print('')
    print("Returning to branch master...")
    os.system("git checkout master")
    print("Creating branch %s..." % branch_name)
    os.system("git checkout -b %s" % branch_name)

    for package_path in branches[branch_name]:
        print("Package path: %s" % package_path)
        package_filename = package_path.split('/')[-1]
        print("Package filename: %s" % package_filename)
        package_name = package_filename.split('.')[0]
        print("Package name: %s" % package_name)
        package_format = package_filename.split('.')[-1]
        print("Package format: %s" % package_format)
        tag_name = package_name[3:]
        print("Package tag: %s" % tag_name)

        print("Cleaning repo...")
        # os.system("git rm -rf *")
        os.system("rm -rfv *")

        print("Decompressing package...")
        if package_format == "zip":
            os.system("7z x %s" % package_path)
        elif package_format == "bz2":
            os.system("tar xvf %s" % package_path)
        else:
            raise Exception(
                "!!!Unknow format found: %s !!!"
                % package_path
            )

        print("Preparing commit...")
        os.system("git add .")

        print("Commiting...")
        os.system("git commit -am \"%s\"" % package_name)

        print("Taging...")
        os.system("git tag %s" % tag_name)



