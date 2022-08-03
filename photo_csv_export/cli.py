# cli.py

import argparse
import sys

__version__ = "0.1.0"

def parse_command_line_arguments():
    """
    This function parses the command line arguments.
    """

    parser = argparse.ArgumentParser(
        prog="photo_csv_export",
        description='Analyze the jpgs in a folder for EXIF info and store in CSV file',
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
    parser.version = f"photo_csv_export v{__version__}"
    parser.add_argument(
        "-v",
        "--version",
        action="version",
    )
    return parser.parse_args()
