from dataclasses import dataclass, field
from functools import wraps

from fastapi import HTTPException

from nova_api import NovaAPIException


def treat_exceptions(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NovaAPIException as e:
            raise HTTPException(status_code=e.status_code,
                                detail=e.message,
                                headers={"X-Error": e.error_code})

    return inner


@dataclass
class SpeciesAlreadyApprovedException(NovaAPIException):
    status_code: int = field(default=400, init=False)
    message: str = field(default="The species is already approved",
                         init=False)
