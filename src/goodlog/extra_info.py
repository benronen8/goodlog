import contextlib
import logging
import json
import typing
from typing import Any


logger = logging.getLogger(__name__)


def set_info(**kwargs: Any) -> None:
    ExtraLoggingInfo(**kwargs)


def get_info() -> dict[str, Any]:
    return ExtraLoggingInfo().as_dict()


@contextlib.contextmanager
def extra_info_context(**extra_info: Any) -> typing.Generator[None, None, None]:
    add_ephemeral_info(**extra_info)
    try:
        yield
    finally:
        remove_ephemeral_info()


def add_ephemeral_info(**kwargs: Any) -> None:
    ExtraLoggingInfo().add_more_info(**kwargs)


def remove_ephemeral_info() -> dict[str, Any]:
    return ExtraLoggingInfo().remove_more_info()


class Singleton(type):
    _instances: dict[type, Any] = {}
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ExtraLoggingInfo(metaclass=Singleton):

    def __init__(self, **kwargs: Any) -> None:
        self._info = kwargs.copy() if kwargs else dict()
        self._more_info: dict[str, Any] = dict()
        self._validate_serialization(self._info)

    def as_dict(self) -> dict[str, Any]:
        return {**self._info, **self._more_info}

    def add_more_info(self, **kwargs: Any) -> None:
        """
        Add more info in a temporary manner - it may be removed by calling the
        `remove_more_info` method.
        """
        self._validate_serialization(kwargs)
        self._more_info = {**self._more_info, **kwargs}

    def remove_more_info(self) -> dict[str, Any]:
        """
        Remove info that weren't provided in initialization but added later.
        """
        removed_info, self._more_info = self._more_info, dict()
        return removed_info

    @classmethod
    def _validate_serialization(cls, d: dict[str, Any]) -> None:
        try:
            json.dumps(d)
        except TypeError as e:
            raise ValueError("The provided dict is not JSON-serializable") from e
