from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Dict, List
from aiohttp import web
from aiohttp.abc import AbstractAccessLogger
from aiohttp.web import BaseRequest, Request, Response, StreamResponse
from discord.ext.commands import Cog
from loguru import logger as log
import config
from tools.heal import Heal
from cashews import cache
from aiohttp_cors import setup as cors_setup, ResourceOptions
import time
cache.setup("mem://")

class AccessLogger(AbstractAccessLogger):
    def log(
        self: "AccessLogger",
        request: BaseRequest,
        response: StreamResponse,
        time: float,
    ) -> None:
        self.logger.info(
            f"Request for {request.path!r} with status of {response.status!r}."
        )

def route(pattern: str, method: str = "GET") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self: "Network", request: Request) -> None:
            try:
                return await func(self, request)
            except Exception as e:
                log.error(f"Error handling request for {pattern}: {e}")
                return web.json_response({"error": "Internal server error"}, status=500)
        wrapper.pattern = pattern
        wrapper.method = method
        return wrapper
    return decorator

class Network(Cog):
    def __init__(self, bot: Heal):
        self.bot: Heal = bot
        self.app = web.Application(logger=log)

        # Set up CORS
        self.cors = cors_setup(self.app, defaults={
            "*": ResourceOptions(
                allow_credentials=False,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })

        # Add routes
        for module in dir(self):
            route = getattr(self, module)
            if not hasattr(route, "pattern"):
                continue
            resource = self.app.router.add_route(route.method, route.pattern, route)
            self.cors.add(resource)  # Enable CORS for this route
            log.info(f"Added route for {route.pattern!r} ({route.method}).")

        # Add root route
        root_resource = self.app.router.add_get("/", self.root_handler)
        self.cors.add(root_resource)

    async def root_handler(self, request):
        return web.json_response({
            "commands": self.bot.command_count,
            "latency": self.bot.latency * 1000,
            "cache": {
                "guilds": len(self.bot.guilds),
                "users": len(self.bot.users),
            }
        })

    async def cog_load(self: "Network") -> None:
        host = "216.105.170.98"
        port = 9118
        self.bot.loop.create_task(
            web._run_app(
                self.app,
                host=host,
                port=port,
                print=None,
                access_log=log,
                access_log_class=AccessLogger,
            ),
            name="Internal-API",
        )
        log.info(f"Started the internal API on {host}:{port}.")

    async def cog_unload(self: "Network") -> None:
        await self.app.shutdown()
        await self.app.cleanup()
        log.info("Gracefully shutdown the API")

    @route("/commands")
    async def commands(self: "Network", request: Request) -> Response:
        """
        Export command information as JSON.
        """
        commands_info = []
        for command in self.bot.commands:
            command_info = {
                "category": command.cog_name or "Uncategorized",
                "description": command.help or "",
                "name": command.name,
                "parameters": [
                    {
                        "name": param.name,
                        "optional": param.default != param.empty
                    }
                    for param in command.clean_params.values()
                ],
                "permissions": [
                    perm for perm in command.permissions
                ] if command.permissions else ["N/A"]
            }
            commands_info.append(command_info)
        return web.json_response(commands_info)

    @route("/status")
    async def status(self, request: Request) -> Response:
        return web.json_response({
            "shards": [
                {
                    "guilds": f"{len([guild for guild in self.bot.guilds if guild.shard_id == shard.id])}",
                    "id": f"{shard.id}",
                    "ping": f"{(shard.latency * 1000):.2f}ms",
                    "uptime": f"{int(self.bot.uptime2)}",
                    "users": f"{len([user for guild in self.bot.guilds for user in guild.members if guild.shard_id == shard.id])}",
                }
                for shard in self.bot.shards.values()
            ]
        })
    
    @route("/usercount")
    async def usercount(self, request: Request) -> Response:
        return web.json_response({
            "users": f"{len(self.bot.users)}"
        })
    
async def setup(bot: "Heal"):
    await bot.add_cog(Network(bot))