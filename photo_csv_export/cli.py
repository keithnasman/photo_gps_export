#!/usr/bin/python3
#
# cli.py
#
# 2022-08-04 - Keith Nasman - keithnasman@gmail.com
#
# Usage: as module for handling command line options

import argparse

__version__ = "0.1.0"


def parse_command_line_arguments():
    """
    This function parses the command line arguments.
    """

    parser = argparse.ArgumentParser(
        prog="photo_csv_export",
        description='Analyze the jpgs in a folder for EXIF GPS info and store in CSV file',
    )
    parser.add_argument(
        "Path",
        metavar="path",
        type=str,
        help="The Path to the image directory")
    parser.add_argument(
        "CSV",
        metavar="csv",
        type=str,
        help="The name of the CSV file",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        action="store_true",
        help="Exclude from the CSV file those files that don't have GPS coordinates",
    )
    parser.add_argument(
        "-s",
        "--show",
        action="store_true",
        help="Show output for each file",
    )

    parser.version = f"photo_csv_export v{__version__}"
    parser.add_argument(
        "-v",
        "--version",
        action="version",
    )
    return parser.parse_args()
