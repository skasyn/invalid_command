#!/usr/bin/python3

import pandas as pd
import sys
import csv

def main(inputfile1, inputfile2, output_file):
    inputs = [inputfile1, inputfile2]
# Determine the field names from the top line of each input file
    fieldnames = []
    for filename in inputs:
        with open(filename, "r", newline="") as f_in:
            reader = csv.reader(f_in)
            headers = next(reader)
            for h in headers:
                if h not in fieldnames:
                    fieldnames.append(h)

# Copy the data
    with open(output_file, "w", newline="") as f_out:   # Comment 2 below
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for filename in inputs:
            with open(filename, "r", newline="") as f_in:
                reader = csv.DictReader(f_in)
                for line in reader:
                    writer.writerow(line)

# Move label column to the end
#    f=pd.read_csv(output_file)
#    cols = list(f.columns.values)
#    cols.pop(cols.index('label'))
#    f = f[cols + ['label']]
    f.to_csv(output_file, index=False)


def usage(filename):
    print("""Usage:
%s [file_OK] [file_KO] [output_file]""" % filename)

def check_argv(argv):
    if len(argv) != 4:
        usage(argv[0])
        exit(1)

if __name__ == '__main__':
    check_argv(sys.argv)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
