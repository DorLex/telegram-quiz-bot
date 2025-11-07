from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str

    model_config = SettingsConfigDict(
        # если в docker-контейнер были переданы переменные заранее, BaseSettings НЕ перетрет их из .env
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


config: Settings = Settings()
