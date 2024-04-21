import pandas as pd
import json


def get_data_from_db(client_id, user_id):
    # database logic here
    pass


def convert_dict_to_df(data):
    return pd.DataFrame.from_dict(data)


def load_csv_and_convert_to_df(path_to_csv):
    # Load CSV file into a DataFrame
    df = pd.read_csv(path_to_csv)
    # Display the DataFrame
    return df


def remove_columns_from_df(df, column):
    df.drop(column, axis=1, inplace=True)
    return df


def filter_df(df, user_id, client_id):
    condition1 = df['client_id'] == client_id
    condition2 = df['user_id'] == user_id
    combined_condition = condition1 & condition2
    filtered_df = df[combined_condition]
    return filtered_df


def feature_data(df):
    with open('config/config.json', 'r') as f:
        config_data = json.load(f)

    required_features = config_data['features_categorical'] + \
        config_data['features_numerical']
    selected_features_df = df[required_features]

    return selected_features_df, config_data['features_categorical'], config_data['features_numerical']
