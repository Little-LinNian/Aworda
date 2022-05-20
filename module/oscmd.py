from re import sub
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import DetectPrefix, MatchContent
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import asyncio
import aiohttp
import subprocess
from utils import text2image

hitokoto_api = "https://v1.hitokoto.cn/"


channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[DetectPrefix("#sh")]))
async def hitokoto(app: Ariadne, group: Group, member: Member, msg: MessageChain):
    if member.id != 2544704967:
        await app.sendGroupMessage(group, MessageChain.create("您无权使用此功能"))
        return
    cmd = msg.asDisplay().removeprefix("#sh ")
    result = await asyncio.to_thread(subprocess.getoutput, cmd)
    img = await text2image.create_image(result)
    await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=img)))
