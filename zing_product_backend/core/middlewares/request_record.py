import time
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


class RequestRecordMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        await self.app(scope, receive, send)