import os
from collections.abc import Mapping

from pydantic import BaseModel
from rich.console import Console


class TerminalCompatibilityResult(BaseModel):
    is_tty: bool
    reason: str | None = None


def _env_flag_true(value: str | None) -> bool:
    if value is None:
        return False
    value = value.strip().lower()
    return value in {"1", "true", "yes", "on"}


def check_terminal_compatibility(
    *,
    console: Console,
) -> TerminalCompatibilityResult:
    is_terminal = bool(console.is_terminal)

    if not is_terminal:
        return TerminalCompatibilityResult(
            reason=(
                "Rich detected a non-interactive or unsupported terminal; "
                "interactive UI may not render correctly"
            ),
            is_tty=is_terminal,
        )

    return TerminalCompatibilityResult(
        is_tty=is_terminal,
    )


def strict_mode_enabled(env: Mapping[str, str] | None = None) -> bool:
    if env is None:
        env = os.environ
    return _env_flag_true(env.get("OPENHANDS_CLI_STRICT_TERMINAL"))
