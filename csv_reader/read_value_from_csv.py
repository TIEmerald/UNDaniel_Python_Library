# -*- coding:utf-8 -*-
import csv
import os
import sys
import inspect
import getopt

def read_key_value_pair_from_csv(file, key, value):
    values = None
    if value is not None:
        values = [value]
    results = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if values is None:
                values = list(row.keys())
                values.remove(key)
            results.append(row)
        if values is not None:
            for value in values:
                print(f'\n Generating Key-Value pair: \"{key}\" = \"{value}\" ------- Start *************')
                for result in results:
                    print(f'\"{result[key]}\" = \"{result[value]}\"')
                print(f'Generating Key-Value pair: \"{key}\" = \"{value}\" ------- End ************* \n')
    

def main(argv):
    searchingFile = None
    key = None
    value = None
    formattedDes = 'read_value_from_csv.py -f <file-name> -k <key> -v <values>'
    try:
        opts, args = getopt.getopt(argv,"f:k:v:",["file-name=","key=","values=","value="])
    except getopt.GetoptError:
        print(formattedDes)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(formattedDes)
            sys.exit()
        elif opt in ("-f", "--file-name"):
            searchingFile = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-v", "--values", "--value"):
            value = arg
    if key is None:
        print(formattedDes + ', Please provide the key in csv')
        sys.exit(2)
    read_key_value_pair_from_csv(searchingFile, key, value)

if __name__ == '__main__':
    main(sys.argv[1:])

