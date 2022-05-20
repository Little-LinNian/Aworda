import re
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

dujitang_api = "https://du.shadiao.app/api.php"


async def get_djt():
    async with aiohttp.ClientSession() as session:
        async with session.get(dujitang_api) as resp:
            return await resp.text() if resp.status == 200 else "获取失败xw"


channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("#毒鸡汤")]))
async def hitokoto(app: Ariadne, group: Group):
    await app.sendGroupMessage(group, MessageChain.create(await get_djt()))
