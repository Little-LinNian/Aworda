import asyncio
import time
from graia.ariadne.event.message import GroupMessage
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Group
from graia.ariadne.message.parser.base import MatchContent
from graia.scheduler.saya.schema import SchedulerSchema
from graia.scheduler.timers import every_hours
from playwright.async_api import async_playwright
from loguru import logger

channel = Channel.current()
saya = Saya.current()


url = [
    "http://yinlan.furbot.icu/",
    "http://yinlan.furbot.icu/startUp/",
    "http://yinlan.furbot.icu/auto",
]
cache = []


async def shot_yinlan_docs():
    if not cache:
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            page = await browser.new_page()
            for i in url:
                await page.goto(i)
                img = await page.screenshot(full_page=True)
                cache.append(img)
            await browser.close()
    return cache


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("洇岚快速上手")]))
async def yinlan(app: Ariadne, message: MessageChain, group: Group):
    url = "http://yinlan.furbot.icu/"
    await app.sendGroupMessage(
        group,
        MessageChain.create(
            [
                Image(data_bytes=cache[0]),
                Image(data_bytes=cache[1]),
            ]
        ),
    )


@channel.use(ListenerSchema([GroupMessage], decorators=[MatchContent("洇岚直播推送")]))
async def yinlan_live(app: Ariadne, message: MessageChain, group: Group):
    await app.sendGroupMessage(
        group,
        MessageChain.create(
            [
                Image(data_bytes=cache[2]),
            ]
        ),
    )


i = 0


async def yinlan_live_update():
    while True:
        cache.clear()
        await shot_yinlan_docs()
        await asyncio.sleep(60 * 30)
        logger.info("洇岚文档截图更新完成")
        if i == 0:
            logger.info("洇岚直播推送更新首次完成")
            time.sleep(5)


loop = saya.broadcast.loop
loop.create_task(shot_yinlan_docs())
