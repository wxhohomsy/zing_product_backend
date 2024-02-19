import datetime
import time
import traceback
import warnings
from typing import Dict
import functools
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import Request, Response
from sqlalchemy import text, select, and_
from zing_product_backend.app_db.connections import get_async_session
from zing_product_backend.models import server_stats, auth_model


def parse_header(scope: Dict):
    headers_tuple = scope['headers']
    headers_dict = {}
    for name, value in headers_tuple:
        name = name.decode('latin1').lower()  # HTTP headers are case-insensitive and encoded as Latin-1
        value = value.decode('latin1')
        if name in headers_dict:
            headers_dict[name] += ', ' + value  # Combine values for headers with the same name
        else:
            headers_dict[name] = value
    return headers_dict


@functools.lru_cache(maxsize=2000)
async def get_user_by_token(token: str, session) -> auth_model.User:
    stmt = select(auth_model.User).join(auth_model.AccessToken).where(
        and_(
            auth_model.AccessToken.user_id == auth_model.User.id, auth_model.AccessToken.token == token)
    )
    usr = await session.execute(stmt)
    return usr.scalar_one_or_none()


async def _create_body_receive_stream(body: bytes):
    async def receive() -> dict:
        return {"type": "http.request", "body": body, "more_body": False}
    return receive


async def request_record_middleware(request: Request, call_next):
    request.scope['request_time'] = datetime.datetime.now()
    header_dict = parse_header(request.scope)
    content_length = header_dict.get('content-length')
    if content_length and int(content_length) < 100000:
        request_body = await request.body()
        receive_func = await _create_body_receive_stream(request_body)
        request = Request(scope=request.scope, receive=receive_func )
    else:
        request_body = b''
    async for s in get_async_session():
        scope = request.scope
        try:
            response = await call_next(request)
            # Assuming parse_header is a function that extracts headers into a dict
            if 'authorization' in header_dict:
                # Assuming get_user_by_token is an async function that returns a user object or None
                user = await get_user_by_token(header_dict['authorization'].split(' ')[1], s)
                user_name = user.user_name if user else None
            else:
                user_name = None
            r = server_stats.RequestRecord(
                request_type=scope['type'],
                client_ip=scope['client'][0],
                server_ip=scope['server'][0],
                server_port=scope['server'][1],
                request_time=scope['request_time'],
                user_name=user_name,
                state=scope['state'],
                duration=(datetime.datetime.now() - scope['request_time']).total_seconds(),
                path=scope['path'],
                method=scope['method'],
                scheme=scope['scheme'],
                request_body=request_body,
                headers=header_dict,
                error_flag=False,
                traceback=None,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            r = server_stats.RequestRecord(
                request_type=scope['type'],
                client_ip=scope['client'][0],
                server_ip=scope['server'][0],
                server_port=scope['server'][1],
                request_time=scope['request_time'],
                user_name=None,
                state=scope['state'],
                duration=(datetime.datetime.now() - scope['request_time']).total_seconds(),
                path=scope['path'],
                method=scope['method'],
                scheme=scope['scheme'],
                request_body=request_body,
                headers=header_dict,
                error_flag=True,
                traceback=traceback.format_exc(),
            )
            warnings.warn(traceback.format_exc())
            # Create a default response in case of an exception
            response = Response(content="An internal server error occurred", status_code=500)

        s.add(r)

        return response
