from datetime import datetime
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import DetectPrefix, MatchContent
from graia.ariadne.message.element import At, Plain, Image, Forward, ForwardNode
from graia.ariadne.model import Friend, Group, Member
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


@channel.use(ListenerSchema([GroupMessage], decorators=[DetectPrefix("showtime")]))
async def showtime(app: Ariadne, group: Group, msg: MessageChain):
    ats = msg.get(At)
    forwards = []
    forwards.append(
        ForwardNode(
            target=await app.getMember(group, ats[0].target),
            time=datetime.now(),
            message=MessageChain.create(At(ats[1].target), Plain(" 傻逼")),
        )
    )
    forwards.append(
        ForwardNode(
            target=await app.getMember(group, ats[1].target),
            time=datetime.now(),
            message=MessageChain.create(At(ats[0].target), Plain(" ?居然敢骂我傻逼")),
        )
    )
    await app.sendGroupMessage(group, MessageChain.create(Forward(nodeList=forwards)))
