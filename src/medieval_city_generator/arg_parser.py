#!/usr/bin/env python3

import argparse


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outfile', type=str, required=False,
                        help='Path for the outfile')
    parser.add_argument('-p', '--population', type=int, required=False,
                        help='Population number')
    parser.add_argument('-d', '--density', type=int, required=False,
                        help='Density for each area')
    parser.add_argument('--walls', action='store_true', required=False,
                        help='Add walls around the city')
    parser.add_argument('--castle', action='store_true', required=False,
                        help='Add a castle in the city')
    parser.add_argument('--river', action='store_true', required=False,
                        help='Add a river (WIP)')

    args = parser.parse_args()

    return args
