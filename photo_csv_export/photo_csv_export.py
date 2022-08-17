#!/usr/bin/python3
#
# photo_csv.py
#
# 2022-08-04 - Keith Nasman - keithnasman@gmail.com
#
# Usage: photo_csv <path to file>
#
import sys
import os.path
import csv
import cli

import piexif


def convert_coordinates_to_decimal(image_gps):
    """
    This function receives a piexif image gps dictionary, extracts the GPS location info
    and converts it to decimal.

    Returns: the latitude and longitude in a tuple.
    """

    gps_latitude_ref = image_gps
    if gps_latitude_ref:
        latitude_multiplier = 1 if image_gps['GPSLatitudeRef'].decode() == 'N' else -1
    else:
        return 0, 0

    # Read and convert Latitude
    gps_latitude_array = image_gps['GPSLatitude']
    if gps_latitude_array[0][1] and gps_latitude_array[1][1] and gps_latitude_array[2][1]:
        latitude_degrees = gps_latitude_array[0][0] // gps_latitude_array[0][1]
        latitude_minutes = gps_latitude_array[1][0] // gps_latitude_array[1][1]
        latitude_seconds = gps_latitude_array[2][0] // gps_latitude_array[2][1]
        latitude = latitude_multiplier * \
            round(latitude_degrees + latitude_minutes / 60 + latitude_seconds / 3600, 4)
    else:
        latitude = None

    # Read and convert Longitude
    longitude_multiplier = 1 if image_gps['GPSLongitudeRef'].decode() == 'E' else -1
    gps_longitude_array = image_gps['GPSLongitude']
    if gps_longitude_array[0][1] and gps_longitude_array[1][1] and gps_longitude_array[2][1]:
        longitude_degrees = gps_longitude_array[0][0] // gps_longitude_array[0][1]
        longitude_minutes = gps_longitude_array[1][0] // gps_longitude_array[1][1]
        longitude_seconds = gps_longitude_array[2][0] // gps_longitude_array[2][1]
        longitude = longitude_multiplier * \
            round((longitude_degrees + longitude_minutes / 60 + longitude_seconds / 3600), 4)
    else:
        longitude = None

    return latitude, longitude


if __name__ == '__main__':

    # Parse the command line arguments
    args = cli.parse_command_line_arguments()
    input_path = args.Path
    csv_file_name = args.CSV
    exclude = args.exclude
    show = args.show

    # Test for a valid path
    if not os.path.isdir(input_path):
        print('The path specified does not exist')
        sys.exit()

    # Open csv file
    try:
        csv_file = open(csv_file_name, 'w')
        fieldnames = ['file_name', 'camera', 'gps_lat', 'gps_long']
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fieldnames)
    except FileNotFoundError:
        print("Couldn't open the csv file")
        sys.exit()

    # Loop through files to process
    file_list = os.listdir(input_path)
    for file_name in file_list:

        # Clear vars of values 
        file, camera, gps_latitude, gps_longitude = None, None, None, None

        # Test for image file

        # Test for valid EXIF image
        try:
            img = piexif.load(os.path.join(input_path, file_name), 'Exif')
        except piexif._exceptions.InvalidImageDataError:
            print('Image:', os.path.join(input_path, file_name))
            if show:
                print('No EXIF information')
                print()
            pass

        # Retrieve EXIF info
        file = os.path.join(input_path, file_name)
        if show:
            print('Image:', os.path.join(input_path, file_name))

        # Retrieve camera make
        # noinspection PyUnboundLocalVariable
        if 'Make' in img['0th']:
            camera = f"{img['0th']['Make'].decode()} {img['0th']['Model'].decode()}"
            if show:
                print('Camera:', camera)

        else:
            camera = 'Unidentified'
            if show:
                print('Camera:', camera)

        # Retrieve and convert latitude and longitude
        if 'GPSLatitudeRef' in img['GPS']:
            (gps_latitude, gps_longitude) = convert_coordinates_to_decimal(img['GPS'])
            if show:
                print(f'Lat/Long: {gps_latitude}, {gps_longitude}')
                print()
            csv_writer.writerow([file, camera, gps_latitude, gps_longitude])
        else:
            if show:
                print('No GPS info found')
                print()
            if exclude:
                continue
            csv_writer.writerow([file, camera, '', ''])

    csv_file.close()
