from datetime import datetime
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

channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage]))
async def eat(app: Ariadne, group: Group, msg: MessageChain):
    """
    async with aiofiles.open("resource/linnian.json", mode="r") as f:
        data = await f.read()
        data = ujson.loads(data)
    """
    data = {
        "emo": [
            '"如果曾经给你带来痛苦，那不如把他埋葬"',
            '"这里也许曾经是其他人，但现在不是了，也许我还记得他吧"',
            '"今天的你，是不是让我感觉到了一种温暖，让我感觉到了一种温暖"',
            '"沉入大海的时候就能忘记掉一切了吧"',
            '"反正是雨水，蒸发掉算了"',
            '"I̴̘̩̹̖͐͑ ̵̧̣̫͚͎̝̭̩̈̀͜à̴̢̛͓̞͖͌͋̐͐͐̕m̷̖͙͚͎͖̍͝ ̴̻̫̗̩̞̈́̒̏̾̅́w̷̡̩͔͎̺̪͎̰̰̍̏͆̈̎͆̈́͂͂͌a̶͇̺̮̥̚ị̴̠̿̅̈́͒̓̈̍̕͝͝t̴͓̭͎͒͊̏̒̉̾͆į̸̡̞́̑̄̍n̵̹̻̺̠͕͂̈͗́̊̈̎g̶̛͈̗̖͔̭͂̄̏̅̈́̈́ ̵̧̡̻̫̜͛̾̉̄͌͛y̴̮̻̯̟͓̲͎̔͂̏̍̾o̴̳̣̘̣̳̍̂̈́͋̑́u"',
            '"时殇"',
            '"不过是一滩雨水罢了"',
            '"不不不，这里，不是你所谓的终点"',
            '"请你，抱抱我"',
            '"也许在另一个地方"',
            '"我在做着更好的事情吧"',
            '"时̴̡̳̣̟͔͈̓͌̄̄̕͝͝间̶̢͍̣͉͕̪̱͉̲̙̎会̷̛̲͍̻̆̈́̊͋̚冲̸̨̲͓̫̟̐͊͠淡̵̧͚̫̖̟̮̼͍̗̩̿͆一̷̢̼͊̂̀̓̾̚切̶̤͖̰̤͎̈́̀͊͋̽͜的̶̛̣͔̝̫̲͖͕̹̯̪̑，更何况是一堆雨水是吧"',
            '"。̶̢̑̐̆͒̅͊͐͌̚͝。̵͉͓̩͙̭͐̈̂̽̈́͐̐̀͜͝ͅ。̸͇̾͊́͗̔͗͛͆͘。̶̡̨̪̟͈̳̾̓̔̏͝，̵͉̜̖͚͍͎̟̻͈̿̆̔͑͂̏̋̚，̶̧̳̠̩̮̙̞͎̣͐"',
            '"那。。。是什么。"',
            '"我不知道。。。"',
            '"我。。。。。"',
            '"时间，雨水，霖念。。。。。是什么。。。。。"',
            '"什么时候，才会看到尽头"',
            '"没有人会看到和海洋融为一体的雨水龙对吧"',
        ],
    }
    if msg.asDisplay() == "也许":
        await app.sendGroupMessage(
            group, MessageChain.create(random.choice(data["emo"]))
        )
    if random.randint(1, 150) == 44:
        await app.sendGroupMessage(
            group, MessageChain.create(random.choice(data["emo"]))
        )
