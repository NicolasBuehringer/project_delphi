import joblib
from project_delphi.params import *
import os


STORAGE_LOCATION = 'test/model.joblib'

class Trainer(object):
    def __init__(self, **kwargs):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = "Hello world"
        #self.X = X
        #self.y = y



    def upload_model_to_gcp(self):


        client = storage.Client()

        bucket = client.bucket(BUCKET_NAME)

        blob = bucket.blob(STORAGE_LOCATION)

        blob.upload_from_filename('model.joblib')


    def save_model(self):
        """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
        HINTS : use joblib library and google-cloud-storage"""

        # saving the trained model to disk is mandatory to then beeing able to upload it to storage
        # Implement here
        joblib.dump(self.pipeline, 'model.joblib')
        print("saved model.joblib locally")

        # Implement here
        self.upload_model_to_gcp()
        print(f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")



if __name__ == "__main__":
    print("CDU WILL WIN!")
    test = Trainer()
    test.save_model()
    
