#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

class encoding() :
    def __init__(self, csv_path : str):
        """
             This function takes csv filepath in input.
             :param csv_path: The filepath.
        """
        self.csv_path : str = csv_path

    @staticmethod
    def recover_data(self) -> list:
        try :
            assert(type(self.csv_path) == str)
            features : list = []
            with open(self.csv_path, encoding='ISO-8859-1') as data:
                read = csv.reader(data, delimiter=',', quotechar='|')
                for line in read :
                    features.append(line)
            return features
        except :
                print("Error: Incorrect filepath")

    @staticmethod
    def encoding_str_ascii(str_convert : str) -> int:
        tab_convert : list = [ord(i) for i in str_convert]
        try :
            int_convert : int = int(''.join(str(d) for d in tab_convert))
        except :
            return 0
        return int_convert
    
    @staticmethod
    def encoding_list_ascii(self) -> list :
        """
            This function takes encoding object in parameter.
            It encode all csv in ascii number.
            :return: List encoded in ascii numbers.
        """
        list_to_convert = self.recover_data(self)
        return_list = []
        line_convert = []
        for line in list_to_convert :
            for parts in line :
                line_convert.append(self.encoding_str_ascii(parts))
            return_list.append(line_convert)
            line_convert = []
        return return_list
