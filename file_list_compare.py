import argparse
import os
import pandas as pd


def compare_lists(main, sec, out_csv):
    names = ['name', 'full_path', 'size_b']
    df_main = pd.read_csv(main, header=0, names=names)
    df_sec = pd.read_csv(sec, header=0, names=names)

    df_main['name_size'] = df_main.name.str.cat(
        df_main.size_b.astype(str), sep='_')

    df_sec['name_size'] = df_sec.name.str.cat(
        df_sec.size_b.astype(str), sep='_')

    df_result = df_main.assign(
        name_size_same=df_main.name_size.isin(df_sec.name_size))

    df_result[df_result['name_size_same']].to_csv(out_csv, index=False)
    print(f'Saved {out_csv}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--main', help='Main list')

    help = 'Secondary list; see if items from main are in this list'
    parser.add_argument('--sec', help=help)

    parser.add_argument('--out', help='csv file to save result to')

    args = parser.parse_args()

    main = args.main
    if not os.path.exists(main):
        print(f'ERROR {main} not found!')
        exit()

    sec = args.sec
    if not os.path.exists(sec):
        print(f'ERROR {sec} not found!')
        exit()

    if args.out is None:
        print('ERROR: csv out file path and name not given!')
        exit()
    else:
        out_csv = args.out

    compare_lists(main, sec, out_csv)
