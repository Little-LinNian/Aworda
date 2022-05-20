from datetime import datetime
import os
import re
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import DetectPrefix, MatchContent
from graia.ariadne.message.element import At, Plain, Image, Forward, ForwardNode
from graia.ariadne.model import Friend, Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import aiofiles
import random
import ujson
import asyncio
from mkdocs.tests.cli_tests import CliRunner, cli

channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("mkdocs!")]))
async def eat(app: Ariadne, group: Group, member: Member):
    if member.id != 2544704967:
        return
    await app.sendGroupMessage(group, MessageChain.create("Making docs..."))
    cmd = "cd docs && mkdocs build && coscmd upload -r site/ / -r"
    os.system(cmd)
    await app.sendGroupMessage(group, MessageChain.create("Done!"))
    await app.sendGroupMessage(group, MessageChain.create("mkdocs Making docs"))
