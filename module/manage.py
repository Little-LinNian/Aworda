from arclet.alconna import manager
from arclet.alconna.arpamar import Arpamar
from arclet.alconna.base import ArgUnit, Args
from arclet.alconna.main import Option
from arclet.alconna.main import Alconna
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.model import Member, Group
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.behaviour import ListenerSchema
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image
from graia.ariadne.message.parser.alconna import AlconnaDispatcher
from arclet.alconna.arpamar.duplication import AlconnaDuplication, OptionStub
from utils.text2image import create_image

channel = Channel.current()
saya = Saya.current()

alc = Alconna(
    headers=["#"],
    command="模组",
    options=[
        Option("安装", Args["模组名":str]),
        Option("卸载", Args["模组名":str]),
        Option("重载", Args["模组名":str]),
        Option("查看所有模组"),
    ],
    help_text="管理小霖念的模组",
)


class SayaManage(AlconnaDuplication):

    安装: OptionStub
    卸载: OptionStub
    重载: OptionStub
    查看所有模组: OptionStub


class SayaManager:
    def __init__(self):
        ...

    def install(self, name):
        if name in saya.channels:
            return "模组已存在"
        try:
            with saya.module_context():
                saya.require(name)
            return "模组安装成功"
        except Exception as e:
            return f"模组安装失败：{str(e)}"

    def uninstall(self, name):
        if name not in saya.channels:
            return "模组不存在"
        try:
            saya.uninstall_channel(saya.channels.get(name))
            return "模组卸载成功"
        except Exception as e:
            return f"模组卸载失败：{str(e)}"

    def module_list(self):
        return "模组列表：\n" + "\n".join(saya.channels.keys())

    def reload(self, name):
        if name not in saya.channels:
            return "模组不存在"
        try:
            with saya.module_context():
                saya.reload_channel(saya.channels.get(name))
            return "模组重载成功"
        except Exception as e:
            return f"模组重载失败：{str(e)}"


@channel.use(
    ListenerSchema(
        [GroupMessage],
        inline_dispatchers=[AlconnaDispatcher(alconna=alc, help_flag="post")],
    )
)
async def sayaM(
    app: Ariadne, dup: SayaManage, group: Group, member: Member, arp: Arpamar
):
    if not arp.matched:
        return
    if member.id != 2544704967:
        await app.sendGroupMessage(
            group, MessageChain.create([Plain("你不是超级管理员，无法使用该命令")])
        )
        return
    manager = SayaManager()
    if dup.安装.available:
        arg = dup.安装.args[0]
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(manager.install(arg))])
        )
    if dup.卸载.available:
        arg = dup.卸载.args[0]
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(manager.uninstall(arg))])
        )
    if dup.重载.available:
        arg = dup.重载.args[0]
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(manager.reload(arg))])
        )
    if dup.查看所有模组.available:
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [Image(data_bytes=await create_image(manager.module_list()))]
            ),
        )
