from tsunami.exception import ProjectException
from tsunami.logger import logging
from tsunami.config.configuration import configuration
from tsunami.entity.config_entity import DataIngestionConfig
from tsunami.entity.artifact_entity import DataIngestionArtifact
import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'>>'*20} data ingestion log started {'<<'*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise ProjectException(e,sys) from e
        



    def get_dataframe(self):
        try:
            logging.info("getting dataset from dataingestion config")
            dataset=self.data_ingestion_config.dataset_path


            logging.info("reading dataset from dataingestion config")
            dataframe=pd.read_csv(dataset)

            return dataframe
        except Exception as e:
            raise ProjectException(e,sys) from e
        



    def split_into_train_test(self):
        try:
            df=self.get_dataframe()

            file_name="tsunami.csv"


            logging.info("spliting dataset into train and test")
            train_df,test_df=train_test_split(df,test_size=0.4,random_state=42)

            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            logging.info("making train file path")
            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            df.to_csv(train_file_path,index=False)


            logging.info("making test file path")
            os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
            test_df.to_csv(test_file_path,index=False)


            data_ingestion_artifact=DataIngestionArtifact(train_file_path, test_file_path)
            logging.info("returning data ingestion artifact")

            return data_ingestion_artifact
        except Exception as e:
            raise ProjectException(e,sys) from e




    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("calling split train test function")
            return self.split_into_train_test()
        except Exception as e:
            raise ProjectException(e,sys) from e