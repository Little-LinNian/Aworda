from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import aiofiles
import random
import ujson

channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("#今天吃点什么")]))
async def eat(app: Ariadne, group: Group):
    async with aiofiles.open("resource/chidiansha.json", mode="r") as f:
        data = await f.read()
        data = ujson.loads(data)
        await app.sendGroupMessage(
            group, MessageChain.create(random.choice(data["food"]))
        )


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("#今天喝点什么")]))
async def drink(app: Ariadne, group: Group):
    async with aiofiles.open("resource/chidiansha.json", mode="r") as f:
        data = await f.read()
        data = ujson.loads(data)
        await app.sendGroupMessage(
            group, MessageChain.create(random.choice(data["drink"]))
        )
