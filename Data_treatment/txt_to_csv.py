#!/usr/bin/python3
import fileinput
import json
import csv
import sys

def to_string(s):
    try:
        return str(s)
    except:
        return s.encode('utf-8')

def flattify(d, key=()):
    if isinstance(d, list):
        result = {}
        for i in d:
            result.update(flattify(i, key))
        return result
    if isinstance(d, dict):
        result = {}
        for k, v in d.items():
            result.update(flattify(v, key + (k,)))
        return result
    return {key: d}

def convert_from_file_with_multiple_json(argv):
    with open(argv, "rt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    total = []
    for line in content:
        if(line.strip()):
            line = json.loads(line)
            line = flattify(line)
            line = {'.'.join(k): v for k, v in line.items()}
            total.append(line)

    keys = set()
    for d in total:
        keys.update(d)

    with open('converted_commands.csv', 'w') as output_file:
        output_file = csv.DictWriter(output_file, sorted(keys))
        output_file.writeheader()
        output_file.writerows(total)
    print("Completed writing CSV file into : converted_commands.csv !")
    print("This file contains %d columns and %d commands." % (len(keys), len(total)))

def usage(filename):
    print("""Usage:
%s [fichier_a_mettre_a_plat]""" % filename)
    return 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage(sys.argv[0])
    else:
        convert_from_file_with_multiple_json(sys.argv[1])
