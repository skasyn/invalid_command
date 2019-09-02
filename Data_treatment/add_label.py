#!/usr/bin/python3

import sys
import csv

def add_label(inputfile, outputfile, label):
    with open(inputfile, 'r') as csvinput:
        with open(outputfile, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            row = next(reader)
            row.append('label')
            all.append(row)

            for row in reader:
                row.append(label)
                all.append(row)
            writer.writerows(all)

def usage(filename):
    print("""Usage:
%s [input_file] [output_file] [label]""" % filename)

def main(argv):
    if len(argv) != 4:
        usage(argv[0])
        exit(1)
    add_label(argv[1], argv[2], argv[3])

if __name__ == '__main__':
    main(sys.argv)
