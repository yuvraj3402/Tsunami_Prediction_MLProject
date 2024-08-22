from tsunami.exception import ProjectException 
from tsunami.logger import logging 
import os,sys
from tsunami.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from tsunami.entity.config_entity import ModelTrainerConfig
from tsunami.utils import load_data,load_object,save_object
from tsunami.entity.model_factory import ModelFactory,evaluate_classification_model,InitializedModelDetail,MetricInfoArtifact
from typing import List





class ModelPredictor:

    def __init__(self,preprocessing_obj,model_object) -> None:
        try:
            self.preprocessing_obj=preprocessing_obj
            self.model_object=model_object
        except Exception as e:
            raise ProjectException(e,sys) from e
    
    def predict(self,input_feature):
        try:
            transformed_features=self.preprocessing_obj.transform(input_feature)
            predicted_values=self.model_object.predict(transformed_features)

            return predicted_values
        except Exception as e:
            raise ProjectException(e,sys) from e







class ModelTrainer:


    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig) -> None:
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config 
        except Exception as e:
            raise ProjectException(e,sys) from e


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:


            logging.info(f"Loading transformed train dataset")
            x_train=load_object(file_path=self.data_transformation_artifact.transformed_train_file_path)


            logging.info(f"Loading target feature dataset")
            y_train=load_data(file_path=self.data_transformation_artifact.target_feature_file_path)
            y_train=y_train.values.ravel() 




            model_config_file_path=self.model_trainer_config.model_config_file_path
            

            base_accuracy=self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy: {base_accuracy}")


            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory_obj=ModelFactory(model_config_path=model_config_file_path)


            best_model=model_factory_obj.get_best_model(x=x_train,y=y_train,base_accuracy=base_accuracy)
            logging.info(f"Best model found on training dataset: {best_model}")



            initialized_model_list:List[InitializedModelDetail]=model_factory_obj.initialized_model_list

            logging.info(f"Extracting initialized model list.")
            model_list=[initilaized_models.model for initilaized_models in initialized_model_list]


            logging.info(f"Evaluation on training dataset")
            evaluated_model:MetricInfoArtifact=evaluate_classification_model(model_list=model_list,X_train=x_train,y_train=y_train,base_accuracy=base_accuracy)
            logging.info(f"Best found model on training dataset.")



            model_obj=evaluated_model.model_object
            prepocessing_obj=load_object(self.data_transformation_artifact.preprocessed_object_file_path)



            model_predictor=ModelPredictor(preprocessing_obj=prepocessing_obj,
                                           model_object=model_obj)
            

            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=model_predictor)


            model_accuracy=evaluated_model.model_accuracy


            model_trainer_artifact=ModelTrainerArtifact(is_trained=True, 
                                                        trained_model_file_path=trained_model_file_path, 
                                                        model_accuracy=model_accuracy)
            
            
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise ProjectException(e,sys) from e