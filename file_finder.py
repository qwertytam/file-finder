import argparse
import csv
import os
from time import time


def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry


def allfiles_to_csv(start_path, out_csv):
    """Print all files and associated paths in all subdirs to given csv file"""
    headers = ['Name', 'Path', 'Size']
    file_paths = []
    for entry in scantree(start_path):
        if not entry.name.startswith('.') and entry.is_file():
            file_paths.append([entry.name, entry.path, entry.stat().st_size])

    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        write = csv.writer(f)
        write.writerow(headers)

        for file in file_paths:
            try:
                write.writerow(file)
            except UnicodeEncodeError as e:
                print(f'\nError for file: {file} \nwith error: {e}\n')
    print(f'Saved {out_csv}')
    return file_paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--path', help='Start path')
    parser.add_argument('--csv', help='Output csv file path and name')
    args = parser.parse_args()

    start_path = args.path
    if not os.path.exists(start_path):
        print(f'ERROR {start_path} not found!')
        exit()

    if args.csv is None:
        print('ERROR: csv file path and name not given!')
        exit()
    else:
        out_csv = args.csv

    tic = time()

    file_paths = allfiles_to_csv(start_path, out_csv)

    print(f'Found {len(file_paths)} files in {time()-tic} seconds')
