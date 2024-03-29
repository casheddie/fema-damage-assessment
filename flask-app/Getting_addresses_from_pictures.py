apisecretkey = 'PUT-API-KEY-HERE'

# Modules that need to be installed are pillow, google_streetview, googlemaps, pygeocoder
py_modules =['pillow','google_streetview', 'googlemaps','pygeocoder']

import os
import io
import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Install the following modules on your device
# %pip install pillow
# %pip install google_streetview
# %pip install googlemaps
# %pip install pygeocoder
# %pip install pyzillow

## Pillow is used to extract data from Imagery ##
# Importing the image library pillow

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Import google_streetview for the api module
import googlemaps
import google_streetview.api
import google_streetview

import json

# Importing for reversing to the address

from pygeocoder import Geocoder

def get_exif(filename):
    """Function for extracting GPS data from image
        Args:
            img (.jpeg / .png et al.): an image file Note: Photos
        Output:
            Will first validate whether or not we have a valid image file and then output the
            metadata in form of a dictionary """
    try:
        image = Image.open(filename)
        image.verify()    #Image verify won't output anything if the image is in the correct format
        exif = image._getexif()
        if exif is not None:
            for key, value in exif.items():
                name = TAGS.get(key, key)
                exif[name] = exif.pop(key)

    except:
        raise ValueError("""Please upload a valid jpg or png file do not use airdrop or messaging apps like WhatsApp
                         or Slack to transfer images. Emailing will keep all of the metadata.""")


    return exif


def get_geotagging(exif):

    """ Returns:
        Dictionary with following key: value pairs:
            'GPSVersionID':  bytes,
            'GPSLatitudeRef': str = 'N' or 'S',
            'GPSLatitude': tuple of tuples,
            'GPSLongitudeRef': str = 'E' or 'W',
            'GPSLongitude': tuple of tuples,
            'GPSAltitudeRef': byte string,
            'GPSAltitude': tuple,
            'GPSTimeStamp': tuple of tuples,
            'GPSSatellites':,
            'GPSStatus':,
            'GPSMeasureMode':,
            'GPSDOP':,
            'GPSSpeedRef': str,
            'GPSSpeed': tuple,
            'GPSImgDirectionRef': str,
            'GPSImgDirection': tuple,
            'GPSDestBearingRef': str,
            'GPSDestBearing': tuple,
            'GPSDateStamp': str representing datetime,
            'GPSDifferential',
            'GPSHPositioningError': tuple,
            'GPSTrackRef',
            'GPSTrack',
            'GPSMapDatum',
            'GPSDestLatitudeRef',
            'GPSDestLatitude',
            'GPSDestLongitudeRef',
            'GPSDestLongitude',
            'GPSDestDistanceRef',
            'GPSDestDistance',
            'GPSProcessingMethod',
            'GPSAreaInformation',

                }
    """

    if not exif:
        raise ValueError("No metadata found please check your camera settings")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            geotagging= exif[tag]

    new = {GPSTAGS[k]: v for k,v in geotagging.items()}

    return new


# Convert to degrees
def to_degrees(coord,direc):
    deg_num, deg_denom = coord[0]
    d = float(deg_num)/float(deg_denom)

    min_num, min_denom = coord[1]
    m = float(min_num)/float(min_denom)
    #Seconds are optional
    try:
        sec_num, sec_denom = coord[2]
        s = float(sec_num)/float(sec_denom)
    except:
        s = 0

    if direc == 'N' or direc == 'E':
        sign = 1
    elif direc == 'S' or direc == 'W':
        sign = -1


    return sign*(d + m/(60.00)+s/(3600.00))


# Putting in the Google API

view = google_streetview

gmaps = googlemaps.Client(apisecretkey) # My key

# Define parameters for street view api
def google_streetviewer(location):

    params = [{
    'size': '1200x800', # max 640x640 pixels
    'location': location ,
#     'heading': '151.78',
    'pitch': '-0.76',
    'key':apisecretkey  # My key
    }]

    # Create a results object
    results = google_streetview.api.results(params)

    # Download images to directory 'downloads'
    return results.download_links(f'google-pics/{location}')


# Setting up the Google API to show the address

def reverse_lookup(lat, long, key=apisecretkey):
    """Function for lookup of addresses from latitude, longitude details using Google Maps API
    Args:
        lat (float): latitude as float
        long (float): longitude as float
        key (str): (default='YOURAPIKEYHERE') google maps api key
    Returns:
        returns a tuple with address (str), zipcode (str)
        """
    result = str(Geocoder(api_key=apisecretkey).reverse_geocode(lat, long))
    location_details = result.split(",")
    address = location_details[0]
    zipcode = location_details[-2]
    city = location_details[1]
    state = location_details[2].split(" ")[1]
    return address, zipcode, city, state


# Function that gets the metadata and gives all the details about the location
def get_coordinates(img_file):
    exif = get_exif(img_file)
    tags = get_geotagging(exif)
    location = f"{to_degrees(tags['GPSLatitude'], tags['GPSLatitudeRef'])},{to_degrees(tags['GPSLongitude'], tags['GPSLongitudeRef'])}"
    google_view = google_streetviewer(location)

    address = reverse_lookup(float(location.split(",")[0]),float(location.split(",")[1]), apisecretkey)
# Code below not used
#     details = zillow_query('X1-ZWz1hg6finlw5n_634pb',address[0],address[1])
#     details = result
#     details_dict = details.__dict__
#     keys = ['zillow_id','home_type','year_built','property_size','home_size',
#             'bathrooms','bedrooms','last_sold_date','last_sold_price','zestimate_amount']
#     dict_outcome = {}
#     dict_outcome= {k:details_dict[k] for k in keys if k in details_dict}
#     dict_outcome['address'] = f'{address[0]},{address[2]},{address[1]}'

#     return dict_outcome
#     google_view
    return location.split(',')[0],location.split(',')[1]


def get_url_geocode(lat, long):
    '''
        Generate Google API url
        Input: lat_long_raw & api_key (see above section 1.1 for instruction)
        Output: Google API url
    '''
    latlng = str(lat)+','+str(long)
    url_geocode = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latlng}&key={apisecretkey}'
    return url_geocode


# Get address from coordinates
def get_address(lat, long):
    '''
        Generate Google API url
        Input: lat_long_raw & api_key
        Output: list of dictionary of addresses
    '''
    N_ADDRESS = 4
    url = get_url_geocode(lat, long)

    res = requests.get(url)
    if res.status_code == 200:
        #print(f'Status code: {res.status_code}')
        res_jas = res.json()

        address_list = []
        for i in range(N_ADDRESS):
            address={}
            address['full_address'] = res_jas['results'][i]['formatted_address']
#             address['street_number'] = address['full_address'].split(', ')[0]
#             address['city'] = address['full_address'].split(', ')[1]
#             address['state'] = address['full_address'].split(', ')[2].split(' ')[0]
#             address['zip_code'] = address['full_address'].split(', ')[2].split(' ')[1]
#             address['lat'] = res_jas['results'][i]['geometry']['location']['lat']
#             address['lng'] = res_jas['results'][i]['geometry']['location']['lng']
#             address['place_id'] = res_jas['results'][i]['place_id']
            address_list.append(address)
    else:
        print('Unexpected error: Check latitude, longitude format and Api Key')
    list_of_addresses=[]
    for i in range(len(address_list)):
       list_of_addresses.append(address_list[i]['full_address'])
    return list_of_addresses
#     return address_list


# Get addresses from image file
def get_addresses(img_file):
    coord = get_coordinates(img_file)
    get_url_geocode(coord[0], coord[1])
    return get_address(coord[0], coord[1])
