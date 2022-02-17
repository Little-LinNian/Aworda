from pydantic import BaseModel


class MiraiApiHttpConfig(BaseModel):
    host: str = ""
    account: int
    authKey: str = ""


class FurBotConfig(BaseModel):
    auth_qq: int
    auth_key: str
