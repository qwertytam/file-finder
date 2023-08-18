import csv
import hashlib
import os
import re
import sys


def find_duplicates(parent_folder):
    # Dups in format {hash:[names]}
    # skip_paths = r'\\\.|01\sIn\sAmazon\sDri|Dropbox\\[A-B]|Courses\\Coursera|Dropbox\\Financials\\Tax'
    skip_paths = r'asdfghjklzxcvbn'
    dups = {}
    for dir_name, subdirs, file_list in os.walk(parent_folder):
        if not re.search(skip_paths, dir_name):
            print(f'Scanning {dir_name}...')
            for filename in file_list:
                # Get the path to the file
                # file_with_ext = r'\.7z|\.ini'
                file_with_ext = r'\.ini'
                if not filename.startswith('.') \
                        and not re.search(file_with_ext, filename):
                    path = os.path.join(dir_name, filename)
                    # Calculate hash
                    file_hash = hashfile(path)
                    # Add or append the file path
                    if file_hash in dups:
                        dups[file_hash].append(path)
                    else:
                        dups[file_hash] = [path]
                else:
                    print(f'Ignoring file {filename}')
        else:
            print(f'Skipping {dir_name}...')
    return dups


# Joins two dictionaries
def join_dicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize=(2**16)):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def print_results(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. ' +
              'The name could differ, but the content is identical')
        print('___________________')
        for result in results:
            for subresult in result:
                print(f'\t\t{subresult}')
            print('___________________')

    else:
        print('No duplicate files found.')


def save_results(dict1, csv_path):
    out_csv = os.path.join(csv_path, os.sep, 'dups.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        writer.writerows(results)

    print(f'Saved {out_csv}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                join_dicts(dups, find_duplicates(i))
            else:
                print(f'{i} is not a valid path, please verify')
                sys.exit()
        print_results(dups)
        save_results(dups, folders[0])
    else:
        print('Usage: python dupFinder.py folder or python dupFinder.py ' +
              'folder1 folder2 folder3')
