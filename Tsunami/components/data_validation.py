from tsunami.exception import ProjectException
from tsunami.logger import logging
from tsunami.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
import os,sys
from tsunami.entity.config_entity import DataValidationConfig


class DataValidation:

    def __init__(self,
                 data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise ProjectException(e,sys) from e
        



    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            schema_file_path=self.data_validation_config.schema_file_path

            data_validation_artifact = DataValidationArtifact(schema_file_path=schema_file_path)
            return data_validation_artifact
        except Exception as e:
            raise ProjectException(e,sys) from e