import asyncio
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import BroadcastBehaviour
from graia.ariadne.app import Ariadne
from graia.ariadne.model import MiraiSession
from database.client import init_db
from fastapi import FastAPI
from config import init_config
 

loop = asyncio.new_event_loop()
init_db(loop)
broadcast = Broadcast(loop=loop)
saya = Saya(broadcast)
saya.install_behaviours(BroadcastBehaviour(broadcast))
config = init_config("./config/config.yml")

with saya.module_context():
    saya.require("module.GroupWordCloudGenerator")
    saya.require("module.furbot")
    saya.require("module.exec")
    saya.require("module.ghrepo")
    saya.require("module.status")
    saya.require("module.event")
    saya.require("module.mkdocs")
    saya.require("module.github")
    saya.require("module.rua")
    saya.require("module.aword")
    saya.require("module.cdsm")
    saya.require("module.sign_in")
    saya.require("module.dujitang")
    saya.require("module.yingyu")
    saya.require("module.ylhelper")
    saya.require("module.manage")
    saya.require("module.photo")
    saya.require("module.oscmd")
    saya.require("module.nokia")

ariadne = Ariadne(
    broadcast=broadcast,
    connect_info=MiraiSession(
        config.mirai.host, config.mirai.account, config.mirai.authKey
    ),
)


print(broadcast.listeners)
if __name__ == "__main__":
    ariadne.launch_blocking()
