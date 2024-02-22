from tsunami.exception import ProjectException
from tsunami.logger import logging
from tsunami.config.configuration import configuration
from tsunami.entity.config_entity import DataIngestionConfig
from tsunami.entity.artifact_entity import DataIngestionArtifact
import os,sys
import pandas as pd
from sklearn.model_selection import train_test_split
from tsunami.constants import *
from tsunami.utils import load_data,read_yaml_file




class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'>>'*20} data ingestion log started {'<<'*20}")
            self.data_ingestion_config=data_ingestion_config
            self.schema_file=read_yaml_file(self.data_ingestion_config.schema_file_path)
        except Exception as e:
            raise ProjectException(e,sys) from e
        




    def drop_features_and_unknowns(self):
        try:
            logging.info("getting dataset")
            df=load_data(file_path=self.data_ingestion_config.dataset_path)

            features_to_drop=self.schema_file[DROP_FEATURES_KEY]

            logging.info("droping features from df")
            df=df.drop(features_to_drop,axis=1)



            logging.info("droping unknown data from df")
            df=df[df[CAUSE_COLUMN_CONSTANT].str.contains(UNKNOWN_DROP_CONSTANT)==False]
            

            return df
        
        except Exception as e:
            raise ProjectException(e,sys) from e        
        



    def map_months_column(self):
        try:
            logging.info("getting dataset drop featuress function")
            df=self.drop_features_and_unknowns()


            logging.info("maping month columns in dataset")
            df[MONTH_COLUMN_CONSTANT]=df[MONTH_COLUMN_CONSTANT].map({1.0:"January", 
                                                                    2.0:"February",
                                                                    3.0: "March",
                                                                    4.0: "April", 
                                                                    5.0:"May", 
                                                                    6.0:"June",
                                                                    7.0: "July", 
                                                                    8.0:"August",
                                                                    9.0: "September",
                                                                    10.0: "October",
                                                                    11.0: "November",
                                                                    12.0: "December"})
                  
         
         
            logging.info("returning datasets after maping")
            return df
        except Exception as e:
            raise ProjectException(e,sys) from e
        



    def split_into_train_test(self):
        try:
            df=self.map_months_column()

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