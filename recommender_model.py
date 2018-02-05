import numpy as np
import pandas as pd
from geopy.distance import great_circle

class RecommenderModel():
    '''
    Takes in a user's preferences for three features, their geographic
    coordinates, and the main recommendation dataframe and outputs the top
    recommended coffee shops for them.
    '''
    def __init__(self, df, mapping_df):
        '''
        Parameters:
        -----------
        df: Pandas DataFrame - The primary recommender dataframe including the W
        matrix from NMF
        mapping_df: Pandas DataFrame - The dataframe mapping user features to
        NMF model's latent features

        Output:
        --------
        None
        '''

        self.df = df
        self.mapping_df = mapping_df

    def recommend(self, f1, f2, f3, lat, lng, r=20, n=3):
        '''
        Takes in a user's preferences for three features, their geographic
        coordinates and outputs the top recommended coffee shops for them.

        Parameters:
        -----------
        f1, f2, f3: Tuples (float, string) - The importance of a specific feature
        for a user and the name of that feature
        lat: Float - User's latitude
        lng: Float - User's longitude
        r: Float - Max distance in miles that the user will travel (Default:20)
        n: Int - Number of recommendations to return (Default, 3)

        Output:
        --------
        Recommendations: List - Top recommendations based on the user's input
        '''

        self.chosen_features = [f1, f2, f3]
        self.mapped_df = self._map_features()
        self.distance_filtered_df = self._filter_by_lat_lng(lat, lng, r)
        self.sorted_df = self._sort_features()
        top_three_df = self.sorted_df.iloc[0:n]
        return top_three_df

    def _sort_features(self):
        '''
        Takes in a user's desired feature weights and a dataframe with feature
        columns and sorts the columns for use in the recommender.

        Parameters:
        -----------
        None

        Output:
        -------
        sorted_df: Pandas Dataframe with the recommended coffeeshops sorted by
        the user's preferences.
        '''

        normalizing_weight = sum([item[0] for item in self.chosen_features])
        self.feature_names = [item[1] for item in self.chosen_features]
        for item in self.chosen_features:
            self.distance_filtered_df['{}'.format(item[1])] = (self.distance_filtered_df['{}'.format(item[1])]
                                                             * item[0]
                                                             / normalizing_weight)

        self.distance_filtered_df['combined_weights'] = self.distance_filtered_df.apply(lambda row: (row[self.feature_names[0]]
                                                                             + row[self.feature_names[1]]
                                                                             + row[self.feature_names[2]]),
                                                                  axis=1)

        sorted_df = self.distance_filtered_df[['name', 'lat', 'lng', 'address',
                                               'shop_id',
                                               'distance_from_location',
                                               'combined_weights']]
        sorted_df = sorted_df.sort_values('combined_weights', ascending=False)
        return sorted_df

    def _filter_by_lat_lng(self, lat, lng, r):
        '''
        Takes in a user's latitude and longitude and a dataframe including
        coffeeshop latitudes and longitudes and filters out coffeeshops that are
        not within a particular distance

        Paramters:
        ----------
        lat: Float - User's latitude
        lng: Float - User's longitude
        r: Range, in miles, to restrict recommendations to

        Output:
        -------
        distance_filtered_df: Pandas DataFrame - Pandas Dataframe only including
        coffeeshops that are within the specified range of the input latitude
        and longitude
        '''
        current_location = (lat, lng)
        self.mapped_df['distance_from_location'] = self.mapped_df.apply(lambda row: great_circle(current_location,
                                                                     (row['lat'],
                                                                      row['lng'])).miles,
                                                          axis=1)
        distance_filtered_df = self.mapped_df[self.mapped_df['distance_from_location'] < r]
        return distance_filtered_df

    def _map_features(self):
        '''
        Maps the output of NMF feature data to categories available to the user
        using the mapping_df.

        Parameters:
        -----------
        None

        Output:
        -------
        feature_mapped_df: Pandas DataFrame - The primary recommender dataframe
        with the W matrix values from NMF removed and replaced with the mapped
        values
        '''

        W = self.df.drop(['name', 'lat', 'lng', 'address', 'shop_id'], axis=1)
        mapping_df_columns = self.mapping_df.columns
        mapped_features = pd.DataFrame(np.dot(W,self.mapping_df),
                                       columns = mapping_df_columns)
        #Normalize the mapped_feature values
        normalized_df=((mapped_features - mapped_features.min()) /
                       (mapped_features.max() - mapped_features.min()))

        feature_mapped_df = pd.concat([self.df[['name', 'lat', 'lng', 'address',
                                      'shop_id']].reset_index(drop=True),
                                      normalized_df], axis=1)
        return feature_mapped_df
