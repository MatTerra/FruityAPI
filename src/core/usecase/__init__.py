from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel


class UseCaseInput(BaseModel):
    pass


class UseCase(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def execute(self, _input: UseCaseInput):
        raise NotImplementedError()
