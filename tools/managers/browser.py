from contextlib import asynccontextmanager
from loguru import logger as log
from secrets import token_urlsafe
from typing import AsyncGenerator, Literal, Optional, List
from anyio import CapacityLimiter
from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)
from pydantic import BaseModel

class BrowserHandler:
    _instance: Optional["BrowserHandler"] = None
    limiter: Optional[CapacityLimiter] = None
    playwright: Optional[Playwright] = None
    browser: Optional[Browser] = None
    context: Optional[BrowserContext] = None

    def __new__(cls) -> "BrowserHandler":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.limiter = CapacityLimiter(4)

    async def cleanup(self) -> None:
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

        self.context = None
        self.browser = None
        self.playwright = None

    async def init(self) -> None:
        if self.context:
            return

        await self.cleanup()

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            proxy=(
                {
                    "server": "http://127.1:40000",
                }
            ),
        )
        self.context = await self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            color_scheme="dark",
            locale="en-US",
        )

    @asynccontextmanager
    async def borrow_page(self) -> AsyncGenerator[Page, None]:
        if not self.context:
            raise RuntimeError("Browser context is not initialized.")

        await self.limiter.acquire()
        identifier, page = token_urlsafe(12), await self.context.new_page()
        log.debug(f"Borrowing page ID {identifier}.")
        try:
            yield page
        finally:
            self.limiter.release()
            await page.close()
            log.debug(f"Released page ID {identifier}.")