from tensorflow import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.layers import Normalization
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Flatten
from keras import layers
from tensorflow.keras import optimizers
import random
from project_delphi.features import get_features
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping 


def stupid_data_function():

    df = pd.read_csv("../notebooks/02luca/data_final_20210826_v3.csv")

    return df

def get_clean_dataframe(df):

    df_merged = df
    df_merged = df_merged[df_merged["reply_count"].notna()] 
    df_merged = df_merged.replace(np.nan, 0)
    
    return df_merged

def split_data(df_merged):

    #getting final prediction data layer
    df_merged_final_test = df_merged.iloc[-14:]

    #getting X_train 
    df_merged_final = df_merged.iloc[:-7]

    return df_merged_final_test, df_merged_final

def scale_data(df_merged_final_test, df_merged_final):

    num_features = [ "retweet_count", "like_count", "avg_user_tweet_count","avg_ff_ratio"]
    remaing_columns = ["share_of_tweets","share_unique_users","weighted_sentiment","share_of_positive_tweets","share_of_negative_tweets"]

    # Scaling numerical features
    mm_scaler = MinMaxScaler()
    mm_scaler.fit(df_merged_final[num_features])

    numerical_train_scaled = mm_scaler.transform(df_merged_final[num_features])
    numerical_test_scaled = mm_scaler.transform(df_merged_final_test[num_features])

    # Scaling pool data
    df_merged_poll = df_merged_final["poll"] / 100
    df_merged_poll_test = df_merged_final_test["poll"] / 100

    # Merging all scaled data into one dataframe

    df_numerical_train_scaled = pd.DataFrame(numerical_train_scaled, columns = num_features, index = df_merged_final.index)

    df_train_scaled = pd.concat([df_numerical_train_scaled,df_merged_final[remaing_columns], 
    pd.DataFrame(df_merged_poll, columns = ["poll"], index = df_merged_final.index)] , axis = 1)

    df_test_scaled = pd.concat([pd.DataFrame(numerical_test_scaled, columns = num_features, 
    index = df_merged_final_test.index),df_merged_final_test[remaing_columns], 
    pd.DataFrame(df_merged_poll_test, columns = ["poll"], index = df_merged_final_test.index)] , axis = 1)

    return df_train_scaled, df_test_scaled


def creating_subsequences(df_train_scaled):

    # Function that creates one subsquece
    def subsequence(df, length, start = 0):
        last_possible_start = len(df) - length 
        X = df[start:start + length]
        y = df["poll"][(start + length ) : (start + length + 7)]
        
        return X, y

    # Creates a list of subsequences
    def multiple_subsequences(df, length):
    
        list_of_X = []
        list_of_y = []
        
        number_of_subsequences = round(len(df) /  7 - (length/7))
        print(number_of_subsequences)
        start = 0
        for num in range(number_of_subsequences):
            temporary_X, temporary_y = subsequence(df, length, start)
            list_of_X.append(temporary_X)
            list_of_y.append(temporary_y)
            start = start + 7
        
        return list_of_X, list_of_y

    # Creating subsequences of lenght specifided (28 / 7parties = 4 days)
    X_train , y_train = multiple_subsequences(pd.DataFrame(df_train_scaled), 21 )

    # Transforn to array to fit model
    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train

def rnn_fit_compile(X_train, y_train):

    model = Sequential()
    model.add(layers.GRU(units=128, activation='tanh', return_sequences=True))
    model.add(layers.GRU(units=64, activation='tanh', return_sequences=False))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(7, activation='linear'))

    es = EarlyStopping(patience = 3, restore_best_weights=True)

    model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    model.fit(X_train, y_train ,
          epochs=40, 
          batch_size=1, 
          verbose=1, 
          validation_split=0.2,
          shuffle = False
            )

    return model

def model_prediction(model, df_test_scaled):

    # Transforming to array and expanding dimensions
    df_merged_final_day = np.array(df_test_scaled)
    df_merged_final_day = np.expand_dims(df_merged_final_day, axis = 0)

    # Prediction
    df_prediction = pd.DataFrame(model.predict(df_merged_final_day)).rename( \
                        columns = {0:'AFD',1:'CDU',2:'FDP',3: 'GRUENE',4: 'LINKE', 5:'OTHER', 6: 'SPD'}).round(3)
    df_prediction.index = ["pred"]

    # Scaling prediction to 100%
    df_prediction_2 = pd.DataFrame((df_prediction.iloc[0]) / np.sum(df_prediction.iloc[0])).T.round(2)

    # Transforming into dictionary

    #prediction_dict = df_prediction_2.to_dict("records")[0]

    return df_prediction_2

def merge_date(df_prediction_2, df_merged_final_test):

    prediction_date = df_merged_final_test["tweet_date"].iloc[-2]

    df_prediction_2.index = [prediction_date]

    return df_prediction_2


if __name__ == "__main__":

    df = stupid_data_function()

    df_merged = get_clean_dataframe(df)

    df_merged_final_test, df_merged_final = split_data(df_merged)

    df_train_scaled, df_test_scaled = scale_data(df_merged_final_test, df_merged_final)

    X_train, y_train = creating_subsequences(df_train_scaled)

    model = rnn_fit_compile(X_train, y_train)

    prediction_df = model_prediction(model, df_test_scaled)

    prediction_df = merge_date(prediction_df, df_merged_final_test)

    print(prediction_df)

