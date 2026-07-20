import optuna
import os

def create_study(study_name: str, path: str, random_state: int, clear: bool = True):
    '''
    create study, optuna db in the specified 'path'
    
    args
        study_name - study name
        path - where to store optuna.db
        clear - restore optuna.db and return existing experiment or create new
        random_state - random state
    '''

    # check dir
    os.makedirs(path, exist_ok=True)

    db_url = f'sqlite:///{path}/optuna.study.db'

    print('db_url:', db_url)

    if clear and optuna.get_all_study_names(db_url).__contains__(study_name):
        optuna.delete_study(study_name=study_name, storage=db_url)

    sampler = optuna.samplers.TPESampler(seed=random_state)
    study = optuna.create_study(study_name=study_name, storage=db_url, sampler=sampler, load_if_exists=True, direction='maximize')
    return study