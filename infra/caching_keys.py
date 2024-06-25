from typing import Optional
from urllib.request import Request

from fastapi_cache import FastAPICache
from starlette.responses import Response


def function_kwargs_builder(*fields: str):
    def key_builder(
        func,
        namespace: Optional[str] = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
):
        prefix = FastAPICache.get_prefix()

        final_kwargs = [f'{field}:{kwargs['kwargs'][field]}' for field in fields if field in kwargs['kwargs']]
        final_kwargs = ','.join(final_kwargs)

        return f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{final_kwargs}"

    return key_builder