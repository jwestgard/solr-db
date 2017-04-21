#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys
import yaml


class cell(object):
    """class representing the individual points of data"""
    def __init__(self, rule, line):
        self.source = rule['source']
        self.inputdata = line[self.source]
        self.operation = rule.get('operation', "copy")
        self.match = rule.get('match', None)
        self.replacement = rule.get('replacement', None)
        self.delimiter = rule.get('delimiter', None)
        self.formatting = rule.get('formatting', None)
        self.add_sources = rule.get('add_sources', None)
    
    def transform(self):
        if self.operation == 'copy':
            return self.inputdata
        elif self.operation == 'replace':
            return self.inputdata.replace(self.match, self.replacement)
        elif self.operation == 'format':
            return 'for,at!'
        elif self.operation == 'split':
            return self.inputdata.split(self.delimiter)


def main(input):
    """Parse arguments, read config, and loop over input."""
    parser = argparse.ArgumentParser(
        description='Process CSV on stdin w/ rules specified by config.')
    parser.add_argument('-c', '--config', help='configuration to apply',
                        required=True)
    args = parser.parse_args()
    
    # try to read and parse specified config file
    try:
        p = os.path.join('config', args.config)
        with open(p, 'r') as configfile:
            cfg = yaml.load(configfile)
            outfields = [field for field in cfg]
    except FileNotFoundError:
        print('  *Error*: the specified configuration file was not found!')
        sys.exit(1)
    
    # set up reader from stdin and writer to stdout
    reader = csv.DictReader(input, delimiter=',')
    writer = csv.DictWriter(sys.stdout, extrasaction='ignore', 
                            fieldnames=outfields)
    writer.writeheader()
    
    # for each line of input, apply specified transformations
    for dataline in reader:
        outputrow = {}
        # iterate over the config file, applying rules for each output field
        for rule in cfg:
<<<<<<< Updated upstream
            datapoint = cell(cfg[rule], dataline)
            outputrow[rule] = datapoint.transform()
=======
            outputrow[rule] = cell(cfg[rule], dataline).transform()
>>>>>>> Stashed changes
        writer.writerow(outputrow)
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.stdin)



