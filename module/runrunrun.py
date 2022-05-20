from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import MessageEvent
from graia.ariadne.message.parser.base import MatchContent
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()

@channel.use(
        ListenerSchema(
            [MessageEvent],
            decorators=[MatchContent("跑路")]
            )
        )
async def run(app: Ariadne):
    for i in await app.getGroupList():
        await app.quitGroup(i)
