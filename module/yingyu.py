from graia.ariadne.model import Group
import yinglish
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.event.message import GroupMessage
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage]))
async def yingyu(app: Ariadne, message: MessageChain, group: Group):
    if message.asDisplay().startswith("#涩涩 "):
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [Plain(yinglish.chs2yin(message.asDisplay()[4:]))],
            ),
        )
