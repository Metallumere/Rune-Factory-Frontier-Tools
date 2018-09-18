#!/usr/bin/env python3

import argparse
import os

if not __debug__:
    from src.bin_dat import extract
else:
    from bin_dat import extract


def __main__():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--bin', dest='bin_file', required=True, nargs=1, type=str)
    arg_parser.add_argument('--dat', dest='dat_file', required=True, nargs=1, type=str)
    arg_parser.add_argument('--output', dest='output_dir', required=True, nargs=1, type=str)
    arg_parser.add_argument('--should_not_map', dest='should_not_map', required=False, action='store_true')
    args = arg_parser.parse_args()

    bin_file = args.bin_file[0]
    dat_file = args.dat_file[0]
    output_dir = args.output_dir[0]
    should_not_map = args.should_not_map

    if not os.path.isfile(bin_file):
        print('Bin file does not exist!')
        return

    if not os.path.isfile(dat_file):
        print('Dat file does not exist!')
        return

    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        print('Specified output directory is not a directory!')
        return
    elif not os.path.exists(output_dir):
        print('Output directory \"{0}\" does not exist... creating...'.format(output_dir))
        os.mkdir(output_dir, 0o775)

    print('Parsing bin file...')
    parsed_bin_file = extract.parse_bin_file(bin_file)
    print('Found {0} entries from bin file'.format(parsed_bin_file.entries))
    print()  # Pretty

    mapped_bin_file = extract.parse_headers(should_not_map, parsed_bin_file)
    print()  # Pretty
    print()  # Pretty

    if mapped_bin_file is None:
        print('Failed to parse bin and dat files!')
        return

    print('Extracting from dat file...')
    print()  # Pretty
    extract.extract_dat_file(mapped_bin_file, dat_file, output_dir)
    return


if __name__ is '__main__':
    __main__()
