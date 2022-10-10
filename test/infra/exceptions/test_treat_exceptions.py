from pytest import raises
from fastapi import HTTPException
from nova_api import NovaAPIException

from infra.exceptions import treat_exceptions

STATUS_CODE = 422
ERROR_MESSAGE = "TEST"


@treat_exceptions
async def raises_nova_exception():
    raise NovaAPIException(status_code=STATUS_CODE, message=ERROR_MESSAGE)


class TestTreatExceptions:
    async def test_should_convert_to_http_exception(self):
        with raises(HTTPException) as e:
            await raises_nova_exception()
        assert e.value.status_code == STATUS_CODE
        assert e.value.detail == ERROR_MESSAGE
