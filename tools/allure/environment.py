from config import settings
import platform
import sys

def create_allure_environment_file():
    os_information = [f'os_info={platform.system()}, {platform.release()}',
                       f'python_version={sys.version}']

    items = [f"{key}={value}" for key, value in settings.model_dump().items()]
    items.extend(os_information)
    properties = '\n'.join(items)

    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w') as file:
        file.write(properties)

