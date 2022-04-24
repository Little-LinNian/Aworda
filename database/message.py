from datetime import datetime
from typing import List
from .client import get_client
from .model import GroupHistoryMessage, PrivateHistoryMessage
from beanie import init_beanie
from graia.ariadne.message.chain import MessageChain


async def get_group_history_message(group_id, time_from: datetime, time_to: datetime):
    """
    获取群历史消息
    :param group_id: 群号
    :param time_from: 开始时间
    :param time_to: 结束时间
    :return list: 群历史消息
    """
    await init_beanie(
        database=get_client().message, document_models=[GroupHistoryMessage]
    )
    _message = await GroupHistoryMessage.find(
        GroupHistoryMessage.group == group_id,
        GroupHistoryMessage.time >= time_from,
        GroupHistoryMessage.time <= time_to
    ).to_list()
    messages: List[GroupHistoryMessage] = []
    for i in _message:
        i.messageChain = MessageChain.fromPersistentString(i.message)
        messages.append(i)
    return messages


async def get_private_history_message(user_id, time_from: datetime, time_to: datetime):
    """
    获取私聊历史消息
    :param user_id: 用户号
    :param time_from: 开始时间
    :param time_to: 结束时间
    :return list: 私聊历史消息
    """
    await init_beanie(
        database=get_client().message, document_models=[PrivateHistoryMessage]
    )
    _message = await PrivateHistoryMessage.find(
        PrivateHistoryMessage.sender == user_id,
        PrivateHistoryMessage.time >= time_from,
        PrivateHistoryMessage.time <= time_to
    ).to_list()
    messages: List[PrivateHistoryMessage] = []
    for i in _message:
        i.messageChain = MessageChain.fromPersistentString(i.message)
        messages.append(i)
    return messages


async def get_member_history_message(
    group_id, user_id, time_from: datetime, time_to: datetime
):
    """
    获取群成员历史消息
    :param group_id: 群号
    :param user_id: 用户号
    :param time_from: 开始时间
    :param time_to: 结束时间
    :return list: 群成员历史消息
    """
    await init_beanie(
        database=get_client().message, document_models=[GroupHistoryMessage]
    )
    _message = await GroupHistoryMessage.find(
        GroupHistoryMessage.group == group_id,
        GroupHistoryMessage.sender == user_id,
        GroupHistoryMessage.time >= time_from,
        GroupHistoryMessage.time <= time_to
    ).to_list()
    messages: List[GroupHistoryMessage] = []
    for i in _message:
        i.messageChain = MessageChain.fromPersistentString(i.message)
        messages.append(i)
    return messages
