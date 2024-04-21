from geopy.distance import geodesic

from data_extraction import convert_dict_to_df, load_csv_and_convert_to_df, remove_columns_from_df
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from frauddetectiononeclasssvm import unsupervised_learning

def calculate_distance(p1, p2):
    # p1 = (latitude, longitude)
    # p2 =  (latitude, longitude)
    return geodesic(p1, p2).kilometers


def rule_01(input_data, dataset, user_id=None):
    if user_id:
        dataset = dataset[dataset['encryptedPAN'].apply(
            lambda x: x == input_data['encryptedPAN'])]

    dataset = dataset[dataset['encryptedHexCardNo'].apply(
        lambda x: x == input_data['encryptedHexCardNo'])]
    twelve_hours_ago = datetime.fromtimestamp(input_data['dateTimeTransaction']) - \
        timedelta(hours=12)

    # filtered_df = dataset[dataset['dateTimeTransaction'].apply(
    #    lambda x: print(x))]
    filtered_df = dataset[dataset['dateTimeTransaction'].apply(
        lambda x: datetime.fromtimestamp(x/1000) >= twelve_hours_ago)]

    if (filtered_df.empty):
        return False

    filtered_df.sort_values(by='dateTimeTransaction')
    if not filtered_df.empty:
        card_balance = filtered_df.iloc[0]
        if card_balance >= 300000:
            if filtered_df['transactionAmount'].sum() >= 0.70*card_balance:
                return True
    return False


def rule_02(input_data, dataset, user_id=None):
    if user_id:
        dataset = dataset[dataset['encryptedPAN'].apply(
            lambda x: x == input_data['encryptedPAN'])]

    dataset = dataset[dataset['encryptedHexCardNo'].apply(
        lambda x: x == input_data['encryptedHexCardNo'])]
    twelve_hours_ago = datetime.fromtimestamp(input_data['dateTimeTransaction']) - \
        timedelta(hours=12)

    # filtered_df = dataset[dataset['dateTimeTransaction'].apply(
    #    lambda x: print(x))]
    filtered_df = dataset[dataset['dateTimeTransaction'].apply(
        lambda x: datetime.fromtimestamp(x/1000) >= twelve_hours_ago)]

    print(filtered_df)
    if (filtered_df.empty):
        return False

    if filtered_df['transactionAmount'].sum() >= 100000:
        count = 0
        for index, row in filtered_df.iterrows():
            distance = calculate_distance(
                (row['longitude'], row['latitude'], (input_data['longitude'], input_data['latitude'])))
            print(distance)
            if distance >= 200:
                count += 1
                if count > 5:
                    return True
    return False


def rule_03(input_data, dataset, user_id=None):
    if user_id:
        dataset = dataset[dataset['encryptedPAN'].apply(
            lambda x: x == input_data['encryptedPAN'])]

    dataset = dataset[dataset['encryptedHexCardNo'].apply(
        lambda x: x == input_data['encryptedHexCardNo'])]
    twelve_hours_ago = datetime.fromtimestamp(input_data['dateTimeTransaction']) - \
        timedelta(hours=12)

    # filtered_df = dataset[dataset['dateTimeTransaction'].apply(
    #    lambda x: print(x))]
    filtered_df = dataset[dataset['dateTimeTransaction'].apply(
        lambda x: datetime.fromtimestamp(x/1000) >= twelve_hours_ago)]
    if filtered_df.empty:
        return False

    remove_columns_from_df(filtered_df, 'encryptedPAN')
    remove_columns_from_df(filtered_df, 'encryptedHexCardNo')
    train_set, test_set = train_test_split(
        filtered_df, test_size=0.3, random_state=42)

    return unsupervised_learning(train_set, test_set, input_data)

def rule_04(input_data, dataset):
    dataset = dataset[dataset['merchantCategoryCode'].apply(
        lambda x: x == input_data['merchantCategoryCode'])]
    twelve_hours_ago = datetime.fromtimestamp(input_data['dateTimeTransaction']) - \
        timedelta(hours=12)

    # filtered_df = dataset[dataset['dateTimeTransaction'].apply(
    #    lambda x: print(x))]
    filtered_df = dataset[dataset['dateTimeTransaction'].apply(
        lambda x: datetime.fromtimestamp(x/1000) >= twelve_hours_ago)]
    if filtered_df.empty:
        return False

    remove_columns_from_df(filtered_df, 'encryptedPAN')
    remove_columns_from_df(filtered_df, 'encryptedHexCardNo')
    train_set, test_set = train_test_split(
        filtered_df, test_size=0.3, random_state=42)

    return unsupervised_learning(train_set, test_set, input_data)


def detect(input_data):
    transaction_data = load_csv_and_convert_to_df('dataset/user_data.csv')
    violations = []
    if (rule_01(input_data, transaction_data)):
        violations.append("RULE-001")

    if (rule_02(input_data, transaction_data)):
        violations.append("RULE-002")

    if (rule_03(input_data, transaction_data)):
        violations.append("RULE-003")

    if (rule_04(input_data, transaction_data)):
        violations.append("RULE-004")

    return violations
