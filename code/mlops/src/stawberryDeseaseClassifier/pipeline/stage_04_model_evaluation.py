
import os
from src.stawberryDeseaseClassifier.config.configuration import ConfigurationManager
from src.stawberryDeseaseClassifier.components.model_evaluation_mlfow import Evaluation
from src.stawberryDeseaseClassifier.utils import logger

STAGE_NAME = "Evaluation stage"


class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        eval_config = config.get_evaluation_config()
        evaluation = Evaluation(eval_config)
        evaluation.evaluation()
        evaluation.save_score()
        # evaluation.log_into_mlflow()


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/Hassen-Elmahrouk/CoTProject.mlflow"
        os.environ["MLFLOW_TRACKING_USERNAME"] = "Hassen-Elmahrouk"
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "92f39719f5c80628067c008d65ad4bdfd797d941"
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
