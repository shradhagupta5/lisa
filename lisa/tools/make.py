# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from pathlib import PurePath
from typing import TYPE_CHECKING, Dict, Optional, cast

from lisa.executable import Tool
from lisa.operating_system import Posix
from lisa.tools import Gcc
from lisa.tools.lscpu import Lscpu

if TYPE_CHECKING:
    from lisa.node import Node


class Make(Tool):
    def __init__(self, node: "Node") -> None:
        super().__init__(node)
        self._thread_count = 0

    @property
    def command(self) -> str:
        return "make"

    @property
    def can_install(self) -> bool:
        return True

    def _install(self) -> bool:
        posix_os: Posix = cast(Posix, self.node.os)
        posix_os.install_packages([self, Gcc])
        return self._check_exists()

    def make_install(
        self,
        cwd: PurePath,
        timeout: int = 600,
        sudo: bool = True,
        update_envs: Optional[Dict[str, str]] = None,
    ) -> None:
        self.make(arguments="", cwd=cwd, timeout=timeout, update_envs=update_envs)

        # install with sudo
        self.make(
            arguments="install",
            cwd=cwd,
            timeout=timeout,
            sudo=sudo,
            update_envs=update_envs,
        )

    def make(
        self,
        arguments: str,
        cwd: PurePath,
        is_clean: bool = False,
        sudo: bool = False,
        timeout: int = 600,
        thread_count: int = 0,
        update_envs: Optional[Dict[str, str]] = None,
    ) -> None:
        if thread_count == 0:
            if self._thread_count == 0:
                lscpu = self.node.tools[Lscpu]
                self._thread_count = lscpu.get_core_count()
            thread_count = self._thread_count

        if is_clean:
            self.run(
                "clean",
                cwd=cwd,
                sudo=sudo,
                shell=True,
                timeout=timeout,
                force_run=True,
                update_envs=update_envs,
            )

        # yes '' answers all questions with default value.
        self.node.execute(
            f"yes '' | make -j{thread_count} {arguments}",
            cwd=cwd,
            timeout=timeout,
            sudo=sudo,
            shell=True,
            update_envs=update_envs,
            expected_exit_code=0,
            expected_exit_code_failure_message="Failed to make",
        )
