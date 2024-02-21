from tsunami.exception import ProjectException
from tsunami.logger import logging
from collections import namedtuple
from tsunami.utils import read_yaml_file
import os,sys
import importlib
from typing import List
from sklearn.metrics import accuracy_score




InitializedModelDetail = namedtuple("InitializedModelDetail",
                                    ["model_serial_number", "model"])



GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                             "model",
                                                             "best_model",
                                                             "best_parameters",
                                                             "best_score",
                                                             ])


ModelAccuracy = namedtuple("ModelAccuracy",["model",
                                            "accuracy_score",
                                            ])



BestModel = namedtuple("BestModel", ["model_serial_number",
                                     "model",
                                     "best_model",
                                     "best_parameters",
                                     "best_score", ])




MetricInfoArtifact = namedtuple("MetricInfoArtifact",
                                ["model_name", 
                                 "model_object", 
                                 "model_accuracy", 
                                 "index_number"])








def evaluate_classification_model(model_list:list,X_train, y_train,base_accuracy) -> MetricInfoArtifact:
    try:
        index_number=0

        for model in model_list:
            model_name = str(model) 

            y_pred=model.predict(X_train)

            model_accuracy=accuracy_score(y_true=y_train,y_pred=y_pred)


            if model_accuracy>=base_accuracy:
                base_accuracy=model_accuracy
                metric_info_artifact=MetricInfoArtifact(model_name=model_name, 
                                                        model_object=model,                                                    
                                                        model_accuracy=model_accuracy, 
                                                        index_number=index_number)
                logging.info(f"Acceptable model found {metric_info_artifact}. ")
           
            index_number += 1
        if metric_info_artifact is None:
            logging.info(f"No model found with higher accuracy than base accuracy")
        return metric_info_artifact                
    except Exception as e:
        raise ProjectException(e,sys) from e







GRID_SEARCH_KEY="grid_search"
CLASS_KEY="class"
MODULE_KEY="module"
PARAMS_KEY="params"
MODEL_SELECTION_KEY="model_selection"
SEARCH_PARAM_GRID_KEY="search_param_grid"

class ModelFactory:


    def __init__(self,model_config_path) -> None:
        self.config=read_yaml_file(file_path=model_config_path)


        self.model_initialization= dict(self.config[MODEL_SELECTION_KEY])

        
        self.initialized_model_list = None
        self.accuracy_searched_model_list = None





    def update_properties(self,model_obj,properties_dict:dict):
        try:
            logging.info(f"updating properties of the {model_obj}")
            for key,value in properties_dict.items():
                setattr(model_obj,key,value)
            return model_obj
        except Exception as e:
            raise ProjectException(e,sys) from e
        


    
    def import_modle_class(self,module_name,class_name):
        try:
            module=importlib.import_module(module_name)

            logging.info(f"performing from {module} import {class_name}")
            model_obj=getattr(module,class_name)
            return model_obj
        except Exception as e:
            raise ProjectException(e,sys) from e
        




    def get_initialized_modle_list(self)->List[InitializedModelDetail]:
        try:
            self.initialized_model_list=[]
            model_list_config=self.model_initialization
            for model_serial_number in model_list_config.keys():
                model_properties=self.model_initialization[model_serial_number]
                model_ref=self.import_modle_class(module_name=model_properties[MODULE_KEY],class_name=model_properties[CLASS_KEY])
                model=model_ref()

                if PARAMS_KEY in model_properties:
                    model=self.update_properties(model_obj=model,properties_dict=dict(model_properties[PARAMS_KEY]))


                model_initialization_config=InitializedModelDetail(model_serial_number=model_serial_number, 
                                                                   model=model )   


                self.initialized_model_list.append(model_initialization_config)

            return self.initialized_model_list


        except Exception as e:
            raise ProjectException(e,sys) from e
        



    def get_accuracy_for_the_models(self,initialized_model_list:List[InitializedModelDetail],input_features,output_features)->List[ModelAccuracy]:
        try:
            self.accuracy_searched_model_list=[]
            for initialized_model in initialized_model_list:
                model1=initialized_model.model.fit(input_features,output_features)
                pred=model1.predict(input_features)
                accuracy=accuracy_score(y_true=output_features,y_pred=pred)

                model_accuracy=ModelAccuracy(model=model1,
                                             accuracy_score=accuracy)
                
                self.accuracy_searched_model_list.append(model_accuracy)

            return self.accuracy_searched_model_list
                

        except Exception as e:
            raise ProjectException(e,sys) from e()



    
    def get_best_model_from_initialized_model_list(self, accuracy_model_list: List[ModelAccuracy],
                                                          base_accuracy)-> BestModel:
        try:
            best_model = None
            for initialized_best_model in accuracy_model_list:
                if base_accuracy < initialized_best_model.accuracy_score:
                    logging.info(f"Acceptable model found:{initialized_best_model}")
                    base_accuracy = initialized_best_model.accuracy_score
                    best_model = initialized_best_model


            if not best_model:
                raise Exception(f"None of Model has base accuracy: {base_accuracy}")
            logging.info(f"Best model: {best_model}")
            return best_model
        except Exception as e:
            raise ProjectException(e, sys) from e
        


 
    def get_best_model(self,x,y,base_accuracy)->BestModel:
        try:


            logging.info("Started Initializing model from config file")
            initialized_model_list=self.get_initialized_modle_list()
            logging.info(f"Initialized model: {initialized_model_list}")


            accuracy_model_list=self.get_accuracy_for_the_models(initialized_model_list=initialized_model_list, 
                                                                             input_features=x, 
                                                                             output_features=y)


            best_model=self.get_best_model_from_initialized_model_list(accuracy_model_list=accuracy_model_list,
                                                                        base_accuracy=base_accuracy)

            return best_model
        except Exception as e:
            raise ProjectException(e,sys) from e