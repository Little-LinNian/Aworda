import asyncio
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import BroadcastBehaviour
from graia.ariadne.app import Ariadne
from graia.ariadne.model import MiraiSession
from config import init_config


loop = asyncio.new_event_loop()
broadcast = Broadcast(loop=loop)
saya = Saya(broadcast)
saya.install_behaviours(BroadcastBehaviour(broadcast))
config = init_config("./config/config.yml")

with saya.module_context():
    saya.require("module.furbot")
    saya.require("module.status")
    saya.require("module.broadcast_event")
    saya.require("module.github")

ariadne = Ariadne(
    broadcast=broadcast,
    connect_info=MiraiSession(
        config.mirai.host, config.mirai.account, config.mirai.authKey
    ),
)


print(broadcast.listeners)


ariadne.launch_blocking()
