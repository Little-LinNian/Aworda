from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from .nokia import generate_image
import asyncio
import aiohttp

hitokoto_api = "https://v1.hitokoto.cn/"


channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[DetectPrefix("#诺基亚")]))
async def hitokoto(app: Ariadne, group: Group, msg: MessageChain):
    content = msg.asDisplay().split("#诺基亚 ")[1]
    image = await asyncio.to_thread(generate_image, content)
    await app.sendGroupMessage(group, MessageChain.create([Image(data_bytes=image)]))
