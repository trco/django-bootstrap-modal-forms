__all__ = ('is_ajax', 'DjangoView', 'LoginAjaxMixinProtocol', 'DeleteMessageMixinProtocol',)

from typing import Protocol, Any, Dict

from django.http import HttpRequest


def is_ajax(meta: Dict):
    if 'HTTP_X_REQUESTED_WITH' not in meta:
        return False

    if meta['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        return True

    return False


class DjangoView(Protocol):
    """
    This is a pure supporting, type hinting class, for mixins that require a HttpRequest attribute.

    @see https://docs.python.org/3/library/typing.html#typing.Protocol
    """

    @property
    def request(self) -> HttpRequest:
        ...


class LoginAjaxMixinProtocol(DjangoView, Protocol):
    """
    This is a pure supporting, type hinting class, for mixins that require a success_message
    attribute and a get_success_url(...) method.

    @see https://docs.python.org/3/library/typing.html#typing.Protocol
    """

    @property
    def success_message(self) -> str:
        ...

    def get_success_url(self) -> str:
        ...


class DeleteMessageMixinProtocol(LoginAjaxMixinProtocol, Protocol):
    """
    This is a pure supporting, type hinting class, for mixins that require a success_message attribute,
    a get_success_url(...) and a get_object(...) method.

    @see https://docs.python.org/3/library/typing.html#typing.Protocol
    """

    def get_object(self) -> Any:
        ...
