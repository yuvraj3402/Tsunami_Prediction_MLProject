import os,sys
from datetime import datetime

ROOT_DIR=os.getcwd()
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


CONFIG_DIR="config"
CONFIG_FILE="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,
                              CONFIG_DIR,
                              CONFIG_FILE)


#pipeline constants
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
PIPELINE_NAME_KEY = "pipeline_name"
ARTIFACT_DIR_KEY = "artifact_dir"



#data ingestion constants
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_DIR_KEY = "data_ingestion"
DATASET_DIR_KEY = "dataset_dir"
DATASET_NAME_KEY="dataset_name"
INGESTED_TRAIN_DIR_KEY = "ingested_train_dir"
INGESTED_TEST_DIR_KEY = "ingested_test_dir"



#data validation constants
DATA_VALIDATION_CONFIG_KEY="data_validation_config"
SCHEMA_DIR_KEY="schema_dir"
SCHEMA_FILE_NAME_KEY="schema_file_name"