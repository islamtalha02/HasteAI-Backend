import os
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings
from pydantic import SecretStr



class Settings(BaseSettings):
    supabase_url =os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    db_url = os.getenv('DATABASE_URL')
    open_api_key = os.getenv('OPEN_API_KEY')

    class config:
        env_file = ".env"


settings = Settings()


DATABASE_URL = settings.db_url


org
save=> userID, date,

3=>signle user 
4=>  multi organztaion 









