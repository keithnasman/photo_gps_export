#!/usr/bin/python3
#
# photo_csv.py
#
# 2022-07-03 - Keith Nasman - keithnasman@gmail.com
#
# Usage: photo_csv <path to file>
#
import sys
import os.path
import argparse
import csv

import piexif


def decimal_lat_long(image):
    """
    This function receives a piexif image object, extracts the GPS location info
    and converts it to decimal.

    Returns: the latitude and longitude in a tuple.
    """

    gpslatref = image['GPS']
    if gpslatref:
        latitude_mult = 1 if image['GPS']['GPSLatitudeRef'].decode() == 'N' else -1
    else:
        return 0, 0

    # Read and convert Latitude
    gps_lat_array = image['GPS']['GPSLatitude']
    if gps_lat_array[0][1] and gps_lat_array[1][1] and gps_lat_array[2][1]:
        latitude_deg = gps_lat_array[0][0] // gps_lat_array[0][1]
        latitude_min = gps_lat_array[1][0] // gps_lat_array[1][1]
        latitude_sec = gps_lat_array[2][0] // gps_lat_array[2][1]
        la = latitude_mult * round(latitude_deg + latitude_min / 60 + latitude_sec / 3600, 4)
    else:
        la = ''

    # Read and convert Longitude
    longitude_mult = 1 if image['GPS']['GPSLongitudeRef'].decode() == 'E' else -1
    gps_long_array = image['GPS']['GPSLongitude']
    if gps_long_array[2][1] and gps_long_array[2][1] and gps_long_array[2][1]:
        longitude_deg = gps_long_array[0][0] // gps_long_array[0][1]
        longitude_min = gps_long_array[1][0] // gps_long_array[1][1]
        longitude_sec = gps_long_array[2][0] // gps_long_array[2][1]
        lo = longitude_mult * round((longitude_deg + longitude_min / 60 + longitude_sec / 3600), 4)
    else:
        lo = ''

    return la, lo


if __name__ == '__main__':

    # Parse the command line arguments
    my_parser = argparse.ArgumentParser(description='Analyze the jpgs in a folder for EXIF info and store in CSV file')
    my_parser.add_argument('Path', metavar='path', type=str, help='The Path to the image directory')
    my_parser.add_argument('CSV', metavar='csv', type=str, help='The name of the CSV file')
    args = my_parser.parse_args()
    input_path = args.Path
    csv_file_name = args.CSV

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
        file, camera, gps_lat, gps_long = None, None, None, None

        # Test for valid EXIF image
        try:
            img = piexif.load(os.path.join(input_path, file_name), 'Exif')
        except piexif._exceptions.InvalidImageDataError:
            print('Image:', os.path.join(input_path, file_name))
            print('Not a jpg or tiff file')
            print()
            pass

        # Retrieve EXIF info
        file = os.path.join(input_path, file_name)
        print('Image:', os.path.join(input_path, file_name))

        # Retrieve camera make
        if 'Make' in img['0th']:
            camera = img['0th']['Make'].decode() + ' ' + img['0th']['Model'].decode()
            print('Camera:', camera)
        else:
            camera = 'Unidentified'
            print('Camera:', camera)

        # Retrieve and convert latitude and longitude
        if 'GPSLatitudeRef' in img['GPS']:
            (gps_lat, gps_long) = decimal_lat_long(img)
            print(f'Lat/Long: {gps_lat}, {gps_long}')
            csv_writer.writerow([file, camera, gps_lat, gps_long])
            print()
        else:
            print("No GPS info found")
            gps = 'No GPS info found'
            csv_writer.writerow([file, camera, '', ''])
            print()
