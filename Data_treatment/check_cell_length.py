#!/usr/bin/python3

import sys

def main(max_limit, filename):
    total_too_large_cell = 0
    with open(filename, 'rt') as f:
        total = f.readlines()
        column_name = total[0]
        for i in range(len(total) - 1): #all lines of the file, except the first column name
            line = total[i + 1].split(',')
            for index in range(len(line)):
                if len(line[index]) > int(max_limit):
                    print('\033[93m' + 'Line %d at column %d(%c%c) has %d characters' % (i + 2, index + 1, chr(int(index / 26) + 64), chr(int(index % 26) + 65), len(line[index])))
                    print('\033[95m-> ' + line[index])
                    total_too_large_cell += 1
    if total_too_large_cell == 0:
        print('\033[92m' + 'All of cells are valid')
    else:
        print('\n\033[91m' + 'The total of cells containing more than %d characters is equal to %d' % (max_limit, total_too_large_cell))


def usage(argv):
    print("""Usage:
%s [nb_of_max_limit] [path_to_file]""" % argv)

def check_argv(argv):
    if len(argv) != 3:
        usage(argv[0])
        exit(1)
    if argv[1].isdigit() == False or int(argv[1]) < 1:
        print('nb_of_max_limit has to be a positive number')
        exit(1)

if __name__ == '__main__':
    check_argv(sys.argv)
    main(int(sys.argv[1]), sys.argv[2])
