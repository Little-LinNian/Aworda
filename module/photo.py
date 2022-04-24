from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Group
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image as MiraiImage, Plain
from graia.ariadne.message.parser.alconna import AlconnaDispatcher, Alconna
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.event.message import GroupMessage
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import asyncio


def make_black_white(image: bytes) -> bytes:
    """
    Convert image to black and white
    :param image: image in bytes
    :return: image in bytes
    """
    img = Image.open(BytesIO(image))
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < 128 else 255, "1")
    img_io = BytesIO()
    img.save(img_io, "JPEG")
    return img_io.getvalue()


def text_at_bottom(image: bytes, text: str) -> bytes:
    """
    Add text at bottom of image
    :param image: image in bytes
    :param text: text to add
    :return: image in bytes
    """
    img = Image.open(BytesIO(image))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font/sarasa-mono-sc-nerd-light.ttf", size=80)
    # add blank at bottom
    draw.text((0, img.height - 20), " ", font=font, fill="black")
    # add text in bottom
    draw.text((0, img.height - 20), text, font=font, fill="white")
    img_io = BytesIO()
    img.save(img_io, "JPEG")
    return img_io.getvalue()


channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], decorators=[DetectPrefix("#黑白照片")]))
async def black_white(app: Ariadne, message: MessageChain, group: Group):
    _image: MiraiImage = message.getFirst(MiraiImage)
    if _image is None:
        return
    _image = await _image.get_bytes()
    image = await asyncio.to_thread(make_black_white, _image)
    await app.sendGroupMessage(
        group, MessageChain.create([Plain("完成啦wwwwww"), MiraiImage(data_bytes=image)])
    )


@channel.use(ListenerSchema([GroupMessage], decorators=[DetectPrefix("#底部写字")]))
async def text_bottom(app: Ariadne, message: MessageChain, group: Group):
    _image: MiraiImage = message.getFirst(MiraiImage)
    if _image is None:
        return
    _image = await _image.get_bytes()
    text = message.getFirst(Plain).text.split(" ")[1]
    image = await asyncio.to_thread(text_at_bottom, _image, text)
    await app.sendGroupMessage(
        group, MessageChain.create([Plain("完成啦wwwwww"), MiraiImage(data_bytes=image)])
    )
