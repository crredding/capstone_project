import numpy as np
import pandas as pd

def make_recommendations(f1, f2, f3, lat, lng, df, n=3):
    '''
    Takes in a user's preferences for three features, their geographic
    coordinates, and the main recommendation database and outputs the top
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

    Outputs:
    --------
    Recommendations: List - Top recommendations based on the user's input
    '''
    #Will need to create a map from user input to feature names
    #Currently prentending columns are the names of the features
    chosen_features = [f1, f2, f3]
    user_feature_names = [item[1] for item in chosen_features
    user_df = df[['name', 'location.lat', 'location.lng',
                  '{}'.format(user_feature_names[0]),
                  '{}'.format(user_feature_names[1]),
                  '{}'.format(user_feature_names[2])]]
    distance_filtered_df = filter_by_lat_lng(lat, lng, user_df)
    sorted_df = _sort_features(chosen_features, distance_filtered_df)
    return list(sorted_df.iloc[0:n-1]['name'])

def _sort_features(chosen_features, user_df):
    '''
    Takes in a user's desired feature weights and a dataframe with feature
    columns and sorts the columns for use in the recommender.

    Parameters:
    -----------
    chosen_features: List of tuples (float, string) - The importance of a specific feature
    for a user and the name of that feature

    user_df: Pandas DataFrame - The recommender dataframe with only the
    applicable columns left in it.

    Output:
    -------
    sorted_df: Pandas Dataframe with the recommended coffeeshops sorted by the
    user's preferences.
    '''

    normalizing_weight = np.sum[item[0] for item in chosen_features]
    feature_names = [item[1] for item in chosen_features]
    for item in chosen_features:
        user_df['{}'.format(item[1])] = user_df['{}'.format(item[1])]
                                      * item[0]
                                      / normalizing_weight

    user_df['combined_weights'] = user_df.apply(lambda row: row['feature_names[0]']
                                                          + row['feature_names[1]']
                                                          + row['feature_names[2]'],
                                                axis=1)
    sorted_df = user_df[['name', 'combined_weights']]
    return sorted_df


def filter_by_lat_lng(lat, lng, df):
