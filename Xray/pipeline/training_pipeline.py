from Xray.component.data_ingestion import DataIngestion
from Xray.component.data_transformation import DataTransformation
from Xray.component.model_training import ModelTrainer
from Xray.entity.artifacts_entity import DataIngestionArtifact,DataTransformationArtifact,ModelTrainerArtifact
from Xray.entity.config_entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
from Xray.exception import XRayException
from Xray.logger import logging
import sys

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        #print(self.data_ingestion_config)
        
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:

            logging.info("Getting the data from s3 bucket")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from s3")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise XRayException(e, sys)
        
    def start_data_transformation(self,data_ingestion_artifacts : DataIngestionArtifact) -> DataTransformationArtifact:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
           logging.info("strating Data transformation")
           data_transformation=DataTransformation(
               data_transformation_config= self.data_transformation_config,
               data_ingestion_artifact=data_ingestion_artifacts)                                            
           
           data_transformation_artifats=(
               data_transformation.initiate_data_transformation()
           )
           logging.info("Exited the start_data_transformation method pf TrainPipeline class"
                        )
           return data_transformation_artifats

        except Exception as e:
            raise XRayException(e,sys)
        
    def start_model_trainer(
        self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        logging.info("Entered the start_model_trainer method of TrainPipeline class")

        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            logging.info("Exited the start_model_trainer method of TrainPipeline class")

            return model_trainer_artifact

        except Exception as e:
            raise XRayException(e, sys)
           
if __name__ == "__main__":
    train_pipeline=TrainPipeline()
    data_ingestion_artifacts=train_pipeline.start_data_ingestion()
    data_transformation_artifacts=(
        train_pipeline.start_data_transformation(data_ingestion_artifacts)
        )
    model_trainer_artifacts=train_pipeline.start_model_trainer(data_transformation_artifacts)
    