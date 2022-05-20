from arclet.alconna.arpamar import Arpamar
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
from playwright.async_api import async_playwright
from io import BytesIO
from utils import text2image
from exception import 又想注入啊
import asyncio
import aiofiles
import aiocache

github_url = "https://hub.xn--gzu630h.xn--kpry57d/"


@aiocache.cached(ttl=600)
async def shot_github(path: str):
    """"""
    async with async_playwright() as pw:
        browser = await pw.firefox.launch()
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
    await app.sendGroupMessage(
        group, MessageChain.create("如果这是第一次请求，请稍安勿躁\n此功能有 ttl = 600 的缓存，请注意x")
    )
    msg = await shot_github(path)
    if msg:
        try:
            await app.sendGroupMessage(group, msg)
        except Exception as e:
            await app.sendGroupMessage(group, MessageChain.create(str(e)))
    else:
        await app.sendGroupMessage(group, MessageChain.create(Plain("超时啦www")))


subcmd_repo = Subcommand(
    "repo",
    [
        Option(
            "--issues",
            Args["issue":str:"issues_id"],
            help_text="获取仓库 issues 默认为无 可指定issues id",
        ),
        Option(
            "--pulls",
            Args["pull":str:"pulls_id"],
            help_text="获取仓库 pull requests 默认为无 可指定 pulls id",
        ),
        Option(
            "--branch",
            Args["branch":str:"main"],
            help_text="配合 codeview 使用，指定分支 默认为 main",
        ),
        Option("--codeview", Args["path":str:"file_path"], help_text="预览 path"),
    ],
    args=Args["repo":str:"repository"],
    help_text="查看github仓库",
)
alconna = Alconna(
    command="github",
    headers=["#"],
    main_args=Args["username":str],
    options=[subcmd_repo],
    help_text="github截图机xxxx",
    is_fuzzy_match=True,
)

channel = Channel.current()


@channel.use(
    ListenerSchema(
        [GroupMessage],
        inline_dispatchers=[AlconnaDispatcher(alconna=alconna, help_flag="post")],
    )
)
async def repository_repo(msg: MessageChain, app: Ariadne, arp: Arpamar, group: Group):
    if arp.matched and arp.find("repo"):
        username = arp.main_args.get("username")
        repo = arp.query("repo")
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
        [GroupMessage],
        inline_dispatchers=[AlconnaDispatcher(alconna=alconna, help_flag="stay")],
    )
)
async def user(app: Ariadne, arp: Arpamar, group: Group):
    logger.warning(arp)
    if arp.matched:
        name = arp.main_args.get("username")
        slashCount = countSlash(name)
        try:
            assert slashCount == 0
            if not len(arp.subcommands) == 0:
                return
        except AssertionError:
            raise 又想注入啊("又想注入啊")
        await sendMsg(app, group, name)
