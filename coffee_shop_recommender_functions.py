import numpy as np
import pandas as pd
from geopy.distance import great_circle

def make_recommendations(f1, f2, f3, lat, lng, df, n=3):
    '''
    Takes in a user's preferences for three features, their geographic
    coordinates, and the main recommendation dataframe and outputs the top
    recommended coffee shops for them.

    Parameters:
    -----------
    f1, f2, f3: Tuples (float, string) - The importance of a specific feature
    for a user and the name of that feature

    lat: Float - User's latitude

    lng: Float - User's longitude

    df: Pandas DataFrame - The primary recommender dataframe including the W
    matrix from NMF

    n: Int - Number of recommendations to return (Default, 3)

    Output:
    --------
    Recommendations: List - Top recommendations based on the user's input
    '''
    #Will need to create a map from user input to feature names
    #Currently prentending columns are the names of the features
    chosen_features = [f1, f2, f3]
    distance_filtered_df = _filter_by_lat_lng(lat, lng, df)
    #return distance_filtered_df
    sorted_df = _sort_features(chosen_features, distance_filtered_df)
    #return sorted_df
    return list(sorted_df.iloc[0:n]['name'])

def _sort_features(chosen_features, user_df):
    '''
    Takes in a user's desired feature weights and a dataframe with feature
    columns and sorts the columns for use in the recommender.

    Parameters:
    -----------
    chosen_features: List of tuples (float, string) - The importance of a specific feature
    for a user and the name of that feature

    user_df: Pandas DataFrame - The main recommender dataframe

    Output:
    -------
    sorted_df: Pandas Dataframe with the recommended coffeeshops sorted by the
    user's preferences.
    '''

    normalizing_weight = sum([item[0] for item in chosen_features])
    feature_names = [item[1] for item in chosen_features]
    mapping_df = pd.read_csv('data/mapping_df.csv', index_col=0)
    mapped_df = _map_features(mapping_df, user_df)
    for item in chosen_features:
        mapped_df['{}'.format(item[1])] = mapped_df['{}'.format(item[1])]   \
                                         * item[0]                          \
                                         / normalizing_weight

    mapped_df['combined_weights'] = mapped_df.apply(lambda row: row[feature_names[0]]   \
                                                              + row[feature_names[1]]   \
                                                              + row[feature_names[2]],
                                                    axis=1)

    sorted_df = mapped_df[['name', 'combined_weights']]
    sorted_df = sorted_df.sort_values('combined_weights', ascending=False)
    return sorted_df

def _filter_by_lat_lng(lat, lng, df, range=15):
    '''
    Takes in a user's latitude and longitude and a dataframe including
    coffeeshop latitudes and longitudes and filters out coffeeshops that are
    not within a particular distance

    Paramters:
    ----------
    lat: Float - User's latitude

    lng: Float - User's longitude

    df: Pandas DataFrame - The primary recommender dataframe including the W
    matrix from NMF

    range: Range, in miles, to restrict recommendations to (Default: 10)

    Output:
    -------
    distance_filtered_df: Pandas DataFrame - Pandas Dataframe only including
    coffeeshops that are within the specified range of the input latitude and
    longitude
    '''
    current_location = (lat, lng)
    df['distance_from_location'] = df.apply(lambda row: great_circle(current_location,
                                                        (row['lat'],
                                                         row['lng'])).miles,
                                            axis=1)
    distance_filtered_df = df[df['distance_from_location'] < range]
    return distance_filtered_df

def _map_features(mapping_df, user_df):
    '''
    Maps the output of NMF feature data to categories available to the user
    using the mapping_df.

    Parameters:
    -----------
    mapping_df: Pandas DataFrame - DataFrame with mapping values

    user_df: Pandas DataFrame - The primary recommender dataframe including the W
    matrix from NMF

    Output:
    -------
    feature_mapped_df: Pandas DataFrame - The primary recommender dataframe
    with the W matrix values from NMF removed and replaced with the mapped
    values
    '''

    W = user_df.drop(['name', 'lat', 'lng', 'address', 'distance_from_location'],
                     axis=1)
    mapping_df_columns = mapping_df.columns
    mapped_features = pd.DataFrame(np.dot(W,mapping_df),
                                   columns = mapping_df_columns)
    feature_mapped_df = pd.concat([user_df[['name', 'lat', 'lng', 'address']].reset_index(drop=True),
                           mapped_features], axis=1)
    #print(user_df)
    return feature_mapped_df
