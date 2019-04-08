"""
_validator -   # FIXME teplates



Copyright (c) 2019 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
import typing

import pluggy

from ._constants import _PLUGIN_NAME

validator_spec = pluggy.HookspecMarker(_PLUGIN_NAME)
rehash_spec = pluggy.HookspecMarker(_PLUGIN_NAME)


@validator_spec
def validate_config(data: typing.Dict):
    """
    Validate new configuration data.

    Args:
        data (typing.Dict): new configuration data  to validate

    Raises:
        ValueError: config section failed to validate.
    """
    ...


@rehash_spec
def rehash_handler(data: typing.Dict):
    """
    Apply new configuration data

    Args:
        data (typing.Dict): new configuration data to apply.

    """
    ...
