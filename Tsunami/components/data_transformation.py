from tsunami.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact,DataIngestionArtifact
from tsunami.entity.config_entity import DataTransformationConfig
from tsunami.exception import ProjectException
from tsunami.logger import logging
import os,sys
import pandas as pd
import numpy as np
from tsunami.constants import *
from tsunami.utils import read_yaml_file,load_data,save_object
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer




class DataTransformation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig) -> None:
        try:
            logging.info(f"{'>>'*30}Data transformation log started.{'<<'*30}")
            self.data_ingestion_artifact=data_ingestion_artifact
            self.schema_file=read_yaml_file(data_validation_artifact.schema_file_path)
            self.data_transformation_config=data_transformation_config

        except Exception as e:
            raise ProjectException(e,sys) from e




    def get_preprocessing_obj(self)->ColumnTransformer:
        try:


            numerical_columns=self.schema_file[UPDATED_NUMERICAL_COLUMNS_KEY]
            cat_columns=self.schema_file[UPDATED_CATEGORICAL_COLUMNS_KEY]


            num_pipeline=Pipeline(steps=[
                ('impute',SimpleImputer(strategy="median")),
                ('StandardScalar',StandardScaler())
            ])
            
            

            cat_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="most_frequent")),
                ('OneHotEncoder',OneHotEncoder()),
                ('scaler', StandardScaler(with_mean=False))
            ])
            

            Preprocessing=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,cat_columns)
            ])


            return Preprocessing
        except Exception as e:
            raise ProjectException(e,sys) from e
        



    def drop_features_and_unknowns(self):
        try:
            logging.info("getting train and test df from data ingestion")
            train_df=load_data(file_path=self.data_ingestion_artifact.train_file_path)
            test_df=load_data(file_path=self.data_ingestion_artifact.test_file_path)

            features_to_drop=self.schema_file[DROP_FEATURES_KEY]

            logging.info("droping features from train df")
            train_df=train_df.drop(features_to_drop,axis=1)

            logging.info("droping features from test df")
            test_df=test_df.drop(features_to_drop,axis=1)


            logging.info("droping unknown data from train df")
            train_df=train_df[train_df[CAUSE_COLUMN_CONSTANT].str.contains(UNKNOWN_DROP_CONSTANT)==False]





            logging.info("droping unknown data from test df")
            test_df=test_df[test_df[CAUSE_COLUMN_CONSTANT].str.contains(UNKNOWN_DROP_CONSTANT)==False]

            


            return train_df,test_df
        
        except Exception as e:
            raise ProjectException(e,sys) from e





    def map_months_column(self):
        try:
            logging.info("getting training and testing data from drop featuress function")
            train_df,test_df=self.drop_features_and_unknowns()


            logging.info("maping month columns in train and test")
            train_df[MONTH_COLUMN_CONSTANT]=train_df[MONTH_COLUMN_CONSTANT].map({1.0:"January", 
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
            
            test_df[MONTH_COLUMN_CONSTANT]=test_df[MONTH_COLUMN_CONSTANT].map({1.0:"January",
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
         
         
            logging.info("returning train and test datasets after maping")
            return train_df,test_df
        except Exception as e:
            raise ProjectException(e,sys) from e
        





    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            
            train,test=self.map_months_column()



            preprocessing_obj=self.get_preprocessing_obj()

            target_column=self.schema_file[TARGET_COLUMN_KEY]

            logging.info("dropping target column from input train features")
            input_train_feature=train.drop(columns=target_column,axis=1)
            train_target_feature=train[target_column]


            logging.info("transforming input train features using preprocessing object")
            input_train_feature_arr=preprocessing_obj.fit_transform(input_train_feature)




            transformed_train_dir=self.data_transformation_config.transformed_train_dir

            logging.info("making transformed train dir")
            filename="tsunami.npz"
            transformed_train_file_path=os.path.join(transformed_train_dir,filename)

            logging.info("saving input transformed arr features in transformed_train_file_path")
            save_object(transformed_train_file_path,input_train_feature_arr)


            logging.info("saving target features in target_feature_file_path")
            target_feature_dir=self.data_transformation_config.target_feature_dir
            os.makedirs(target_feature_dir,exist_ok=True)
            target_feature_file_name="target_feature.csv"
            target_feature_file_path=os.path.join(target_feature_dir,target_feature_file_name)
            train_target_feature.to_csv(target_feature_file_path,index=False)
            

           


           


            logging.info("saving preprocessing object in preprocessed_object_file_path")
            preprocessed_object_file_path=self.data_transformation_config.preprocessed_object_file_path
            save_object(preprocessed_object_file_path,preprocessing_obj)


            data_transformation_artifact=DataTransformationArtifact(transformed_train_file_path=transformed_train_file_path,
                                                                    target_feature_file_path=target_feature_file_path,
                                                                    preprocessed_object_file_path=preprocessed_object_file_path)
            

            logging.info("returning DataTransformationArtifact")
            
            return data_transformation_artifact

        except Exception as e:
            raise ProjectException(e,sys) from e