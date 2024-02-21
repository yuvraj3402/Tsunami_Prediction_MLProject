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


#data transformation constants
DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_DIR="data_transformation"
TRANSFORMED_DIR_KEY="transformed_dir"
TRANSFORMED_TRAIN_DIR_KEY="transformed_train_dir"
TARGET_FEATURE_DIR_KEY="target_feature_dir"
PREPROCESSING_DIR_KEY="preprocessing_dir"
PREPROCESSED_OBJECT_FILE_NAME_KEY="preprocessed_object_file_name"


#schema file constants
COLUMNS_KEY="columns"
NUMERICAL_COLUMNS_KEY="numerical_columns"
CATEGORICAL_COLUMNS_KEY="categorical_columns"
DROP_FEATURES_KEY="drop_features"
TARGET_COLUMN_KEY="target_column"
UPDATED_CATEGORICAL_COLUMNS_KEY="updated_categorical_columns"
UPDATED_NUMERICAL_COLUMNS_KEY="updated_numerical_columns"


#columns to transform
CAUSE_COLUMN_CONSTANT="CAUSE"
UNKNOWN_DROP_CONSTANT="Unknown"
MONTH_COLUMN_CONSTANT="MONTH"


#model trainer constants

MODEL_TRAINER_CONFIG_KEY="model_trainer_config"
TRAINED_MODEL_DIR_KEY="trained_model_dir"
MODEL_TRAINER_DIR="model_trainer"
MODEL_FILE_NAME_KEY="model_file_name"
BASE_ACCURACY_KEY="base_accuracy"
MODEL_CONFIG_DIR_KEY="model_config_dir"
MODEL_CONFIG_FILE_NAME_KEY="model_config_file_name"
