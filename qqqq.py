import aiohttp
from pydantic import BaseModel

class WebGetModel(BaseModel):
    
    @classmethod
    async def from_network(cls, url: str, params: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                return cls.parse_obj(await resp.json())

class WeiBoHotSearch(WebGetModel):
    """
    微博热搜
    """
    ok: int
async def main():
    wb = await WeiBoHotSearch.from_network('https://weibo.com/ajax/side/hotSearch')
    print(wb)

import asyncio
asyncio.run(main())
