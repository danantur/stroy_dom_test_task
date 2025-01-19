import os

import yaml

SETTINGS: dict # Настройки запуска для проекта, заданные в deploy_settings

with open(f"../deploy_settings.yaml", 'r', encoding='utf-8') as file:
    SETTINGS = yaml.load(file, Loader=yaml.FullLoader)

MODELS_SETTINGS = SETTINGS["models"]

USERS_SETTINGS = MODELS_SETTINGS["Users"]
ROLES_SETTINGS = MODELS_SETTINGS["Roles"]


SERVER_SETTINGS = SETTINGS["server"]