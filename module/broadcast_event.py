import traceback

from io import StringIO
from graia.saya import Saya, Channel
from graia.ariadne.event.message import (
    FriendMessage,
    GroupEvent,
    FriendEvent,
    GroupMessage,
)
from graia.ariadne.event.mirai import BotInvitedJoinGroupRequestEvent
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.broadcast.builtin.event import ExceptionThrowed
from graia.saya.builtins.broadcast.schema import ListenerSchema

from utils.text2image import create_image

saya = Saya.current()
channel = Channel.current()
broadcast = saya.broadcast


async def make_msg_for_unknow_exception(event):
    with StringIO() as fp:
        traceback.print_tb(event.exception.__traceback__, file=fp)
        tb = fp.getvalue()
    msg = str(
        f"异常事件：\n{str(event.event)}"
        + f"\n异常类型：\n{type(event.exception)}"
        + f"\n异常内容：\n{str(event.exception)}"
        + f"\n异常追踪：\n{tb}"
    )
    image = await create_image(msg)
    return MessageChain.create([Plain("发生未捕获的异常\n"), Image(data_bytes=image)])


@channel.use(ListenerSchema([ExceptionThrowed]))
async def except_handle(event: ExceptionThrowed):
    app = Ariadne.get_running(Ariadne)
    if isinstance(event.exception, IndexError):
        return
    if isinstance(event.event, GroupMessage):
        await app.sendGroupMessage(
            event.event.sender.group, await make_msg_for_unknow_exception(event)
        )
    elif isinstance(event.event, FriendMessage):
        await app.sendFriendMessage(
            event.event.sender, await make_msg_for_unknow_exception(event)
        )


@channel.use(ListenerSchema([BotInvitedJoinGroupRequestEvent]))
async def group_invite_handle(app: Ariadne, event: BotInvitedJoinGroupRequestEvent):
    await event.accept()
