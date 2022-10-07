from functools import wraps
from typing import Type

from core.usecase import UseCase, UseCaseInput
from infra.exceptions import treat_exceptions
from infra.repository.species_sql_repository import SpeciesSQLRepository


def controller(use_case: Type[UseCase], input_type: Type[UseCaseInput]):
    def inner(func):
        @treat_exceptions
        @wraps(func)
        async def wrapper(_input: input_type):
            handler = use_case(SpeciesSQLRepository())
            return await handler.execute(_input)
        return wrapper
    return inner