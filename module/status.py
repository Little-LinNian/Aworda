from os import rmdir
import psutil
import asyncio

from utils.text2image import create_image
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.element import Image
from graia.ariadne.event.message import GroupMessage
from graia.saya.channel import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


def general_system_status() -> str:
    status = f"""
    系统状态
    内存：{psutil.virtual_memory().percent}%
    CPU：{psutil.cpu_percent()}%
    磁盘：{psutil.disk_usage('/').percent}%
    开机时间：{psutil.boot_time()}
    磁盘余空间：{psutil.disk_usage('/').free/1024/1024/1024}GB
    磁盘总空间：{psutil.disk_usage('/').total/1024/1024/1024}GB
    内存剩余空间：{psutil.virtual_memory().free/1024/1024/1024}GB
    内存总空间：{psutil.virtual_memory().total/1024/1024/1024}GB
    NetIO：{psutil.net_io_counters()}
    DiskIO：{psutil.disk_io_counters()}
    TCP连接数：{len(psutil.net_connections(kind='tcp'))}
    UDP连接数：{len(psutil.net_connections(kind='udp'))}
    """
    return status


@channel.use(ListenerSchema([GroupMessage]))
async def on_group_message(app: Ariadne, group: Group, message: MessageChain):
    if message.asDisplay() == "错误测试":
        raise KeyError("错误测试")
    if message.asDisplay() == "#status":
        status = await asyncio.to_thread(general_system_status)
        image = await create_image(status)
        await app.sendGroupMessage(
            group, MessageChain.create([Image(data_bytes=image)])
        )
