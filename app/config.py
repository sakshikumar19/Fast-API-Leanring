from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
    
settings = Settings()

# We create a pydantic model for env variables because we don't want to be validating the existence of each env variable
# thus if a wrong datatype is provided or there is no default + nothing provided by user, there will be validation errors thrown by pydantic
# don't worry about the case mismatch in env variables. Pydantic converts to lower case anyway to simplify things and the norm is to keep env variables in caps