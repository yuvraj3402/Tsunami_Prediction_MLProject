import dill 
import yaml
from tsunami.exception import ProjectException
import os,sys




def read_yaml_file(file_path):
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ProjectException(e,sys) from e