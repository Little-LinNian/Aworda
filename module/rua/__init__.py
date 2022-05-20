import asyncio
from io import BytesIO
from os import path
from PIL import Image as im
from .rua_data.data_source import generate_gif
import aiohttp

import os
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema


from graia.ariadne.app import Ariadne
from graia.ariadne.message.element import Image, Plain, At
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.model import Group, Member

saya = Saya.current()
channel = Channel.current()


data_dir = os.path.join(path.dirname(__file__), "rua_data/data")


async def ruaer(id):
    url = f"http://q1.qlogo.cn/g?b=qq&nk={id}&s=160"
    async with aiohttp.request("get", url) as resp:
        resp_cont = await resp.read()
    avatar = im.open(BytesIO(resp_cont))
    output = await asyncio.to_thread(generate_gif, data_dir, avatar)
    return output


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def rua(app: Ariadne, member: Member, group: Group, msg: MessageChain):
    if msg.asDisplay().startswith("rua") or msg.asDisplay().endswith("rua"):

        qid = msg.get(At)[0].target
        data = await ruaer(qid)
        ph = Image(data_bytes=data)
        await app.sendGroupMessage(group, MessageChain.create([ph]))
