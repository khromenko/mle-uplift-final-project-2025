import mlflow
from dotenv import load_dotenv
import os, shutil

def init_mlflow(clean_model_dump_directory: str | None = None):
    '''
    connect to mlflow server with url and env vars - http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}
    
    args
        clean_model_dump_directory - if not None, clean this directory for model dumping (should be empty when making dump)
            path = {clean_model_dump_directory}/model-dump
    
    return
        mlflow.MlflowClient
    '''
    load_dotenv()

    TRACKING_SERVER_HOST = os.getenv('TRACKING_SERVER_HOST')
    TRACKING_SERVER_PORT = os.getenv('TRACKING_SERVER_PORT')

    MLFLOW_SERVER_URL = f'http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}'

    mlflow.set_tracking_uri(MLFLOW_SERVER_URL)
    mlflow.set_registry_uri(MLFLOW_SERVER_URL)

    mlflow_client = mlflow.MlflowClient(mlflow.get_tracking_uri(), mlflow.get_registry_uri())
    
    # clean model dump directory
    if clean_model_dump_directory != None:
        local_model_path = f'{clean_model_dump_directory}/model-dump'
        if os.path.exists(local_model_path):
            shutil.rmtree(local_model_path)
    
    return mlflow_client