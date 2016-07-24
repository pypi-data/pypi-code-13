import aiohttp

from osuapi import endpoints

mode = {
    "osu!": 0,
    "taiko": 1,
    "ctb": 2,
    "mania": 3
}


class Osu:
    def __init__(self, key, mode):
        self.key = key
        self.mode = mode

    async def get_user(self, username):
        """
        Enter a name and receive stats
        """
        params = {
            "k": self.key,
            "u": username,
            "m": self.mode
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoints.USER, params=params) as f:
                return await f.json()

    async def get_beatmaps(self, beatmapset_id, limit=10):
        params = {
            "k": self.key,
            "s": beatmapset_id,
            "limit": self.mode
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoints.BEATMAP_SET, params=params) as f:
                return await f.json()

    async def get_user_best(self, username):
        params = {
            "k": self.key,
            "u": username,
            "m": self.mode
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoints.USER_BEST, params=params) as f:
                return await f.json()
