from datetime import datetime
from typing import Optional
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
import beanie


class GroupHistoryMessage(beanie.Document):

    sender: int
    group: int
    message: str
    time: datetime
    messageChain: Optional[MessageChain] = None


class PrivateHistoryMessage(beanie.Document):

    sender: int
    message: str
    time: datetime
    messageChain: Optional[MessageChain] = None
