import logging
import uuid
import warnings
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pytz

import pyttman
from pyttman.core.communication.models.containers import MessageMixin, Reply

"""
Details:
    2020-07-05
    
    pyttman framework internal source file

Module details:
    
    data containers and functions used by objects in
    the pyttman package.
"""


def is_dst(timezone: str):
    """
    method for returning a bool whether or not a timezone
    currently is in daylight savings time, useful for servers
    that run_client systems outside of the user timezone.
    :param timezone:
        string, timezone to give pytz for the dst query.
        look up available timezones at this url:
        https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz
        -timezones
    :returns:
        bool
    """
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(datetime.now(), is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


@dataclass
class _cim:
    """
    This class is only used as a namespace
    for internal messages used by exceptions
    or elsewhere by pyttman classes
    and functions. Not for instantiating.
    """
    deprecated_warn: str = "pyttman DEPRECATED WARNING"
    warn: str = "Pyttman WARNING"
    err: str = "Pyttman ERROR"


def load_settings(*args):
    raise DeprecationWarning("The function 'load_settings' is deprecated "
                             "deprecated as of version 1.1.4. Instead of "
                             "manually loading settings in your main.py, "
                             "consider creating a project with pyttman-cli "
                             "and use the clients provided in the framework, "
                             "or create your own by subclassing BaseClient.")


def _generate_name(name):
    """
    Generates a user-friendly name out of
    Command or Feature class names, by
    inserting spaces in camel cased names
    as well as truncating 'Command' and 'Feature'
    in the names.
    :param name: string, name of a class.
                 hint: Command or Feature subclass
    :return: str, 'SetTimeCommand' -> 'Set Time'
    """
    new_name = ""
    for i in ("Feature", "feature", "Command", "command"):
        name = name.replace(i, "")

    for i, c in enumerate(name):
        if i > 0 and c.isupper():
            new_name += " "
        new_name += c
    return new_name


def _generate_error_entry(message: MessageMixin, exc: BaseException) -> Reply:
    """
    Creates a log entry for critical errors with a UUID bound
    to the log file entry, explaining the error. For the front
    end clients, a Reply object is returned to provide for
    end users who otherwise would experience a chatbot who
    didn't reply back at all.
    :param message: MessageMixin
    :param exc: Exception
    :return: Reply
    """
    error_id = uuid.uuid4()
    warnings.warn(f"{datetime.now()} - A critical error occurred in the "
                  f"application logic. See logs for details. Error id: {error_id}")

    pyttman.logger.log(level="error",
                       message=f"CRICITAL ERROR: ERROR ID={error_id} - "
                               f"The error was caught while processing "
                               f"message: '{message}'. Error message: '{exc}'")

    return Reply(f"{pyttman.settings.FATAL_EXCEPTION_AUTO_REPLY} - "
                 f"Error id: {error_id}")
