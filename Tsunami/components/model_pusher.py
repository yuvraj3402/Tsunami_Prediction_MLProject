from tsunami.exception import ProjectException
from tsunami.logger import logging
from tsunami.config.configuration import configuration
from tsunami.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact
from tsunami.entity.config_entity import ModelPusherConfig
import shutil
import os,sys

class ModelPusher:

    def __init__(self,
                 model_evaluation_artifact:ModelEvaluationArtifact,
                 model_pusher_config:ModelPusherConfig):
        try:
            self.model_evaluation_artifact=model_evaluation_artifact
            self.model_pusher_config=model_pusher_config
        except Exception as e:
            raise ProjectException(e,sys) from e
        


    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            evaluated_model_file_path=self.model_evaluation_artifact.evaluated_model_path
            export_dir=self.model_pusher_config.export_dir_path
            file_name=os.path.basename(evaluated_model_file_path)
            export_model_file_path=os.path.join(export_dir,file_name)
            os.makedirs(export_dir,exist_ok=True)

            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)

            model_pusher_artifact=ModelPusherArtifact(is_model_pusher=True,
                                                      export_model_file_path=export_model_file_path)
            return model_pusher_artifact
        except Exception as e:
            raise ProjectException(e,sys) from e


