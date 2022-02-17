from .config import FurBotConfig, MiraiApiHttpConfig

import yaml


def init_config(config_path: str):
    global CONFIG
    CONFIG = Config(config_path)
    return CONFIG


class Config:

    mirai: MiraiApiHttpConfig
    furbot: FurBotConfig

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_content = yaml.safe_load(f.read())
        self.mirai = MiraiApiHttpConfig(**config_content["mah"])
        self.furbot = FurBotConfig(**config_content["FurBot"])
