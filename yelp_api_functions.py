def yelp_search_params(lat, lng, name):
    search_params = dict(
        term=name,
        latitude=lat,
        longitude=lng,
        radius=20,
        limit=1,
        )
    return search_params

def get_yelp_api_id(lat, lng, name, key):
    '''
    Takes in latitude, longitude, name, and Yelp's API key and outputs Yelp's id for location.
    '''
    yelp_search_url = 'https://api.yelp.com/v3/businesses/search'
    search_params = yelp_search_params(lat, lng, name)
    search_resp = requests.get(url=yelp_search_url, params=search_params,
                               headers={'Authorization':'Bearer {}'.format(key)})
    search_data = json.loads(search_resp.text)
    try:
        return search_data['businesses'][0]['id']
    except:
        return None

def populate_yelp_reviews_url(yelp_id):
    '''
    Takes in Yelp id and outputs the applicable api url.
    '''
    yelp_reviews_url = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(yelp_id)
    return yelp_reviews_url

def get_yelp_id_reviews(yelp_id, api_key):
    '''
    Takes in Yelp id and Yelp API key and outputs text reviews for locations.
    '''
    yelp_reviews_url = populate_yelp_reviews_url(yelp_id)
    reviews_resp = requests.get(url=yelp_reviews_url, params={'locale':'en_US'},
                               headers={'Authorization':'Bearer {}'.format(api_key)})
    reviews_data = json.loads(reviews_resp.text)
    #return reviews_data
    reviews_list = []
    try:
        for review in reviews_data['reviews']:
            reviews_list.append(review['text'])
        return reviews_list
    except:
        return reviews_list

def fill_addresses_with_yelp_ids(yelp_id, api_key):
    '''
    Takes in Yelp id and Yelp API key and outputs location address.
    '''
    yelp_search_url = 'https://api.yelp.com/v3/businesses/{}'.format(yelp_id)
    search_resp = requests.get(url=yelp_search_url,
                               headers={'Authorization':'Bearer {}'.format(api_key)})
    search_data = json.loads(search_resp.text)
    try:
        return search_data['location']['address1']
    except:
        return None
