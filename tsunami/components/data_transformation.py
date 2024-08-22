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
        


        





    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            
            df=load_data(file_path=self.data_ingestion_artifact.train_file_path)



            preprocessing_obj=self.get_preprocessing_obj()

            target_column=self.schema_file[TARGET_COLUMN_KEY]

            logging.info("dropping target column from input train features")
            input_feature=df.drop(columns=target_column,axis=1)
            target_feature=df[target_column]


            logging.info("transforming input train features using preprocessing object")
            input_feature_arr=preprocessing_obj.fit_transform(input_feature)




            transformed_train_dir=self.data_transformation_config.transformed_train_dir

            logging.info("making transformed train dir")
            filename="tsunami.npz"
            transformed_train_file_path=os.path.join(transformed_train_dir,filename)

            logging.info("saving input transformed arr features in transformed_train_file_path")
            save_object(transformed_train_file_path,input_feature_arr)


            logging.info("saving target features in target_feature_file_path")
            target_feature_dir=self.data_transformation_config.target_feature_dir
            os.makedirs(target_feature_dir,exist_ok=True)
            target_feature_file_name="target_feature.csv"
            target_feature_file_path=os.path.join(target_feature_dir,target_feature_file_name)
            target_feature.to_csv(target_feature_file_path,index=False)
            

           


           


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