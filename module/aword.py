from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import asyncio
import aiohttp

hitokoto_api = "https://v1.hitokoto.cn/"


async def get_hitokoto():
    async with aiohttp.ClientSession() as session:
        async with session.get(hitokoto_api) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["hitokoto"]
            else:
                return "获取失败"


channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("#一言")]))
async def hitokoto(app: Ariadne, group: Group):
    await app.sendGroupMessage(group, MessageChain.create(await get_hitokoto()))
