from tsunami.exception import ProjectException
from tsunami.logger import logging
from tsunami.constants import *
import os,sys
from tsunami.utils import read_yaml_file
from tsunami.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig

class configuration:

    def __init__(self,config_file_path=CONFIG_FILE_PATH,current_time_stamp=CURRENT_TIME_STAMP):
        try:
            self.config=read_yaml_file(file_path=config_file_path)
            self.pipeline_config=self.get_pipeline_config()
            self.current_time_stamp=current_time_stamp
        except Exception as e:
            raise ProjectException(e,sys) from e
        

        

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_info=self.config[DATA_INGESTION_CONFIG_KEY]

            artifact_dir=self.pipeline_config.artifact_dir

            data_ingestion_dir=os.path.join(artifact_dir,
                                      DATA_INGESTION_DIR_KEY,
                                      self.current_time_stamp)

            dataset_path=os.path.join(ROOT_DIR,
                                      data_ingestion_info[DATASET_DIR_KEY],
                                      data_ingestion_info[DATASET_NAME_KEY])
            
            ingested_train_dir=os.path.join(data_ingestion_dir,
                                            data_ingestion_info[INGESTED_TRAIN_DIR_KEY])
            
            ingested_test_dir=os.path.join(data_ingestion_dir,
                                            data_ingestion_info[INGESTED_TEST_DIR_KEY])

            data_ingestion_config=DataIngestionConfig(dataset_path=dataset_path,
                                                      ingested_train_dir=ingested_train_dir,
                                                      ingested_test_dir=ingested_test_dir)
            
            return data_ingestion_config
        except Exception as e:
            raise ProjectException(e,sys) from e





    def get_data_validation_config(self)->DataValidationConfig:
        try:

            data_validation_info=self.config[DATA_VALIDATION_CONFIG_KEY]

            schema_dir=data_validation_info[SCHEMA_DIR_KEY]

            schema_file_name=data_validation_info[SCHEMA_FILE_NAME_KEY]

            schema_file_path=os.path.join(ROOT_DIR,
                                          schema_dir,
                                          schema_file_name)
            
            data_validation_config=DataValidationConfig(schema_file_path=schema_file_path)

            return data_validation_config
        
        except Exception as e:
            raise ProjectException(e,sys) from e
        



    
    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir=self.pipeline_config.artifact_dir
            
            data_transformation_config_info=self.config[DATA_TRANSFORMATION_CONFIG_KEY]

            data_transformation_dir=os.path.join(artifact_dir,
                                                 DATA_TRANSFORMATION_DIR,
                                                 self.current_time_stamp)
            

            transformed_train_dir=os.path.join(data_transformation_dir,
                                               data_transformation_config_info[TRANSFORMED_DIR_KEY],
                                               data_transformation_config_info[TRANSFORMED_TRAIN_DIR_KEY])
            


            target_feature_dir=os.path.join(data_transformation_dir,
                                               data_transformation_config_info[TRANSFORMED_DIR_KEY],
                                               data_transformation_config_info[TARGET_FEATURE_DIR_KEY])
            

            preprocessed_object_file_path=os.path.join(data_transformation_dir,
                                                       data_transformation_config_info[PREPROCESSING_DIR_KEY],
                                                       data_transformation_config_info[PREPROCESSED_OBJECT_FILE_NAME_KEY])

            data_transformation_config=DataTransformationConfig(transformed_train_dir=transformed_train_dir,
                                                                target_feature_dir=target_feature_dir,
                                                                preprocessed_object_file_path=preprocessed_object_file_path)
            

            return data_transformation_config
        except Exception as e:
            raise ProjectException(e,sys) from e 






    def get_pipeline_config(self)->TrainingPipelineConfig:
        try:
            pipeline_info=self.config[TRAINING_PIPELINE_CONFIG_KEY]

            pipeline_name=pipeline_info[PIPELINE_NAME_KEY]
            artifact_dir_name=pipeline_info[ARTIFACT_DIR_KEY]
            artifact_dir=os.path.join(ROOT_DIR,pipeline_name,artifact_dir_name)
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)

            return training_pipeline_config
        except Exception as e:
            raise ProjectException(e,sys) from e