import asyncio
from aiohttp import ClientSession
from graia.broadcast import Broadcast
from yarl import URL
from avilla.core import Avilla, event
from avilla.io.core.aiohttp import AiohttpService
from avilla.onebot.config import OnebotWsClientConfig
from avilla.onebot.protocol import OnebotProtocol
from avilla.onebot.service import OnebotService
from avilla.core.selectors import entity
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import BroadcastBehaviour


loop = asyncio.new_event_loop()
broadcast = Broadcast(loop=loop)
saya = Saya(broadcast)
saya.install_behaviours(BroadcastBehaviour(broadcast))

with saya.module_context():
    saya.require("module.sign_in")

avilla = Avilla(
    broadcast=broadcast,
    protocols=[OnebotProtocol],
    services=[
        AiohttpService(ClientSession(loop=loop)),
    ],
    config={
        OnebotService: {
            entity.account['2954819930']: OnebotWsClientConfig(
                url=URL("ws://localhost:6700/"),
                access_token=None
            )
        }
    }
)


loop.run_until_complete(avilla.launch())
