from typing import List
from arclet.alconna import manager
from arclet.alconna.arpamar import Arpamar
from arclet.alconna.base import ArgUnit, Args
from arclet.alconna import Option
from arclet.alconna import Alconna
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.model import Member, Group
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.behaviour import ListenerSchema
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image
from graia.ariadne.message.parser.alconna import AlconnaDispatcher
from pydantic.main import BaseModel
from utils.text2image import create_image
import aiohttp

channel = Channel.current()
saya = Saya.current()

alc = Alconna(headers=["#"], command="ghrepo", main_args=Args["repo":str])


class License(BaseModel):
    name: str


class GithubRepoInfo(BaseModel):
    name: str
    html_url: str
    description: str
    language: str
    watchers: str
    open_issues: str
    license: License = License(name="没有许可证诶")
    forks: str
    topics: List[str]


github_api = "https://api.github.com/repos/"


@channel.use(
    ListenerSchema(
        [GroupMessage],
        inline_dispatchers=[AlconnaDispatcher(alconna=alc, help_flag="post")],
    )
)
async def ghRepo(app: Ariadne, arp: Arpamar, group: Group):
    if not arp.matched:
        return
    repo = arp.main_args.get("repo")
    if not isinstance(repo, str):
        return
    if repo.count("/") != 1:
        await app.sendGroupMessage(
            group, MessageChain.create("你应该像这样用 < #ghrepo Owner/Repo >")
        )
        return
    async with aiohttp.ClientSession() as cs:
        url = github_api + repo
        async with cs.get(url) as r:
            if r.status != 200:
                await app.sendGroupMessage(
                    group, MessageChain.create(f"错误惹喵\n{await r.text()}")
                )
            else:
                data = GithubRepoInfo(**await r.json())
                text = "\n".join(
                    (
                        "Github 仓库信息喵",
                        f"名字: {data.name}",
                        f"描述:\n    {data.description}",
                        f"语言: {data.language}",
                        f"Issues: {data.open_issues}",
                        f"小星星: {data.watchers}",
                        f"复刻: {data.forks}",
                        f"许可证: {data.license.name}",
                        f" URL: {data.html_url}",
                        "喵",
                    )
                )


                await app.sendGroupMessage(
                    group,
                    MessageChain.create(Image(data_bytes=await create_image(text, 48))),
                )
