def get_tips_data(venue_id):
    '''
    Takes in a venue id and performs a GET request to Foursquare's API to retrieve a max of 500 tips formatted
    as a json object. Returns a list of strings of tips.
    '''
    tips_list = []
        tips_url = 'https://api.foursquare.com/v2/venues/{}/tips'.format(venue_id)
        try:
            tips_resp = requests.get(url=tips_url, params=tips_params)
            tips_data = json.loads(tips_resp.text)
            if tips_data['meta']['code'] == 403:
                print('403 error - Exceeded rate limit')
                print(tips_data)
                return tips_list
            for tip in tips_data['response']['tips']['items']:
                tips_list.append(tip['text'])
        except:
            tips_list.append(venue_id)
    return tips_list

def populate_search_params(lat, long):
    search_params = dict(
        client_id=secrets['client_id'],
        client_secret=secrets['client_secret'],
        ll = '{}, {}'.format(lat, long),
        intent='browse',
        radius='200', #Meters
        limit='50',
        categoryId='4bf58dd8d48988d1e0931735',#Coffee shop
        llAcc='1',#Accuracy of lat & long in meters
        v='20180113' #Date of current version
        )
    return search_params

def get_venue_data(longitude_group, latitude_group):
    '''
    Takes in lists of longitudes and latitudes and performs a grid search of them, returning a max of 50 coffee
    shops per each intersection formatted as a list of json objects.
    '''
    search_url = 'https://api.foursquare.com/v2/venues/search'
    search_list = []
    for i, long in enumerate(longitude_group):
        for lat in latitude_group:
            search_params = populate_search_params(lat, long)
            try:
                search_resp = requests.get(url=search_url, params=search_params)
                search_data = json.loads(search_resp.text)
                if search_data['meta']['code'] == 403:
                    print('403 error - Exceeded rate limit')
                    print(search_data)
                    return search_list
                search_list.append(search_data)
            except:
                search_list.append((lat, long))
        print('Step {} of {}'.format(i+1, len(longitude_group)))
    return search_list

def write_venue_info_to_file(search_data, filename):
    '''
    Takes in a list of loaded json objects and writes them to a text file.
    '''
    venues = []
    for item in search_data:
        # Checks for empty response
        try:
            if item['response']['venues'] != []:
                for venue in item['response']['venues']:
                    venues.append(venue)
        except:
            continue
    with open(filename, 'a') as f:
        for item in venues:
            f.write("{}\n".format(item))
    print('Done!')
