from datetime import datetime
from types import MethodDescriptorType
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as IMG
from numpy.core.multiarray import RAISE
from wordcloud import WordCloud, ImageColorGenerator
from dateutil.relativedelta import relativedelta
import jieba.analyse
import re
import asyncio
from graia.ariadne.message.parser.base import MatchContent
from io import BytesIO
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group, Member
from database.message import get_group_history_message, get_member_history_message
from database.model import GroupHistoryMessage
import asyncio

saya = Saya.current()
channel = Channel.current()
global WORKING
WORKING = False


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage], decorators=[MatchContent("#本群本月词云")]
    )
)
async def group_wordcloud_generator(
    app: Ariadne, msg: MessageChain, group: Group, member: Member
):
    messages = await get_group_history_message(
        group.id, datetime.now() - relativedelta(months=1), datetime.now()
    )
    msg_count = len(messages)
    plains = pre_deal(messages)
    frequencies = await asyncio.to_thread(get_frequencies, plains)
    image = await asyncio.to_thread(make_wordcloud, frequencies)
    await app.sendGroupMessage(
        group,
        MessageChain.create(
            [Plain(text=f"本群本月词云\n共 {msg_count} 条消息"), Image(data_bytes=image)]
        ),
    )


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage], decorators=[MatchContent("#我的本月词云")]
    )
)
async def member_wordcloud_generator(
    app: Ariadne, msg: MessageChain, group: Group, member: Member
):
    messages = await get_member_history_message(
        group.id, member.id, datetime.now() - relativedelta(months=1), datetime.now()
    )
    print(messages)
    msg_count = len(messages)
    plains = pre_deal(messages)
    frequencies = await asyncio.to_thread(get_frequencies, plains)
    image = await asyncio.to_thread(make_wordcloud, frequencies)
    await app.sendGroupMessage(
        group,
        MessageChain.create(
            [Plain(text=f"乃的本月词云\n共 {msg_count} 条消息"), Image(data_bytes=image)]
        ),
    )


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage], decorators=[MatchContent("#本群今日词云")]
    )
)
async def group_wordcloud_generator_today(
    app: Ariadne, msg: MessageChain, group: Group, member: Member
):
    messages = await get_group_history_message(
        group.id, datetime.now() - relativedelta(days=1), datetime.now()
    )
    msg_count = len(messages)
    plains = pre_deal(messages)
    frequencies = await asyncio.to_thread(get_frequencies, plains)
    image = await asyncio.to_thread(make_wordcloud, frequencies)
    await app.sendGroupMessage(
        group,
        MessageChain.create(
            [Plain(text=f"本群今日词云\n共 {msg_count} 条消息"), Image(data_bytes=image)]
        ),
    )


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage], decorators=[MatchContent("#我的今日词云")]
    )
)
async def member_wordcloud_generator_today(
    app: Ariadne, msg: MessageChain, group: Group, member: Member
):
    messages = await get_member_history_message(
        group.id, member.id, datetime.now() - relativedelta(days=1), datetime.now()
    )
    msg_count = len(messages)
    plains = pre_deal(messages)
    frequencies = await asyncio.to_thread(get_frequencies, plains)
    image = await asyncio.to_thread(make_wordcloud, frequencies)


def pre_deal(messages):
    content = []
    for message in messages:
        content.append(message.messageChain)
    msg_count = len(messages)
    plains = []
    for message in content:
        for element in message:
            if isinstance(element, Plain):
                plains.append(element.text)
            if isinstance(element, Image):
                plains.append("[图片]")
    return plains


def get_frequencies(msg_list):
    text = "\n".join(msg_list)
    words = jieba.analyse.extract_tags(text, topK=800, withWeight=True)
    return dict(words)


def make_wordcloud(words):
    global WORKING
    if WORKING:
        raise Exception("已经有一个正在运行的词云了，请稍后再试")
    WORKING = True
    wordcloud = WordCloud(
        font_path="font/sarasa-mono-sc-nerd-light.ttf",
        background_color="white",
        max_words=800,
        scale=2,
    )
    wordcloud.generate_from_frequencies(words)
    image = wordcloud.to_image()
    imageio = BytesIO()
    image.save(imageio, format="JPEG", quality=98)
    WORKING = False
    return imageio.getvalue()
