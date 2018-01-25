import json, requests

def populate_google_search_url(lat, lng, place_name, api_key):
    '''
    Takes in latitude, longitude, place name (sting), and Google api key, and outputs the applicable api url.
    '''
    google_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=5&language=english&keyword={}&key={}'.format(lat, lng, place_name, api_key)
    return google_search_url

def populate_google_photos_url(photoreference, api_key, maxwidth=800):
    '''
    Takes in maxheight, the photo reference id, and Google api key, and outputs the applicable api url.
    '''
    google_photo_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&key={}'.format(maxwidth, photoreference, api_key)
    return google_photo_url

def get_google_api_id(lat, lng, name, api_key):
    '''
    Takes in latitude, longitude, name, and Google API key and outputs Google's place id for location.
    '''
    search_url = populate_google_search_url(lat, lng, name, api_key)
    search_resp = requests.get(url=search_url)
    search_data = json.loads(search_resp.text)
    try:
        return search_data['results'][0]['place_id']
    except:
        return None

def get_google_api_photo_id(lat, lng, name, api_key):
    '''
    Takes in latitude, longitude, name, and Google API key and outputs Google's photo id for location.
    '''
    search_url = populate_google_search_url(lat, lng, name, api_key)
    search_resp = requests.get(url=search_url)
    search_data = json.loads(search_resp.text)
    try:
        return search_data['results'][0]['photos'][0]['photo_reference']
    except:
        return None

def get_google_photos(lat, lng, name, api_key):
    photoreference = get_google_photo_id(lat, lng, name, api_key)
    photo_url = populate_google_photos_url(photoreference, api_key)
    photo_resp = requests.get(url=photo_url)
    return photo_resp

def populate_google_details_url(google_id, api_key):
    '''
    Takes in place id and Google api key, and outputs the applicable api url.
    '''
    google_details_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&language=english&key={}'.format(google_id, api_key)
    return google_details_url

def get_google_id_reviews(google_id, api_key):
    '''
    Takes in place id and Google API key and outputs text reviews for locations.
    '''
    details_url = populate_google_details_url(google_id, api_key)
    details_resp = requests.get(url=details_url)
    details_data = json.loads(details_resp.text)
    reviews_list = []
    try:
        for review in details_data['result']['reviews']:
            reviews_list.append(review['text'])
        return reviews_list
    except:
        return reviews_list

def fill_address_with_google_ids(google_id, api_key):
    '''
    Takes in a google place id and Google API key and outputs address pulled from Google's API.
    '''
    details_url = populate_google_details_url(google_id, api_key)
    details_resp = requests.get(url=details_url)
    details_data = json.loads(details_resp.text)
    try:
        address = details_data['result']['formatted_address'].split(',')[0]
        return address
    except:
        return None
