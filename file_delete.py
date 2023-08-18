import argparse
import os
import pandas as pd
from win32com.shell import shell, shellcon


def deltorecyclebin(filename):
    """Delete files to Windows recycle bin"""
    num_del = 0
    if not os.path.exists(filename):
        print(f'Did not find {filename}')
        return num_del

    res = shell.SHFileOperation(
        (0,
         shellcon.FO_DELETE,
         filename,
         None,
         shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO |
         shellcon.FOF_NOCONFIRMATION,
         None,
         None)
    )

    if not res[1] and os.path.exists(filename):
        print(f'Trying alternate delete for {filename}')
        os.system('del '+filename)

    num_del += 1
    return num_del


def del_files(file_list):
    num_del = 0
    df_list = pd.read_csv(file_list)

    for file_path in df_list['full_path']:
        num_del += deltorecyclebin(file_path)

    print(f'Deleted {num_del} files')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--list', help='List to delete')
    args = parser.parse_args()

    file_list = args.list
    if not os.path.exists(file_list):
        print(f'ERROR {file_list} not found!')
        exit()

    del_files(file_list)
