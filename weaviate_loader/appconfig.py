import environ

@environ.config(prefix="")
class AppConfig:
    weaviate_host = environ.var()
    weaviate_port = environ.var()

config = environ.to_config(AppConfig)
