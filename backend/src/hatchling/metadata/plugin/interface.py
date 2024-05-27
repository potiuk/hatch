from __future__ import annotations

import contextlib
from abc import ABC, abstractmethod
from typing import Generator


class MetadataHookInterface(ABC):  # no cov
    """
    Example usage:

    ```python tab="plugin.py"
    from hatchling.metadata.plugin.interface import MetadataHookInterface


    class SpecialMetadataHook(MetadataHookInterface):
        PLUGIN_NAME = 'special'
        ...
    ```

    ```python tab="hooks.py"
    from hatchling.plugin import hookimpl

    from .plugin import SpecialMetadataHook


    @hookimpl
    def hatch_register_metadata_hook():
        return SpecialMetadataHook
    ```
    """

    PLUGIN_NAME = ''
    """The name used for selection."""

    def __init__(self, root: str, config: dict) -> None:
        self.__root = root
        self.__config = config
        self.__build_version: str | None = None

    @property
    def root(self) -> str:
        """
        The root of the project tree.
        """
        return self.__root

    @property
    def config(self) -> dict:
        """
        The hook configuration.

        ```toml config-example
        [tool.hatch.metadata.hooks.<PLUGIN_NAME>]
        ```
        """
        return self.__config

    @property
    def build_version(self) -> str | None:
        """
        Gets the version of build (standard/editable) that is being run.
        """
        return self.__build_version

    @abstractmethod
    def update(self, metadata: dict) -> None:
        """
        This updates the metadata mapping of the `project` table in-place.
        """

    def get_known_classifiers(self) -> list[str]:  # noqa: PLR6301
        """
        This returns extra classifiers that should be considered valid in addition to the ones known to PyPI.
        """
        return []

    @contextlib.contextmanager
    def set_build_version(self, build_version: str) -> Generator[None, None, None]:
        old_build_version = self.build_version
        self.__build_version = build_version
        yield
        self.__build_version = old_build_version
