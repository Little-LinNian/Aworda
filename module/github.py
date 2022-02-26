from arclet.alconna.component import Arpamar
from arclet.alconna.types import Empty
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.ariadne.event.message import GroupMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.alconna import AlconnaDispatcher
from loguru import logger
from arclet.alconna import Alconna, Option, Subcommand
from arclet.alconna import Args
from arclet.alconna import change_help_send_action
from playwright.async_api import async_playwright
from io import BytesIO
from utils import text2image
from exception import 又想注入啊
import asyncio
import aiofiles

github_url = "https://hub.xn--gzu630h.xn--kpry57d/"


async def shot_github(path: str):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        try:
            await asyncio.wait_for(page.goto(github_url + path), timeout=30)
        except asyncio.TimeoutError:
            await browser.close()
            return None
        with BytesIO() as buffer:
            buffer.write(await page.screenshot(full_page=True))
            await browser.close()
            msgChain = MessageChain.create(Image(data_bytes=buffer.getvalue()))
            return msgChain


def countSlash(path: str):
    return path.count("/")


async def sendMsg(app: Ariadne, group: Group, path: str):
    msg = await shot_github(path)
    if msg:
        try:
            await app.sendGroupMessage(group, msg)
        except Exception as e:
            await app.sendGroupMessage(group, Plain(f"{e}"))
    else:
        await app.sendGroupMessage(group, MessageChain.create(Plain("超时啦www")))


subcmd_repo = Subcommand(
    "repo",
        Option("--issues", Args["issue":str:"issues_id"]).help(
            "获取仓库 issues 默认为无 可指定issues id"
        ),
        Option("--pulls", Args["pull":str:"pulls_id"]).help(
            "获取仓库 pull requests 默认为无 可指定 pulls id"
        ),
        Option("--branch", Args["branch":str:"main"]).help(
            "配合 codeview 使用，指定分支 默认为 main"
        ),
        Option("--codeview", Args["path":str:"file_path"]).help("预览 path"),
    args=Args["repo":str:"repository"],
).help("查看github仓库")
alconna = Alconna(
    command="github",
    headers=["#"],
    main_args=Args["username":str],
    options=[subcmd_repo],
).help("github截图机xxxx")

channel = Channel.current()


@channel.use(
    ListenerSchema(
        [GroupMessage], inline_dispatchers=[AlconnaDispatcher(alconna=alconna)]
    )
)
async def repository(msg: MessageChain, app: Ariadne, arp: Arpamar, group: Group):
    if "--help" in msg.asDisplay().split(" "):
        image = await text2image.create_image(alconna.get_help())
        await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=image)))
        return


@channel.use(
    ListenerSchema(
        [GroupMessage], inline_dispatchers=[AlconnaDispatcher(alconna=alconna)]
    )
)
async def repository_repo(msg: MessageChain, app: Ariadne, arp: Arpamar, group: Group):

    if arp.matched and arp.has("repo"):
        username = arp.main_args.get("username")
        repo = arp.get("repo")
        reponame = repo.get("repo")
        basepath = username + "/" + reponame
        logger.success(arp)
        if "issues" in repo:
            issue = repo.get("issues").get("issue")
            if issue == "issues_id":
                await sendMsg(app, group, basepath + "/issues")
            else:
                await sendMsg(app, group, basepath + "/issues/" + issue)
            return
        elif "pulls" in repo:
            pull = repo.get("pulls").get("pull")
            if pull == "pulls_id":
                await sendMsg(app, group, basepath + "/pulls")
            else:
                await sendMsg(app, group, basepath + "/pulls/" + pull)
            return
        elif "codeview" in repo:
            path = repo.get("codeview").get("path")
            try:
                branch = repo.get("branch").get("branch")
            except:
                branch = "main"
            await sendMsg(app, group, basepath + "/blob/" + branch + "/" + path)
            return
        if countSlash(basepath) == 1:
            if "repository" == repo.get("repo"):
                await sendMsg(app, group, username + "?tab=repositories")
                return
            await sendMsg(app, group, basepath)
            return


@channel.use(
    ListenerSchema(
        [GroupMessage], inline_dispatchers=[AlconnaDispatcher(alconna=alconna)]
    )
)
async def user(app: Ariadne, arp: Arpamar, group: Group):
    logger.warning(arp)
    if arp.matched:
        name = arp.main_args.get("username")
        slashCount = countSlash(name)
        try:
            assert slashCount == 0
            assert len(arp.options) == 0
        except AssertionError:
            raise 又想注入啊("又想注入啊")
        await sendMsg(app, group, name)
