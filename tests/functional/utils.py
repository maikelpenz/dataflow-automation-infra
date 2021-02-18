import time
from enum import Enum
from typing import Callable


class MaxCheckAttemptReached(Exception):
    pass


class FailedTest(Exception):
    pass


class ResourceCheckStatus(Enum):
    FINISHED = 1
    RETRY = 2
    FAILED = 3


def is_resource_available(
    check_function: Callable,
    wait_time_sec: int = 2,
    backoff_rate: int = 2,
    max_attempts: int = 10,
    exausted_attempts_message: str = "",
):
    """
    Args:
        check_function (Callable): [description]
        wait_time_sec (int, optional): [description]. Defaults to 1.
        backoff_rate (int, optional): [description]. Defaults to 2.
        max_attempts (int, optional): [description]. Defaults to 10.
        exausted_attempts_message (str, optional): [description]. Defaults to "".
    Returns:
        bool:
    """
    for attempt in range(max_attempts):
        time.sleep(attempt * wait_time_sec * backoff_rate)
        state = check_function()
        if state == ResourceCheckStatus.FINISHED:
            return
        elif state != ResourceCheckStatus.RETRY:
            raise FailedTest
    raise MaxCheckAttemptReached(
        f"Condition not met {exausted_attempts_message} after {max_attempts} attempts"
    )
