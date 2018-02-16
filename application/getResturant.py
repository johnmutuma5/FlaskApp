
# encoding=utf8

from application.geocode import getGeocodeLocation
import json
import httplib2


import sys
'''import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout.detach())
sys.stderr = codecs.getwriter('utf8')(sys.stderr.detach())
'''
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='utf-16')

foursquare_client_id = "W2YJR5A34YRDQEHOPVSHZF32SG3S0QUR2BEWGFCYYH1IR4J3"
foursquare_client_secret = "RZW44YWO5KEVDG0H0DQJH5ZE43QPSSPVLGYQKAU3YHMTYN0Z"


def findARestaurant(mealType, location):
    lat, lng = getGeocodeLocation(location)
    url = 'https://api.foursquare.com/v2/venues/search?client_id=' + foursquare_client_id + '&client_secret='\
          + foursquare_client_secret+'&v=20161016&ll=' + str(lat) + ',' + str(lng) + '&query=' + mealType+'&intent=browse&radius=15000'

    h = httplib2.Http()
    response, content = h.request(url, 'GET')

    first_venue = [{}]
    if response['status'] == '200':
        content = json.loads(content.decode('utf-8'))
        try:
            restaurant = content['response']['venues'][0]
            first_venue[0]['Restaurant Name'] = restaurant['name']
            first_venue[0]['Restaurant Address'] = ', '.join(restaurant['location']['formattedAddress'])
            venue_id = restaurant['id']
            first_venue[0]['venue id'] = venue_id
            first_venue[0]['Image'] = getRestaurantImage(venue_id)
        except (IndexError, KeyError):
            print("No venue found within the raduis\n")
            return None
    else:
        print("Bad Response")
        return None

    return first_venue


# 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

# 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
# HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=C
# LIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

# 3. Grab the first restaurant
# 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by alteri
# ng the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
# 5. Grab the first image
# 6. If no image is available, insert default a image url
# 7. Return a dictionary containing the restaurant name, address, and image url

def getRestaurantImage(venue_id):
    url = 'https://api.foursquare.com/v2/venues/' + venue_id + '/photos?client_id='\
        + foursquare_client_id + \
        '&client_secret=' + foursquare_client_secret + \
        '&v=20161016'
    image_size = '300x300'

    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    if response['status'] == '200':
        content = json.loads(content.decode('utf8'))
        try:
            first_photo = content['response']['photos']['items'][0]
            prefix = first_photo['prefix']
            suffix = first_photo['suffix']
            image_url = prefix + image_size + suffix
            return image_url
        except (KeyError, IndexError):
            return 'http://pixabay.com/'

    else:
        print("Bad Response")
        return
