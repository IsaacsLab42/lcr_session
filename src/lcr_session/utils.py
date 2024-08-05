"""
This module contains utility functions used elsewhere in the LCR Session library.
"""

__all__ = ["get_user_agent", "merge_dict"]

import platform
from typing import Any

from fake_useragent import UserAgent  # type: ignore


def get_user_agent() -> str:
    """
    Get a user agent string that represents a real browser.

    This can help by making ourselves blend in better with browser traffic, so the
    script doesn't stand out. The user agent string returned will be based on the
    platform that this script is run from.

    Returns:
        User-Agent string
    """
    my_platform = platform.system().lower()
    if my_platform == "windows":
        browsers = ["chrome", "edge", "firefox"]
    elif my_platform == "linux":
        browsers = ["chrome", "firefox"]
    elif my_platform == "darwin":
        browsers = ["safari", "chrome", "firefox"]
        my_platform = "mac"
    else:
        raise Exception(f"Unknown platform: {my_platform}")
    ua = UserAgent(platforms="pc", os=my_platform, browsers=browsers)
    return ua.random


def merge_dict(dict1: dict[Any, Any], dict2: dict[Any, Any]) -> dict[Any, Any]:
    """
    Merge the contents of two dictionaries together and create a 3rd
    dictionary. Items in dict1 with the same name as items in dict2
    will be overridden. i.e. dict2 wins.

    Args:
        dict1: First dictionary of items
        dict2: Second dictionary of items. This one wins in the
            situation where both dictionaries have the same key name.

    Returns:
        Combined dictionary
    """
    # This works by expanding each dict into (key, value) pairs
    merged = {**dict1, **dict2}
    return merged
