#!/usr/bin/env python

from . import parser
from .kinetix import *
import argparse 
import sys 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input yaml file with reaction definitions')
    args = parser.parse_args()

    # Read the yaml file:
    yaml_parser = parser.KinetixParser(args.input)
    yaml_parser.parse()




