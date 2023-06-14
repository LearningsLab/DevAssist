#GetEnvironmentVariables
# This service will be used to get the environment variables passed on to the container.
import os
from dotenv import load_dotenv

load_dotenv()

class GetEnvVariables:
    def __init__(self):
        pass
    
    def get_env_variable(self,key):
        env_variable_value = os.environ[key]
        return env_variable_value