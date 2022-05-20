from datetime import datetime
import time
import traceback

from io import StringIO
from typing import Deque
from graia.ariadne.model import Friend, Group, Member
from graia.ariadne import get_running
from graia.saya import Saya, Channel
from graia.ariadne.event.message import (
    FriendMessage,
    GroupEvent,
    FriendEvent,
    GroupMessage,
    MessageEvent,
)
from graia.ariadne.message.parser.base import DetectPrefix, MatchContent
from graia.ariadne.event.mirai import BotInvitedJoinGroupRequestEvent, NudgeEvent
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image, Plain, Poke
from graia.broadcast.builtin.event import ExceptionThrowed
from graia.ariadne.message.parser.alconna import AlconnaHelpMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from pydantic.networks import NameEmail
from database.model import GroupHistoryMessage, PrivateHistoryMessage
from database.client import get_client
from beanie import init_beanie
from utils.text2image import create_image
from loguru import logger

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
async def except_handle(app: Ariadne, event: ExceptionThrowed):
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


@channel.use(ListenerSchema([AlconnaHelpMessage]))
async def alconna_help_handle(help_string: str, source_event: MessageEvent):
    app = get_running()
    print(help_string)
    print(source_event)
    image = await create_image(help_string)
    if isinstance(source_event, GroupMessage):
        await app.sendGroupMessage(
            source_event.sender.group,
            MessageChain.create(Image(data_bytes=image)),
        )


@channel.use(ListenerSchema([GroupMessage]))
async def group_message_handle(
    app: Ariadne, group: Group, member: Member, msg: MessageChain
):
    await init_beanie(
        database=get_client().message, document_models=[GroupHistoryMessage]
    )
    await GroupHistoryMessage(
        group=group.id,
        sender=member.id,
        message=msg.asPersistentString(binary=False),
        time=datetime.now(),
    ).insert()
    logger.success(f"[Database] Message has been saved to database")


@channel.use(ListenerSchema([FriendMessage]))
async def friend_message_handle(app: Ariadne, friend: Friend, msg: MessageChain):
    await init_beanie(
        database=get_client().message, document_models=[PrivateHistoryMessage]
    )
    await PrivateHistoryMessage(
        sender=friend.id,
        message=msg.asPersistentString(binary=False),
        time=datetime.now(),
    ).insert()
    logger.success(f"[Database] Message has been saved to database")


@channel.use(ListenerSchema([NudgeEvent]))
async def nudge_handle(app: Ariadne, event: NudgeEvent):
    if event.target == app.account:
        if event.group_id:
            await app.sendNudge(event.supplicant, event.group_id)
        else:
            await app.sendNudge(event.supplicant)


help_text = open("help.txt", "r").read()


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("菜单")]))
async def get_help(app: Ariadne, group: Group):
    image = await create_image(help_text)
    await app.sendGroupMessage(
        group, MessageChain.create([Plain("小霖念菜单"), Image(data_bytes=image)])
    )


@channel.use(ListenerSchema([GroupMessage], decorators=[DetectPrefix("#循环十遍@")]))
async def _(app: Ariadne, msg: MessageChain, group: Group, member: Member):
    if not member.id == 2544704967:
        return
    at = msg.getFirst(At)
    for i in range(10):
        await app.sendGroupMessage(group, MessageChain.create(At(target=at.target)))
