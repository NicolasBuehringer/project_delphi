import joblib
from project_delphi.params import *
import os
import pandas as pd
from germansentiment import SentimentModel
import numpy as np

STORAGE_LOCATION = 'nlp_model_test/sentiment.joblib'

def get_data():

    path = "../raw_data/sample_twitter_api.csv"
    df = pd.read_csv(path, lineterminator='\n')

    return df

class NLPModelTrainer():

    def __init__(self, **kwargs):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.df = df
        self.pipeline = None

    def predict_nlp_sentiment():


        model = SentimentModel()
        self.pipeline = model
        #sentiments = model.predict_sentiment(data_full.text)

        return sentiments

    def upload_model_to_gcp(self):


        client = storage.Client()

        bucket = client.bucket(BUCKET_NAME)

        blob = bucket.blob(STORAGE_LOCATION)

        blob.upload_from_filename('sentiment.joblib')


    def save_model(self):
        """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
        HINTS : use joblib library and google-cloud-storage"""

        # saving the trained model to disk is mandatory to then beeing able to upload it to storage
        # Implement here
        joblib.dump(self.pipeline, 'sentiment.joblib')
        print("saved model.joblib locally")

        # Implement here
        self.upload_model_to_gcp()
        print(f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")


if __name__ == "__main__":

    df = get_data()
    trainer = NLPModelTrainer()
    trainer.save_model()
    print(df)
    