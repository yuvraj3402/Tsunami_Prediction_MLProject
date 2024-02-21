import dill 
import yaml
from tsunami.exception import ProjectException
import os,sys
import pandas as pd



def read_yaml_file(file_path):
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ProjectException(e,sys) from e



def load_data(file_path):
    try:
        df=pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ProjectException(e,sys) from e




def save_object(file_path:str,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise ProjectException(e,sys) from e



def load_object(file_path:str):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise ProjectException(e,sys) from e
        