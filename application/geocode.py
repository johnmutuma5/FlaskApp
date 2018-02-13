import httplib2
import json

API_KEY = 'AIzaSyA9d011L5McVs9hKf3-7YUoaq6ZvtxW7CY'


def getGeocodeLocation(location):
    addressString = location.replace(" ", "+")
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+addressString+'&key='+API_KEY
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    content = json.loads(content.decode('utf8'))

    location = content['results'][0]['geometry']['location']
    return(location['lat'], location['lng'])
