from tsunami.utils import load_object
from tsunami.exception import ProjectException
import os,sys
import pandas as pd




class TsunamiData:

    def __init__(self,MONTH,
                 COUNTRY,	
                 REGION,
                 CAUSE,
                 EQ_MAGNITUDE,
                 EQ_DEPTH,
                 TS_INTENSITY) -> None:
        try:
            self.MONTH=MONTH
            self.COUNTRY=COUNTRY	
            self.REGION=REGION	
            self.CAUSE=	CAUSE
            self.EQ_MAGNITUDE=EQ_MAGNITUDE	
            self.EQ_DEPTH=EQ_DEPTH	
            self.TS_INTENSITY=TS_INTENSITY
        except Exception as e:
            raise ProjectException(e,sys) from e



    def get_data_as_dict(self):
        try:
            input_data={"MONTH":[self.MONTH],
                        "COUNTRY":[self.COUNTRY],
                        "REGION":[self.REGION],
                        "CAUSE":[self.CAUSE],
                        "EQ_MAGNITUDE":[self.EQ_MAGNITUDE],
                        "EQ_DEPTH":[self.EQ_DEPTH],
                        "TS_INTENSITY":[self.TS_INTENSITY]
            }
                    
            return input_data
        except Exception as e:
            raise ProjectException(e,sys) from e
        


    def get_data_as_dataframe(self):
        try:
            data=self.get_data_as_dict()
            dataframe=pd.DataFrame(data)

            return dataframe
        except Exception as e:
            raise ProjectException(e,sys) from e
        

class DataPredictor:


    def __init__(self,model_dir):
        try:
            self.model_dir=model_dir
        except Exception as e:
            raise ProjectException(e,sys) from e


    def get_latest_model_path(self):
        try:
            folder_name=list(map(int, os.listdir(self.model_dir)))
            latest_model_dir=os.path.join(self.model_dir,f"{max(folder_name)}")
            file_name=os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise ProjectException(e,sys) from e
        
    def predict(self,X):
        try:
            model_path=self.get_latest_model_path()
            model=load_object(file_path=model_path)
            median_house_value=model.predict(X)
            return median_house_value
        except Exception as e:
            raise ProjectException(e,sys) from e