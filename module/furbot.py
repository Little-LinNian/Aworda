from hashlib import md5
from time import time
from graia.ariadne.entry import Ariadne, Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import aiohttp
from pydantic import BaseModel

from config import CONFIG

channel = Channel.current()

api: str = f"https://api.tail.icu/"


class FurPic(BaseModel):
    id: int
    name: str
    url: str
    thumb: str


@channel.use(ListenerSchema([GroupMessage]))
async def on_message(app: Ariadne, group: Group, message: MessageChain):
    """根据 毛毛名字 查询毛毛图片"""
    if message.asDisplay().startswith("#来只 "):
        content = message.asDisplay()[4:]
        sign: str = f"api/v2/getFursuitByName-{int(time())}-{CONFIG.furbot.auth_key}"
        path: str = f"api/v2/getFursuitByName/?qq={CONFIG.furbot.auth_qq}&timestamp={int(time())}&sign={md5(sign.encode('utf-8')).hexdigest()}&name={content}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api + path) as resp:
                data: dict = await resp.json()
                if resp.status == 200:
                    furpic = FurPic(**data["data"])
                else:
                    await app.sendGroupMessage(
                        group, MessageChain.create([Plain(data["msg"])])
                    )
                    return
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [
                    Plain(f"嘟嘟嘟\n{furpic.name}"),
                    Image(url=furpic.url.replace("\/", "/")),
                    Plain(f"Power by MircoTailAPI\n Used by LinNian"),
                ]
            ),
        )
