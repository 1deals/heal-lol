from tools.configuration import api
from typing import Any, Optional

from munch import Munch
from pydantic import BaseModel
import aiohttp

class Profile(BaseModel):
    url: str
    username: str
    display_name: Optional[str]
    avatar: str
    country: Optional[str] = "Unknown"
    tracks: int
    artists: int
    albums: int
    registered: int
    pro: bool
    scrobbles: int
    nowplaying: Optional[str] = None

class FMHandler():

    async def request(self, slug: Optional[str] = None, **params: Any) -> Munch:
        data: Munch = await aiohttp.ClientSession().request(
            "http://ws.audioscrobbler.com/2.0/",
            params={
                "api_key": api.lastfm,
                "format": "json",
                **params,
            },
            slug=slug,
        )
        return data

    async def profile(self, username: str) -> Profile:
    
        data = await self.request(
            method="user.getinfo",
            username=username,
            slug="user",
        )

        return Profile(
            url=data.url,
            username=data.name,
            display_name=data.realname,
            country=data.country if data.country != "None" else "Unknown",
            avatar=data.image[-1]["#text"],
            tracks=int(data.track_count),
            albums=int(data.album_count),
            artists=int(data.artist_count),
            scrobbles=int(data.playcount),
            registered=int(data.registered.unixtime),
            pro=data.subscriber == "1",
            nowplaying=data.getRecentTracks
        )
    

    async def now_playing(self, username: str) -> Optional[str]:
        data = await self.request(
            method="user.getRecentTracks",
            username=username,
            limit=1
        )
        track_info = data.recenttracks.track[0] if 'recenttracks' in data and 'track' in data.recenttracks else None

        if track_info and track_info.get('@attr', {}).get('nowplaying') == 'true':
            track_name = track_info['name']
            artist_name = track_info['artist']['#text']
            return f"{track_name} by - {artist_name}"

        return None