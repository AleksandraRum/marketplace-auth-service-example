import uuid
from typing import Any

from starlette.types import ASGIApp, Receive, Scope, Send

from src.trace import reset_trace_id, set_trace_id

TRACE_HEADER = "x-trace-id"


class TraceMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self._app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        incoming = headers.get(TRACE_HEADER.encode())
        trace_id = incoming.decode() if incoming else str(uuid.uuid4())
        token = set_trace_id(trace_id)

        async def send_with_trace(message: Any) -> None:
            if message["type"] == "http.response.start":
                raw = list(message.get("headers", []))
                raw.append((TRACE_HEADER.encode(), trace_id.encode()))
                message = {**message, "headers": raw}
            await send(message)

        try:
            await self._app(scope, receive, send_with_trace)
        finally:
            reset_trace_id(token)
