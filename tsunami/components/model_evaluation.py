from tsunami.exception import ProjectException
from tsunami.logger import logging
from tsunami.entity.artifact_entity import ModelEvaluationArtifact,ModelTrainerArtifact,DataIngestionArtifact
from tsunami.entity.config_entity import ModelEvaluationConfig
from tsunami.entity.model_factory  import evaluate_classification_model
from tsunami.utils import load_data,load_object,read_yaml_file,write_yaml_file
import os,sys
from tsunami.constants import *



class ModelEvaluation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 model_evaluation_config:ModelEvaluationConfig,
                 model_trainer_artifact:ModelTrainerArtifact) -> None:
        try:
            self.model_evaluation_config=model_evaluation_config
            self.model_trainer_artifact=model_trainer_artifact
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise ProjectException(e,sys) from e
        


    def get_best_model(self):
        try:
            model=None
            model_evaluation_file=self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(path=model_evaluation_file):
                write_yaml_file(file_path=model_evaluation_file)
                return model
            
            file_content=read_yaml_file(file_path=model_evaluation_file)

            file_content= dict() if file_content is None else file_content

            if BEST_MODEL_KEY not in file_content:
                return model
            

            model=load_object(file_path=file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])

            return model
        
        except Exception as e:
            raise ProjectException(e,sys) from e
    
        


    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:

            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"Previous eval result: {model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path,
                }
            }
 
            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated eval result:{model_eval_content}")
            write_yaml_file(file_path=eval_file_path, data=model_eval_content)

        except Exception as e:
            raise ProjectException(e,sys) from e






    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            model_file_path=self.model_trainer_artifact.trained_model_file_path
            model_obj=load_object(file_path=model_file_path)
            df=load_data(self.data_ingestion_artifact.train_file_path)
            xtrain=df.drop(EVENT_VALIDITY_CONSTANT,axis=1)
            ytrain=df[EVENT_VALIDITY_CONSTANT]


            model=self.get_best_model()


            if model is None:
                model_evaluation_artifact=ModelEvaluationArtifact(is_model_accepted=True,
                                                                  evaluated_model_path=model_file_path)
                self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)

                return model_evaluation_artifact
            
            model_list=[model,model_obj]


            best_model=evaluate_classification_model(model_list=model_list,
                                                     X_train=xtrain,
                                                     y_train=ytrain,
                                                     base_accuracy=self.model_trainer_artifact.model_accuracy)
            
            logging.info(f"Model evaluation completed. model metric artifact: {best_model}")


            if best_model.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=model_file_path,
                                                                    is_model_accepted=True)
                
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=model_file_path,
                                                                    is_model_accepted=False)
            return model_evaluation_artifact


        except Exception as e:
            raise ProjectException(e,sys) from e