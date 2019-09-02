#!/usr/bin/python3
import sys
import pandas as pd

def main(input_file, output_file):
    f = pd.read_csv(input_file)
    f = f.drop('urlSouscriptionBoursorama', axis=1)
    f.to_csv(output_file, index=False)

def usage(argv):
    print("""Usage:
%s [file_to_treat] [file_to_generate]""" % argv)

def check_argv(argv):
    if len(argv) != 3:
        usage(argv[0])
        exit(1)

if __name__ == '__main__':
    check_argv(sys.argv)
    main(sys.argv[1], sys.argv[2])
